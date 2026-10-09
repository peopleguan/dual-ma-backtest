import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("moutai.csv")
df["日期"] = pd.to_datetime(df["日期"])
df["MA5"] = df["收盘"].rolling(5).mean()
df["MA20"] = df["收盘"].rolling(20).mean()

df["信号"] = (df["MA5"] > df["MA20"]).astype(int)
df["持仓"] = df["信号"].shift(1)                    # 防前视: 今天信号明天持有
df["日收益"] = df["收盘"].pct_change()
df["策略收益"] = df["持仓"].fillna(0) * df["日收益"]

def 体检(收益序列, 名字):
    r = 收益序列.dropna().values          # 扔掉NaN, 变numpy
    nav = np.cumprod(1 + r)
    years = len(r) / 252
    total = nav[-1] - 1
    annual = nav[-1] ** (1 / years) - 1
    vol = r.std() * np.sqrt(252)
    sharpe = annual / vol
    peak = np.maximum.accumulate(nav)
    mdd = ((nav - peak) / peak).min()
    print(f"--- {名字} ---")
    print(f"总收益:   {total:+.1%}")
    print(f"年化收益: {annual:+.1%}")
    print(f"年化波动: {vol:.1%}")
    print(f"夏普比率: {sharpe:.2f}")
    print(f"最大回撤: {mdd:.1%}\n")

体检(df["策略收益"], "双均线策略")
体检(df["日收益"], "买入持有")

# 画图
df["策略净值"] = (1 + df["策略收益"]).cumprod()
df["买入持有净值"] = (1 + df["日收益"].fillna(0)).cumprod()
plt.plot(df["日期"], df["买入持有净值"], label="Buy & Hold", alpha=0.6)
plt.plot(df["日期"], df["策略净值"], label="Dual-MA")
plt.legend()
plt.show()