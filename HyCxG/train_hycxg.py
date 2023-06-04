import os
from config import parse_args
from DataProcessor import HyperDataLM, KFoldWrapper
from torch.utils.data import DataLoader
import torch
from utils import get_device, set_seed, collate_hypercxg_glue as collate_fn_glue, collate_hypercxg_aspect as collate_fn_absa
from utils import DATASET_MAP, cal4scheduler, output_results, get_linear_schedule_with_warmup, calculate_cxg_size
from Model import HyperCxG as HyCxG
from transformers import AdamW
from Trainer import HyCxGTrainerABSA, HyCxGTrainerGLUE

def train(args, check_dirname = ""):
    print('=' * 50 + 'Train HyCxG Model' + '=' *50)
    # Checkpoint
    check_dir = args.checkpoints if check_dirname == "" else os.path.join(args.checkpoints, check_dirname)
    if os.path.exists(check_dir) is not True:
        os.makedirs(check_dir)
        print('>> Create Checkpoint Dir at %s' % check_dir)
    # Dataset
    # Note: the counterfactual dataset need to fit with KFoldWrapper module
    if os.path.exists(os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'train_{}{}.pt'.format(args.lm_group, args.lm_hidden_size))) is not True:
        Trainset = HyperDataLM(args, args.data_name, 'train', num_workers=args.num_workers)
        torch.save(Trainset, os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'train_{}{}.pt'.format(args.lm_group, args.lm_hidden_size)))
    else:
        Trainset = torch.load(os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'train_{}{}.pt'.format(args.lm_group, args.lm_hidden_size)))
        print('Direct Load Train Dataset')
    if os.path.exists(os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'valid_{}{}.pt'.format(args.lm_group, args.lm_hidden_size))) is not True:
        Validset = HyperDataLM(args, args.data_name, 'valid', num_workers=args.num_workers)
        torch.save(Validset, os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'valid_{}{}.pt'.format(args.lm_group, args.lm_hidden_size)))
    else:
        Validset = torch.load(os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'valid_{}{}.pt'.format(args.lm_group, args.lm_hidden_size)))
        print('Direct Load Valid Dataset')
    # DataLoader
    Trainloader = DataLoader(Trainset, batch_size=args.batch_size, shuffle=args.shuffle, drop_last=args.droplast, collate_fn=collate_fn_absa if 'ABSA' in args.data_name.split('_')[0] else collate_fn_glue)
    Validloader = DataLoader(Validset, batch_size=args.batch_size, shuffle=args.shuffle, drop_last=args.droplast, collate_fn=collate_fn_absa if 'ABSA' in args.data_name.split('_')[0] else collate_fn_glue)
    # Params calculation
    args = cal4scheduler(args, args.num_epoch, len(Trainset), args.batch_size, args.warmup_ratio)
    args = calculate_cxg_size(args, Trainset)
    # Device
    device = get_device(args.cuda, args.gpu_id)
    # Model
    model = HyCxG(args, device).to(device)
    # Optimizer & Criterion
    no_decay = ['bias', 'LayerNorm.weight', 'LayerNorm.gamma', 'Layernorm.beta']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': 1e-2},
        {'params': [p for n, p in model.named_parameters() if any(
            nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.lr)
    scheduler = get_linear_schedule_with_warmup(optimizer, args.warmup_steps, args.train_steps) if args.scheduler else None
    criterion = torch.nn.CrossEntropyLoss().to(device) if args.data_name.split('_')[-1] not in ['STS'] else torch.nn.MSELoss().to(device)
    trainer = HyCxGTrainerABSA(args, model, criterion, optimizer, device, check_dir, scheduler=scheduler) if 'ABSA' in args.data_name.split('_')[0] \
        else HyCxGTrainerGLUE(args, model, criterion, optimizer, device, check_dir, scheduler=scheduler, sets_name=args.data_name.split('_')[-1])
    trainer.train(Trainloader, Validloader)
    print('>>> Experiments finished.')

def test(args, check_dirname = ""):
    print('=' * 50 + 'Test HyCxG Model' + '=' * 50)
    args.__str__()
    if os.path.exists(os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'test_{}{}.pt'.format(args.lm_group, args.lm_hidden_size))) is not True:
        Testset = HyperDataLM(args, args.data_name, 'test', num_workers=args.num_workers)
        torch.save(Testset, os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'test_{}{}.pt'.format(args.lm_group, args.lm_hidden_size)))
    else:
        Testset = torch.load(os.path.join(DATASET_MAP[args.data_name]['base_dir'], 'test_{}{}.pt'.format(args.lm_group, args.lm_hidden_size)))
        print('Direct Load Test Dataset')
    # DataLoader
    Testloader = DataLoader(Testset, batch_size=args.batch_size, shuffle=False, drop_last=args.droplast, collate_fn=collate_fn_absa if 'ABSA' in args.data_name.split('_')[0] else collate_fn_glue)
    model_path = os.path.join(args.checkpoints, check_dirname, 'checkpoint.pt')
    args = calculate_cxg_size(args, Testset)
    device = get_device(args.cuda, args.gpu_id)
    # Model
    model = HyCxG(args, device).to(device)
    model_param = torch.load(model_path)['model']
    model.load_state_dict(model_param)
    trainer = HyCxGTrainerABSA(args, model, None, None, device, None) if 'ABSA' in args.data_name.split('_')[0] \
        else HyCxGTrainerGLUE(args, model, None, None, device, None, sets_name=args.data_name.split('_')[-1])
    _, pred_results = trainer.test(Testloader) if 'ABSA' in args.data_name.split('_')[0]  else trainer.test(Testloader, more=True)
    # Output file
    output_results(os.path.join(DATASET_MAP[args.data_name]['base_dir'], args.test_outpath), Testset, pred_results, sets=args.data_name)

if __name__ == '__main__':
    args = parse_args()
    set_seed(args)
    if args.mode == 'train':
        train(args, args.checkp)
    elif  args.mode == 'test':
        test(args, args.checkp)
    else:
        raise Exception('Error experiment mode `{}`'.format(args.mode))