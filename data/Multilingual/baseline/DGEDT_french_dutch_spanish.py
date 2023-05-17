import numpy as np
import spacy
import pickle
import tqdm
nlp = spacy.load('fr') # fr - franch / es - spanish / nl -dutch
import re

def tokenize(text):
    text=text.strip()
    text=re.sub(r' {2,}',' ',text)
    document = nlp(text)
    return [token.text for token in document]

def update_edge(text,vocab):
    # https://spacy.io/docs/usage/processing-text
    document = nlp(text)
    seq_len = len(text.split())
    for token in document:
           if token.dep_ not in vocab:
               vocab[token.dep_]=len(vocab)
    return 0
def dependency_adj_matrix(text,edge_vocab):
    # https://spacy.io/docs/usage/proclessing-text
    document = nlp(text.strip())
    seq_len = len(tokenize(text))
    matrix = np.zeros((seq_len, seq_len)).astype('float32')
    matrix1 = np.zeros((seq_len, seq_len)).astype('float32')
    edge = np.zeros((seq_len, seq_len)).astype('int32')
    edge1 = np.zeros((seq_len, seq_len)).astype('int32')
    assert len(document)==seq_len
    for token in document:
        if token.i >= seq_len:
            print('bug')
            print(text)
            print(text.split())
            print(document)
            print([token.i for token in document])
            print([token.text for token in document])
            a=input('hahha')
        if token.i < seq_len:
            matrix[token.i][token.i] = 1
            matrix1[token.i][token.i] = 1
            # https://spacy.io/docs/api/token
            for child in token.children:
                if child.i < seq_len:
                    matrix[token.i][child.i] = 1
                    matrix1[child.i][token.i] = 1
                    edge[token.i][child.i] = edge_vocab.get(child.dep_,1)
                    edge1[child.i][token.i] = edge_vocab.get(child.dep_,1)
    return matrix,matrix1,edge,edge1
def concat(texts,aspect):
    source=''
    splitnum=0
    for i,text in enumerate(texts):
        source+=text
        splitnum+=len(tokenize(text))
        if i <len(texts)-1:
           source+=' '+aspect+' '
           splitnum+=len(tokenize(aspect))
    if splitnum!=len(tokenize(source.strip())):
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
    fin = open(filename, 'r', encoding='utf-8', newline='\n', errors='ignore')
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
            update_edge(concat(text_left,aspect),edge_vocab)
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
    # e.g., french
   edge_vocab = process('./datasets/french/restaurant_train.raw',None, True)
   process('./datasets/french/restaurant_test.raw', edge_vocab, False)
