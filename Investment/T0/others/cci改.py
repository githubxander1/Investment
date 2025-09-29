import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def cci_modified_signal(df: pd.DataFrame, n=34, m=13):
    """
    将通达信指标 'cci改' 转换为 Python 函数。

    参数:
        df (pd.DataFrame): 包含列 ['open', 'high', 'low', 'close']
        n (int): LLV/HHV 的周期长度，默认 34
        m (int): EMA 周期长度，默认 13

    返回:
        pd.DataFrame: 原始数据 + 指标计算结果 + 信号列
    """
    # VAR1 := (2*C + H + L)/4
    df['VAR1'] = (2 * df['close'] + df['high'] + df['low']) / 4

    # VAR2 := LLV(LOW, N)
    df['VAR2'] = df['low'].rolling(window=n).min()

    # VAR3 := HHV(HIGH, N)
    df['VAR3'] = df['high'].rolling(window=n).max()

    # AA := EMA((VAR1 - VAR2) / (VAR3 - VAR2) * 100, M)
    df['AA'] = ((df['VAR1'] - df['VAR2']) / (df['VAR3'] - df['VAR2']) * 100).ewm(span=m, adjust=False).mean()

    # BB := EMA(0.667*REF(AA,1)+0.333*AA, 2)
    df['BB'] = (0.667 * df['AA'].shift(1) + 0.333 * df['AA']).ewm(span=2, adjust=False).mean()

    # 黄柱：CROSS(AA,22) AND BB < AA
    df['黄柱'] = (df['AA'].shift(1) <= 22) & (df['AA'] > 22) & (df['BB'] < df['AA'])

    # XG：CROSS(AA,BB) AND AA < 20
    df['XG'] = (df['AA'].shift(1) <= df['BB'].shift(1)) & (df['AA'] > df['BB']) & (df['AA'] < 20)

    # 速顶：FILTER(CROSS(BB,AA) AND AA > 80.3, 3)
    cross_bb_aa = (df['BB'].shift(1) <= df['AA'].shift(1)) & (df['BB'] > df['AA'])
    df['速顶'] = cross_bb_aa & (df['AA'] > 80.3)
    df['速顶'] = df['速顶'].rolling(window=3).apply(lambda x: not x[:-1].any() and x[-1], raw=True)

    return df[['open', 'high', 'low', 'close', 'AA', 'BB', '黄柱', 'XG', '速顶']]

def plot_cci_signals(df):
    """
    可视化 CCI 改进策略的指标与交易信号。
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    # 绘制 AA 和 BB 曲线
    ax.plot(df.index, df['AA'], label='AA', color='blue')
    ax.plot(df.index, df['BB'], label='BB', color='orange')

    # 标记黄柱（底部参与）
    yellow_signals = df[df['黄柱']]
    ax.scatter(yellow_signals.index, yellow_signals['AA'], marker='^', color='gold', s=100, label='底部参与 (黄柱)')

    # 标记 XG（买入）
    buy_signals = df[df['XG']]
    ax.scatter(buy_signals.index, buy_signals['AA'], marker='o', color='green', s=100, label='XG 买入')

    # 标记速顶（卖出）
        # 修改速顶计算逻辑
    cross_bb_aa = (df['BB'].shift(1) <= df['AA'].shift(1)) & (df['BB'] > df['AA'])
    df['速顶'] = cross_bb_aa & (df['AA'] > 80.3)

    # 使用 rolling().sum() 来实现类似 FILTER 的功能
    # 即最近 3 根 K 线中是否有且仅有当前一根满足条件
    df['速顶'] = df['速顶'].rolling(window=3, min_periods=1).apply(
        lambda x: (x.iloc[-1] == True) & (x.iloc[:-1].sum() == 0),
    ).astype(bool)
    print(df[['AA', 'BB', '速顶']].tail(10))


    # 设置阈值线
    ax.axhline(20, color='gray', linestyle='--', linewidth=0.8)
    ax.axhline(80, color='gray', linestyle='--', linewidth=0.8)

    # 图表美化
    ax.set_title('CCI 改进指标与交易信号')
    ax.set_xlabel('时间')
    ax.set_ylabel('指标值')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # 示例获取某股票的日线行情
    import akshare as ak

    def get_stock_data(stock_code="000001", period="daily"):
        df = ak.stock_zh_a_hist(symbol=stock_code, period=period, adjust="")
        df.rename(columns={
            "开盘": "open",
            "最高": "high",
            "最低": "low",
            "收盘": "close"
        }, inplace=True)
        return df[['open', 'high', 'low', 'close']]

    df = get_stock_data("000001")
    df = cci_modified_signal(df)

    # 打印最新信号
    latest = df.iloc[-1]
    print("当前信号:")
    if latest['黄柱']:
        print("🔔 发现【底部参与】信号！")
    if latest['XG']:
        print("🔔 发现【XG买入】信号！")
    if latest['速顶']:
        print("🔔 发现【速顶卖出】信号！")

    # 新增：绘制图表
    plot_cci_signals(df)
    # plt.savefig('cci_signals.png')
