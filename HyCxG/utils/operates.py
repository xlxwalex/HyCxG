import numpy as np
import torch
from scipy.special import logsumexp
from utils.define import LM_PAD

def _padding(inputs : list, paddings : int, pad_val : int, lm_group : str = 'BERT') -> np.ndarray:
    if lm_group in LM_PAD.keys():
        pad_val = LM_PAD[lm_group]
    doc = np.array([
        np.pad(x[0:paddings], ( 0, paddings - len(x[0:paddings])),
               'constant', constant_values=pad_val)
        for x in inputs
    ]).astype('int64')
    return doc

def _pad_adj(inputs : list, paddings : int, pad_val : int) -> np.ndarray:
    batch = len(inputs)
    adjs = np.zeros((batch, paddings, paddings)) # Not available in this repo
    return adjs

def _attention_mask(padded : np.ndarray, pad_val : int, lm_group : str = 'BERT') -> torch.Tensor:
    if lm_group in LM_PAD.keys():
        pad_val = LM_PAD[lm_group]
    np_mask = (padded != pad_val).astype('int32')
    return torch.from_numpy(np_mask)

def _save_model(path : str, checkp : dict) -> None:
    torch.save(checkp, path)

def _normalize_logits(logits):
    numerator = logits
    denominator = logsumexp(logits)
    return numerator - denominator

def _softmax_logits(logits :torch.Tensor, dim : int = 1):
    return torch.softmax(logits, dim=dim)