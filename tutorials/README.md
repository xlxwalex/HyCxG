<p align="center" >
    <a href="https://github.com/xlxwalex/HyCxG/tree/main/HyCxG">
    <br>
    <img src="https://github.com/xlxwalex/HyCxG/blob/main/figures/sub-logo.png" width="275"/>
    <br>
    </a>
</p>
<p align="center">
    <a href="https://github.com/xlxwalex/HyCxG/blob/main/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/xlxwalex/HyCxG.svg?color=blue&style=flat-square">
    </a>
</p>

---
## Tutorials of HyCxG

[**English**](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/README_ZH.md)

## Content

- [Tutorials of HyCxG](#tutorials-of-hycxg)
- [Content](#content)
  - [The Usage of CxGTokenizer](#the-usage-of-cxgtokenizer)
  - [2 The Usage of Cond-MC Solver](#2-the-usage-of-cond-mc-solver)
    - [Q\&A](#qa)
  - [3 The Generation of Hypergraph](#3-the-generation-of-hypergraph)
- [Paper and Resource List](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/PaperLists.md)
---

### The Usage of CxGTokenizer

In order to encode constructional information via HyCxG, we need to extract all constructions from the sentences. `CxGTokenizer` is included in the [`Tokenizer`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Tokenizer) part of the code, and its main code is inherited from the [`c2xg`](https://github.com/jonathandunn/c2xg) package. The aim of `CxGTokenizer` is to extract all constructions included in the construction list from the sentence, and align them with the tokenized tokens via the pre-trained model. The version in this repository supports `BERT` and `RoBERTa` models. Meanwhile, it can be easily modified to support other pre-trained language models.

**Note:** Before extracting constructions, please make sure to all of the download steps in the README from [`Tokenizer`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Tokenizer) and [`dataset`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset).

After all the preparations are ready, you can obtain the complete tutorial by running the script [`01_cxgtokenizer_tutorial.py`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/01_cxgtokenizer_tutorial.py), or use the simple code sample and output below:

1. Prepare the required initialization parameters

```python
import os
class ARG_Test:
    cxg_vocab_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dataset/Vocab/CxG")) # Please check the path
    lm_path: str = 'bert-base-uncased'
    do_lower_case: bool = True
    lm_group: str = 'BERT' # BERT or RoBERTa
```

2.  Instantiate `CxGTokenizer`

```python
from Tokenizer.constants import *
from Tokenizer.ModelTokenizer import CxGTokenizer
args = ARG_Test()
cxg_tokenizer = CxGTokenizer(args, lang='eng') # default language is English
```

3. Extract constructions

```python
test_sentence = "The restaurants try too hard to make fancy food."
constructions = cxg_tokenizer.tokenize(test_sentence, raw=True)
print(constructions)
```

4. The returned result is a dictionary as shown below:

```python
constructions = {
'text': 'The restaurants try too hard to make fancy food.',
'token': ['the', 'restaurants', 'try', 'too', 'hard', 'to', 'make', 'fancy', 'food', '.'],
'cons_idx': [1501, 10765, 1943], 'cons_start': [3, 3, 4], 'cons_end': [7, 6, 7],
'cons_pattern': ['ADV--hard--to--VERB', 'ADV--hard--to', 'hard--PART--VERB']
}
```

The meanings of each key are:

+ **text**: Input sentence
+ **token**: Tokens (Tokenized via Basic Tokenizer)
+ **cons_idx**: The index in the construction list (Note: the index starts from 1, and 0 is left for `PAD`.)
+ **cons_start**:  Starting index of a construction (The indexes of tokens after being tokenized by the Tokenizer of pre-trained model)
+ **cons_end**: Ending index of a construction (The indexes of tokens after being tokenized by the Tokenizer of pre-trained model)
+ **cons_pattern**: Construction pattern (Calculate the scores for constructions)

**Example explanation**:
In the sentence of "The restaurants try too hard to make fancy food.", the tokenized tokens are(Note: tokenized by space):['the', 'restaurants', 'try', 'too', 'hard', 'to', 'make', 'fancy', 'food', '.'].
The three constructions 'ADV--hard--to--VERB', 'ADV--hard--to', 'hard--PART--VERB' can be acquired. Their indexes are: 1501, 10765, 1943. The span indexes of construction 'ADV--hard--to'are 3 and 6(Left inclusive, right exclusive). Thus the token list of token[3:6) is ['too', 'hard', 'to'], it is similar for other constructions.

### 2 The Usage of Cond-MC Solver

After obtaining all of the constructions, we need to select the  discriminative constructions for encoding. We formalized the selecting process as a multi-objective optimization problem, which is detailed in Section 2.2 of the paper. Since this is an NP problem, we utilzie Simulated Annealing (SA) as a heuristic approach to find the optimal set of constructions. This section will provide an introduction to the code used for solving the problem.

And you can obtain the complete tutorial by running the script [`02_coverage_solver_tutorial.py`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/02_coverage_solver_tutorial.py), or use the simple code sample and output below:

1. Extract the constructions of the sample

```python
from Simuann import CxGCoverage
import random

t_minutes = 0.05
test_cxgs = {
    'the--NOUN--was--ADV' : (1, 5),
    'the--NOUN--was' : (1, 4),
    'NOUN--AUX--ADV' : (2, 5),
    'AUX--so--ADJ' : (3, 6)
}
cxg_names = list(test_cxgs)
```

2. Initialize the states

```python
init_state = [0] * len(cxg_names)
for _ in range(random.randint(1, len(cxg_names))):
    init_state[random.randint(0, len(cxg_names)-1)] = 1
# You can also directly initialize the states with all-zeroes.
```

3. Prepare the args of consructions

```python
starts, ends, patterns = [], [], []
for cxg in test_cxgs:
    starts.append(test_cxgs[cxg][0])
    ends.append(test_cxgs[cxg][1])
    patterns.append(cxg)
```

4. Instantiate `CxGCoverage` and solve the problem

```python
cp = CxGCoverage(init_state, patterns, starts, ends, vis=True)
cp.set_schedule(cp.auto(minutes=t_minutes))
state, energy = cp.anneal()
```

5. The outputs is as below:

```python
Output:
 Temperature        Energy    Accept   Improve     Elapsed   Remaining
     0.10000          0.66     0.00%     0.00%     0:00:01     0:00:00
 Temperature        Energy    Accept   Improve     Elapsed   Remaining
     0.10000          0.66     0.07%     0.04%     0:00:03     0:00:00
>> Results:
CXG : the--NOUN--was, (1, 4)
CXG : AUX--so--ADJ, (3, 6)
```

**Note**:The weight hyperparameters in the paper have been hard-coded in the header of [`Simuann/CxGCoverage.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/CxGCoverage.py) file. If you need to do modifications, please directly modify the values in the corresponding dict of the file.

#### Q&A

**1Q**: If there are two identical constructions in a sentence, will there be a conflict if a dictionary is used to store keys?

**1A**: We will add --[X] at the end of the same constructions starting from the second constructions and beyond, where X represents the sorting index number of the same constructions.

**2Q**: Why is the watchdog necessary in `CxGCoverageProblem`?

**2A**: If there are only two constructions in a sentence and their scores are exactly the same, it will result in a deadlock. To avoid getting stuck, the program sets a maximum search limit for this case.


### 3 The Generation of Hypergraph

After obtaining the set of selected constructions in the sentence, we can generate the set as a hypergraph. The code for this part is mainly in [`utils/hypergraph.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/utils/hypergraph.py). And you can obtain the complete tutorial by running the script [`03_hypergraph_tutorial.py`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/03_hypergraph_tutorial.py), or use the simple code sample and output below:

1. Import the required packages and declare the parameters.

```python
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
```

2. Intialize the componets

```python
args = ARG_Test()
cxgprocessor = CxGTokenizer(args, lang='eng')
tokenizer = AutoTokenizer.from_pretrained(args.lm_path)
```

3. Tokenization

```python
sentence = 'I can understand the prices if it served better food.'
tokens = tokenizer.tokenize(sentence)
sentence_mask = [0] + [1] * len(tokens) + [0] 
tokens = ['<s>'] + tokens + ['</s>']
token_ids = tokenizer.convert_tokens_to_ids(tokens)
```

4. Construction extraction and selection

```python
cxgs = cxgprocessor.tokenize(sentence, raw=True)
selected = cxg_max_coverage(cxgs['cons_start'], cxgs['cons_end'], cxgs['cons_idx'], cxgs['cons_pattern'], T_minutes=args.t_minutes)
```

5. Generate the matrix for hypergraph

```python
hg, edges = construct_graph([selected], [sentence_mask], pad_len=15)
```

6. Output all the information:

```python
print('>> Results')
print('Tokens = {}'.format(tokens))
print('Token ids = {}'.format(token_ids))
print('constructions = {}'.format(cxgs))
print('selected constructions = {}'.format(selected))
print('hypergraph adjs =\n{}'.format(hg))

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
```