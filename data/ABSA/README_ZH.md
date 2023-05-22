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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/data/ABSA) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/data/ABSA/README_ZH.md)
## 方面级情感分析数据集

方面级情感分析(Aspect-based sentiment analysis, ABSA)数据集基于SemEval 2014/2015/2016以及MAMS任务及数据。其中SemEval 2014中包含了餐厅(Restaurant)和笔记本电脑(laptop)两个领域的评论，而SemEval 2014/2015均为餐厅领域的评论。MAMS是一个更大尺度的数据集，其每个句子都有多个方面，因此更具挑战性。

比较特别的是，由于SemEval 2014/2015/2016包含的四个数据集仅包含训练集和测试集，因此为了能更好评估模型性能，我们独立地将训练集按照`9:1`随机划分为了新的训练集和验证集，该类数据集会用`Split`后缀进行标识。

### 数据下载及处理
在使用数据处理及下载脚本前，请您确认已经安装了[`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt)中的依赖包。在安装完依赖包后，用以下命令来获得并处理数据(可以不附加任何参数，所有参数均有默认值)：
```shell
bash download_and_process_absa.sh  [--DATA_DIR] [--OUTPUT_DIR] [--STANFORD_DIR]
```
**参数含义：**
+ DATA_DIR: 下载的原始数据所在文件夹, 默认为当前文件夹
+ OUTPUT_DIR: 处理好后的数据存储的文件夹, 默认为`dataset`
+ STANFORD_DIR: 斯坦福解析器所在位置，默认为上一级目录的`stanford-corenlp-3.9.2-minimal`

**注意：** 如果共享的解析器文件夹不存在，那么程序会询问是否从我们的镜像数据源拉取斯坦福解析器(共353MB)，选择`Y`即可

### 基准模型数据处理
在论文的Section4.2 - Results on ABSA tasks中以及Appendix K - Detailed Results on ABSA Tasks中我们对比了多个模型在方面级情感数据集上的性能，我们在[`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines)提供了更多关于基线模型的复现信息。

### 数据来源
本部分数据来自SemEval 2014/2015/2016，我们的镜像数据来源[ASGCN-data](https://github.com/GeneZC/ASGCN/tree/master/datasets)以及[MAMS](https://github.com/siat-nlp/MAMS-for-ABSA)，如果您也使用了该数据集，您可以引用他们的论文，分别为：

**SemEval 2014**
```
@inproceedings{pontiki2014semeval,
    title = "{S}em{E}val-2014 Task 4: Aspect Based Sentiment Analysis",
    author = "Pontiki, Maria  and
      Galanis, Dimitris  and
      Pavlopoulos, John  and
      Papageorgiou, Harris  and
      Androutsopoulos, Ion  and
      Manandhar, Suresh",
    booktitle = "{S}em{E}val 2014",
    year = "2014",
    url = "https://aclanthology.org/S14-2004",
    pages = "27--35",
}
```
**SemEval 2015**
```
@inproceedings{pontiki2015semeval,
    title = "{S}em{E}val-2015 Task 12: Aspect Based Sentiment Analysis",
    author = "Pontiki, Maria  and
      Galanis, Dimitris  and
      Papageorgiou, Haris  and
      Manandhar, Suresh  and
      Androutsopoulos, Ion",
    booktitle = "{S}em{E}val 2015",
    year = "2015",
    url = "https://aclanthology.org/S15-2082",
    pages = "486--495",
}
```
**SemEval 2016**
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
**MAMS**
```
@inproceedings{jiang2019challenge,
    title = "A Challenge Dataset and Effective Models for Aspect-Based Sentiment Analysis",
    author = "Jiang, Qingnan  and
      Chen, Lei  and
      Xu, Ruifeng  and
      Ao, Xiang  and
      Yang, Min",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    year = "2019",
    url = "https://aclanthology.org/D19-1654",
    pages = "6280--6285",
}
```