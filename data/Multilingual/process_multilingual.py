from __future__ import absolute_import
from __future__ import division
import sys
sys.path.append('..')
import json
import os
import argparse
from tqdm import tqdm
import unicodedata
try:  import stanfordnlp
except: raise 'The script need stanfordnlp>=0.2.0 package, you need to proceed `pip install stanfordnlp` first.'
try: from stanza.server import CoreNLPClient
except: raise 'The script need stanza>=1.4.2 package, you need to proceed `pip install stanza` first.'

MAP_POLARITY = {0 : 'neutral', 1 : 'positive', -1 : 'negative'}
LANGUAGE_MAP = {'french': 'fr', 'spanish': 'spanish', 'turkish': 'tr', 'dutch': 'nl'}

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

def obtain_annotate_stanza(results: dict, only_tokens: bool=False, encode_eng:bool=False):
    sentences = results['sentences']
    tokens, postag, heads, deprels = [], [], [], []
    for sentence in sentences:
        if encode_eng:
            tok, pos = zip(*[[str(unicodedata.normalize('NFKD', ele['word']).encode('ascii', 'ignore'), encoding='utf-8'), ele['pos']] for ele in sentence['tokens']])
        else:
            tok, pos = zip(*[[ele['word'], ele['pos']]for ele in sentence['tokens']])
        postag.extend(pos)
        tokens.extend(tok)
        dep = [(ele['dep'], ele['governor'], ele['dependent']) for ele in sentence['basicDependencies']]
        head, rel = parse_adj(dep)
        heads.extend([he+len(heads) for he in head])
        deprels.extend(rel)
    if not only_tokens:
        return tokens, postag, heads, deprels
    else:
        return tokens

def obtain_annotate_stanford(results: dict, only_tokens: bool=False, encode_eng:bool=False):
    tokens, postag, heads, deprels = [], [], [], []
    for sentence in results.sentences:
        tok, pos = zip(*[[word.text, word.xpos.split('|')[0]] for word in sentence.words])
        postag.extend(pos)
        tokens.extend(tok)
        dep = [(word.dependency_relation if word.dependency_relation != 'root' else 'ROOT', word.governor, eval(word.index)) for word in sentence.words]
        head, rel = parse_adj(dep)
        heads.extend([he+len(heads) for he in head])
        deprels.extend(rel)
    if not only_tokens:
        return tokens, postag, heads, deprels
    else:
        return tokens


def convert_raw2json(path : str, desc: str='train', lang: str='french', port:int=9000):
    data = []
    with open(path, 'r', encoding='utf-8') as fp:
        raw_data = fp.readlines()
    fp.close()
    if lang in ['french', 'spanish']:
        with CoreNLPClient(start_server=0, endpoint='http://localhost:{}'.format(port) , output_format="json") as nlpmodel:
            for idx in tqdm(range(0, len(raw_data), 3), desc='Process {} file for {}'.format(desc, lang)):
                obj = {}
                sentence = raw_data[idx].strip()
                target = raw_data[idx + 1].strip()
                polarity = MAP_POLARITY[eval(raw_data[idx + 2].strip())]
                if '$T$' not in sentence:
                    print('Error sentence : %s' % sentence)
                    continue
                post_sentence = sentence.replace('$T$', target)
                results = nlpmodel.annotate(post_sentence, properties=LANGUAGE_MAP[lang])
                tokens, pos_tag, heads, rels = obtain_annotate_stanza(results)
                obj['token'] = tokens
                obj['pos'] = pos_tag
                obj['head'] = heads
                obj['deprel'] = rels
                context_l = sentence.split('$T$')[0]
                try: token_l = obtain_annotate_stanza(nlpmodel.annotate(context_l, properties=LANGUAGE_MAP[lang]), only_tokens=True)
                except: token_l = []
                token_term = obtain_annotate_stanza(nlpmodel.annotate(target, properties=LANGUAGE_MAP[lang]), only_tokens=True)
                obj['aspects'] = [{
                    'term' : obtain_annotate_stanza(nlpmodel.annotate(target, properties=LANGUAGE_MAP[lang]), only_tokens=True),
                    'from': len(token_l),
                    'to': len(token_l) + len(token_term),
                    'polarity' : polarity
                }]
                data.append(obj)
    else:
        nlpmodel = stanfordnlp.Pipeline(processors='tokenize,pos,depparse', lang=LANGUAGE_MAP[lang])
        for idx in tqdm(range(0, len(raw_data), 3), desc='Process {} file for {}'.format(desc, lang)):
            obj = {}
            sentence = raw_data[idx].strip()
            target = raw_data[idx + 1].strip()
            polarity = MAP_POLARITY[eval(raw_data[idx + 2].strip())]
            if '$T$' not in sentence:
                print('Error sentence : %s' % sentence)
                continue
            post_sentence = sentence.replace('$T$', target)
            results = nlpmodel(post_sentence)
            tokens, pos_tag, heads, rels = obtain_annotate_stanford(results)
            obj['token'] = tokens
            obj['pos'] = pos_tag
            obj['head'] = heads
            obj['deprel'] = rels
            context_l = sentence.split('$T$')[0]
            try: token_l = obtain_annotate_stanford(nlpmodel(context_l), only_tokens=True)
            except:token_l=[]
            token_term = obtain_annotate_stanford(nlpmodel(target), only_tokens=True)
            obj['aspects'] = [{
                'term': obtain_annotate_stanford(nlpmodel(target), only_tokens=True),
                'from': len(token_l),
                'to': len(token_l) + len(token_term),
                'polarity': polarity
            }]
            data.append(obj)
    return data

def output_json(data: list, folder_path: str, file_path: str):
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    with open(os.path.join(folder_path, file_path), 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(data, indent=4))
    fp.close()

def process_data(args: argparse.Namespace):
    assert os.path.exists(args.train_file) and os.path.exists(args.test_file), "The path of data is not exist, please download first."
    train_json = convert_raw2json(args.train_file, lang=args.lang, port=args.port)
    output_json(train_json, args.out_path, 'train.json')
    print('The train file of Multilingual dataset ({}) is saved at {}'.format(args.lang, os.path.join(args.out_path, 'train.json')))

    test_json = convert_raw2json(args.test_file,  desc='test', lang=args.lang, port=args.port)
    output_json(test_json, args.out_path, 'test.json')
    print('The test file of Multilingual dataset ({}) is saved at {}'.format(args.lang, os.path.join(args.out_path, 'test.json')))

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--out_path", default='dataset/JSONABSA_French', type=str, help="Output path of multilingual dataset.")
    parser.add_argument("--lang", default='french', type=str, choices=["french", "spanish", "turkish", "dutch"], help="The language of the dataset.")
    parser.add_argument("--port", default=9000, type=int, help="The port of the stanza server.")
    parser.add_argument("--train_file", default='french_train.raw', type=str, help="The path of train file.")
    parser.add_argument("--test_file", default='french_test.raw', type=str, help="The path of test file.")
    args = parser.parse_args()
    process_data(args)
    print('Multilingual data for {} has been processed.'.format(args.lang))

if __name__ == '__main__':
    main()
