# FinEco-hw — LN429 金融计量 作业仓库

- 作者：魏致衡（LN429）
- 课程：中山大学岭南学院 LN429 金融计量（连玉君）
- HW02 作业页面：<https://lianxhcn.github.io/FinEco/exercises/hw-02.html>

| 目录 | 内容 | 入口 |
|---|---|---|
| [`hw02-1/`](hw02-1/) | 股票收益与组合风险分析（10 只 A 股，2021-01-04—2026-09-16） | `hw02-1/hw02-1.ipynb` |
| [`hw02-2/`](hw02-2/) | 房地产上市公司财务特征分析（2005—2015） | `hw02-2/hw02-2.ipynb` |

## 数据说明

两道题的数据都来自 **CSMAR（中山大学授权）**。根据数据库授权范围，**本仓库不包含任何 CSMAR 原始或行级数据**，`.gitignore` 已排除 `data/raw/`、`data/processed/`、`outputs/` 及所有 CSV/ZIP 文件。
- 有 CSMAR 权限的读者：按各题 `data/README.md` 下载同名 ZIP，放入 `data/raw/`（**不要解压**），然后运行 Notebook。
- 其他读者：可以直接阅读 Notebook 中保存的输出。

## 运行

```bash
pip install -r hw02-1/requirements.txt
cd hw02-1 && jupyter nbconvert --to notebook --execute --inplace hw02-1.ipynb
cd ../hw02-2 && jupyter nbconvert --to notebook --execute --inplace hw02-2.ipynb
cd .. && python verify/verify_hw02.py   # 可选：独立复核关键数值
```

两个 Notebook 相互独立，运行顺序不限；每个都可以 Restart Kernel → Run All。

## AI 使用

使用了 ChatGPT / Codex 与 Claude，详见各 Notebook 第一个单元的 AI 使用声明。
