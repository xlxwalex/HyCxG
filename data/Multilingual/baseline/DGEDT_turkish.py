import numpy as np
import pickle
import tqdm
import re

import stanfordnlp
nlpmodel = stanfordnlp.Pipeline(processors='tokenize,pos,depparse', lang="tr")

def tokenize(text):
    text=text.strip()
    text=re.sub(r' {2,}',' ',text)
    document = nlpmodel(text)
    tokens = []
    for sentence in document.sentences:
        tok= [word.text for word in sentence.words]
        tokens.extend(tok)
    return tokens

def update_edge(text,vocab):
    # https://spacy.io/docs/usage/processing-text
    document = nlpmodel(text)
    tokens = []
    for sentence in document.sentences:
        dep = [word.dependency_relation for word in sentence.words]
        tokens.extend(dep)
    seq_len = len(text.split())
    for token in tokens:
           if token not in vocab:
               vocab[token]=len(vocab)
    return 0


def dependency_adj_matrix(text,edge_vocab):
    # https://spacy.io/docs/usage/processing-text
    document = nlpmodel(text)
    deprels = []
    for sentence in document.sentences:
        dep = [(word.dependency_relation, word.governor, eval(word.index)) for word in sentence.words]
        deprels.extend(dep)
    seq_len = len(tokenize(text))
    matrix = np.zeros((seq_len, seq_len)).astype('float32')
    matrix1 = np.zeros((seq_len, seq_len)).astype('float32')
    edge = np.zeros((seq_len, seq_len)).astype('int32')
    edge1 = np.zeros((seq_len, seq_len)).astype('int32')

    for tokid in range(len(deprels)):
        matrix[tokid][tokid] = 1
        matrix1[tokid][tokid] = 1

    for link in deprels:
        if link[0] == 'root':
            continue
        matrix[link[1] - 1][link[2] - 1] = 1
        matrix1[link[2] - 1][link[1] - 1] = 1
        edge[link[1] - 1][link[2] - 1] = edge_vocab.get(link[0], 1)
        edge1[link[2] - 1][link[1] - 1] = edge_vocab.get(link[0],1)
    return matrix, matrix1, edge, edge1

def concat(texts,aspect):
    source=''
    splitnum=0
    for i, text in enumerate(texts):
        source+=text
        if text == '80 tl.': text = '80 tl .'
        if len(text) < 1:
            splitnum +=0
        else:
            splitnum+=len(tokenize(text))
        if i <len(texts)-1:
           source+=' '+aspect+' '
           tmp_aspect = tokenize(aspect)
           splitnum+=len(tmp_aspect)
    if splitnum != len(tokenize(source.strip())):
        print(texts)
        print(aspect)
        print(source)
        print(splitnum)
        print(tokenize(source.strip()))
        print(len(tokenize(source.strip())))
        a=input('gfg')
    return re.sub(r' {2,}',' ',source.strip())

def process(filename,edge_vocab=None,savevocab=True):
    if edge_vocab is not None:
        pass
    else:
        edge_vocab={'<pad>':0,'<unk>':1}
    fin = open(filename, 'r', newline='\n', errors='ignore')
    lines = fin.readlines()
    fin.close()
    idx2graph = {}
    fout = open(filename+'.graph', 'wb')
    if savevocab:
        fout1 = open(filename+'.edgevocab', 'wb')
    if savevocab:
        for i in tqdm.tqdm(range(0, len(lines), 3)):
            text_left = [s.lower().strip() for s in lines[i].split("$T$")]
            aspect = lines[i + 1].lower().strip()
            concater = concat(text_left,aspect)
            update_edge(concater, edge_vocab)
    for i in tqdm.tqdm(range(0, len(lines), 3)):
        text_left = [s.lower().strip() for s in lines[i].split("$T$")]
        aspect = lines[i + 1].lower().strip()
        adj_matrix = dependency_adj_matrix(concat(text_left,aspect),edge_vocab)
        idx2graph[i] = adj_matrix
    pickle.dump(idx2graph, fout)
    if savevocab:
        pickle.dump(edge_vocab, fout1)
    fout.close()
    if savevocab:
        fout1.close()
    return edge_vocab
def processe(filename,filename2):
    savevocab=True

    edge_vocab={'<pad>':0,'<unk>':1}
    fin = open(filename, 'r', encoding='utf-8', newline='\n', errors='ignore')
    lines = fin.readlines()
    fin.close()
    idx2graph = {}
    fout = open(filename+'.graph', 'wb')
    if savevocab:
        fout1 = open(filename+'.edgevocab', 'wb')
    if savevocab:
        for i in tqdm.tqdm(range(0, len(lines), 1)):
            update_edge(re.sub(r' {2,}',' ',lines[i].strip()),edge_vocab)
    for i in tqdm.tqdm(range(0, len(lines), 1)):
        adj_matrix = dependency_adj_matrix(re.sub(r' {2,}',' ',lines[i].strip()),edge_vocab)
        idx2graph[i] = adj_matrix
    pickle.dump(idx2graph, fout)
    if savevocab:
        pickle.dump(edge_vocab, fout1)
    fout.close()
    if savevocab:
        fout1.close()
    return edge_vocab
if __name__ == '__main__':
   edge_vocab = process('./datasets/turkish/restaurant_train.raw', None, True)
   process('./datasets/turkish/restaurant_test.raw', edge_vocab, False)
