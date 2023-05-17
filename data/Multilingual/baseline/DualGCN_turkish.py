try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from tqdm import tqdm
import json
import stanfordnlp
nlpmodel = stanfordnlp.Pipeline(processors='tokenize,pos,depparse', lang="tr")

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

def parse_xml(path : str):
    data = []
    tree = ET.parse(path)
    root = tree.getroot()
    for review in tqdm(root.findall('Review'), 'Process'):
        for sentences in review.findall('sentences'):
            for sentence in sentences.findall('sentence'):
                obj = {}
                text = sentence.find('text').text
                if text is None or len(text) < 1: continue
                results = nlpmodel(text)
                tokens, pos_tag, heads, rels = obtain_annotate(results)
                obj['token'] = tokens
                obj['pos'] = pos_tag
                obj['head'] = heads
                obj['deprel'] = rels
                asp_total = []
                for asps in sentence.findall('Opinions'):
                    for asp in asps.findall('Opinion'):
                        aspect_dict = {}
                        from_idx = eval(asp.get('from'))
                        to_idx = eval(asp.get('to'))
                        polarity = asp.get('polarity')
                        term = asp.get('target')
                        if polarity == 'conflict': continue
                        if term == 'NULL':continue
                        context_l = text[:from_idx]
                        term_lr = text[from_idx:to_idx]
                        if term_lr.lower() != term:
                            print(text + ' / ' + term)
                        if len(context_l) > 0:
                            token_l = obtain_annotate(nlpmodel(context_l), only_tokens=True)
                        else:
                            token_l = []
                        if len(text[from_idx:to_idx]) < 1: continue
                        token_term = obtain_annotate(nlpmodel(text[from_idx:to_idx]), only_tokens=True)
                        aspect_dict['term'] = token_term
                        aspect_dict['from'] = len(token_l)
                        aspect_dict['to'] = len(token_l) + len(token_term)
                        aspect_dict['polarity'] = polarity
                        asp_total.append(aspect_dict)

                obj['aspects'] = asp_total
                if len(asp_total) > 0: data.append(obj)
    return data

if __name__ == '__main__':
    # Original Data Source
    train_data = parse_xml('ABSA16Tur_Train.xml')
    with open('train.json', 'w', encoding='utf-8') as tr_fp:
        json_str = json.dumps(train_data, indent=4)
        tr_fp.write(json_str)
    tr_fp.close()

    test_data = parse_xml('ABSA16Tur_Test.xml')
    with open('test.json', 'w', encoding='utf-8') as te_fp:
        json_str = json.dumps(test_data, indent=4)
        te_fp.write(json_str)
    te_fp.close()
    print('WELL DONE.')