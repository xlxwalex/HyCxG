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

## Aspect-based Sentiment Analysis Dataset for ABSA

The Aspect-based Sentiment Analysis (ABSA) dataset is based on SemEval 2014, 2015, 2016, and MAMS. SemEval 2014 contains reviews from two domains: restaurants and laptops. SemEval 2014 and 2015 include reviews from the restaurant domain only. MAMS is a larger-scale dataset, where each sentence has multiple aspects, making it more challenging.

### Download and process the data
Before using the data processing and downloading script, please make sure that the dependencies in [`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt) have already been installed. After installing the dependencies, use the following command to download and process the data (note: you may not attach any parameters, all parameters have default values):

Specifically, since the four datasets included in SemEval 2014, 2015 and 2016 only contain train and test sets, we split the training set into new training and validation sets in a `9:1` random ratio for better evaluating model performances. Such datasets will be identified with a `Split`suffix.

```shell
bash download_and_process_absa.sh  [--DATA_DIR] [--OUTPUT_DIR] [--STANFORD_DIR]
```
**Parameters:**
+ DATA_DIR: The folder where the downloaded raw data is located. The default parameter is the current folder.
+ OUTPUT_DIR: The folder where the processed data is stored. The default parameter is `dataset`.
+ STANFORD_DIR: The location of the Stanford parser. The default parameter is `stanford-corenlp-3.9.2-minimal` in the parent directory.

**Note:** If the shared parser directory does not exist, the program will ask if you want to fetch the Stanford parser from our mirror data source, which is 353MB in size. Choose `Y` to proceed.

### Data processing for baseline models
In Section4.2 - Results on ABSA tasks and Appendix K - Detailed Results on ABSA Tasks of our paper, we compared the performance of multiple baseline models. Therefore, we provide more information on reproducing the baseline models in [`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines).

### Resource of data
Our mirror data is obtained from SemEval 2014, 2015, 2016 and MAMS, as well as the data sources [ASGCN-data](https://github.com/GeneZC/ASGCN/tree/master/datasets) and [MAMS](https://github.com/siat-nlp/MAMS-for-ABSA). If you have also used this dataset, you can cite their papers as follows:
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