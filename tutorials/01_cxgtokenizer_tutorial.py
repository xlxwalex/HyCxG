from Tokenizer.constants import *
from Tokenizer.ModelTokenizer import CxGTokenizer

class ARG_Test:
    cxg_vocab_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dataset/Vocab/CxG"))
    lm_path: str = 'bert-base-uncased'
    do_lower_case: bool = True
    lm_group: str = 'BERT'

# Prepare the args
args = ARG_Test()

# Initialize CxGTokenizer
cxg_tokenizer = CxGTokenizer(args, lang='eng') # Current language is English

# acquire constructions
test_sentence = "The restaurants try too hard to make fancy food."
constructions = cxg_tokenizer.tokenize(test_sentence, raw=True)
print(constructions)
# Output:
#{
# 'text': 'The restaurants try too hard to make fancy food.',
# 'token': ['the', 'restaurants', 'try', 'too', 'hard', 'to', 'make', 'fancy', 'food', '.'],
# 'cons_idx': [1501, 10765, 1943], 'cons_start': [3, 3, 4], 'cons_end': [7, 6, 7],
# 'cons_pattern': ['ADV--hard--to--VERB', 'ADV--hard--to', 'hard--PART--VERB']
# }
