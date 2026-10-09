import pandas as pd
import matplotlib.pyplot as plt

# 1. 读数据
df = pd.read_csv("moutai.csv")
df["日期"] = pd.to_datetime(df["日期"])

# 2. 算均线 —— 新知识① rolling(窗口): 每天回看最近N天求平均
df["MA5"] = df["收盘"].rolling(5).mean()
df["MA20"] = df["收盘"].rolling(20).mean()

# 3. 生成信号 —— 新知识② True/False 变成 1/0
df["信号"] = (df["MA5"] > df["MA20"]).astype(int)   # 1=金叉区持有, 0=死叉区空仓

# 4. 找出所有死叉日: 今天信号=0 且 昨天信号=1
death = df[(df["信号"] == 0) & (df["信号"].shift(1) == 1)]
print(f"7年里共出现 {len(death)} 次死叉")
print(death[["日期", "收盘"]])

# 5. 画图: 价格 + 两条均线
plt.plot(df["日期"], df["收盘"], label="price", alpha=0.4)
plt.plot(df["日期"], df["MA5"], label="MA5")
plt.plot(df["日期"], df["MA20"], label="MA20")
plt.legend()
plt.show()