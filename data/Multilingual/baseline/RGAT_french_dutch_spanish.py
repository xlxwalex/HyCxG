import numpy as np
import spacy
import pickle
from tqdm import tqdm
import json
nlp = spacy.load('fr') # fr - franch / es - spanish / nl -dutch
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
    out_data = []
    for text in tqdm(data, desc='Processing'):
        sentence, term, polarity = text[0],  text[1], text[2]
        document = nlp(sentence.replace('$T$', term))
        tokens, pos_tag = zip(*[[token.text, token.tag_.split('_')[0]] for token in document])
        sentence_post = sentence.replace('$T$', term)
        aspect_sentiment = [[term, MAP_INV[polarity]]]
        from_idx = len([tok.text for tok in nlp(sentence.split('$T$')[0])])
        term_tok = len([tok.text for tok in nlp(term)])
        from_to = [[from_idx, from_idx + term_tok]]
        predicted_dependencies = [token.dep_.split(':')[0] if token.dep_ != 'ROOT'  else 'root' for token in document]
        predicted_heads = [token.head.i+1 if token.dep_ != 'ROOT' else 0 for token in document]
        dependencies = [list(ele) for ele in list(zip(predicted_dependencies, predicted_heads, list(range(1, len(predicted_heads) + 1))))]
        obj = {}
        obj['sentence'] = sentence_post
        obj['tokens'] = list(tokens)
        obj['tags'] = list(pos_tag)
        obj['predicted_dependencies'] = predicted_dependencies
        obj['predicted_heads'] = predicted_heads
        obj['dependencies'] = dependencies
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
