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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/data) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/data/README_ZH.md)

## HyCxG使用的数据集

在本工作中，我们用到了以下五个方面的数据集(括号中为在论文中提到的位置)：
 + **方面级情感分析数据集** `[Rest 14/Lap 14/Rest 15/Rest 16/MAMS]` (4.2节的Results on ABSA tasks)
 + **GLUE基准数据集** `[CoLA/SST-2/MNLI/QNLI/RTE/QQP/MRPC/STS]` (4.2节的Results on GLUE tasks)
 + **多语言情感分析数据集** `[French/Spanish/Turkish/Dutch]` (4.3节的Multilingual results)
 + **反事实检测数据集** (附录F的Pattern Recognition Capability of CxG)
 + **口语化情感分析数据集** `[Twitter/GermEval]` (附录H的Colloquial Expression Results)

### 方面级情感分析数据集
方面级情感分析(Aspect-based sentiment analysis)数据集请见[`ABSA文件夹`](https://github.com/xlxwalex/HyCxG/tree/main/data/ABSA)，其包含来自SemEval 2014/15/16的4个数据集以及MAMS数据集。我们在文件夹中给出了数据集的原始链接以及镜像数据下载脚本，并提供了转换为HyCxG所需数据格式的脚本。

除此之外，为了方便使用者在其他基线模型上评估性能，我们给不同的基线模型提供了转换脚本可以转换为它们官方数据格式的脚本(更多关于基线模型的信息请见[`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines))

### GLUE基准数据集
GLUE基准(GLUE benchmark)是常用的自然语言理解任务评估基准，共由11个任务组成，请见[`GLUE文件夹`](https://github.com/xlxwalex/HyCxG/tree/main/data/GLUE)。我们测试了除`Winograd NLI(WNLI)`以及`Diagnostics Main(DM)`外的所有任务。我们在文件夹中给出了GLUE基准的原始下载链接以及镜像下载脚本(该镜像我们直接使用了Hugging Face datasets中的数据)，并提供了转换为HyCxG所需数据格式的脚本。

### 多语言情感分析数据集
多语言情感分析数据集基于SemEval 2016，我们选择了法语、西班牙语、土耳其语以及荷兰语作为多语言实验数据集，请见[`Multilingual文件夹`](https://github.com/xlxwalex/HyCxG/tree/main/data/Multilingual)。我们在文件夹中给出了数据集的原始链接以及镜像数据下载脚本，并提供了转换为HyCxG所需数据格式的脚本。

另外由于其他基线模型只在英语数据集上进行了性能评估，为了方便使用者能够对比基线模型在多语言实验下的性能，我们提供了不同的基线模型的数据转换脚本以将它们的数据格式进行转换，具体细节请见[`Multilingual文件夹`](https://github.com/xlxwalex/HyCxG/tree/main/data/Multilingual)以及[`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines)。

### 反事实检测数据集
反事实检测(Counterfactual detection)数据集基于SemEval2020的Task5，请见[`Counterfactual文件夹`](https://github.com/xlxwalex/HyCxG/tree/main/data/Counterfactual)。我们同样在文件夹中给出了数据集的原始链接以及镜像数据下载脚本，并提供了转换为HyCxG所需数据格式的脚本。

### 口语化情感分析数据集
口语化情感分析实验基于Twitter以及GermEval这两个在社交媒体数据上标注的数据集，请见[`Colloquial文件夹`](https://github.com/xlxwalex/HyCxG/tree/main/data/Colloquial)。我们在该文件夹中给出了数据集的原始链接以及镜像数据下载脚本，并提供了转换为HyCxG所需数据格式的脚本。

## 快速下载并处理
除了进入以上各个子目录分别下载数据文件并处理的方式之外，我们也提供了只需一步即可直接下载并处理所有数据的脚本[`data_pipeline.sh`](https://github.com/xlxwalex/HyCxG/tree/main/data/data_pipeline.sh)。在使用脚本前，请您确认已经安装了[`requirements.txt`](https://github.com/xlxwalex/HyCxG/blob/main/requirements.txt)中的依赖包。在安装完依赖包后，用以下命令来获得并处理数据(可以不附加任何参数，所有参数均有默认值)：
```shell
bash data_pipeline.sh [--DATA_DIR] [--OUTPUT_DIR] [--STANFORD_DIR]
```
**参数含义：**
+ DATA_DIR: 下载的原始数据所在文件夹, 默认为当前文件夹
+ OUTPUT_DIR: 处理好后的数据存储的文件夹, 默认为`dataset`
+ STANFORD_DIR: 斯坦福解析器所在位置，默认为本目录的`stanford-corenlp-3.9.2-minimal`

**注意：** 如果您的系统中存有斯坦福解析器，请将`STANFORD_DIR`设置为解析器所在目录。若解析器文件夹不存在，那么程序会自动从镜像源中进行下载(共353MB)。您也可以使用[`download_stanfordcore.py`](https://github.com/xlxwalex/HyCxG/tree/main/data/download_stanfordcore.py)手动进行下载。

## 镜像数据源
由于以上数据集以及解析器均为公开数据集并且能够直接得到，因此为了方便使用者进行统一下载，我们提供了以上数据的备份镜像源(除了GLUE基准数据集)。如果您是数据集以及解析器的版权所有者，并认为在该数据源分发可能违反您的公开许可，请联系[`xlxw@zju.edu.cn`](mailto:xlxw@zju.edu.cn)，我们会立刻撤下您的数据集或解析器。

## 数据使用规范
通过下载数据或以任何方式访问这些数据集，请遵守原始数据集的使用条款，具体原始数据集的链接请见各数据集文件夹。请注意这些数据不得用于任何`非法`或`歧视性`的目的。