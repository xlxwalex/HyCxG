<p align="center" >
    <a href="https://github.com/xlxwalex/HyCxG">
    <br>
    <img src="https://github.com/xlxwalex/HyCxG/blob/main/figures/main-logo.png" width="100%"/>
    <br>
    </a>
</p>

# HyCxG
The official code for paper "**Enhancing Language Representation with Constructional Information for Natural Language Understanding**"

<a href="http://www.repostatus.org/#active"><img src="http://www.repostatus.org/badges/latest/active.svg" /></a>
<a href="https://github.com/xlxwalex/HyCxG/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/xlxwalex/HyCxG.svg"> </a>

[**English**](https://github.com/xlxwalex/HyCxG/) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/README_ZH.md)

🔗 [Data](https://github.com/xlxwalex/HyCxG/tree/main/data) • [Tutorial](https://github.com/xlxwalex/HyCxG/tree/main/tutorials) • [Guideline](https://github.com/xlxwalex/HyCxG/tree/main/guidelines) • [Quick Start](#-quick-start) • [Related Work](https://github.com/xlxwalex/HyCxG/blob/main/tutorials/PaperLists.md) • [FAQ❓](https://github.com/xlxwalex/HyCxG/tree/main/guidelines/faq.md)

> **Note**
> 
> This repository is still under construction and will take some time to complete.
> 

## 🌀 Content
* [📖 Introduction of HyCxG](#-introduction-of-hycxg)
* [📃 About this Repository](#-about-this-repository)
* [🐍 Quick Start](#-quick-start)
* [🔗 Other Information](#-appreciation)

## 📖 Introduction of HyCxG
**Construction Grammar** (CxG) is a branch of cognitive linguistics. It assumes that grammar is a meaningful continuum of lexicon,
morphology and syntax. Constructions can be defined as linguistic patterns that store different form and meaning pairs.
As the meaning of a construction is assigned to a linguistic pattern rather than specific words, learning constructional information
can be more challenging via PLMs and requires large bulk training data, which may lead to failure in NLU tasks.

It motivates us to incorporate construction grammar with PLMs. Therefore, we propose a preliminary framework **HyCxG** (Hypergraph network of construction grammar) to enhance the language representation with constructional information via a three stage solution.
First, we extract and select the discriminative constructions from the input sentence. Then the Relational Hypergraph Attention Network are  applied to attach the constructional information to the words. 
Then we can acquire the final representation to fine-tune on a variety of downstream tasks.


## 📃 About this Repository
The content contained in each section of this repository includes:
- [**HyCxG**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG) includes the entire code for HyCxG framework.
- [**Data**](https://github.com/xlxwalex/HyCxG/tree/main/data) contains all the datasets used in this work as well as processing scripts. Most of the datasets will be downloaded from our mirror source. Meanwhile, some data processing scripts for baseline models are also provided.
- [**Tutorial**](https://github.com/xlxwalex/HyCxG/tree/main/tutorials) includes some tutorials for HyCxG and related resources to our work.
- [**Guideline**](https://github.com/xlxwalex/HyCxG/tree/main/guidelines) (Under construction) illustrates the information about baseline models & FAQ.

## 🐍 Quick Start
**1 Experimental environment setup**

We adopt `Python=3.8.5` as the base environment, You can create the environment and install the dependencies with the following code:
```shell
conda create -n hycxg_env python=3.8.5
source activate hycxg_env
pip install -r requirements.txt
```
**2 Prepare the dataset**

We provide the script for data download in the [`data`](https://github.com/xlxwalex/HyCxG/tree/main/data) folder. You can directly use the following command to get the data: 
```shell
cd data
bash data_pipeline.sh
```
After downloading the data, please move each data folder (e.g., JSONABSA_MAMS) to the [`HyCxG/dataset`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset) directory.

**3 Prepare the data for components** 

Before running the code, it is necessary to download the required data for components (e.g., construction lists). The download process is under [`HyCxG/dataset`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset) and [`HyCxG/Tokenizer`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Tokenizer) respectively. You can also obtain the data directly using the following command:
```shell
cd HyCxG/dataset
bash download_vocab.sh
cd ../Tokenizer
bash download_cxgdict.sh
```

**4 Run HyCxG**

We provide some examples of code for running HyCxG in [`HyCxG/run_hycxg.sh`](https://github.com/xlxwalex/HyCxG/blob/main/HyCxG/run_hycxg.sh).

## 🙏 Appreciation
- [c2xg](https://github.com/jonathandunn/c2xg) for extracting the constructions from the sentence  
- [simanneal](https://github.com/perrygeo/simanneal) for a convenient simulated annealing framework to solve problems

## 👋 How to Cite
If you think our work is helpful, feel free to cite our paper "Enhancing Language Representation with Constructional Information for Natural Language Understanding":
```
@inproceedings{xu2023enhance,
    title = "Enhancing Language Representation with Constructional Information for Natural Language Understanding",
    author = "Xu, Lvxiaowei  and
      Wu, Jianwang  and
      Peng, Jiawei  and
      Gong, Zhilin  and
      Cai, Ming and
      Wang, Tianxiang",
    booktitle = "Proceedings of the 61th Annual Meeting of the Association for Computational Linguistics ",
    year = "2023",
    publisher = "Association for Computational Linguistics",
}
```
<p align="center">
    <a href="https://arxiv.org/abs/2306.02819">
        <img alt="Arxiv" src="https://img.shields.io/badge/ HyCxG- Paper-plastic?logo=arXiv&style=for-the-badge&logoColor=white&color=blue&link=https://arxiv.org/abs/2210.12364">
    </a>
</p>

## 📧 Contact
If you have any questions about the code, feel free to submit an Issue or contact [`xlxw@zju.edu.cn`](mailto:xlxw@zju.edu.cn)
