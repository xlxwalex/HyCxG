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

## Multilingual Dataset for ABSA

The Multilingual sentiment analysis dataset is based on Semeval 2016 Task 5, which provides data in 8 different languages from various domains. We selected 4 different languages from the Restaurant domain for the multilingual performance evaluation, including `French`, `Spanish`, `Turkish`, and `Dutch`.

### Download and process the data
Before using the data processing and downloading script, please make sure that the dependencies in [`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt) have already been installed. After installing the dependencies, use the following command to download and process the data (note: you may not attach any parameters, all parameters have default values):
```shell
bash download_and_process_multilingual.sh [--DATA_DIR] [--OUTPUT_DIR]
```
**Parameters:**
+ DATA_DIR: The folder where the downloaded raw data is located. The default parameter is the current folder.
+ OUTPUT_DIR: The folder where the processed data is stored. The default parameter is `dataset`.

**Note:** The `PORT` variable in the script represents the startup port of the Stanza server, which is set to `9000` by default. If this port is already in use on your machine, you need to manually set a different port in the script.

### Data processing for baseline models
In Section4.3 - Multilingual results of our paper, we compared the performance of four models, namely RGAT, DualGCN, DGEDT, and KumaGCN on these multilingual sentiment datasets. Therefore, we provide a conversion script for processing the data in the [`baseline`](https://github.com/xlxwalex/HyCxG/tree/main/data/Multilingual/baseline) folder. For more information on reproducing the baseline models, please refer to the [`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines).

### Resource of data
Our mirror data is obtained from SemEval 2016, as well as the data sources [SemEval-2016 Task 5](https://alt.qcri.org/semeval2016/task5/). If you have also used this dataset, you can cite their papers as follows:
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
