<p align="center" >
    <a href="https://github.com/xlxwalex/HyCxG/data">
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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/data/Counterfactual) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/data/Counterfactual/README_ZH.md)
## 反事实检测数据集



反事实检测(Counterfactual recognition, CR)数据集来自SemEval2020 Task5中的子任务1-反事实陈述检测(Recognizing Counterfactual Statements, RCS)，数据采集自政治、金融和健康领域，共有13k训练数据以及7k测试数据。

### 数据下载及处理
在使用数据处理及下载脚本前，请您确认已经安装了[`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt)中的依赖包。在安装完依赖包后，用以下命令来获得并处理数据(可以不附加任何参数，所有参数均有默认值)：
```shell
bash download_and_process_counterfactual.sh [--DATA_DIR] [--OUTPUT_DIR] [--STANFORD_DIR]
```
**参数含义：**
+ DATA_DIR: 下载的原始数据所在文件夹, 默认为当前文件夹
+ OUTPUT_DIR: 处理好后的数据存储的文件夹, 默认为`JSON_Counterfactual`
+ STANFORD_DIR: 斯坦福解析器所在位置，默认为上一级目录的`stanford-corenlp-3.9.2-minimal`

**注意：** 如果共享的解析器文件夹不存在，那么程序会询问是否从我们的镜像数据源拉取斯坦福解析器(共353MB)，选择`Y`即可

### 数据来源
本部分数据来自SemEval2020 Task5，我们的镜像数据来源官方Github[SemEval2020_Task5](https://github.com/Jiaqi1008/SemEval2020_Task5)，如果您也使用了该数据集，您可以引用他们的论文：
```
@inproceedings{yang-etal-2020-semeval,
    title = "{S}em{E}val-2020 Task 5: Counterfactual Recognition",
    author = "Yang, Xiaoyu  and
      Obadinma, Stephen  and
      Zhao, Huasha  and
      Zhang, Qiong  and
      Matwin, Stan  and
      Zhu, Xiaodan",
    booktitle = "Proceedings of the Fourteenth Workshop on Semantic Evaluation",
    year = "2020",
    publisher = "International Committee for Computational Linguistics",
    url = "https://aclanthology.org/2020.semeval-1.40",
    doi = "10.18653/v1/2020.semeval-1.40",
    pages = "322--335",
}
```