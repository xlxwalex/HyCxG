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

## Data of HyCxG
In this work, we used the following five datasets (mentioned in parentheses in the paper):
 + **Aspect-based sentiment analysis datasets** `[Rest 14/Lap 14/Rest 15/Rest 16/MAMS]` (Section 4.2 - Results on ABSA tasks)
 + **GLUE benchmark** `[CoLA/SST-2/MNLI/QNLI/RTE/QQP/MRPC/STS]` (Section 4.2 - Results on GLUE tasks)
 + **Multilingual sentiment analysis datasets** `[French/Spanish/Turkish/Dutch]` (Section 4.3 - Multilingual results)
 + **Counterfactual detection dataset** (Appendix F - Pattern Recognition Capability of CxG)
 + **Colloquial datasets for ABSA** `[Twitter/GermEval]` (Appendix H - Colloquial Expression Results)

### Aspect-based Sentiment Analysis Datasets
Aspect-based sentiment analysis (ABSA) datasets are referred to the folder of [`ABSA`](https://github.com/xlxwalex/HyCxG/tree/main/data/ABSA), including four datasets from SemEval 2014, 2015, 2016 and the MAMS dataset. We provide the original links to the datasets and download scripts (from mirror data sources) in the folder, as well as scripts to convert the data into the HyCxG required format.

Besides, for convenient evaluation of performance on other baseline models, we provide scripts for different baseline models that can convert the data to their official formats (for more information on baseline models, please see the [`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines)).

### GLUE Benchmark
The GLUE benchmark is a commonly used benchmark for evaluating natural language understanding tasks, consisting of 11 tasks, can be found in the [`GLUE`](https://github.com/xlxwalex/HyCxG/tree/main/data/GLUE) folder. We tested all tasks except for Winograd NLI (WNLI) and Diagnostics Main (DM). The original download links and download scripts (from mirror data sources) for the GLUE benchmark are provided in the folder. We also produce a script for converting the data format to our HyCxG. The mirror source we used for this benchmark is directly from the Hugging Face datasets.

### Multilingual Sentiment Analysis Datasets
Based on SemEval 2016, we have chosen French, Spanish, Turkish and Dutch as our multilingual experimental datasets. Please refer to the [`Multilingual`](https://github.com/xlxwalex/HyCxG/tree/main/data/Multilingual) and [`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines) folders, where we provide the original links and mirror data downloading scripts for the datasets. We also provide scripts to convert the data into the required format for HyCxG.

### Counterfactual Detection Dataset
The Counterfactual detection dataset is derived from Task 5 of SemEval 2020. Please refer to the [`Counterfactual`](https://github.com/xlxwalex/HyCxG/tree/main/data/Counterfactual) folder. We also provide the link of the dataset and the script for downloading the mirrored data and converting the data into the required format of HyCxG in the folder.

### Colloquial datasets for ABSA
The colloquial sentiment analysis experiments are based on two annotated datasets on social media, Twitter and GermEval. Please refer to the [`Colloquial`](https://github.com/xlxwalex/HyCxG/tree/main/data/Colloquial) folder. We provide the original links of the datasets and mirror data and converting the data into the required format of HyCxG in this folder.

## Quick Download and Process
In addition to downloading and processing data files separately from each subdirectory, we also provide a data pipeline script [`data_pipeline.sh`](https://github.com/xlxwalex/HyCxG/tree/main/data/data_pipeline.sh), which downloads and processes all data with just one step. Before using the data processing and downloading script, please make sure that the dependencies in [`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt) have already been installed. After installing the dependencies, use the following command to obtain and process data (Note: you may not attach any parameters, all parameters have default values):
```shell
bash data_pipeline.sh [--DATA_DIR] [--OUTPUT_DIR] [--STANFORD_DIR]
```
**Parameters:**
+ DATA_DIR: The folder where the downloaded raw data is located. The default parameter is the current folder.
+ OUTPUT_DIR: The folder where the processed data is stored. The default parameter is `dataset`.
+ STANFORD_DIR: The location of the Stanford parser. The default parameter is `stanford-corenlp-3.9.2-minimal` in this directory.

**Note:** If you have the Stanford Parser in your system, please set `STANFORD_DIR` to the directory where the parser is located. If the parser folder does not exist, the program will automatically download it (353MB) from the mirror source. You can also use [`download_stanfordcore.py`](https://github.com/xlxwalex/HyCxG/tree/main/data/download_stanfordcore.py) for manual download.

## Mirror data source
As both the datasets and parser mentioned above are publicly available and can be downloaded directly, we provide a backup mirror source for the convenience of users to download them uniformly (except for the GLUE benchmark). If you are the copyright owner of the datasets or parser and believe that distributing them through this source may violate your data license, please contact [`xlxw@zju.edu.cn`](mailto:xlxw@zju.edu.cn) and we will immediately remove your dataset or parser.

## Data Usage Regulations
Please follow the usage terms of the original datasets when downloading or accessing the datasets in any way. The links to the specific original datasets can be found in each dataset folder. Please note these data should not be used for any `illegal` or `discriminatory` purposes.