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

## GLUE Benchmark

The General Language Understanding Evaluation (GLUE) benchmark is a common collection of natural language understanding systems based on a set of nine understanding tasks constructed from various existing natural language understanding datasets. These tasks are carefully selected to include a diverse range of dataset sizes, types, and difficulty levels. We evaluated the performance of this benchmark dataset on eight tasks, including `CoLA` (linguistic acceptability), `SST-2` (sentiment analysis), `MRPC`/`STS-B`/`QQP` (semantic similarity computation and equivalence matching), `MNLI`/`QNLI`/`RTE` (natural language inference).

### Download and process the data
Before using the data processing and downloading script, please make sure that the dependencies in [`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt) have already been installed. After installing the dependencies, use the following command to download and process the data (Note: you may not attach any parameters, all parameters have default values):
```shell
bash download_and_process_glue.sh [--OUTPUT_DIR] [--STANFORD_DIR] [--TASK]
```
**Parameters:**
+ OUTPUT_DIR: The folder where the processed data is stored. The default parameter is `dataset`.
+ STANFORD_DIR: The location of the Stanford parser. The default parameter is `stanford-corenlp-3.9.2-minimal` in the parent directory.
+ TASK: The GLUE tasks that need to be handled can be selected from [cola, sst2, mnli, qnli, qqp, rte, mrpc, stsb]. If you want to download all of them, you can use `all` directly.

**Note:** If the shared parser directory does not exist, the program will ask if you want to fetch the Stanford parser from our mirror data source, which is 353MB in size. Choose `Y` to proceed. In addition, the MNLI task is relatively special, so there will be two extra files (matched/mismatched) in the output.

### Resource of data
This data is proposed in GLUE benchmark, and our data comes from datasets library of Hugging Face [GLUE](https://huggingface.co/datasets?sort=downloads&search=glue). If you also want to use this dataset, you can cite their paper:
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
Or the other bib below:
```
@inproceedings{wangglue,
  title={GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R},
  booktitle={International Conference on Learning Representations (ICLR)},
  year = "2019"
}
```