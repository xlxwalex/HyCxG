import os
import numpy as np
import pandas as pd
from sklearn.utils import murmurhash3_32
from Tokenizer.CxGProcessor.rdrpos_tagger.pSCRDRtagger.RDRPOSTagger import RDRPOSTagger
from Tokenizer.CxGProcessor.rdrpos_tagger.Utility.Utils import readDictionary
from Tokenizer.CxGProcessor.Loader import Loader

class Encoder(object):
    def __init__(self, args="", lang='eng'):

        MODEL_STRING = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/{}.RDR".format(lang)))
        DICT_STRING = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/{}.DICT".format(lang)))
        DICTIONARY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/{}.clusters.fastText.v2.gz".format(lang)))
        pos_list = Loader.pos_list
        seed = Loader.seed

        self.args = args
        self.pos_dict = {murmurhash3_32(pos, seed=seed): pos for pos in pos_list}
        self.word_dict = pd.read_csv(DICTIONARY_FILE, index_col=0).to_dict()["Cluster"]
        self.domain_dict = {murmurhash3_32(str(key), seed=seed): self.word_dict[key] for key in self.word_dict.keys()}
        self.word_dict = {murmurhash3_32(str(key), seed=0): key for key in self.word_dict.keys()}
        self.build_decoder()

        self.DICT = readDictionary(DICT_STRING)
        self.r = RDRPOSTagger(word_dict=self.domain_dict, DICT=self.DICT)
        self.r.constructSCRDRtreeFromRDRfile(MODEL_STRING)

    def build_decoder(self):
        #LEX = 1, POS = 2, CAT = 3
        decoding_dict = {}
        decoding_dict[1] = self.word_dict
        decoding_dict[2] = self.pos_dict
        decoding_dict[3] = {key: "<" + str(key) + ">" for key in list(set(self.domain_dict.values()))}
        self.decoding_dict = decoding_dict

    def tagline(self, line):
        line = self.r.tagRawSentenceHash(line)
        return np.array(line)





