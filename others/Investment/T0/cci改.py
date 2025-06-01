import pandas as pd
import numpy as np

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
