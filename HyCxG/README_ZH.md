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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/README_ZH.md)
## 运行HyCxG

### 快速运行指引
在运行HyCxG模型前，我们需要先进行多种数据的准备，以下为所需的操作步骤：
1. (**数据集准备**) 请先准备数据，我们提供了数据的自动下载处理脚本，详情请见[`data`](https://github.com/xlxwalex/HyCxG/tree/main/data)文件夹。在默认配置下，处理完的数据会以文件夹的形式保存在`datas/dataset`文件夹中，请复制所有的数据文件夹(例如：`JSONABSA_MAMS`等)到本目录下的`dataset`文件夹中
2. (**构式语法表数据准备**) 在本目录下的[`dataset`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset)文件夹中，我们提供了构式语法列表数据的自动下载脚本，详情请见文件夹中的README文件。在默认配置下，所需数据文件会自动下载到对应位置
3. (**构式词表数据准备**) 在本目录下的[`Tokenizer`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/dataset)文件夹内，我们提供了构式词表数据的自动下载脚本，执行命令请见文件夹中的README文件。同样在默认配置下，所需数据文件会自动下载到对应位置
4. (**运行HyCxG**) 在[`run_hycxg.sh`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/run_hycxg.sh)中我们给出了运行模型的命令，可以通过修改参数来适应不同的数据集

**注意**：各个任务的超参数设置请见[`guidelines`](https://github.com/xlxwalex/HyCxG/tree/main/guidelines)。