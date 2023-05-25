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

[**English**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann) | [**简体中文**](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/README_ZH.md)

## Cond-MC Solver

The code in this package is utilized to solve the Cond-MC problem in the second section of our paper (Construction Extraction and Selection) via simulated annealing (SA). Please refer to the paper for problem definition and solution steps. Meanwhile, you can browse [`tutorials`](https://github.com/xlxwalex/HyCxG/tree/main/tutorials) for more detailed information.

### Quick Start
We provide multiple instances in the [`CxGCoverage.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/CxGCoverage.py) file, and you can directly run the following code to browse the results (these instances can also serve as a reference for hyper-parameters adjustment):

```shell
python CxGCoverage.py
```
**Hyper-parameters:**
+ PATTERN_SCORE: The dict represents scores for slots with different levels of abstraction in the constructions, corresponding to ![](http://latex.codecogs.com/svg.latex?s_{syn}), ![](http://latex.codecogs.com/svg.latex?s_{sem}) and ![](http://latex.codecogs.com/svg.latex?s_{lex}) in the paper.
+ COVERAGE_SCORE: The weights in the objective function are stored in this dict, corresponding to ![](http://latex.codecogs.com/svg.latex?w_{1})，![](http://latex.codecogs.com/svg.latex?w_{2})，![](http://latex.codecogs.com/svg.latex?w_{3}) in our paper.

**Note:** These hyper-parameters are hardcoded in the code, please modify the hyper-parameters in the header of [`CxGCoverage.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/CxGCoverage.py) directly.

### Acknowledgement
The code in [`SimuAnneal.py`](https://github.com/xlxwalex/HyCxG/tree/main/HyCxG/Simuann/SimuAnneal.py) is modified from [`simanneal`](https://github.com/perrygeo/simanneal), which provides a convenient framework for solving problems. We are extremely grateful for the efforts and contributions by the owner of this repo!
