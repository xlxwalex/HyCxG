import os
from utils.coverage import cxg_max_coverage
from utils.hypergraph import construct_graph
from Tokenizer import CxGTokenizer
from transformers import AutoTokenizer
import random
random.seed(0)

class ARG_Test:
    cxg_vocab_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dataset/Vocab/CxG"))
    lm_path: str = 'roberta-base-english'
    do_lower_case: bool = True
    lm_group: str = 'RoBERTa'
    t_minutes: float = 0.05

# Prepare the args
args = ARG_Test()
cxgprocessor = CxGTokenizer(args, lang='eng')
tokenizer = AutoTokenizer.from_pretrained(args.lm_path)

# Process the sentence
sentence = 'I can understand the prices if it served better food.'
tokens = tokenizer.tokenize(sentence)
sentence_mask = [0] + [1] * len(tokens) + [0]
tokens = ['<s>'] + tokens + ['</s>']
token_ids = tokenizer.convert_tokens_to_ids(tokens)
cxgs = cxgprocessor.tokenize(sentence, raw=True)
selected = cxg_max_coverage(cxgs['cons_start'], cxgs['cons_end'], cxgs['cons_idx'], cxgs['cons_pattern'], T_minutes=args.t_minutes)
hg, edges = construct_graph([selected], [sentence_mask], pad_len=15)

print('>> Results')
print('Tokens = {}'.format(tokens))
print('Token ids = {}'.format(token_ids))
print('constructions = {}'.format(cxgs))
print('selected constructions = {}'.format(selected))
print('hypergraph adjs =\n{}'.format(hg))

# Outputs:
# >> Results
# Tokens = ['<s>', 'I', 'Ġcan', 'Ġunderstand', 'Ġthe', 'Ġprices', 'Ġif', 'Ġit', 'Ġserved', 'Ġbetter', 'Ġfood', '.', '</s>']
# Token ids = [0, 100, 64, 1346, 5, 850, 114, 24, 1665, 357, 689, 4, 2]
# constructions = {
#   'text': 'I can understand the prices if it served better food.',
#   'token': ['i', 'can', 'understand', 'the', 'prices', 'if', 'it', 'served', 'better', 'food', '.'],
#   'cons_idx': [5943, 6071, 16646, 6388, 13591, 11402, 786, 4387, 13648, 5683, 12421, 12967],
#   'cons_start': [0, 0, 0, 1, 1, 2, 3, 3, 3, 4, 4, 5], 'cons_end': [4, 5, 3, 5, 4, 5, 7, 6, 8, 8, 7, 8],
#   'cons_pattern': ['i--AUX--VERB--DET', 'i--AUX--VERB--DET--NOUN', 'i--AUX--VERB', 'can--VERB--DET--NOUN', 'can--VERB--DET', 'understand--DET--NOUN', 'the--NOUN--SCONJ--PRON', 'the--NOUN--SCONJ', 'the--NOUN--SCONJ--PRON--VERB', 'NOUN--SCONJ--PRON--VERB', 'NOUN--SCONJ--PRON', 'if--PRON--VERB']
# }
# selected constructions = [(0, 5, 6071, 'i--AUX--VERB--DET--NOUN'), (5, 8, 12967, 'if--PRON--VERB')]
# hypergraph adjs =
# [array([[0., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
#        [0., 0., 0., 0., 0., 0., 1., 1., 1., 0., 0., 0., 0., 0., 0.],
#        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])]