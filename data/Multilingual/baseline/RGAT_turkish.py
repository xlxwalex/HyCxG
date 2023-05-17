import numpy as np
import pickle
from tqdm import tqdm
import json

import stanfordnlp
nlpmodel = stanfordnlp.Pipeline(processors='tokenize,pos,depparse', lang="tr")

MAP_INV = {0 : 'neutral', 1 : 'positive', -1 : 'negative'}

def parse_adj(edge):
    e_id, dep_rels, dep_heads = 1, [], []
    for eidx in range(len(edge)):
        if (eidx + 1) != edge[0][2]:
            dep_heads.append(edge[e_id][1])
            dep_rels.append(edge[e_id][0])
            e_id += 1
        else:
            dep_heads.append(0)
            dep_rels.append(edge[0][0])
    return dep_heads, dep_rels


def obtain_annotate(results: dict, only_tokens: bool=False, encode_eng:bool=False):
    tokens, postag, heads, deprels, deps = [], [], [], [], []
    for sentence in results.sentences:
        tok, pos = zip(*[[word.text, word.xpos.split('|')[0].upper()] for word in sentence.words])
        postag.extend(pos)
        tokens.extend(tok)
        dep = [(word.dependency_relation, word.governor, eval(word.index)) for word in sentence.words]
        head, rel = parse_adj(dep)
        heads.extend([he+len(heads) for he in head])
        deprels.extend(rel)
        dep =[list(gr) for gr in dep]
        for idx in range(len(dep)):
            if dep[idx][1] !=0:dep[idx][1] += len(deps)
            dep[idx][2] += len(deps)
            if dep[idx][0] == 'ROOT' : dep[idx][0] = 'root'
        deps.extend(dep)
    if not only_tokens:
        return tokens, postag, deps, heads, deprels
    else:
        return tokens


def read_data(path : str):
    with open(path, 'r') as fp:
        data = fp.readlines()
    fp.close()
    data_gp = []
    for idx in range(0, len(data), 3):
        sentence = data[idx].strip()
        term = data[idx+1].strip()
        polarity = eval(data[idx+2].strip())
        data_gp.append([sentence, term, polarity])
    return data_gp

def construct_data(data : list):
    out_data = []
    for text in tqdm(data, desc='Processing'):
        sentence, term, polarity = text[0],  text[1], text[2]
        results = nlpmodel(sentence.replace('$T$', term))
        tokens, pos_tag, deps, heads, rels = obtain_annotate(results)
        predicted_heads = [ele[1] for ele in deps]
        sentence_post = sentence.replace('$T$', term)
        aspect_sentiment = [[term, MAP_INV[polarity]]]
        tok_lr = sentence.split('$T$')[0]
        if len(tok_lr) < 1:
            from_idx = 0
        else:
            from_idx = len(obtain_annotate(nlpmodel(sentence.split('$T$')[0]), only_tokens=True))
        term_tok = len(obtain_annotate(nlpmodel(term), only_tokens=True))
        from_to = [[from_idx, from_idx + term_tok]]
        obj = {}
        obj['sentence'] = sentence_post
        obj['tokens'] = list(tokens)
        obj['tags'] = list(pos_tag)
        obj['predicted_dependencies'] = rels
        obj['predicted_heads'] = predicted_heads
        obj['dependencies'] = deps
        obj['aspect_sentiment'] = aspect_sentiment
        obj['from_to'] = from_to
        out_data.append(obj)
    return out_data

if __name__ == '__main__':
    train_data = read_data('restaurant_train.raw')
    train_data = construct_data(train_data)
    with open('restaurant_Train.json', 'w', encoding='utf-8') as tr_fp:
        json_str = json.dumps(train_data, indent=4)
        tr_fp.write(json_str)
    tr_fp.close()

    test_data = read_data('restaurant_test.raw')
    test_data = construct_data(test_data)
    with open('restaurant_Test.json', 'w', encoding='utf-8') as te_fp:
        json_str = json.dumps(test_data, indent=4)
        te_fp.write(json_str)
    te_fp.close()
    print('WELL DONE.')
