from Tokenizer.BaseTokenizer import BasicTokenizer, WordpieceTokenizer, Tokenizer
from Tokenizer.constants import *
from Tokenizer.CxGProcessor.CxGCore import CxGCore
from Tokenizer.Vocab import CxGVocab
from transformers import AutoTokenizer

# Not available in this repo
class BertTokenizer(Tokenizer):
    def __init__(self, args):
        super().__init__(args, token_mode=CONST_TOKEN_MODE_WORD)
        self.basic_tokenizer = BasicTokenizer(do_lower_case=args.do_lower_case)
        self.wordpiece_tokenizer = WordpieceTokenizer(vocab=self.vocab, unk_token=UNK_TOKEN)

    def tokenize(self, text) -> list:
        tokens, split_tokens = [], []
        if isinstance(text, str):
            text = [text]
        for ele in text:
            split_tokens = []
            for token in self.basic_tokenizer.tokenize(ele):
                for sub_token in self.wordpiece_tokenizer.tokenize(token):
                    split_tokens.append(sub_token)
            tokens.append(split_tokens)
        if len(text) == 1:
            return split_tokens
        return tokens


class CxGTokenizer(object):
    def __init__(self, args, visible=True, workers=None, lang='eng'):
        self.cxg = CxGCore(args, workers=workers, lang=lang)
        self.bert = AutoTokenizer.from_pretrained(args.lm_path)
        self.cons_vocab = CxGVocab(args.cxg_vocab_path, lang=lang)
        self.visible = visible

    def tokenize(self, text, raw=True) -> dict:
        results = self.cxg.parse_text(text)
        # return results
        if raw:
            cons_pattern = [self.cons_vocab.cxg_i2c[ele] for ele in results['cons_idx']]
            results['cons_pattern'] = cons_pattern
            return results
        # else branch is not avalible in Github Repo