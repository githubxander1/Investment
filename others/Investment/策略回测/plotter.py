# plotter.py
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mplcursors import cursor


def plot_kline_with_ma(df, stock_name, strategy_dir, strategy_module_name):
    df['5日均线'] = df['收盘价_复权'].rolling(window=5).mean()
    df['20日均线'] = df['收盘价_复权'].rolling(window=20).mean()
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['收盘价_复权'], label='收盘价')
    plt.plot(df.index, df['5日均线'], label='5日均线')
    plt.plot(df.index, df['20日均线'], label='20日均线')

    # 绘制买入信号
    buy_signals = df[df['信号'] == '买入']
    plt.scatter(buy_signals.index, buy_signals['收盘价_复权'], color='red', marker='^', label='买入信号')

    # 绘制卖出信号
    sell_signals = df[df['信号'] == '卖出']
    plt.scatter(sell_signals.index, sell_signals['收盘价_复权'], color='green', marker='v', label='卖出信号')

    # 添加虚线的横竖线
    for date in df.index:
        plt.axvline(date, linestyle='--', color='gray', alpha=0.3)

    # 在每个交易日线条的第一个端点显示黑点
    plt.scatter(df.index, df['收盘价_复权'], color='black', marker='.', s=20)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    plt.title(f'{stock_name} K线图+均线')
    plt.xlabel('交易日期')
    plt.ylabel('价格')
    plt.legend()
    # 添加鼠标悬停显示具体日期和价格
    cursor(plt.gca(), hover=True)

    # 创建保存图表的目录
    chart_dir = os.path.join(strategy_dir, f'{strategy_module_name}图表')
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)

    # 保存图表
    chart_path = os.path.join(chart_dir, f'{stock_name}_均线图.png')
    plt.savefig(chart_path)
    plt.close()

def plot_assets_and_cumulative_returns(df, stock_name, strategy_dir,strategy_module_name):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 14), sharex=True)

    # 绘制收益情况
    ax1.plot(df.index, df['收益'], label='收益', color='blue')
    ax1.set_title(f'{stock_name} 收益')
    ax1.set_ylabel('收益')
    ax1.legend()
    ax1.grid(True)

    # 绘制累计收益情况
    ax2.plot(df.index, df['累计收益'], label='累计收益', color='green')
    ax2.set_title(f'{stock_name} 累计收益曲线')
    ax2.set_xlabel('交易日期')
    ax2.set_ylabel('累计收益')
    ax2.legend()
    ax2.grid(True)

    # 添加虚线的横竖线
    for date in df.index:
        ax1.axvline(date, linestyle='--', color='gray', alpha=0.3)
        ax2.axvline(date, linestyle='--', color='gray', alpha=0.3)

    # 在每个交易日线条的第一个端点显示黑点
    ax1.scatter(df.index, df['收益'], color='black', marker='.', s=50)
    ax2.scatter(df.index, df['累计收益'], color='black', marker='.', s=50)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    # 添加鼠标悬停显示具体日期和价格
    cursor(ax1, hover=True)
    cursor(ax2, hover=True)

    # 创建保存图表的目录
    chart_dir = os.path.join(strategy_dir, f'{strategy_module_name}图表')
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)

    # 保存图表
    chart_path = os.path.join(chart_dir, f'{stock_name}_收益图.png')
    plt.savefig(chart_path)
    plt.close()
