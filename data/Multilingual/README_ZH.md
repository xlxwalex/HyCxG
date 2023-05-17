<p align="center" >
    <a href="https://github.com/xlxwalex/HyCxG/tree/main/data">
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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/data/Multilingual) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/data/Multilingual/README_ZH.md)
## 多语情感数据集

多语(Multilingual)情感数据集基于Semeval 2016的Task5，其除了常规英语外还提供了不同领域的8种语言的数据。我们从其中的餐厅领域(Resturant)选择了4个不同的语言作为多语性能评估数据集，它们分别是`法语`、`西班牙语`、`土耳其语`以及`荷兰语`。

### 数据下载及处理
在使用数据处理及下载脚本前，请您确认已经安装了[`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt)中的依赖包。在安装完依赖包后，用以下命令来获得并处理数据(可以不附加任何参数，所有参数均有默认值)：
```shell
bash download_and_process_multilingual.sh [--DATA_DIR] [--OUTPUT_DIR]
```
**参数含义：**
+ DATA_DIR: 下载的原始数据所在文件夹, 默认为当前文件夹
+ OUTPUT_DIR: 处理好后的数据存储的文件夹, 默认为`dataset`

**注意：** 在脚本内的PORT变量表示stanza服务器启动端口，默认为`9000`，如果您的机器上该端口被占用，您需要手动在脚本中进行设置

### 基准模型数据处理
在论文的Section4.3 - Multilingual results中，我们对比了RGAT、DualGCN、DGEDT以及KumaGCN这四个模型在多语情感数据集上的性能，因此在[`baseline文件夹`](https://github.com/xlxwalex/HyCxG/tree/main/data/Multilingual/baseline)中我们提供了四种语言数据转换脚本(我们尽可能用了和官方代码一致的处理工具包)。更多关于基线模型的复现信息请见[`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines)。

### 数据来源
本部分数据来自SemEval 2016，我们的镜像数据来源[SemEval-2016 Task 5](https://alt.qcri.org/semeval2016/task5/)，如果您也使用了该数据集，您可以引用他们的论文：
```
@inproceedings{pontiki2016semeval,
    title = "{S}em{E}val-2016 Task 5: Aspect Based Sentiment Analysis",
    author = {Pontiki, Maria  and
      Galanis, Dimitris  and
      Papageorgiou, Haris  and
      Androutsopoulos, Ion  and
      Manandhar, Suresh  and
      AL-Smadi, Mohammad  and
      Al-Ayyoub, Mahmoud  and
      Zhao, Yanyan  and
      Qin, Bing  and
      De Clercq, Orph{\'e}e  and
      Hoste, V{\'e}ronique  and
      Apidianaki, Marianna  and
      Tannier, Xavier  and
      Loukachevitch, Natalia  and
      Kotelnikov, Evgeniy  and
      Bel, Nuria  and
      Jim{\'e}nez-Zafra, Salud Mar{\'\i}a  and
      Eryi{\u{g}}it, G{\"u}l{\c{s}}en},
    booktitle = "{S}em{E}val-2016",
    year = "2016",
    url = "https://aclanthology.org/S16-1002",
    pages = "19--30",
}
```
