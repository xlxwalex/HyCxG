import pickle
from Tokenizer.BaseTokenizer import BasicTokenizer, WordpieceTokenizer
from transformers import AutoTokenizer
from sklearn.utils import murmurhash3_32
from collections import defaultdict
import Tokenizer.CxGProcessor.utils as utils
from Tokenizer.constants import *

# Load Construction
class Loader(object):
    pos_list = ["PROPN", "SYM", "VERB", "DET", "CCONJ", "AUX",
                "ADJ", "INTJ", "SCONJ", "PRON", "NUM", "PUNCT",
                "ADV", "ADP", "X", "NOUN", "PART"]
    seed = 0

    def __init__(self, args, lang='eng'):
        self.args = args
        self.cons_path = args.cxg_vocab_path + "/construction.pkl" if lang == 'eng' else args.cxg_vocab_path + "/{}.construction.pkl".format(lang)
        self.pos_list = Loader.pos_list
        self.seed = Loader.seed
        self.lmg = args.lm_group
        self.cons = self.load_cons()
        self.dict_cons = self.load_dict_cons()
        self.basic_tokenizer = BasicTokenizer(do_lower_case=self.args.do_lower_case)
        self.auto_tokenizer = AutoTokenizer.from_pretrained(args.lm_path)

    def load_dict_cons(self):
        encoded_cons = self.cons
        dict_cons = dict()
        X = list(set([encoded_cons[i][0][0] for i in range(len(encoded_cons))]))
        for x in X:
            dict_cons[x] = defaultdict(list)
            for i, encoded_con in enumerate(encoded_cons):
                if encoded_con[0][0] == x:
                    dict_cons[x][encoded_con[0][1]].append((encoded_con, i))
        return X, dict_cons

    def load_cons(self):
        if self.cons_path.endswith(".pkl"):
            with open(self.cons_path, "rb") as f:
                res = pickle.load(f)
        else:
            cons = self.read_cons()
            res = self.encode_cons(cons)
        return res

    def load_text(self, text):
        tokens = self.tokenize(text)
        map_word2_token = self.map_cxgtoken2plmtoken(tokens)
        tokens = self.replace(tokens)
        lines = self.tokens2lines(tokens)
        return lines, map_word2_token

    def load_from_file(self, file):
        text = []
        with open(file, "r") as f:
            for line in f.readlines():
                if line.strip():
                    text.append(line.strip())
        lines, _ = self.load_text(text)
        return lines

    def tokenize(self, text):
        if isinstance(text, str):
            text = [text]
        tokens = []
        basic_tokenizer = BasicTokenizer(do_lower_case=self.args.do_lower_case)
        for ele in text:
            tokens.append(basic_tokenizer.tokenize(ele))
        return tokens

    def replace(self, tokens, no_number=True, no_phone=True, no_email=True, no_currency=True):
        if no_phone:
            tokens = [self.replace_with_phone(token) for token in tokens]
        if no_number:
            tokens = [self.replace_with_number(token) for token in tokens]
        if no_email:
            tokens = [self.replace_with_email(token) for token in tokens]
        if no_currency:
            tokens = [self.replace_with_currency_symbol(token) for token in tokens]
        return tokens

    def map_cxgtoken2plmtoken(self, tokens):
        accum_idx = 0
        mapper = []
        for token in tokens[0]:
            tok = []
            wp_tokens = self.auto_tokenizer.tokenize(token) if self.lmg == 'BERT' else self.auto_tokenizer.tokenize(' ' + token)
            tok.extend(wp_tokens)
            mapper.append([accum_idx, accum_idx + len(tok) -1])
            accum_idx += len(tok)
        return mapper

    @staticmethod
    def replace_with_number(token, alternative="<number>"):
        return [utils.NUMBERS_REGEX.sub(alternative, x) for x in token]

    @staticmethod
    def replace_with_currency_symbol(token, alternative="<cur>"):
        return [utils.CURRENCY_REGEX.sub(alternative, x) for x in token]

    @staticmethod
    def replace_with_email(token, alternative="<email>"):
        return [utils.EMAIL_REGEX.sub(alternative, x) for x in token]

    @staticmethod
    def replace_with_phone(token, alternative="<phone>"):
        return [utils.PHONE_REGEX.sub(alternative, x) for x in token]

    def tokens2lines(self, tokens):
        lines = [" ".join(token) for token in tokens]
        return lines

    def read_cons(self):
        cons = []
        with open(self.cons_path, "r") as f:
            for line in f.readlines():
                con = line.strip().split("--")
                cons.append(con)
        return cons

    def write_cons(self, encoded_cons):
        path = self.cons_path.replace(".txt", ".pkl")
        with open(path, "wb") as f:
            pickle.dump(encoded_cons, f)

    def encode_cons(self, cons):
        encoded_cons = []
        for con in cons:
            encoded_cons.append(self.encode_con(con))
        return encoded_cons

    def encode_con(self, con):
        encoded_con = []
        for x in con:
            if x.startswith("<"):
                encoded_con.append((3, int(x[1:-1])))
            elif x in self.pos_list:
                encoded_con.append((2, murmurhash3_32(x, seed=self.seed)))
            else:
                encoded_con.append((1, murmurhash3_32(x, seed=self.seed)))
        return tuple(encoded_con)
