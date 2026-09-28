"""Independent re-computation of key HW02 statistics (separate code path from the notebooks).
Run from the repo root after both notebooks have executed. Compares against the notebooks' saved tables."""
import io, zipfile, glob, re
import numpy as np, pandas as pd

ok = True
def check(name, a, b, tol=1e-6):
    global ok
    good = abs(a - b) <= tol
    ok &= good
    print(f"{'OK ' if good else 'BAD'} {name}: verify={a:.6f} notebook={b:.6f}")

# ---------------- HW02-1 ----------------
rd = lambda f, m: pd.read_csv(io.BytesIO(zipfile.ZipFile(f).read(m)), encoding="utf-8-sig", dtype={"Stkcd": str})
t = pd.concat([rd(f, "TRD_Dalyr.csv") for f in sorted(glob.glob("hw02-1/data/raw/日个股*.zip"))])
t["Trddt"] = pd.to_datetime(t.Trddt)
ret = t.pivot(index="Trddt", columns="Stkcd", values="Dretwd")
mv = t.pivot(index="Trddt", columns="Stkcd", values="Dsmvtll").ffill()
w = mv.shift(1); w = w.div(w.sum(axis=1), axis=0)
m = (ret.index >= "2021-01-01") & (ret.index <= "2026-09-16")
R = ret[m].fillna(0.0); W = w[m]
res = {"等权组合": R.mean(axis=1), "市值加权组合(t−1)": (W * R).sum(axis=1)}
nb = pd.read_csv("hw02-1/outputs/tables/portfolio_performance.csv", index_col=0)
for k, r in res.items():
    nav = np.r_[1.0, (1 + r).cumprod().values]
    WT = nav[-1]
    mdd = (1 - nav / np.maximum.accumulate(nav)).max()
    check(f"{k} T", len(r), float(nb.loc["T", k]))
    check(f"{k} 期末净值", WT, float(nb.loc["期末净值", k]))
    check(f"{k} 几何年化%", 100 * (WT ** (252 / len(r)) - 1), float(nb.loc["几何年化收益%", k]))
    check(f"{k} 年化波动%", 100 * r.std() * np.sqrt(252), float(nb.loc["年化波动%", k]))
    check(f"{k} 最大回撤%", 100 * mdd, float(nb.loc["最大回撤%", k]))
check("VW 权重和最大偏离", float((W.sum(axis=1) - 1).abs().max()), 0.0, 1e-12)
# single-day stats: drop suspension days AND the first trading day after each suspension spell
r1 = ret[m].copy()
for s in r1.columns:
    full = ret[s]
    susp = full.isna() & (full.index >= "2020-12-01")
    resume = (~full.isna()) & susp.shift(1, fill_value=False)
    r1.loc[resume[m].values, s] = np.nan
desc = pd.read_csv("hw02-1/outputs/tables/stock_descriptive_stats.csv", index_col=0)
check("长江电力 单日年化波动%", 100 * r1["600900"].std() * np.sqrt(252), float(desc.loc["长江电力(600900)", "年化波动%"]))
check("长江电力 N(单日)", r1["600900"].count(), float(desc.loc["长江电力(600900)", "N(单日)"]))
c = r1.corr(min_periods=200).values
check("相关系数均值（45 对）", c[np.triu_indices(10, 1)].mean(),
      pd.read_csv("hw02-1/outputs/tables/corr_matrix.csv", index_col=0).values[np.triu_indices(10, 1)].mean())

