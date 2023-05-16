import numpy as np
import spacy
import pickle
from tqdm import tqdm
import json

MAP_INV = {0 : 'neutral', 1 : 'positive', -1 : 'negative'}
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
    nlp = spacy.load('de')
    out_data = []
    for text in tqdm(data, desc='Processing'):
        sentence, term, polarity = text[0],  text[1], text[2]
        if len(term) <1:continue
        document = nlp(sentence.replace('$T$', term))
        tokens, pos_tag = zip(*[[token.text, token.tag_.split('_')[0]] for token in document])
        from_idx = len([tok.text for tok in nlp(sentence.split('$T$')[0])])
        term_tok = [tok.text for tok in nlp(term)]
        from_to = [[from_idx, from_idx + len(term_tok)]]
        predicted_dependencies = [token.dep_.split(':')[0] if token.dep_ != 'ROOT'  else 'root' for token in document]
        predicted_heads = [token.head.i+1 if token.dep_ != 'ROOT' else 0 for token in document]
        obj = {}
        obj['token'] = list(tokens)
        obj['pos'] = list(pos_tag)
        obj['head'] = predicted_heads
        obj['deprel'] = predicted_dependencies
        obj['aspects'] = [{
            'term': term_tok,
            'from' : from_to[0][0],
            'to' : from_to[0][1],
            'polarity' : MAP_INV[polarity]
        }]
        out_data.append(obj)
    return out_data

if __name__ == '__main__':
    train_data = read_data('germeval_train.raw')
    train_data = construct_data(train_data)
    with open('train.json', 'w', encoding='utf-8') as tr_fp:
        json_str = json.dumps(train_data, indent=4)
        tr_fp.write(json_str)
    tr_fp.close()

    valid_data = read_data('germeval_valid.raw')
    valid_data = construct_data(valid_data)
    with open('valid.json', 'w', encoding='utf-8') as va_fp:
        json_str = json.dumps(valid_data, indent=4)
        va_fp.write(json_str)
    va_fp.close()

    test_data = read_data('germeval_test.raw')
    test_data = construct_data(test_data)
    with open('test.json', 'w', encoding='utf-8') as te_fp:
        json_str = json.dumps(test_data, indent=4)
        te_fp.write(json_str)
    te_fp.close()
    print('WELL DONE.')
