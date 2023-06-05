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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/README_ZH.md)
## HyCxG教程

### 目录
- [HyCxG教程](#hycxg教程)
- [目录](#目录)
  - [CxGTokenizer的使用](#CxGTokenizer的使用)
  - [Cond-MC求解器的使用](#Cond-MC求解器的使用)
    - [Q\&A](#qa)
  - [Hypergraph的生成](#Hypergraph的生成)
- [论文及资源表 (仅英文)](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/PaperLists.md)

---
### CxGTokenizer的使用
在HyCxG中为了编码构式信息，我们需要从句子中抽取出所有的构式。`CxGTokenizer`被包含在了代码中的[`Tokenizer`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Tokenizer)部分，其主要代码继承自[`c2xg`](https://github.com/jonathandunn/c2xg)包。主要功能是从句子中抽取所有在构式表中包含的构式，并与预训练模型词例化(tokenize)后的词例(token)进行对齐，仓库中的版本支持`BERT`以及`RoBERTa`预训练模型，要支持其余的预训练模型也可以很方便地进行修改。

**注意**：在进行构式抽取前，请先确保执行[`Tokenizer`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Tokenizer)以及[`dataset`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset)的README中所有的下载步骤。

在所有准备工作就绪之后，你可以通过[`01_cxgtokenizer_tutorial.py`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/01_cxgtokenizer_tutorial.py)脚本获得完整的教程，或查看下方简易的代码样例和输出：
1. 准备必须的初始化参数
```python
import os
class ARG_Test:
    cxg_vocab_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dataset/Vocab/CxG")) # 请注意核对路径
    lm_path: str = 'bert-base-uncased'
    do_lower_case: bool = True
    lm_group: str = 'BERT' # BERT 或者 RoBERTa
```
2. 实例化`CxGTokenizer`
```python
from Tokenizer.constants import *
from Tokenizer.ModelTokenizer import CxGTokenizer
args = ARG_Test()
cxg_tokenizer = CxGTokenizer(args, lang='eng') # 选择语言，默认为英语
```
3. 抽取构式
```python
test_sentence = "The restaurants try too hard to make fancy food."
constructions = cxg_tokenizer.tokenize(test_sentence, raw=True)
print(constructions)
```
返回的结果为一个字典，如下所示：
```python
constructions = {
'text': 'The restaurants try too hard to make fancy food.',
'token': ['the', 'restaurants', 'try', 'too', 'hard', 'to', 'make', 'fancy', 'food', '.'],
'cons_idx': [1501, 10765, 1943], 'cons_start': [3, 3, 4], 'cons_end': [7, 6, 7],
'cons_pattern': ['ADV--hard--to--VERB', 'ADV--hard--to', 'hard--PART--VERB']
}
```
各键的含义是：
+ **text**: 输入文本
+ **token**: 文本词例化后的Token(由Basic Tokenizer切分)
+ **cons_idx**: 构式的ID (在构式表中的索引，注意下标从1开始，0留给了`PAD`)
+ **cons_start**: 构式的起始索引 (预训练模型的Tokenizer切分后的Tokens索引)
+ **cons_end**: 构式的终止索引 (预训练模型的Tokenizer切分后的Tokens索引)
+ **cons_pattern**: 构式本身 (计算构式分数)

**例子解释**：
在句子“The restaurants try too hard to make fancy food.”中，词例化后得到tokens为(注意：这个词例是按照空格切分的)['the', 'restaurants', 'try', 'too', 'hard', 'to', 'make', 'fancy', 'food', '.']，
抽取得到了三个构式'ADV--hard--to--VERB', 'ADV--hard--to', 'hard--PART--VERB'，它们的索引分别为1501, 10765, 1943。其中'ADV--hard--to'构式的起始索引是3和6(左开右闭)，因此对应token[3:6)=['too', 'hard', 'to']，其他构式同。

### Cond-MC求解器的使用
在获得所有的构式后，我们对这些构式进行了筛选，选择了代表性的构式进行编码。我们将筛选过程形式化为了一个多目标的优化问题，可以在论文的Section 2.2中找到详细过程。由于这是一个NP问题，我们采用了模拟退火(Simulated Annealing, SA)来启发式地找到最优的构式集合，本部分将对求解代码进行介绍。

你可以通过[`02_coverage_solver_tutorial.py`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/02_coverage_solver_tutorial.py)脚本获得完整的教程，或查看下方简易的代码样例和输出：
1. 抽取得到的构式例子
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
2. 初始化选择状态
```python
init_state = [0] * len(cxg_names)
for _ in range(random.randint(1, len(cxg_names))):
    init_state[random.randint(0, len(cxg_names)-1)] = 1
# 直接初始化为全0也可
```
3. 准备实例化参数
```python
starts, ends, patterns = [], [], []
for cxg in test_cxgs:
    starts.append(test_cxgs[cxg][0])
    ends.append(test_cxgs[cxg][1])
    patterns.append(cxg)
```
4. 实例化`CxGCoverage`并求解
```python
cp = CxGCoverage(init_state, patterns, starts, ends, vis=True)
cp.set_schedule(cp.auto(minutes=t_minutes))
state, energy = cp.anneal()
```
5. 输出的信息及最终选择的构式
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
**注意**：论文中的权重超参数已经硬编码在了[`Simuann/CxGCoverage.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/CxGCoverage.py)的头部字典中，如果需要测试修改，请直接修改文件中对应部分的值
#### Q&A
**1Q**: 如果一个句子中有两个一样的构式，那么如果用字典存储键的话会产生冲突？

**1A**: 我们会在第二个及之后相同构式末尾加上--[X]，X为相同构式的排序索引号

**2Q**: 为什么`CxGCoverageProblem`中需要看门狗?

**2A**: 如果句子中只有两个构式，且它们的分数完全相同，那么就会形成死锁卡住。为了避免卡住因此程序设置了最大的搜索上限

### Hypergraph的生成
在获得了句子中被选定的构式集合后，我们可以将集合生成为超图。该部分的代码主要在[`utils/hypergraph.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/utils/hypergraph.py)中。你可以通过[`03_hypergraph_tutorial.py`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials/03_hypergraph_tutorial.py)脚本获得完整的教程，或查看下方简易的代码样例和输出：
1. 引入所需的包以及声明参数
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
2. 初始化各组件
```python
args = ARG_Test()
cxgprocessor = CxGTokenizer(args, lang='eng')
tokenizer = AutoTokenizer.from_pretrained(args.lm_path)
```
3. 词例化
```python
sentence = 'I can understand the prices if it served better food.'
tokens = tokenizer.tokenize(sentence)
sentence_mask = [0] + [1] * len(tokens) + [0] 
tokens = ['<s>'] + tokens + ['</s>']
token_ids = tokenizer.convert_tokens_to_ids(tokens)
```
4. 构式抽取及构式选择
```python
cxgs = cxgprocessor.tokenize(sentence, raw=True)
selected = cxg_max_coverage(cxgs['cons_start'], cxgs['cons_end'], cxgs['cons_idx'], cxgs['cons_pattern'], T_minutes=args.t_minutes)
```
5. 生成超图矩阵
```python
hg, edges = construct_graph([selected], [sentence_mask], pad_len=15)
```
6. 输出的所有信息：
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
