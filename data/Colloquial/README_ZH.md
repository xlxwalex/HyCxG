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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/data/Colloquial) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/data/Colloquial/README_ZH.md)
## 口语化情感数据集

口语化情感数据集由Twitter数据集以及GermEval2017两部分方面级情感分析数据集组成，这两个数据集的数据均来自于社交媒体平台，因此相较于其他数据集包含更多的口语化语料。由于GermEval远大于Twitter，我们对GermEval采样为了一个子集进行性能测试。

### 数据下载及处理
在使用数据处理及下载脚本前，请您确认已经安装了[`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt)中的依赖包。在安装完依赖包后，用以下命令来获得并处理数据(可以不附加任何参数，所有参数均有默认值)：
```shell
bash download_and_process_counterfactual.sh [--DATA_DIR] [--OUTPUT_DIR] [--STANFORD_DIR]
```
**参数含义：**
+ DATA_DIR: 下载的原始数据所在文件夹, 默认为当前文件夹
+ OUTPUT_DIR: 处理好后的数据存储的文件夹, 默认为`dataset`
+ STANFORD_DIR: 斯坦福解析器所在位置，默认为上一级目录的`stanford-corenlp-3.9.2-minimal`

**注意：** 如果共享的解析器文件夹不存在，那么程序会询问是否从我们的镜像数据源拉取斯坦福解析器(共353MB)，选择`Y`即可。另外GermEval需要用到SpaCy，在调用时其会自动下载所需模型。

### 基准模型数据处理
在论文的Appendix H - Colloquial Expression Results中，我们对比了RGAT、DualGCN、DGEDT以及KumaGCN这四个模型在口语化情感数据集上的性能，因此在[`baseline文件夹`](https://github.com/xlxwalex/HyCxG/tree/main/data/Colloquial/baseline)中我们提供了GermEval数据的转换脚本(由于Twitter是常用数据集，这些基线模型都包含了处理好的数据)。更多关于基线模型的复现信息请见[`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines)。

### 数据来源
本部分数据来自Twitter和GermEval，我们的镜像数据来源[acl-14-short-data](https://github.com/songyouwei/ABSA-PyTorch/tree/master/datasets/acl-14-short-data)以及[GermEval 2017](http://ltdata1.informatik.uni-hamburg.de/germeval2017/)，如果您也使用了该数据集，您可以引用他们的论文，分别为：
#### Twitter数据集：
```
@inproceedings{dong2014adaptive,
    title = "Adaptive Recursive Neural Network for Target-dependent {T}witter Sentiment Classification",
    author = "Dong, Li  and
      Wei, Furu  and
      Tan, Chuanqi  and
      Tang, Duyu  and
      Zhou, Ming  and
      Xu, Ke",
    booktitle = "Proceedings of the 52nd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)",
    year = "2014",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P14-2009",
    pages = "49--54",
}
```
#### GermEval 2017评测比赛：
```
@article{wojatzki2017germeval,
  title={Germeval 2017: Shared task on aspect-based sentiment in social media customer feedback},
  author={Wojatzki, Michael and Ruppert, Eugen and Holschneider, Sarah and Zesch, Torsten and Biemann, Chris},
  journal={GermEval},
  pages={1--12},
  year={2017}
}
```