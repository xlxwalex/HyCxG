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

## Colloquial Dataset for ABSA

The colloquial ABSA datasets are composed of two sources in sentiment analysis: the Twitter dataset and the GermEval2017 dataset. Both datasets are derived from social media, so they contain more colloquial language compared to other datasets. Since GermEval is much larger than Twitter, we sampled a subset of GermEval for performance testing.

### Download and process the data
Before using the data processing and downloading script, please make sure that the dependencies in [`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt) have already been installed. After installing the dependencies, use the following command to download and process the data (note: you may not attach any parameters, all parameters have default values):
```shell
bash download_and_process_colloquial.sh.sh [--DATA_DIR] [--OUTPUT_DIR] [--STANFORD_DIR]
```
**Parameters:**
+ DATA_DIR: The folder where the downloaded raw data is located. The default parameter is the current folder.
+ OUTPUT_DIR: The folder where the processed data is stored. The default parameter is `dataset`.
+ STANFORD_DIR: The location of the Stanford parser. The default parameter is `stanford-corenlp-3.9.2-minimal` in the parent directory.

**Note:** If the shared parser directory does not exist, the program will ask if you want to fetch the Stanford parser from our mirror data source, which is 353MB in size. Choose `Y` to proceed. Additionally, GermEval requires SpaCy package, which automatically downloads the necessary models when initialized.

### Data processing for baseline models
In Appendix H - Colloquial Expression Results of our paper, we compared the performance of four models, namely RGAT, DualGCN, DGEDT, and KumaGCN, on these colloquial sentiment datasets. Therefore, in the [`baseline`](https://github.com/xlxwalex/HyCxG/tree/main/data/Colloquial/baseline) folder, we provide a conversion script for the GermEval dataset (as Twitter is a commonly used dataset, these baseline models already include the processed data). For more information on reproducing the baseline models, please refer to the [`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines).

### Resource of data
Our mirror data is obtained from Twitter and GermEval, as well as the data sources [acl-14-short-data](https://github.com/songyouwei/ABSA-PyTorch/tree/master/datasets/acl-14-short-data) and [GermEval 2017](http://ltdata1.informatik.uni-hamburg.de/germeval2017/). If you have also used this dataset, you can cite their papers as follows:

#### Twitter Dataset
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
#### GermEval 2017 Competition
```
@article{wojatzki2017germeval,
  title={Germeval 2017: Shared task on aspect-based sentiment in social media customer feedback},
  author={Wojatzki, Michael and Ruppert, Eugen and Holschneider, Sarah and Zesch, Torsten and Biemann, Chris},
  journal={GermEval},
  pages={1--12},
  year={2017}
}
```