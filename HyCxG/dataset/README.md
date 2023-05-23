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

[**English**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset/README_ZH.md)

## Construction grammar list

In this repository, we provide mirror data and download script for six language (English, French, German, Spanish, Dutch, and Turkish) pattern syntax lists based on the `c2xg` package.

### Download data
You can use the following command to download and process the data (Note: you may not attach any parameters, all parameters have default values):
```shell
bash download_vocab.sh [--LANGUAGES]
```
**Parameters:**
+ LANGUAGES: The abbreviation of the required languages. If you want to download all languages, use `all` for `LANGUAGES` parameter. If you only want to download part of languages, please include the abbreviation of the required languages in the parameter according to the following abbreviations:
  1. English: `eng`
  2. French: `fra`
  3. German: `deu`
  4. Spanish: `spa`
  5. Dutch: `nld`
  6. Turkish: `tur`

**Note:** The list of construction crammar corresponding to different languages will be downloaded to the `CxG` folder in the current directory.

### Resource of data
Our mirror data is obtained from c2xg package, as well as the data sources [c2xg - data](https://github.com/jonathandunn/c2xg/tree/master/c2xg/data/models). If you have also used these construction grammar lists, you can cite their papers as follows:
```
@article{dunn2017computational,
  title={Computational learning of construction grammars},
  author={Dunn, Jonathan},
  journal={Language and cognition},
  volume={9},
  number={2},
  pages={254--292},
  year={2017},
  publisher={Cambridge University Press}
}
```
