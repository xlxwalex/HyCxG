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
[**English**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/README_ZH.md)
## Cond-MC求解器

该部分代码用于对我们论文第二章节(Construction Extraction and Selection)的Cond-MC问题使用模拟退火(Simulated Annealing, SA)的方式进行求解。问题定义以及求解步骤请见论文。更多详细的细节请参考[`tutorials`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials)。

### 快速上手
我们在[`CxGCoverage.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/CxGCoverage.py)中提供了多个例子，您可以直接使用以下代码直接运行来浏览结果(同时，这些例子也可以作为超参调整的参考)：
```shell
python CxGCoverage.py
```
**超参数列表：**
+ PATTERN_SCORE：该字典中表示的是构式不同抽象等级的槽的分数，对应论文中![](http://latex.codecogs.com/svg.latex?s_{syn}), ![](http://latex.codecogs.com/svg.latex?s_{sem}), ![](http://latex.codecogs.com/svg.latex?s_{lex})
+ COVERAGE_SCORE：该字典中存储的是目标函数中的权重，对应论文中的![](http://latex.codecogs.com/svg.latex?w_{1})，![](http://latex.codecogs.com/svg.latex?w_{2})，![](http://latex.codecogs.com/svg.latex?w_{3})

**注意：** 这些超参数被硬编码在了代码文件中，因此请直接修改[`CxGCoverage.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/CxGCoverage.py)头部的两个字典。

### 致谢
本部分的[`SimuAnneal`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/SimuAnneal.py)修改自[`simanneal`](https://github.com/perrygeo/simanneal)，其提供了一个很方便的框架来对问题进行求解，我们十分感谢该仓库开发者的贡献！