# ---------------- HW02-2 ----------------
Z = lambda p: glob.glob(f"hw02-2/data/raw/{p}")[0]
rz = lambda p, m, **k: pd.read_csv(io.BytesIO(zipfile.ZipFile(Z(p)).read(m)), encoding="utf-8-sig", **k)
b = rz("上市公司基本信息年度表*.zip", "STK_LISTEDCOINFOANL.csv", dtype=str)
o = rz("中国上市公司股权性质文件*.zip", "EN_EquityNatureAll.csv", dtype=str)
bs = rz("资产负债表221438189*.zip", "FS_Combas.csv", dtype={"Stkcd": str})
ic = rz("利润表*.zip", "FS_Comins.csv", dtype={"Stkcd": str})
b["y"] = b.EndDate.str[:4].astype(int); o["y"] = o.EndDate.str[:4].astype(int)
bs["y"] = bs.Accper.str[:4].astype(int); ic["y"] = ic.Accper.str[:4].astype(int)
s = b[(b.IndustryCodeC == "K70") & (b.LISTINGDATE <= b.EndDate)][["Symbol", "y"]]
s = s.merge(o[["Symbol", "y", "EquityNatureID"]], on=["Symbol", "y"], how="left")
s = s.merge(bs.rename(columns={"Stkcd": "Symbol"}), on=["Symbol", "y"], how="left")
lag = bs.rename(columns={"Stkcd": "Symbol", "A001000000": "TA0", "A003000000": "EQ0"})[["Symbol", "y", "TA0", "EQ0"]]
lag["y"] += 1
s = s.merge(lag, on=["Symbol", "y"], how="left").merge(ic.rename(columns={"Stkcd": "Symbol"})[["Symbol", "y", "B002000000"]], on=["Symbol", "y"], how="left")
check("HW02-2 公司-年", len(s), 1193, 0); check("HW02-2 公司数", s.Symbol.nunique(), 172, 0)
s["own"] = s.EquityNatureID.map({"1": "国企", "2": "民营"}).fillna("其他")
s.loc[s.EquityNatureID.isna(), "own"] = "产权不明"
cnt = pd.read_csv("hw02-2/outputs/tables/firm_counts_by_ownership.csv", index_col=0)
for g in ["国企", "民营", "其他", "产权不明"]:
    check(f"2015 年 {g} 公司数", (s[(s.y == 2015)].own == g).sum(), float(cnt.loc[2015, g]), 0)
s["lev"] = s.A002000000 / s.A001000000
s["bankloan"] = (s.A002101000 + s.A002201000) / s.A002000000      # NaN propagates: missing ≠ 0
s["stdebt"] = s.A002100000 / s.A002000000
s["roa"] = s.B002000000 / ((s.A001000000 + s.TA0) / 2)
ae = (s.A003000000 + s.EQ0) / 2
s["roe"] = np.where(ae > 0, s.B002000000 / ae, np.nan)
s["cash_ta"] = s.A001101000 / s.A001000000
summ = pd.read_csv("hw02-2/outputs/tables/soe_private_summary.csv", index_col=0)
names = {"lev": "资产负债率", "bankloan": "bankloan（借款/总负债）", "stdebt": "短期负债占比", "roa": "ROA", "roe": "ROE", "cash_ta": "Cash_TA（货币资金/总资产）"}
for v, nmv in names.items():
    check(f"{nmv} 国企合并中位数%", 100 * s.loc[s.own == "国企", v].median(), float(summ.loc[nmv, "合并中位数：国企%"]))
    check(f"{nmv} 民营合并中位数%", 100 * s.loc[s.own == "民营", v].median(), float(summ.loc[nmv, "合并中位数：民营%"]))
check("ROE 有效 N", s.roe.notna().sum(), 1163, 0)
allmm = pd.read_csv("hw02-2/outputs/tables/all_firms_mean_median.csv", header=[0, 1], index_col=0)
check("2015 资产负债率中位数%", 100 * s[s.y == 2015].lev.median(), float(allmm.loc[2015, ("资产负债率", "中位数%")]))
check("2009 资产负债率均值%", 100 * s[s.y == 2009].lev.mean(), float(allmm.loc[2009, ("资产负债率", "均值%")]))
print("\nALL CHECKS PASSED" if ok else "\nMISMATCH FOUND")
