import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import Formatter


# ---------------------- 1. 获取股票日线数据 ----------------------
def get_stock_data(stock_code, start_date, end_date):
    """
    获取股票日线数据（成交量、close价等）
    :param stock_code: 股票代码（如 "600900"）
    :param start_date: 起始日期（如 "2024-01-01"）
    :param end_date: 结束日期（如 "2025-06-05"）
    :return: 日线数据（索引为日期）
    """
    # df = ak.stock_zh_a_hist(
    #     symbol=stock_code,
    #     period="daily",
    #     start_date=start_date,
    #     end_date=end_date,
    #     adjust=""  # 未复权数据（与通达信默认一致）
    # )
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
    M:=10;（实际未使用，忽略）
    A:=VOL*C;                  → 成交额
    B:=SUM(A,1)/SUM(VOL,1);    → 均价（周期1简化为 A/VOL）
    B1:=EMA(B,17);             → B的17周期EMA
    资金:=(B-B1)*100/B;        → 资金偏离度
    DIFF:EMA(资金,12)-EMA(资金,26); → 资金的MACD快线
    DEA:EMA(DIFF,9);           → MACD慢线
    MAC:2*(DIFF-DEA);          → MACD柱状线
    STICKLINE条件: MAC>=REF(MAC,1) AND MAC>0（修复原公式可能的笔误，O→0）
    """
    # 基础变量计算
    df['A'] = df['VOL'] * df['CLOSE']  # 成交额 = 成交量 * 收盘价
    df['B'] = df['A'] / df['VOL']  # 均价 = 成交额 / 成交量（处理周期1的简化）

    # 处理除零错误（理论上VOL不会为0，保险措施）
    df['B'] = np.where(df['VOL'] == 0, 0, df['B'])

    # EMA计算（通达信默认递归模式，对应 adjust=False）
    df['B1'] = df['B'].ewm(span=17, adjust=False).mean()  # B1: EMA(B,17)
    df['资金'] = np.where(df['B'] == 0, 0, (df['B'] - df['B1']) * 100 / df['B'])  # 资金偏离度

    # MACD类指标计算
    ema12 = df['资金'].ewm(span=12, adjust=False).mean()  # DIFF的基础：EMA(资金,12)
    ema26 = df['资金'].ewm(span=26, adjust=False).mean()  # DIFF的基础：EMA(资金,26)
    df['DIFF'] = ema12 - ema26  # DIFF线
    df['DEA'] = df['DIFF'].ewm(span=9, adjust=False).mean()  # DEA线
    df['MAC'] = 2 * (df['DIFF'] - df['DEA'])  # MAC柱状线

    # STICKLINE条件（修复原公式可能的笔误：O→0，区分柱状线正负）
    df['MAC_cond'] = (df['MAC'] >= df['MAC'].shift(1)) & (df['MAC'] > 0)

    return df


# ---------------------- 3. 可视化指标（复现通达信风格） ----------------------
class DateFormatter(Formatter):
    """自定义时间轴格式化，适配Matplotlib"""

    def __init__(self, dates):
        self.dates = dates

    def __call__(self, x, pos=None):
        if x < 0 or x >= len(self.dates):
            return ''
        return self.dates[int(x)].strftime('%Y-%m-%d')


def plot_indicator(df):
    """
    绘制指标图：
    - 上半部分：DIFF、DEA曲线 + MAC柱状线（区分颜色）
    - 下半部分：资金指标曲线
    """
    fig, (ax_macd, ax_fund) = plt.subplots(
        2, 1, figsize=(12, 8),
        gridspec_kw={'height_ratios': [3, 1]}
    )

    # ------------------- 绘制 DIFF & DEA 曲线 -------------------
    ax_macd.plot(df.index, df['DIFF'], label='DIFF', color='yellow', linewidth=1.5)
    ax_macd.plot(df.index, df['DEA'], label='DEA', color='lightgray', linewidth=1.5)
    ax_macd.set_ylabel('DIFF / DEA', fontsize=12)
    ax_macd.legend(loc='upper left')
    ax_macd.grid(alpha=0.3, linestyle='--')

    # ------------------- 绘制 MAC 柱状线（区分条件） -------------------
    # 1. 满足条件：MAC>=REF(MAC,1) 且 MAC>0（蓝色高亮）
    cond_mask = df['MAC_cond'] & (df['MAC'] > 0)
    ax_macd.bar(
        df[cond_mask].index, df[cond_mask]['MAC'],
        color='#0000AA', width=0.8, alpha=0.8,
        label='MAC 上升'
    )
    # 2. 仅 MAC>0 但不满足条件（青色填充）
    pos_mask = (df['MAC'] > 0) & ~cond_mask
    ax_macd.bar(
        df[pos_mask].index, df[pos_mask]['MAC'],
        color='cyan', width=0.8, alpha=0.5
    )
    # 3. MAC<=0（红色填充）
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
    plt.show()


# ---------------------- 4. 主程序运行（示例） ----------------------
if __name__ == "__main__":
    # 配置参数
    # stock_code = "sh600900"  # 长江电力（示例）
    stock_code = "sh601728"  # 长江电力（示例）
    start_date = "20250117"  # 起始日期
    end_date = "20250605"  # 结束日期

    # 1. 获取日线数据
    df = get_stock_data(stock_code, start_date, end_date)

    # 2. 计算指标
    df = calculate_indicator(df)

    # 3. 可视化
    plot_indicator(df)