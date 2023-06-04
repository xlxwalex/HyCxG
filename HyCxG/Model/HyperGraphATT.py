from torch import nn
from Model.Layer import HGAL
from Model.Layer import LayerNorm

class RHGAT(nn.Module):
    def __init__(self, args, device, input_size, inter_size, output_size, dropout=0.3, alpha=0.2, edge_trans=False, remove_layernorm=False):
        super(RHGAT, self).__init__()
        self.hgat      = HGAL(args, device, input_size, input_size, dropout=dropout, do_scale=True, edge_trans=edge_trans, remove_layernorm=remove_layernorm)
        # self.hgat    = HGAL_MH(args, device, input_size, input_size, dropout=dropout, do_scale=True, edge_trans=edge_trans, remove_layernorm=remove_layernorm) - Not available in this REPO
        self.dropout_1 = nn.Dropout(dropout)
        self.dropout_2 = nn.Dropout(dropout)
        # FFN + Rs
        self.leakyrelu = nn.LeakyReLU(alpha)
        self.linear_1  = nn.Linear(input_size, inter_size, bias=True)
        self.linear_2  = nn.Linear(inter_size, output_size, bias=True)
        self.layer_norm_1 = LayerNorm(args, device, input_size)
        self.layer_norm_2 = LayerNorm(args, device, input_size)

    def forward(self, hidden, HT, edge_emb):
        inter = self.hgat(hidden, HT, edge_emb)
        inter = self.dropout_1(inter)
        inter = self.layer_norm_1(inter + hidden)
        output = self.dropout_2(self.linear_2(self.leakyrelu(self.linear_1(inter))))
        output = self.layer_norm_2(output + inter)
        return output