<p align="center" >
    <a href="https://github.com/xlxwalex/HyCxG/tree/main/HyCXG">
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

[**English**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/README_ZH.md)

## Run HyCxG

### Quick start
Before running our HyCxG model, a variety of preparation steps are required. The following are the necessary steps:
1. (**Data preparation**) Please prepare the data first. We have provided an automatic download and processing script for all data. Please refer to the [`data`](https://github.com/xlxwalex/HyCxG/tree/main/data) folder for details. With the default configuration, the processed data will be saved in the `data/dataset` folder in the form of folders. Please copy all the data folders (e.g. `JSONABSA_MAMS`) to the `dataset` folder in this directory.
2. (**Preparation for CxG lists**) In the [`dataset`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset) folder under this directory, we provide an automatic download script for the list of CxG. Please refer to the README file in the folder for details. Under the default configuration, the required data files will be automatically downloaded to the corresponding location.
3. (**Preparation for CxG vocabulary**) In the [`Tokenizer`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset) folder from this directory, we provide an automatic download script for the construction vocabulary data. Please refer to the README file in the folder for the execution command. Similarly, under the default configuration, the required data files will be automatically downloaded to the corresponding location.
4. (**Run HyCxG**): In the [`run_hycxg.sh`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/run_hycxg.sh) file, we provide the command to run the HyCxG model, which can be adapted to different datasets by modifying the parameters.

**Note:** The hyper-parameter settings for each task can be found in the [`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines).