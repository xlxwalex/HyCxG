import torch
from torch import nn
from argparse import Namespace
from Model.lm import LM
from Model.HyperGraphATT import RHGAT
from Model.Layer.Linear import Linear

class HyperCxG(nn.Module):
    def __init__(self, args : Namespace, device : torch.device):
        super(HyperCxG, self).__init__()
        self.device = device
        # LM model
        self.lm = LM(args, device, use_encoder=True, pooler_output=False)
        self.lm_dropout = nn.Dropout(args.lm_dropout)
        # Edge embedding
        self.edgemb = nn.Embedding(args.cxg_vocab_size, args.lm_hidden_size, padding_idx=0)
        # Relational hyper-graph attention network
        self.hgatt  = RHGAT(args, device, args.lm_hidden_size, args.inter_size, args.lm_hidden_size, args.hg_dropout, args.leaky_alpha, args.edge_trans, args.remove_layernorm)
        # Classifier
        self.classifier = Linear(args.lm_hidden_size, args.num_classes)
        self.do_squeeze = args.num_classes == 1 # Combine for this repo

    def forward(self, input: torch.Tensor, attention_mask: torch.Tensor, HT: torch.Tensor, edges: torch.Tensor, adj_matrix: torch.Tensor, node_mask: torch.Tensor, asp_masks: torch.Tensor):
        # adj_matrix and asp_masks is not available in this repo
        # Encoder
        encoded = self.lm(input, attention_mask = attention_mask)
        encoded = self.lm_dropout(encoded)
        edge_emb = self.edgemb(edges)
        # RHGAT
        hidden = self.hgatt(encoded, HT, edge_emb)
        # Pooling
        node_wn = node_mask.sum(dim=1).unsqueeze(-1)
        mask = node_mask.unsqueeze(-1).repeat(1, 1, hidden.shape[-1])
        final = (hidden * mask).sum(dim=1) / node_wn
        outputs = self.classifier(final)
        if self.do_squeeze: outputs = outputs.squeeze(-1) # Combine for this repo
        return outputs