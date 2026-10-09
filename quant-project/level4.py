import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("moutai.csv")
df["日期"] = pd.to_datetime(df["日期"])
df["MA5"] = df["收盘"].rolling(5).mean()
df["MA20"] = df["收盘"].rolling(20).mean()

# 1. 信号(当天收盘后才知道)
df["信号"] = (df["MA5"] > df["MA20"]).astype(int)

# 2. 持仓: 信号挪后一天 —— 今天出信号, 明天才算持有 防前视!
df["持仓"] = df["信号"].shift(1)

# 3. 策略日收益 = 持仓 × 次日涨跌; 持仓为NaN(前20天)当0
df["日收益"] = df["收盘"].pct_change()
df["策略收益"] = df["持仓"].fillna(0) * df["日收益"]

# 4. 两条净值曲线
df["买入持有"] = (1 + df["日收益"].fillna(0)).cumprod()
df["策略净值"] = (1 + df["策略收益"]).cumprod()

print(f"买入持有总收益: {(df['买入持有'].iloc[-1] - 1):+.1%}")
print(f"策略总收益:     {(df['策略净值'].iloc[-1] - 1):+.1%}")
print(f"交易次数:       {int(df['信号'].diff().abs().sum())}")

# 5. 画图对比
plt.plot(df["日期"], df["买入持有"], label="Buy & Hold", alpha=0.6)
plt.plot(df["日期"], df["策略净值"], label="Dual-MA")
plt.legend()
plt.show()