from __future__ import absolute_import
from __future__ import division
import sys
sys.path.append('..')
import json
import os
import numpy as np
import pandas as pd
import argparse
from tqdm import tqdm
import spacy

MAP_POLARITY = {0 : 'neutral', 1 : 'positive', -1 : 'negative'}

def initialize_spacy(lang: str='de'):
    try: nlpmodel = spacy.load(lang)
    except: raise 'The script need spacy>=2.3.5 package, you need to proceed `pip install spacy` first.'
    return nlpmodel

def convert_raw2json(path : str, nlpmodel, desc: str='train'):
    data = []
    with open(path, 'r', encoding='utf-8') as fp:
        raw_data = fp.readlines()
    fp.close()
    for idx in tqdm(range(0, len(raw_data), 3), desc='Process {} file in GermEval'.format(desc)):
        obj = {}
        sentence = raw_data[idx].strip()
        target = raw_data[idx + 1].strip()
        polarity = MAP_POLARITY[eval(raw_data[idx + 2].strip())]
        if '$T$' not in sentence:
            print('Error sentence : %s' % sentence)
            continue
        post_sentence = sentence.replace('$T$', target)
        document = nlpmodel(post_sentence)
        tokens, pos_tag = zip(*[[token.text, token.tag_.split('_')[0]] for token in document])
        obj['token'] = list(tokens)
        pos_tag = list(pos_tag)
        obj['pos'] = pos_tag
        heads = [token.head.i + 1 if token.dep_ != 'ROOT' else 0 for token in document]
        rels = [token.dep_.split(':')[0] if token.dep_ != 'ROOT' else 'root' for token in document]
        obj['head'] = heads
        obj['deprel'] = rels
        term, targl = [tok.text for tok in nlpmodel(target)], [tok.text for tok in nlpmodel(sentence.split('$T$')[0])]
        obj['aspects'] = [{
            'term' : term,
            'from' : len(targl),
            'to' : len(targl) + len(term),
            'polarity' : polarity
        }]
        data.append(obj)
    return data

def read_semeval_data(path : str):
    data_out = []
    data = np.array(pd.read_csv(path))
    for dat in data: data_out.append([dat[0], dat[2], dat[1]])
    return data_out

def output_json(data: list, folder_path: str, file_path: str):
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    with open(os.path.join(folder_path, file_path), 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(data, indent=4))
    fp.close()

def process_data(args: argparse.Namespace):
    assert os.path.exists(args.train_file) and os.path.exists(args.test_file) and os.path.exists(args.test_file), "The path of data is not exist, please download first."
    train_json = convert_raw2json(args.train_file, args.nlpmodel)
    output_json(train_json, args.out_path, 'train.json')
    print('The train file of GermEval dataset is saved at %s' % os.path.join(args.out_path, 'train.json'))

    valid_json = convert_raw2json(args.valid_file, args.nlpmodel, desc='valid')
    output_json(valid_json, args.out_path, 'valid.json')
    print('The valid file of GermEval dataset is saved at %s' % os.path.join(args.out_path, 'valid.json'))

    test_json = convert_raw2json(args.test_file, args.nlpmodel, desc='test')
    output_json(test_json, args.out_path, 'test.json')
    print('The test file of GermEval dataset is saved at %s' % os.path.join(args.out_path, 'test.json'))

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--out_path", default='dataset/JSONABSA_German', type=str, help="Output path of GermEval dataset.")
    parser.add_argument("--train_file", default='germeval_train.raw', type=str, help="The path of train file.")
    parser.add_argument("--valid_file", default='germeval_valid.raw', type=str, help="The path of valid file.")
    parser.add_argument("--test_file", default='germeval_test.raw', type=str, help="The path of test file.")
    args = parser.parse_args()
    args.nlpmodel = initialize_spacy()
    process_data(args)
    print('GermEval data has been processed.')

if __name__ == '__main__':
    main()
