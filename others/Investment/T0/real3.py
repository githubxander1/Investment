import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def indicator3(close, high, low):
    """
    阻力支撑与买卖信号指标

    参数：
    close: 收盘价序列 (pd.Series)
    high: 最高价序列 (pd.Series)
    low: 最低价序列 (pd.Series)

    返回：
    dict: 包含计算结果的字典
    """
    # 计算昨收、今高、今低
    prev_close = close.shift(1)  # DYNAINFO(3)
    today_high = high  # DYNAINFO(5)
    today_low = low  # DYNAINFO(6)

    # 计算H1和L1
    H1 = pd.concat([prev_close, today_high], axis=1).max(axis=1)
    L1 = pd.concat([prev_close, today_low], axis=1).min(axis=1)

    # 计算阻力与支撑
    P1 = H1 - L1
    resistance = L1 + P1 * 7 / 8  # 阻力位
    support = L1 + P1 * 0.5 / 8  # 支撑位（等价于 P1*(1/16)）

    # 计算买卖信号（LONGCROSS转换为2周期交叉判断）
    # 买入信号：支撑线在2周期内上穿现价
    buy_signal = (close.shift(2) < support.shift(2)) & (close.shift(1) > support.shift(1))

    # 卖出信号：现价在2周期内下穿阻力线
    sell_signal = (close.shift(2) > resistance.shift(2)) & (close.shift(1) < resistance.shift(1))

    return {
        'resistance': resistance,
        'support': support,
        'buy_signal': buy_signal,
        'sell_signal': sell_signal,
        'close': close
    }


# -------------------
# 示例用法与绘图
# # -------------------
# # 假设df包含'close', 'high', 'low'列
# # result = indicator3(df['close'], df['high'], df['low'])
#
# # 绘制图形
# def plot_indicator(df):
#     result = indicator3(df['close'], df['high'], df['low'])
#
#     plt.figure(figsize=(12, 6))
#
#     # 绘制价格曲线
#     plt.plot(df.index, result['close'], label='现价', color='white', linewidth=1)
#
#     # 绘制阻力与支撑线
#     plt.plot(df.index, result['resistance'], label='阻力', color='#00DD00', linestyle='--')
#     plt.plot(df.index, result['support'], label='支撑', color='#00DD00', linestyle='--')
#
#     # 绘制买入信号（红色文本+箭头）
#     buy_points = df.index[result['buy_signal']]
#     for point in buy_points:
#         plt.text(point, result['support'][point] * 1.001, '买', color='red', va='bottom')
#         plt.scatter(point, result['support'][point], marker='^', color='red', zorder=5)
#
#     # 绘制卖出信号（绿色文本+箭头）
#     sell_points = df.index[result['sell_signal']]
#     for point in sell_points:
#         plt.text(point, result['close'][point], '卖', color='green', va='top')
#         plt.scatter(point, result['close'][point], marker='v', color='green', zorder=5)
#
#     # 绘制交叉柱状线（黄色）
#     cross_dates = df.index[(result['buy_signal'] | result['sell_signal'])]
#     for date in cross_dates:
#         plt.bar(date,
#                 height=result['resistance'][date] - result['support'][date],
#                 bottom=result['support'][date],
#                 width=0.2,
#                 color='yellow',
#                 alpha=0.5)
#
#     plt.title('阻力支撑与买卖信号')
#     plt.legend()
#     plt.grid(True)
#     plt.show()
#
# # 示例数据调用（需替换为真实数据）
# # import yfinance as yf
# # data = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
# # plot_indicator(data)