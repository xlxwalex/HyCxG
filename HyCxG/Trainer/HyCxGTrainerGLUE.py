import torch
from Trainer.Trainer import Trainer
from torch.utils.data import DataLoader
from tqdm import tqdm
import time
import numpy as np
from utils import padding, save_model, attention_mask, Metric
import os

class HyCxGTrainerGLUE(Trainer):
    def __init__(self, args, model, criterion, optimizer, device, checkp, scheduler = None, model_save_name = None, sets_name = 'CoLA', save_flag=True):
        super(HyCxGTrainerGLUE, self).__init__(args, model, criterion, optimizer, device, checkp, scheduler)
        self.eval_inform = {'loss': [], 'acc': [], 'f1_score': [], 'pearson' : []}
        self.train_loss = []
        self.eval_loss = []
        self.sets_name = sets_name
        self.save_flag = save_flag
        self.train_metric = 'acc' if sets_name.split('_')[-1] not in ['STS'] else 'pearson'
        self.model_save_name = model_save_name
        self.metric = Metric(args)

    def train(self, Trainset: DataLoader, Validset: DataLoader):
        self.optimizer.zero_grad()
        self.step, pred, truth = 0, [], []
        for epoch in tqdm(range(self.args.num_epoch), desc='Training Epoch'):
            for step, batch_data in enumerate(Trainset):
                st_time = time.time()
                self.model.train()
                tokens, masks, HT, edges, adjs, labels = batch_data
                padded_token = padding(tokens, self.args.padding_size, self.args.padding_val, self.args.lm_group)
                tr_attn_mask = attention_mask(padded_token, self.args.padding_val, self.args.lm_group).to(self.device)
                tr_tokens    = torch.from_numpy(padded_token).to(self.device)
                tr_labels    = torch.from_numpy(labels).to(self.device) if self.sets_name not in ['STS'] else  torch.from_numpy(labels).to(torch.float32).to(self.device)
                tr_HTs       = torch.from_numpy(HT).to(self.device)
                tr_adjs      = None # Not available in this repo
                tr_masks     = torch.from_numpy(padding(masks, self.args.padding_size, self.args.padding_val)).to(self.device)
                tr_edges     = torch.from_numpy(edges).to(self.device)
                logits       = self.model(tr_tokens, tr_attn_mask, tr_HTs, tr_edges, tr_adjs, tr_masks, None)
                loss         = self.criterion(logits, tr_labels)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.args.max_grad_norm)
                self.optimizer.step()
                self.scheduler.step() if self.scheduler is not None else None
                self.train_loss.append(loss.item())
                self.optimizer.zero_grad()
                truth.extend(tr_labels.detach().cpu().numpy().astype('int32')) if self.sets_name not in ['STS'] else truth.extend(tr_labels.detach().cpu().numpy().astype('float32'))
                # truth.extend(tr_labels.detach().cpu().numpy().astype('int32')) if self.sets_name not in ['STS'] else truth.extend(tr_labels.detach().cpu().numpy().astype('float32') * 5)
                pred_polar = np.argmax(logits.detach().cpu().numpy(), axis=1).astype('int32')  if self.sets_name not in ['STS'] else logits.detach().cpu().numpy()
                pred.extend(pred_polar)
                if (self.step + 1) % self.args.print_step == 0:
                    if self.sets_name not in ['STS']:
                        met = self.metric(np.array(pred), np.array(truth))
                        acc, _, _, f1 = met
                        print("step: %s, ave loss = %f, %s_%s  = %f, %s_f1 = %f, speed: %f steps/s" %
                              (self.step + 1, self.train_loss[-1], self.sets_name, self.train_metric, acc, self.sets_name, f1, 1 / (time.time() - st_time)))
                    else:
                        pred_pear = np.array(pred)
                        pred_pear = np.clip(pred_pear, 0.0, 5.0)
                        perason = self.metric(pred_pear, np.array(truth), sets_name=self.sets_name)
                        print("step: %s, ave loss = %f, %s_%s  = %f, speed: %f steps/s" %
                              (self.step + 1, self.train_loss[-1], self.sets_name, self.train_metric, perason, 1 / (time.time() - st_time)))
                    pred, truth = [], []
                if (self.step + 1) % self.args.eval_step == 0:
                    eval_time = time.time()
                    if self.sets_name not in ['STS']:
                        loss, acc, f1 = self.valid(Validset)
                        unimet = acc
                        print(
                            "Final validation result: step: %d, ave loss: %f, ave %s_acc: %f, %s_f1 = %f, speed: %f s/total" %
                            (self.step, loss, self.sets_name, acc, self.sets_name, f1, 1 / (time.time() - eval_time)))
                    else:
                        loss, pearson = self.valid(Validset)
                        unimet = pearson
                        print(
                            "Final validation result: step: %d, ave loss: %f, ave %s_pearson: %f, speed: %f s/total" %
                            (self.step, loss, self.sets_name, pearson, 1 / (time.time() - eval_time)))
                    if self.best < unimet:
                        if self.save_flag:
                            if self.model_save_name is not None:
                                save_model(os.path.join(self.checkpoint, self.model_save_name), self._generate_checkp())
                            else:
                                save_model(os.path.join(self.checkpoint, 'checkpoint.pt'), self._generate_checkp())
                            print("Model Reached Best Performance, Save To Check_points")
                        else:
                            print("Model Reached Best Performance")
                        self.best = unimet
                self.step += 1
            self.epoch += 1

    def valid(self, Validset: DataLoader):
        self.model.eval()
        pred, truth, eval_loss = [], [], []
        for step, batch_data in enumerate(Validset):
            tokens, masks, HT, edges, adjs, labels = batch_data
            padded_token = padding(tokens, self.args.padding_size, self.args.padding_val, self.args.lm_group)
            tr_attn_mask = attention_mask(padded_token, self.args.padding_val, self.args.lm_group).to(self.device)
            tr_tokens    = torch.from_numpy(padded_token).to(self.device)
            tr_labels    = torch.from_numpy(labels).to(self.device) if self.sets_name not in ['STS'] else  torch.from_numpy(labels).to(torch.float32).to(self.device)
            tr_HTs       = torch.from_numpy(HT).to(self.device)
            tr_adjs      = None # Not available in this repo
            tr_masks     = torch.from_numpy(padding(masks, self.args.padding_size, self.args.padding_val)).to(self.device)
            tr_edges     = torch.from_numpy(edges).to(self.device)
            with torch.no_grad():
                logits   = self.model(tr_tokens, tr_attn_mask, tr_HTs, tr_edges, tr_adjs, tr_masks, None)
            loss = self.criterion(logits, tr_labels)
            eval_loss.append(loss.item())
            pred_polar = np.argmax(logits.detach().cpu().numpy(), axis=1).astype('int32')  if self.sets_name not in ['STS'] else logits.detach().cpu().numpy()
            pred.extend(pred_polar)
            truth.extend(tr_labels.detach().cpu().numpy().astype('int32')) if self.sets_name not in ['STS'] else truth.extend(tr_labels.detach().cpu().numpy().astype('float32'))
        self.eval_loss.append(np.mean(eval_loss))
        self.eval_inform['loss'].append(np.mean(eval_loss))
        if self.sets_name not in ['STS']:
            acc, _, _, f1 = self.metric(np.array(pred), np.array(truth))
            self.eval_inform['acc'].append(acc)
            self.eval_inform['f1_score'].append(f1)
            return np.mean(eval_loss), acc, f1
        else:
            pred_pear = np.array(pred)
            pred_pear = np.clip(pred_pear, 0.0, 5.0)
            pearson = self.metric(pred_pear, np.array(truth), sets_name=self.sets_name)
            self.eval_inform['pearson'].append(pearson)
            return np.mean(eval_loss), pearson

    def test(self, Testset: DataLoader, more=False, wo_tqdm=False):
        self.model.eval()
        pred, truth = [], []
        package = enumerate(tqdm(Testset, desc='Inference')) if wo_tqdm is not True else enumerate(Testset)
        for step, batch_data in package:
            tokens, masks, HT, edges, adjs, labels = batch_data
            padded_token = padding(tokens, self.args.padding_size, self.args.padding_val, self.args.lm_group)
            tr_attn_mask = attention_mask(padded_token, self.args.padding_val, self.args.lm_group).to(self.device)
            tr_tokens = torch.from_numpy(padded_token).to(self.device)
            tr_HTs = torch.from_numpy(HT).to(self.device)
            tr_adjs = None # Not available in this repo
            tr_masks = torch.from_numpy(padding(masks, self.args.padding_size, self.args.padding_val)).to(self.device)
            tr_edges = torch.from_numpy(edges).to(self.device)
            with torch.no_grad():
                logits = self.model(tr_tokens, tr_attn_mask, tr_HTs, tr_edges, tr_adjs, tr_masks, None)
            pred_polar = np.argmax(logits.detach().cpu().numpy(), axis=1).astype('int32').tolist() if self.sets_name not in ['STS'] else logits.detach().cpu().numpy()
            pred.extend(pred_polar)
            truth.extend(labels)
        if self.sets_name == 'CoLA':
            if more:
                return pred, truth
            else:
                matt = self.metric.print_matthew(np.array(pred), np.array(truth))
                return matt
        elif self.sets_name in ['RTE', 'MRPC', 'QNLI', 'MNLI', 'QQP', 'SST']:
            if more:
                acc, _, _, _ = self.metric(np.array(pred), np.array(truth))
                return acc, (pred, truth)
            else:
                return pred, truth
        elif self.sets_name in ['STS']:
            pred_pear = np.array(pred)
            pred_pear = np.clip(pred_pear, 0.0, 5.0)
            if more:
                pearson = self.metric(pred_pear, np.array(truth), sets_name=self.sets_name)
                return pearson, (pred_pear, truth)
            else:
                return pred_pear, truth
        else:
            acc, precision, recall, f1score = self.metric(np.array(pred), np.array(truth))
            return acc * 100
