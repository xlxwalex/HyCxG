import os

class Vocab(object):
    def __init__(self):
        # Reserved Vocabulary
        self.reserved_vocab_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../models/reserved_vocab.txt"))

    def load(self, vocab_path):
        raise NotImplementedError

    def save(self, save_path):
        raise NotImplementedError

class BERTVocab(Vocab):
    """
    Vocabulary of BERT Tokenizer
    """

    def __init__(self, vocab_path='dataset/Vocab/BERT/'):
        super().__init__()
        self.word_w2i = {}
        self.word_i2w = []
        self.word_w2c = {}
        self.load(vocab_path)

    def load(self, vocab_path):
        with open(os.path.join(vocab_path, 'vocab.txt'), mode="r", encoding="utf-8") as reader:
            for index, line in enumerate(reader):
                w = line.strip("\n").split()[0] if line.strip() else line.strip("\n")
                self.word_w2i[w] = index
                self.word_i2w.append(w)

    def save(self, save_path):
        print("Word Vocabulary size: ", len(self))
        with open(save_path, mode="w", encoding="utf-8") as f:
            for w in self.word_i2w:
                f.write(w + "\n")
        print("Word Vocabulary saving done.")

    def get(self, w):
        return self.word_w2i[w]

    def __len__(self):
        return len(self.word_i2w)


class CxGVocab(Vocab):
    """
    Vocabulary of CxGBERT Tokenizer
    """
    def __init__(self, vocab_path = "../dataset/CxGBERT/", lang='eng'):
        super().__init__()
        # Externel Construction Vocabulary
        self.cxg_c2i = {}
        self.cxg_i2c = []
        self.cxg_c2c = {}
        self.lang = lang
        self.load(vocab_path)

    def __len__(self):
        return len(self.cxg_i2c)

    def load(self, vocab_path):
        with open(os.path.join(vocab_path, 'construction.txt' if self.lang == 'eng' else '{}.construction.txt'.format(self.lang)), mode="r", encoding="utf-8") as reader:
            self.cxg_c2i['<PAD>'] = 0
            self.cxg_i2c.append('<PAD>')
            for index, line in enumerate(reader):
                w = line.strip("\n").replace(' ', '').split()[0] if line.strip() else line.strip("\n")
                self.cxg_c2i[w] = index + 1
                self.cxg_i2c.append(w)

    def get(self, w):
        return self.cxg_c2i[w]