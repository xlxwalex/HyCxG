from Tokenizer.CxGProcessor.Loader import Loader
from Tokenizer.CxGProcessor.Encoder import Encoder
from Tokenizer.CxGProcessor.Parser import Parser

class CxGCore(object):
    def __init__(self, args, workers = None, lang='eng'):
        self.args = args
        self.Loader = Loader(args, lang=lang)
        self.Encoder = Encoder(lang=lang)
        self.Parser = Parser(self.Loader, self.Encoder, workers=workers)

    def parse_text(self, text):
        if isinstance(text, str):
            text = [text]
        tokens = self.Loader.tokenize(text)
        lines, mapper, tokenizer_tokens = self.Loader.load_text(text)
        results = self.Parser.parse_lines(lines)
        # return results
        results_ = {}
        for i, res in enumerate(results):
            temp = {}
            temp["text"] = text[i]
            temp["token"] = tokenizer_tokens[i]
            temp["cons_idx"] = [ele + 1 for ele in res[0]] # 0 -<PAD>
            temp["cons_start"] = [mapper[ele][0] for ele in res[1]]
            temp["cons_end"] = [mapper[ele-1][-1] + 1 for ele in res[2]]
            results_[i] = temp
        return results_[0]

    def parse_file(self, file):
        lines = self.Loader.load_from_file(file)
        results = self.Parser.parse_lines(lines)
        return results

