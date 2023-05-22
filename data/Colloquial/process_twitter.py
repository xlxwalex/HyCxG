from __future__ import absolute_import
from __future__ import division
import sys
import json
import os
import numpy as np
import pandas as pd
import argparse
from tqdm import tqdm
from stanfordcorenlp import StanfordCoreNLP
try:
    sys.path.append('.')
    from download_stanfordcore import download_stanfordcore, unzip_stanfordcore, STANFORD_CORE_LINK
except:
    sys.path.append('..')
    from download_stanfordcore import download_stanfordcore, unzip_stanfordcore, STANFORD_CORE_LINK


MAP_POLARITY = {0 : 'neutral', 1 : 'positive', -1 : 'negative'}

def initialize_stanfordcore(stanford_path: str):
    try: nlpmodel = StanfordCoreNLP(stanford_path)
    except:
        print('The script need stanfordparser>=3.9.2 package, while the path is not exist for the package, do you want to download it? (Y/N)')
        download_flag = input()
        download_flag = download_flag.lower()
        assert download_flag in ['y'], "Abort"
        download_stanfordcore(STANFORD_CORE_LINK, stanford_path+'.zip')
        unzip_stanfordcore(stanford_path+'.zip', '../')
        nlpmodel = StanfordCoreNLP(stanford_path)
    return nlpmodel

def convert_raw2json(path : str, nlpmodel, desc: str='train'):
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

    data = []
    with open(path, 'r', encoding='utf-8') as fp:
        raw_data = fp.readlines()
    fp.close()
    for idx in tqdm(range(0, len(raw_data), 3), desc='Process {} file in Twitter'.format(desc)):
        obj = {}
        sentence = raw_data[idx].strip()
        target = raw_data[idx + 1].strip()
        polarity = MAP_POLARITY[eval(raw_data[idx + 2].strip())]
        if '$T$' not in sentence:
            print('Error sentence : %s' % sentence)
            continue
        post_sentence = sentence.replace('$T$', target)
        obj['token'] = nlpmodel.word_tokenize(post_sentence)
        pos_tag = nlpmodel.pos_tag(post_sentence)
        dependecy = nlpmodel.dependency_parse(post_sentence)
        obj['pos'] = [tag[1] for tag in pos_tag]
        heads, rels = parse_adj(dependecy)
        obj['head'] = heads
        obj['deprel'] = rels
        obj['aspects'] = [{
            'term' : nlpmodel.word_tokenize(target),
            'from' : len(nlpmodel.word_tokenize(sentence.split('$T$')[0])),
            'to' : len(nlpmodel.word_tokenize(sentence.split('$T$')[0])) + len(nlpmodel.word_tokenize(target)),
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
    assert os.path.exists(args.train_file) and os.path.exists(args.test_file), "The path of data is not exist, please download first."
    train_json = convert_raw2json(args.train_file, args.nlpmodel)
    output_json(train_json, args.out_path, 'train.json')
    print('The train file of Twitter dataset is saved at %s' % os.path.join(args.out_path, 'train.json'))

    test_json = convert_raw2json(args.test_file, args.nlpmodel, desc='test')
    output_json(test_json, args.out_path, 'test.json')
    print('The test file of Twitter dataset is saved at %s' % os.path.join(args.out_path, 'test.json'))

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--out_path", default='dataset/JSONABSA_Twitter', type=str, help="Output path of twitter dataset.")
    parser.add_argument("--stanford_path", default='stanford-corenlp-3.9.2-minimal', type=str, help="The path for stanfordparser.")
    parser.add_argument("--train_file", default='twitter_train.raw', type=str, help="The path of train file.")
    parser.add_argument("--test_file", default='twitter_test.raw', type=str, help="The path of test file.")
    args = parser.parse_args()
    args.nlpmodel = initialize_stanfordcore(args.stanford_path)
    process_data(args)
    print('Twitter data has been processed.')

if __name__ == '__main__':
    main()
