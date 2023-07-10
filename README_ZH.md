<p align="center" >
    <a href="https://github.com/xlxwalex/HyCxG">
    <br>
    <img src="https://github.com/xlxwalex/HyCxG/blob/main/figures/main-logo.png" width="100%"/>
    <br>
    </a>
</p>

# HyCxG
论文"**Enhancing Language Representation with Constructional Information for Natural Language Understanding**"的代码仓库

<a href="http://www.repostatus.org/#active"><img src="http://www.repostatus.org/badges/latest/active.svg" /></a>
<a href="https://github.com/xlxwalex/HyCxG/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/xlxwalex/HyCxG.svg"> </a>

[**English**](https://github.com/xlxwalex/HyCxG/) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/README_ZH.md) 


🔗 [数据集](https://github.com/xlxwalex/HyCxG/tree/main/data) • [教程](https://github.com/xlxwalex/HyCxG/tree/main/tutorials) • [指南](https://github.com/xlxwalex/HyCxG/tree/main/guidelines) • [快速开始](#-快速开始) • [相关工作](https://github.com/xlxwalex/HyCxG/blob/main/tutorials/PaperLists.md) • [FAQ❓](https://github.com/xlxwalex/HyCxG/tree/main/guidelines/faq.md)

> **注意**
> 
> 本仓库还在建设中，需要过一段时间才能完成
> 

## 🌀 目录
* [📖 HyCxG介绍](#-hycxg介绍)
* [📃 仓库资源](#-仓库资源)
* [🐍 快速开始](#-快速开始)
* [🔗 其他信息](#-使用的项目)

## 📖 HyCxG介绍
**构式语法** (Construction Grammar, CxG)是认知语言学的一个分支。它认为语法是词汇、形态和句法的连续统。构式可以被定义为一系列存储不同形式和意义对的语言模式项(Linguistic Pattern)。由于构式的意义被分配给这些模式项而不是其实例化后内部包含的特定词汇，因此通过预训练模型学习构式信息可能更具挑战且需要大量的训练数据，这可能在自然语言理解任务中遇到问题。

这促使我们有动机将构式语法与预训练模型结合起来。因此我们提出了一个新的编码框架 - **HyCxG**（基于构式语法的超图网络），其通过三阶段过程来使用构式信息增强语言表示。首先，我们从句子中提取和选择出所需的构式集合。然后使用关系引导的超图注意网络将构式信息附加到词汇表示上。最后我们获取了最终表示就可以在各种下游任务中进行微调了。

## 📃 仓库资源
本代码仓库中各部分包含的内容为：
- [**HyCxG**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG) 包含了HyCxG的完整框架
- [**Data**](https://github.com/xlxwalex/HyCxG/tree/main/data) 包括了该工作中用到的所有数据集以及处理脚本。其中的绝大部分数据会从我们的镜像源中进行下载。同时，该部分也提供了基线模型对一些数据的处理脚本
- [**Tutorial**](https://github.com/xlxwalex/HyCxG/tree/main/tutorials) 包含了一些HyCxG相关的教程以及与我们工作相关的资源
- [**Guideline**](https://github.com/xlxwalex/HyCxG/tree/main/guidelines) (正在建设中) 展示了基线模型的一些信息和问答内容


## 🐍 快速开始
**1 实验环境搭建**

我们采用了`Python=3.8.5`作为基础实验环境，您可以用以下代码创建环境并安装依赖的包:
```shell
conda create -n hycxg_env python=3.8.5
source activate hycxg_env
pip install -r requirements.txt
```

**2 准备数据集**
我们在[`data`](https://github.com/xlxwalex/HyCxG/tree/main/data)文件夹中提供了数据下载脚本。你可以直接用以下代码来获得所有数据集：
```shell
cd data
bash data_pipeline.sh
```
在下载完数据后，请将每个数据文件夹(例如JSONABSA_MAMS)移动到[`HyCxG/dataset`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset) 路径下

**3 准备组件所需数据** 
在运行代码之前，您需要下载组件必须的数据(例如构式表)，关于下载步骤请分别见[`HyCxG/dataset`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset) 以及 [`HyCxG/Tokenizer`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Tokenizer) 。 你也可以直接通过以下代码来下载这些数据到对应位置：
```shell
cd HyCxG/dataset
bash download_vocab.sh
cd ../Tokenizer
bash download_cxgdict.sh
```

**4 运行HyCxG**

我们提供了一些HyCxG的运行样例脚本在[`HyCxG/run_hycxg.sh`](https://github.com/xlxwalex/HyCxG/blob/main/HyCxG/run_hycxg.sh)中，方便您参考


## 🙏 使用的项目
- [c2xg](https://github.com/jonathandunn/c2xg) 被用于从句子中抽取构式
- [simanneal](https://github.com/perrygeo/simanneal)是一个很方便的模拟退火框架被用于解决Cond-MC问题

## 👋 引用
如果您认为我们的工作对您有帮助，您可以引用我们的论文： Enhancing Language Representation with Constructional Information for Natural Language Understanding
```
@inproceedings{xu-etal-2023-enhancing,
    title = "Enhancing Language Representation with Constructional Information for Natural Language Understanding",
    author = "Xu, Lvxiaowei  and
      Wu, Jianwang  and
      Peng, Jiawei  and
      Gong, Zhilin  and
      Cai, Ming  and
      Wang, Tianxiang",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    year = "2023",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-long.258",
    pages = "4685--4705",
}
```

<p align="center">
    <a href="https://arxiv.org/abs/2306.02819">
        <img alt="Arxiv" src="https://img.shields.io/badge/ HyCxG- Paper-plastic?logo=arXiv&style=for-the-badge&logoColor=white&color=blue&link=https://arxiv.org/abs/2210.12364">
    </a>
</p>


## 📧 联系我们
如果您对代码有任何问题，可以提交Issue或联系 [`xlxw@zju.edu.cn`](mailto:xlxw@zju.edu.cn)
