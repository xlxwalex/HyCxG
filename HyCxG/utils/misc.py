import torch
import numpy as np
import random
from argparse import Namespace

# Device
def _get_device(cuda : bool, gpu_id : int = 0) -> torch.device:
    gpu_count = torch.cuda.device_count()
    if torch.cuda.is_available() and gpu_id < gpu_count:
        device = torch.device("cuda:" + str(gpu_id) if cuda else "cpu")
    else:
        device = torch.device("cpu")
    return device

# Seed
def set_seed(args):
    args.seed = int(args.seed)
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)
    torch.cuda.manual_seed(args.seed)

def print_config(args : Namespace):
    print(args)

def cal4scheduler(args, epoch_nums : int, train_num : int, batch_size : int, warm_up : float):
    import math
    train_steps = math.ceil(epoch_nums * train_num / batch_size)
    warm_up_steps = math.floor(train_steps * warm_up)
    args.train_steps = train_steps
    args.warmup_steps = warm_up_steps
    return args