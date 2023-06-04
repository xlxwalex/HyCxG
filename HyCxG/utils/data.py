from utils.define import ABSA_POLARITY_MAP, ABSAJSON_POLARITY_MAP, NLI_POLARITY_MAP
from utils.hypergraph import construct_graph
import numpy as np
import pandas as pd
import json
from copy import deepcopy

# Data Reader Part
def read_dataset(set_name : str, path : str):
    if set_name.startswith('ABSA'):
        data = read_absa_txtonly(path)
    elif set_name.startswith('JSONABSA'):
        if set_name.split('_')[-1] in ['French', 'Dutch', 'Turkish']:
            data = read_absa(path, do_lower_case=False)
        else:
            data = read_absa(path)
    elif set_name.startswith('JSONGLUE'):
        data = read_collate_glue(set_name, path)
    else:
        raise Exception('Cannot parse the dataset : {}'.format(set_name))
    return data

def read_collate_glue(set_name : str, path : str):
    dataset_name = set_name.split('_')[-1]
    if dataset_name in ['CoLA', 'SST', 'Counterfactual']:
        data_out = read_single(path)
    elif dataset_name in ['RTE', 'MNLIM', 'MNLI']:
        data_out = read_nli_data(path, dataset_name)
    elif dataset_name in ['QNLI']:
        data_out = read_qnli_data(path, dataset_name)
    elif dataset_name in ['MRPC', 'STS', 'QQP']:
        data_out = read_mrpc_data(path, dataset_name)
    else:
        raise Exception('Cannot parse the glue dataset : {}'.format(dataset_name))
    return data_out

