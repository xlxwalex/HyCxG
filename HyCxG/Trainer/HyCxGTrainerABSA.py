import torch
from Trainer.Trainer import Trainer
from torch.utils.data import DataLoader
from tqdm import tqdm
import time
import numpy as np
from utils import padding, save_model, attention_mask, Metric
import os

class HyCxGTrainerABSA(Trainer):
    def __init__(self, args, model, criterion, optimizer, device, checkp, scheduler = None, model_save_name = None):
        super(HyCxGTrainerABSA, self).__init__(args, model, criterion, optimizer, device, checkp, scheduler)
        self.eval_inform = {'loss': [], 'acc': [], 'f1_score': []}
        self.train_loss = []
        self.eval_loss = []
        self.model_save_name = model_save_name
        self.metric = Metric(args)

    def train(self, Trainset: DataLoader, Validset: DataLoader):
        self.optimizer.zero_grad()
        self.step, pred, truth = 0, [], []
        for epoch in tqdm(range(self.args.num_epoch), desc='Training Epoch'):
            for step, batch_data in enumerate(Trainset):
                st_time = time.time()
                self.model.train()
                tokens, masks, aspmasks, HT, edges, adjs, labels = batch_data
                padded_token = padding(tokens, self.args.padding_size, self.args.padding_val)
                tr_attn_mask = attention_mask(padded_token, self.args.padding_val).to(self.device)
                tr_tokens    = torch.from_numpy(padded_token).to(self.device)
                tr_labels    = torch.from_numpy(labels).to(self.device)
                tr_HTs       = torch.from_numpy(HT).to(self.device)
                tr_adjs      = None # Not available in this repo
                tr_aspmasks  = torch.from_numpy(padding(aspmasks, self.args.padding_size, self.args.padding_val)).to(self.device)
                tr_masks     = torch.from_numpy(padding(masks, self.args.padding_size, self.args.padding_val)).to(self.device)
                tr_edges     = torch.from_numpy(edges).to(self.device)
                logits       = self.model(tr_tokens, tr_attn_mask, tr_HTs, tr_edges, tr_adjs, tr_masks, tr_aspmasks)
                loss         = self.criterion(logits, tr_labels)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.args.max_grad_norm)
                self.optimizer.step()
                self.scheduler.step() if self.scheduler is not None else None
                self.train_loss.append(loss.item())
                self.optimizer.zero_grad()
                truth.extend(tr_labels.detach().cpu().numpy().astype('int32'))
                pred_polar = np.argmax(logits.detach().cpu().numpy(), axis=1).astype('int32')
                pred.extend(pred_polar)
                if (self.step + 1) % self.args.print_step == 0:
                    met = self.metric(np.array(pred), np.array(truth))
                    acc, _, _, f1 = met
                    pred, truth = [], []
                    print("step: %s, ave loss = %f, polairty_acc  = %f, polairty_f1 = %f, speed: %f steps/s" %
                          (self.step + 1, self.train_loss[-1], acc, f1, 1 / (time.time() - st_time)))
                if (self.step + 1) % self.args.eval_step == 0:
                    eval_time = time.time()
                    loss, acc, f1 = self.valid(Validset)
                    print(
                        "Final validation result: step: %d, ave loss: %f, ave polarity_acc: %f, polarity_f1 = %f, speed: %f s/total" %
                        (self.step, loss, acc, f1, 1 / (time.time() - eval_time)))
                    if self.best < acc:
                        if self.model_save_name is not None:
                            save_model(os.path.join(self.checkpoint, self.model_save_name), self._generate_checkp())
                        else:
                            save_model(os.path.join(self.checkpoint, 'checkpoint.pt'), self._generate_checkp())
                        print("Model Reached Best Performance, Save To Check_points")
                        self.best = acc
                self.step += 1
            self.epoch += 1

    def valid(self, Validset: DataLoader):
        self.model.eval()
        pred, truth, eval_loss = [], [], []
        for step, batch_data in enumerate(Validset):
            tokens, masks, aspmasks, HT, edges, adjs, labels = batch_data
            padded_token = padding(tokens, self.args.padding_size, self.args.padding_val)
            tr_attn_mask = attention_mask(padded_token, self.args.padding_val).to(self.device)
            tr_tokens    = torch.from_numpy(padded_token).to(self.device)
            tr_labels    = torch.from_numpy(labels).to(self.device)
            tr_HTs       = torch.from_numpy(HT).to(self.device)
            tr_adjs      = None # Not available in this repo
            tr_aspmasks  = torch.from_numpy(padding(aspmasks, self.args.padding_size, self.args.padding_val)).to(self.device)
            tr_masks     = torch.from_numpy(padding(masks, self.args.padding_size, self.args.padding_val)).to(self.device)
            tr_edges     = torch.from_numpy(edges).to(self.device)
            with torch.no_grad():
                logits   = self.model(tr_tokens, tr_attn_mask, tr_HTs, tr_edges, tr_adjs, tr_masks, tr_aspmasks)
            loss = self.criterion(logits, tr_labels)
            eval_loss.append(loss.item())
            pred_polar = np.argmax(logits.detach().cpu().numpy(), axis=1).astype('int32')
            pred.extend(pred_polar)
            truth.extend(tr_labels.detach().cpu().numpy().astype('int32'))
        acc, _, _, f1 = self.metric(np.array(pred), np.array(truth))
        self.eval_loss.append(np.mean(eval_loss))
        self.eval_inform['loss'].append(np.mean(eval_loss))
        self.eval_inform['acc'].append(acc)
        self.eval_inform['f1_score'].append(f1)
        return np.mean(eval_loss), acc, f1

    def test(self, Testset: DataLoader, only_report : bool=False):
        self.model.eval()
        pred, truth = [], []
        for step, batch_data in enumerate(tqdm(Testset, desc='Inference')):
            tokens, masks, aspmasks, HT, edges, adjs, labels = batch_data
            padded_token = padding(tokens, self.args.padding_size, self.args.padding_val)
            tr_attn_mask = attention_mask(padded_token, self.args.padding_val).to(self.device)
            tr_tokens = torch.from_numpy(padded_token).to(self.device)
            tr_HTs = torch.from_numpy(HT).to(self.device)
            tr_adjs = None # Not available in this repo
            tr_aspmasks = torch.from_numpy(padding(aspmasks, self.args.padding_size, self.args.padding_val)).to(self.device)
            tr_masks = torch.from_numpy(padding(masks, self.args.padding_size, self.args.padding_val)).to(self.device)
            tr_edges = torch.from_numpy(edges).to(self.device)
            with torch.no_grad():
                logits = self.model(tr_tokens, tr_attn_mask, tr_HTs, tr_edges, tr_adjs, tr_masks, tr_aspmasks)
            pred_polar = np.argmax(logits.detach().cpu().numpy(), axis=1).astype('int32').tolist()
            pred.extend(pred_polar)
            truth.extend(labels)
        self.metric.report(np.array(pred), np.array(truth))
        if only_report is not True:
            return None, (pred, truth)
        else:
            acc, _, _, f1 = self.metric(np.array(pred), np.array(truth))
            return acc, f1
