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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/data/GLUE) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/data/GLUE/README_ZH.md)
## GLUE基准数据集

The General Language Understanding Evaluation (GLUE) benchmark is a common collection of natural language understanding systems based on a set of nine understanding tasks constructed from various existing natural language understanding datasets. These tasks are carefully selected to include a diverse range of dataset sizes, types, and difficulty levels. We evaluated the performance of this benchmark dataset on eight tasks, including `CoLA` (linguistic acceptability), `SST-2` (sentiment analysis), `MRPC`/`STS-B`/`QQP` (semantic similarity computation and equivalence matching), `MNLI`/`QNLI`/`RTE` (natural language inference).

### 数据下载及处理
在使用数据处理及下载脚本前，请您确认已经安装了[`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt)中的依赖包。在安装完依赖包后，用以下命令来获得并处理数据(可以不附加任何参数，所有参数均有默认值)：
```shell
bash download_and_process_glue.sh [--OUTPUT_DIR] [--STANFORD_DIR] [--TASK]
```
**参数含义：**
+ OUTPUT_DIR: 处理好后的数据存储的文件夹, 默认为`dataset`
+ STANFORD_DIR: 斯坦福解析器所在位置，默认为上一级目录的`stanford-corenlp-3.9.2-minimal`
+ TASK: 需要处理的GLUE任务，可以选择[cola, sst2, mnli, qnli, qqp, rte, mrpc, stsb]，如果都要下载可以直接使用`all`替代

**注意：** 如果共享的解析器文件夹不存在，那么程序会询问是否从我们的镜像数据源拉取斯坦福解析器(共353MB)，选择`Y`即可。除此之外，`MNLI`任务较为特别因此输出的文件会多两个文件(matched/mismatched)

### 数据来源
本部分数据来自GLUE基准，我们的数据来源Hugging Face的datasets库[GLUE](https://huggingface.co/datasets?sort=downloads&search=glue)，如果您也使用了该数据集，您可以引用他们的论文：
```
@inproceedings{wang2018glue,
    title = "{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding",
    author = "Wang, Alex  and
      Singh, Amanpreet  and
      Michael, Julian  and
      Hill, Felix  and
      Levy, Omer  and
      Bowman, Samuel",
    booktitle = "Proceedings of the 2018 {EMNLP} Workshop {B}lackbox{NLP}: Analyzing and Interpreting Neural Networks for {NLP}",
    month = nov,
    year = "2018",
    url = "https://aclanthology.org/W18-5446",
}
```
或者
```
@inproceedings{wangglue,
  title={GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R},
  booktitle={International Conference on Learning Representations (ICLR)},
  year = "2019"
}
```