def read_mrpc_data(path : str, sets : str):
    data_out = []
    with open(path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        for obj in data:
            sentence1 = obj['sentence1']
            sentence1 = [t.lower() for t in sentence1]
            sentence2 = obj['sentence2']
            sentence2 = [t.lower() for t in sentence2]
            label = obj['label']
            data_out.append([sentence1, sentence2, label])
    return data_out

def read_nli_data(path : str, sets : str):
    data_out = []
    with open(path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        for obj in data:
            premise = obj['premise']
            premise = [t.lower() for t in premise]
            hypothesis = obj['hypothesis']
            hypothesis = [t.lower() for t in hypothesis]
            label = NLI_POLARITY_MAP[sets][obj['label']]
            data_out.append([premise, hypothesis, label])
    return data_out

def read_qnli_data(path : str, sets : str):
    data_out = []
    with open(path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        for obj in data:
            question = obj['question']
            question = [t.lower() for t in question]
            sentence = obj['sentence']
            sentence = [t.lower() for t in sentence]
            label = NLI_POLARITY_MAP[sets][obj['label']]
            data_out.append([question, sentence, label])
    return data_out

def read_single(path : str):
    data_out = []
    with open(path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        for obj in data:
            sentence = obj['token']
            sentence = [t.lower() for t in sentence]
            polarity = obj['label']
            data_out.append([sentence, polarity])
    return data_out

def read_absa(path : str, do_lower_case:bool = True):
    data_out = []
    with open(path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        data = unpack(data)
        for obj in data:
            sentence = obj['token']
            sentence = [t.lower() if do_lower_case else t for t in sentence]
            aspect = obj['aspects'][0]
            term = ' '.join(aspect['term'])
            from_to = [aspect['from'], aspect['to']]
            polarity = ABSAJSON_POLARITY_MAP[aspect['polarity']]
            data_out.append([sentence, term, from_to, polarity])
    fp.close()
    return data_out

def construct_dependency_graph(args, data):
    # Not available in this repo
    adjs = []
    return adjs

def unpack(json_data : list):
    data = []
    for item in json_data:
        aspects = item['aspects']
        if len(aspects) < 2:
            data.append(item)
        else:
            for aspidx in range(len(aspects)):
                new_item = deepcopy(item)
                new_item['aspects'] = [item['aspects'][aspidx]]
                data.append(new_item)
    return data

def tokenize_aspect(tokenizer, sentence : list, from_to : list, adj : np.array = None):
    tokens, aspect_mask = [], []
    if adj is not None:
        adjrow_expand, adjcol_expand, counter = [], [], []
    for tokidx in range(len(sentence)):
        tok = sentence[tokidx]
        tok = tokenizer.tokenize(tok)
        tokens.extend(tok)
        if adj is not None:
            counter.append(len(tok))
            adjrow_expand.extend([adj[tokidx, :]] * len(tok))
        if tokidx >= from_to[0] and tokidx < from_to[1]:
            aspect_mask += [1] * len(tok)
        else:
            aspect_mask += [0] * len(tok)
    if adj is not None:
        adj_row = np.vstack(adjrow_expand)
        for tokidx in range(len(counter)):
            adjcol_expand.extend([adj_row[:, tokidx]] * counter[tokidx])
        adj = np.vstack(adjcol_expand).T
        return tokens, aspect_mask, ' '.join(sentence), adj
    else:
        return tokens, aspect_mask, ' '.join(sentence)

def tokenize_glue(tokenizer, sentence : list, adj : np.array = None):
    tokens = []
    if adj is not None:
        adjrow_expand, adjcol_expand, counter = [], [], []
    for tokidx in range(len(sentence)):
        tok = sentence[tokidx]
        tok = tokenizer.tokenize(' ' + tok)
        tokens.extend(tok)
        if adj is not None:
            counter.append(len(tok))
            adjrow_expand.extend([adj[tokidx, :]] * len(tok))
    if adj is not None:
        adj_row = np.vstack(adjrow_expand)
        for tokidx in range(len(counter)):
            adjcol_expand.extend([adj_row[:, tokidx]] * counter[tokidx])
        adj = np.vstack(adjcol_expand).T
        return tokens, ' '.join(sentence), adj
    else:
        return tokens, ' '.join(sentence)

def reconstruct_sentence(tokens : list, lmg : str = 'BERT'):
    if lmg == 'BERT':
        sentence = ' '.join(tokens).replace(' #', '')
    elif lmg == 'RoBERTa':
        sentence = ''.join(tokens).replace(chr(288), ' ')
    else:
        raise Exception('Error for parse the languege model name : {}'.format(lmg))
    return sentence

def read_absa_txtonly(path : str):
    data_out = []

    def collate_absa(data, idx):
        sentence = data[idx].strip()
        aspect = data[idx + 1].strip()
        polarity = ABSA_POLARITY_MAP[eval(data[idx + 2].strip())]
        filled = sentence.replace('$T$', aspect)
        if '$' in filled and aspect not in filled:
            'Sentence Err : {}'.format(sentence)
        return [filled, aspect, polarity]

    with open(path, 'r', encoding='utf-8') as fp:
        data = fp.readlines()
        for idx in range(0, len(data), 3):
            data_out.append(collate_absa(data, idx))
    fp.close()
    return data_out

def pair_hypocxg(connections : list, bias : int):
    new_connections = []
    for conn in connections:
        new_connections.append((conn[0] + bias, conn[1] + bias, conn[2], conn[3]))
    return new_connections

# Data Collate-Fn for ABSA
def collate_hypercxg_aspect(batch):
    pad_size = batch[0]['padding']
    tok_ids = [item['tok'] for item in batch]
    masks = [item['mask'] for item in batch]
    aspmasks = [item['aspmask'] for item in batch]
    cxgs = [item['cxg'] for item in batch]
    adjs = [item['adj'] for item in batch]
    labels = [item['label'] for item in batch]
    hyper_results = construct_graph(cxgs, masks, pad_size)
    if isinstance(hyper_results, int):
        print('Error prompt : {}'.format(' '.join(batch[hyper_results]['aux_token'])))
        raise Exception('Error in hyper graph construction.')
    HT, edges = hyper_results
    return tok_ids, masks, aspmasks, np.array(HT), np.array(edges), adjs, np.array(labels)

# Data Collate-Fn for GLUE and Counterfactual
def collate_hypercxg_glue(batch):
    pad_size = batch[0]['padding']
    tok_ids = [item['tok'] for item in batch]
    masks = [item['mask'] for item in batch]
    cxgs = [item['cxg'] for item in batch]
    adjs = [item['adj'] for item in batch]
    labels = [item['label'] for item in batch]
    HT, edges = construct_graph(cxgs, masks, pad_size)
    return tok_ids, masks, np.array(HT), np.array(edges), adjs, np.array(labels)

def calculate_cxg_size(args, dataset):
    args.cxg_vocab_size = len(dataset.cxgprocessor.cons_vocab)
    return args

# Prediction output
def output_results(out_path, testset, results, sets='JSONABSA'):
    if sets.startswith('JSONABSA'):
        sentence, aspect, _, _ = list(zip(*testset.data))
        sentence = [' '.join(sent) for sent in sentence]
        out_array = np.vstack((np.array(sentence), np.array(aspect), np.array(results))).T
        df = pd.DataFrame(out_array, columns=['Sentence', 'Aspects', 'Preds', 'Gts'])
    elif 'GLUE' in sets:
        set = sets.split('_')[-1]
        if set in ['CoLA', 'SST', 'Counterfactual']:
            sentence, _ = list(zip(*testset.data))
            sentence = [' '.join(sent) for sent in sentence]
            out_array = np.vstack((np.array(sentence), np.array(results[0]))).T
            df = pd.DataFrame(out_array, columns=['sentence', 'label'])
        elif set in ['RTE', 'MRPC', 'STS', 'QNLI', 'MNLI', 'QQP']:
            premise, hypothesis, _ = list(zip(*testset.data))
            premise_sentence = [' '.join(sent) for sent in premise]
            hypothesis_sentence = [' '.join(sent) for sent in hypothesis]
            out_array = np.vstack((np.array(premise_sentence), np.array(hypothesis_sentence), np.array(results))).T
            df = pd.DataFrame(out_array, columns=['Premise', 'Hypothesis', 'Preds', 'Gts'])
        else:
            raise Exception('[ERROR] error mode to parse the results for GLUE dataset')
    else:
        raise Exception('[ERROR] error mode to parse the results')
    df.to_csv(out_path, index=False, encoding='utf_8_sig')
