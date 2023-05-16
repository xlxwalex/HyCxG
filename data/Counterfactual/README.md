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

[**English**](https://github.com/xlxwalex/HyCxG/tree/main/data) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/data/README_ZH.md)

## Counterfactual Detection Dataset

The Counterfactual Recognition (CR) dataset is derived from Subtask 1 - Recognizing Counterfactual Statements (RCS) of SemEval2020 Task5. The data is collected from the domains of politics, finance, and health, and consists of 13k training data with 7k test data.

### Download and process the data
Before using the data processing and downloading script, please make sure that the dependencies in [`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt) have already been installed. After installing the dependencies, use the following command to download and process the data (note: you may not attach any parameters, all parameters have default values):
```shell
bash download_and_process_counterfactual.sh [--DATA_DIR] [--OUTPUT_DIR] [--STANFORD_DIR]
```
**Parameters:**
+ DATA_DIR: The folder where the downloaded raw data is located. The default parameter is the current folder.
+ OUTPUT_DIR: The folder where the processed data is stored. The default parameter is `JSON_Counterfactual`.
+ STANFORD_DIR: The location of the Stanford parser. The default parameter is `stanford-corenlp-3.9.2-minimal` in the parent directory.

**Note:** If the shared parser directory does not exist, the program will ask if you want to fetch the Stanford parser from our mirror data source, which is 353MB in size. Choose `Y` to proceed.

### Resource of data
This data is proposed in SemEval2020 Task5, and our mirrored data comes from official source [SemEval2020_Task5](https://github.com/Jiaqi1008/SemEval2020_Task5). If you also want to use this dataset, you can cite their paper:
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