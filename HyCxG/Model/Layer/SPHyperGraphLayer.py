import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from Model.Layer.LayerNorm import LayerNorm

INF_SUB_NUM = -9e15

# Simplified version
class HyperGraphAttentionLayer(nn.Module):
    def __init__(self, args, device, input_size, output_size, dropout, do_scale=True, edge_trans=False, remove_layernorm=False):
        super(HyperGraphAttentionLayer, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.scale = do_scale
        self.layernorm = not remove_layernorm
        if self.layernorm: self.lnorm = LayerNorm(args, device, input_size)
        self.wnk = Parameter(torch.Tensor(self.input_size, self.output_size))
        self.wek = Parameter(torch.Tensor(self.output_size, self.output_size))
        if edge_trans: self.w_edge = Parameter(torch.Tensor(self.input_size, self.input_size))
        else: self.register_parameter('w_edge', None)
        self.dropout_emb = nn.Dropout(dropout)
        self.dropout = nn.Dropout(dropout)
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1. / math.sqrt(self.output_size)
        self.wnk.data.uniform_(-stdv, stdv)
        self.wek.data.uniform_(-stdv, stdv)
        if self.w_edge is not None: self.w_edge.data.uniform_(-stdv, stdv)

    def forward(self, hidden, ht, edge_emb):
        if self.layernorm: edge_emb = self.lnorm(edge_emb)
        edge_emb = self.dropout_emb(edge_emb)
        node_k = hidden.matmul(self.wnk)
        if self.w_edge is not None: edge_q = torch.matmul(edge_emb, self.w_edge)
        else: edge_q = edge_emb
        edge_attnscores = torch.matmul(edge_q, node_k.permute(0, 2, 1))
        if self.scale: edge_attnscores = edge_attnscores * (1 / (self.input_size ** (1/2)))
        zero_vec = INF_SUB_NUM * torch.ones_like(edge_attnscores)
        edge_attnscores = torch.where(ht > 0, edge_attnscores, zero_vec)
        attention_edge = F.softmax(edge_attnscores, dim=2)
        edge_h = torch.matmul(attention_edge, hidden)
        edge_h = self.dropout(edge_h)
        edge_h = edge_h + edge_emb
        edge_k = edge_h.matmul(self.wek)
        node_q = node_k
        node_attnscores = torch.matmul(node_q, edge_k.permute(0, 2, 1))
        if self.scale: node_attnscores = node_attnscores * (1 / (self.input_size ** (1/2)))
        zero_vec = INF_SUB_NUM * torch.ones_like(node_attnscores)
        node_attnscores = torch.where(ht.permute(0, 2, 1) > 0, node_attnscores, zero_vec)
        attention_node = F.softmax(node_attnscores, dim=1)
        node_hidden = torch.matmul(attention_node, edge_h)
        return node_hidden