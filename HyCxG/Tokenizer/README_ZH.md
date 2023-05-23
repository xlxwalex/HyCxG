<p align="center" >
    <a href="https://github.com/xlxwalex/HyCxG/tree/main/HyCxG">
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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Tokenizer) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Tokenizer/README_ZH.md)
## CxGTokenizer所需的构式语法词表数据

在本仓库中，我们基于c2xg包提供了六种语言(英语、法语、德语、西班牙语、荷兰语以及土耳其语)的构式语法词表的镜像数据以及下载脚本。关于具体CxGTokenizer的使用指导，请参考[`tutorials`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials)。

### 数据下载
您可以用以下命令来获得并处理数据(可以不附加任何参数，所有参数均有默认值)：
```shell
bash download_cxgdict.sh [--LANGUAGES]
```
**参数含义：**
+ LANGUAGES: 所需语言的简称，如果需要下载全部语言，使用`all`即可。若只希望下载部分语言，请按照以下对应关系在参数中加入所需语言简称：
  1. 英语：`eng`
  2. 法语：`fra`
  3. 德语：`deu`
  4. 西班牙语：`spa`
  5. 荷兰语：`nld`
  6. 土耳其语：`tur`

**注意：** 不同语言对应的构式语法词表会被下载到本目录下的`CxGProcessor/data`文件夹中

### 数据来源
本部分数据来自c2xg，我们的镜像数据来源[c2xg - dictionaries](https://github.com/jonathandunn/c2xg/tree/master/c2xg/data/dictionaries)，如果您也使用了该语法表，您可以引用他们的论文：
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
