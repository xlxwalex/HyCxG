import numpy as np
import scipy.sparse as sp

def construct_graph(cxg, mask, pad_len : int = 150):
    assert len(cxg) == len(mask)
    HT, edges = [], []
    max_n_edge = max([len(item) + 1 for item in cxg])
    for idx in range(len(cxg)):
        bs_cxg = cxg[idx]

        rows = []
        cols = []
        vals = []

        edge_labels = []
        for edge in range(len(bs_cxg)):
            start = bs_cxg[edge][0] + 1     # 1 - CLS
            end = bs_cxg[edge][1] + 1       # 1 - CLS
            edge_label = bs_cxg[edge][2]    # CxG Index
            edge_labels.append(edge_label)
            for node in range(start, end):
                rows.append(node)
                cols.append(edge)
                vals.append(1.0)

        # FULLY RELATION
        # Not available in this repo
        try:
            u_H = sp.coo_matrix((vals, (rows, cols)), shape=(pad_len, max_n_edge))
            HT.append(np.asarray(u_H.T.todense()))
        except:
            u_H = np.zeros((pad_len, max_n_edge), dtype=np.float)
            HT.append(u_H.T)
        edges.append(edge_labels + [0] * (max_n_edge - len(edge_labels)))
    return HT, edges

