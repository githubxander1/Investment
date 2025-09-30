import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import Formatter
#添加中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------------------- 1. 获取日线数据 ----------------------
def get_stock_data(stock_code, start_date, end_date):
    """
    获取股票日线数据（成交量、close价等）
    :param stock_code: 股票代码（如 "600900"）
    :param start_date: 起始日期（如 "2024-01-01"）
    :param end_date: 结束日期（如 "2025-06-05"）
    :return: 日线数据（索引为日期）
    """
    df = ak.stock_zh_a_hist_tx(symbol=stock_code, start_date=start_date, end_date=end_date, adjust='qfq')
    print(df)
    # 处理时间索引 & 列名适配
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.rename(columns={
        'close': 'CLOSE',
        'amount': 'VOL'
    }, inplace=True)
    return df


# ---------------------- 2. 计算通达信指标（严格还原公式） ----------------------
def calculate_indicator(df):
    """
    还原通达信指标逻辑：

    指标公式简要说明：
    A := VOL * CLOSE         -> 成交额 = 成交量 × 收盘价
    B := A / VOL            -> 均价 = 成交额 ÷ 成交量（周期为1）
    B1 := EMA(B, 17)        -> 对均价B计算17周期EMA
    资金 := (B - B1) * 100 / B   -> 资金偏离度，反映价格与均价的偏离程度
    DIFF := EMA(资金,12) - EMA(资金,26)   -> 快速EMA减去慢速EMA
    DEA := EMA(DIFF,9)      -> DIFF的9周期EMA
    MAC := 2*(DIFF-DEA)     -> MACD柱状图
    STICKLINE条件：MAC >= REF(MAC,1) AND MAC > 0 → 绘制彩色柱状线

    参数：
    df: 包含CLOSE和VOL字段的DataFrame对象，索引为日期时间格式

    返回值：
    df: 添加了以下列的DataFrame：
        - A: 成交额
        - B: 均价
        - B1: B的17周期EMA
        - 资金: 资金偏离度
        - DIFF: MACD快线
        - DEA: MACD慢线
        - MAC: MACD柱状图数据
        - MAC_cond: 用于绘制MAC柱状图的条件掩码
    """



# ---------------------- 3. 可视化指标（复现通达信风格） ----------------------
class DateFormatter(Formatter):
    """自定义时间轴格式化，适配Matplotlib"""

    def __init__(self, dates):
        self.dates = dates

    def __call__(self, x, pos=None):
        if x < 0 or x >= len(self.dates):
            return ''
        return self.dates[int(x)].strftime('%Y-%m-%d')


import mplcursors

def plot_indicator(df):
    """
    绘制指标图：
    - 上半部分：DIFF、DEA曲线 + MAC柱状线（区分颜色）
    - 下半部分：资金指标曲线
    """
    fig, (ax_close, ax_macd, ax_fund) = plt.subplots(
        3, 1, figsize=(12, 8), sharex=True,
        gridspec_kw={'height_ratios': [3, 1, 2]}
    )

    # ------------------- 绘制价格线 -------------------
    ax_close.plot(df.index, df['CLOSE'], label='CLOSE', color='blue', linewidth=1.2)
    ax_close.set_ylabel('价格', fontsize=12)
    ax_close.legend(loc='upper left')
    ax_close.grid(alpha=0.3, linestyle='--')

    # ------------------- 绘制 DIFF & DEA 曲线 -------------------
    ax_macd.plot(df.index, df['DIFF'], label='DIFF', color='yellow', linewidth=1.5)
    ax_macd.plot(df.index, df['DEA'], label='DEA', color='lightgray', linewidth=1.5)
    ax_macd.set_ylabel('DIFF / DEA', fontsize=12)
    ax_macd.legend(loc='upper left')
    ax_macd.grid(alpha=0.3, linestyle='--')

    # ------------------- 绘制 MAC 柱状线（区分条件） -------------------
    cond_mask = df['MAC_cond'] & (df['MAC'] > 0)
    ax_macd.bar(
        df[cond_mask].index, df[cond_mask]['MAC'],
        color='#0000AA', width=0.8, alpha=0.8,
        label='MAC 上升'
    )
    pos_mask = (df['MAC'] > 0) & ~cond_mask
    ax_macd.bar(
        df[pos_mask].index, df[pos_mask]['MAC'],
        color='cyan', width=0.8, alpha=0.5
    )
    neg_mask = df['MAC'] <= 0
    ax_macd.bar(
        df[neg_mask].index, df[neg_mask]['MAC'],
        color='red', width=0.8, alpha=0.5
    )

    # ------------------- 绘制 资金指标 曲线 -------------------
    ax_fund.plot(df.index, df['资金'], label='资金偏离度', color='green', linewidth=1.2)
    ax_fund.set_ylabel('资金指标', fontsize=12)
    ax_fund.legend(loc='upper left')
    ax_fund.grid(alpha=0.3, linestyle='--')

    # ------------------- 时间轴格式化（适配股票date） -------------------
    dates = df.index.tolist()
    ax_macd.xaxis.set_major_formatter(DateFormatter(dates))
    ax_fund.xaxis.set_major_formatter(DateFormatter(dates))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # ------------------- 添加鼠标悬停注释 -------------------
    def show_annotation(sel):
        x, y = sel.target
        date_str = df.index[int(x)].strftime('%Y-%m-%d')
        sel.annotation.set_text(f'Date: {date_str}\nValue: {y:.2f}')

    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", show_annotation)

    plt.show()



# ---------------------- 4. 主程序运行（示例） ----------------------
if __name__ == "__main__":
    # 配置参数
    # stock_code = "sh600900"  # 长江电力（示例）
    stock_code = "sh601728"  # 工商银行
    start_date = "20250117"  # 起始日期
    end_date = "20250605"  # 结束日期

    # 1. 获取日线数据
    df = get_stock_data(stock_code, start_date, end_date)

    # 2. 计算指标
    df = calculate_indicator(df)

    # 3. 可视化
    plot_indicator(df)