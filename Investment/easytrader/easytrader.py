import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 初始化Tushare接口，将YOUR_API_TOKEN替换为你自己的API令牌
pro = ts.pro_api('2e9a7a0827b4c655aa6c267dc00484c6e76ab1022b5717092b44573e')

# 获取粤传媒近5年的日线数据
df = pro.daily(ts_code='002181.SZ', start_date='20201210', end_date='20241210')
df['trade_date'] = pd.to_datetime(df['trade_date'])
df.set_index('trade_date', inplace=True)

# 将数据保存到Excel
df.to_excel('yuechuanmei_data.xlsx')
# 计算MACD指标
def calculate_macd(data):
    exp12 = data['close'].ewm(span=12, adjust=False).mean()
    exp26 = data['close'].ewm(span=26, adjust=False).mean()
    macd = exp12 - exp26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

df['MACD'], df['MACD_signal'], df['MACD_histogram'] = calculate_macd(df)

# 初始化本金和持仓状态
principal = 20000
holding = False
shares = 0
transaction_records = []

# 根据MACD金叉死叉进行交易操作
for i in range(1, len(df)):
    if df['MACD'].iloc[i] > df['MACD_signal'].iloc[i] and df['MACD'].iloc[i - 1] <= df['MACD_signal'].iloc[i - 1] and not holding:
        # MACD金叉且当前未持仓，买入
        price = df['close'].iloc[i]
        shares = int(principal / price)
        holding = True
        transaction_records.append(('buy', df.index[i], price, shares))
        principal -= price * shares
    elif df['MACD'].iloc[i] < df['MACD_signal'].iloc[i] and df['MACD'].iloc[i - 1] >= df['MACD_signal'].iloc[i - 1] and holding:
        # MACD死叉且当前持仓，卖出
        price = df['close'].iloc[i]
        principal += price * shares
        holding = False
        transaction_records.append(('sell', df.index[i], price, shares))
        shares = 0

# 如果最后仍持仓，以收盘价卖出
if holding:
    price = df['close'].iloc[-1]
    principal += price * shares
    transaction_records.append(('sell', df.index[-1], price, shares))

# 计算总资产价值
df['portfolio_value'] = principal + (df['close'] * shares).fillna(0)

# 绘制资产价值曲线
plt.figure(figsize=(12, 6))
plt.plot(df['portfolio_value'])
plt.title('Portfolio Value over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.show()

# 打印交易记录和最终本金
print("交易记录:")
for record in transaction_records:
    print(record)
print("最终本金:", principal)