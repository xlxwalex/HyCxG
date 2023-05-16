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
from stanfordcorenlp import StanfordCoreNLP
try: from datasets import load_dataset
except: raise Exception('GLUE benchmark needs datasets package of Hugging Face, please use pip to install the package first.')
try: from download_stanfordcore import download_stanfordcore, unzip_stanfordcore, STANFORD_CORE_LINK
except: from ..download_stanfordcore import download_stanfordcore, unzip_stanfordcore, STANFORD_CORE_LINK

LABEL_MAPPING = {
    'qnli': {0: 'entailment', 1: 'not entailment', -1 : 'none'},
    'mnli': {0: 'entailment', 1: 'neutral', 2: 'contradiction', -1: 'none'},
    'rte': {0: 'entailment', 1: 'not_entailment', -1: 'none'}
}

COLUMNS = {
    'cola': ['idx', 'sentence', 'label'],
    'sst2': ['idx', 'sentence', 'label'],
    'mnli': ['idx', 'premise', 'hypothesis', 'label'],
    'qnli': ['idx', 'question', 'sentence', 'label'],
    'qqp': ['idx', 'question1', 'question2', 'label'],
    'rte': ['idx', 'sentence1', 'sentence2', 'label'],
    'mrpc': ['idx', 'sentence1', 'sentence2', 'label'],
    'stsb': ['idx', 'sentence1', 'sentence2', 'label'],
}

FOLDER_MAPPING = {
    'cola': 'GLUE_CoLA',
    'sst2': 'GLUE_SST-2',
    'mnli': 'GLUE_MNLI',
    'qnli': 'GLUE_QNLI',
    'qqp': 'GLUE_QQP',
    'rte': 'GLUE_RTE',
    'mrpc': 'GLUE_MRPC',
    'stsb': 'GLUE_STS-B'
}

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

def read_json_data(task: str, desc: str='train'):
    data = []
    for item in tqdm(load_dataset('glue', task, split=desc), desc='load {}-{} data'.format(task, desc)):
        data.append([item[col] for col in COLUMNS[task]])
    return data

def process_single_data(data: list, nlpmodel, task_name: str, desc: str='train'):
    data_out = []
    for dat in tqdm(data, desc='Process {} file for {}'.format(desc, task_name)):
        obj = {}
        gid = dat[0]
        obj['id'] = gid
        sentence = dat[1].strip()
        label = dat[2]
        pos_tag = nlpmodel.pos_tag(sentence)
        obj['token'] = nlpmodel.word_tokenize(sentence)
        obj['pos'] = [tag[1] for tag in pos_tag]
        obj['label'] = label
        data_out.append(obj)
    return data_out

def process_pair_data(data: list, nlpmodel, task_name: str, desc: str='train'):
    data_out = []
    for dat in tqdm(data, desc='Process {} file for {}'.format(desc, task_name)):
        obj ={}
        gid =dat[0]
        obj['id'] = gid
        premise = dat[1].strip()
        hypothesis = dat[2].strip()
        label = dat[3]
        obj['sentence1'] = nlpmodel.word_tokenize(premise)
        obj['sentence2'] = nlpmodel.word_tokenize(hypothesis)
        obj['label'] = label if task_name not in LABEL_MAPPING else LABEL_MAPPING[task_name][label]
        data_out.append(obj)
    return data_out

def output_json(data: list, folder_path: str, file_path: str):
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    with open(os.path.join(folder_path, file_path), 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(data, indent=4))
    fp.close()

def process_data(args):
    if 'all' in args.task: args.task = 'cola sst2 mnli qnli qqp rte mrpc stsb'.split()
    for task in args.task:
        assert task in 'cola sst2 mnli qnli qqp rte mrpc stsb'.split(), 'the task name of `{}` is incorrect.'.format(task)
        train_data = read_json_data(task)
        if task in ['cola', 'sst2']: train_json = process_single_data(train_data, args.nlpmodel, task)
        else: train_json = process_pair_data(train_data, args.nlpmodel, task)
        output_json(train_json, os.path.join(args.out_path, FOLDER_MAPPING[task]), 'train.json')
        if task not in ['MNLI']:
            dev_data = read_json_data(task, 'validation')
            if task in ['cola', 'sst2']: dev_json = process_single_data(dev_data, args.nlpmodel, task, 'validation')
            else: dev_json = process_pair_data(dev_data, args.nlpmodel, task, 'validation')
            output_json(dev_json, os.path.join(args.out_path, FOLDER_MAPPING[task]), 'valid.json')
            test_data = read_json_data(task, 'test')
            if task in ['cola', 'sst2']: test_json = process_single_data(test_data, args.nlpmodel, task, 'test')
            else: test_json = process_pair_data(test_data, args.nlpmodel, task, 'test')
            output_json(test_json, os.path.join(args.out_path, FOLDER_MAPPING[task]), 'test.json')
        else:
            dev_matched_data = read_json_data(task, 'validation_matched')
            dev_matched_json = process_pair_data(dev_matched_data, args.nlpmodel, task, 'validation_matched')
            output_json(dev_matched_json, os.path.join(args.out_path, FOLDER_MAPPING[task]), 'valid_m.json')
            dev_mismatched_data = read_json_data(task, 'validation_mismatched')
            dev_mismatched__json = process_pair_data(dev_mismatched_data, args.nlpmodel, task, 'validation_mismatched')
            output_json(dev_mismatched__json, os.path.join(args.out_path, FOLDER_MAPPING[task]), 'valid_mm.json')
            test_matched_data = read_json_data(task, 'test_matched')
            test_matched_json = process_pair_data(test_matched_data, args.nlpmodel, task, 'test_matched')
            output_json(test_matched_json, os.path.join(args.out_path, FOLDER_MAPPING[task]), 'test_m.json')
            test_mismatched_data = read_json_data(task, 'test_mismatched')
            test_mismatched__json = process_pair_data(test_mismatched_data, args.nlpmodel, task, 'test_mismatched')
            output_json(test_mismatched__json, os.path.join(args.out_path, FOLDER_MAPPING[task]), 'test_mm.json')
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--out_path", default='dataset', type=str, help="Output path of glue dataset.")
    parser.add_argument("--task", default=[], nargs='+', type=str, help="List of glue task.")
    parser.add_argument("--stanford_path", default='stanford-corenlp-3.9.2-minimal', type=str, help="The path for stanfordparser.")
    args = parser.parse_args()
    args.nlpmodel = initialize_stanfordcore(args.stanford_path)
    process_data(args)
    print('GLUE benchmark has been processed.')

if __name__ == '__main__':
    main()