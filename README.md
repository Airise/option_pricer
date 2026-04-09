# Mini Option Pricer (Assignment 3)

本项目实现了一个基于 `tkinter` 的迷你期权定价器，按作业要求支持欧式、亚式、篮子、美式与 KIKO 看跌期权的定价与相关计算。

## 1. 功能概览

### 已实现功能（对应作业要求）

1. **欧式看涨/看跌期权**：Black-Scholes 闭式公式。
2. **隐含波动率**：二分法反解波动率。
3. **几何亚式看涨/看跌期权**：闭式公式。
4. **算术亚式看涨/看跌期权**：蒙特卡洛 + 控制变量（几何亚式）。
5. **算术两资产篮子看涨/看跌期权**：蒙特卡洛 + 控制变量（几何篮子）。
6. **KIKO 看跌期权（含返利）**：拟蒙特卡洛（Halton）定价 + 有限差分 Delta。
7. **美式看涨/看跌期权**：CRR 二叉树。
8. **图形界面（GUI）**：多标签页输入、计算与结果展示。

---

## 2. 项目结构

```text
option_pricer/
├── README.md
├── requirements.txt
├── main.py
├── core/
│   ├── market_data.py
│   ├── option.py
│   ├── payoff.py
│   └── math_utils.py
├── engines/
│   ├── closed_form.py
│   ├── monte_carlo.py
│   ├── quasi_monte_carlo.py
│   ├── binomial_tree.py
│   └── implied_volatility.py
├── gui/
│   ├── main_window.py
│   ├── european_tab.py
│   ├── american_tab.py
│   ├── asian_tabs.py
│   ├── basket_tabs.py
│   ├── kiko_tab.py
│   ├── implied_vol_tab.py
│   └── result_panel.py
├── tests/
│   ├── test_black_scholes.py
│   ├── test_mc.py
│   ├── test_binomial.py
│   ├── test_qmc_kiko.py
│   └── test_implied_vol.py
└── docs/
    └── sample_outputs.txt
```

---

## 3. 运行环境

- Python: **3.12**（建议）
- 依赖：尽量仅使用标准库（符合课程约束）

---

## 4. 快速开始（Windows PowerShell）

在 `option_pricer` 目录下执行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

如果激活脚本被策略阻止，可先执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

## 5. 使用说明（GUI）

启动后每个标签页对应一种任务：

- `欧式期权`
- `美式期权`
- `几何亚式`
- `算术亚式`
- `几何篮子`
- `算术篮子`
- `KIKO 看跌`
- `隐含波动率`

输入参数后点击对应按钮即可得到价格结果。

### 调试输出

计算结果会同时输出到：

1. GUI 结果面板；
2. 终端（stdout）。

便于调试和留存日志。

---

## 6. 参数与输入约束（部分）

GUI 中已做基础合法性校验：

- `S0, K, T, n_paths, n_obs, steps, n_monitors` 等需为正；
- 波动率与返利需非负；
- 篮子相关系数 `rho ∈ [-1, 1]`；
- KIKO 参数需满足 `L < S0 < U`。

---

## 7. 测试

在虚拟环境中运行：

```powershell
pytest -q
```

测试覆盖：

- Black-Scholes 基准值与 put-call parity；
- implied vol 反解一致性；
- MC/QMC 输出基本性质与置信区间合理性；
- 美式树模型性质检查。

---

## 8. 课程约束说明

- 项目遵循“尽量不使用第三方库”的作业约束；
- 数学函数（正态 CDF/逆CDF、随机数、低差异序列）在项目内自行实现；
- 便于在报告中说明每个模块与函数职责。
