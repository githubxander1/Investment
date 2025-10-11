import pandas as pd
import numpy as np

def trend_buy_sell_signals(df: pd.DataFrame, window=55):
    """
    将通达信的趋势买卖信号公式转为 Python 函数。

    参数:
        df (pd.DataFrame): 包含 ['open', 'high', 'low', 'close']
        window (int): LLV/HHV 的周期长度，默认 55

    返回:
        pd.DataFrame: 所有中间指标 + 最终信号字段
    """

    # A1 = MAX(DYNAINFO(3), DYNAINFO(5)) => 最新价与最高价取最大
    df['A1'] = df[['high', 'close']].max(axis=1)

    # B1 = MIN(DYNAINFO(3), DYNAINFO(6)) => 最新价与最低价取最小
    df['B1'] = df[['low', 'close']].min(axis=1)

    # C1 = A1 - B1
    df['C1'] = df['A1'] - df['B1']

    # 阻力 = B1 + C1 * 7/8
    df['阻力'] = df['B1'] + df['C1'] * 7 / 8

    # 支撑 = B1 + C1 * 0.5/8
    df['支撑'] = df['B1'] + df['C1'] * 0.5 / 8

    # 中线 = (支撑 + 阻力) / 2
    df['中线'] = (df['支撑'] + df['阻力']) / 2

    # V11 := 3*SMA((C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100,5,1) - 2*SMA(SMA(...),3,1)
    llv = df['low'].rolling(window=window).min()
    hhv = df['high'].rolling(window=window).max()
    rsv = (df['close'] - llv) / (hhv - llv) * 100
    sma_rsv_5 = rsv.rolling(window=5).mean()
    v11 = 3 * sma_rsv_5 - 2 * sma_rsv_5.rolling(window=3).mean()

    df['V11'] = v11

    # 趋势 := EMA(V11,3)
    df['趋势'] = df['V11'].ewm(span=3, adjust=False).mean()

    # V12 := (趋势 - REF(趋势,1))/REF(趋势,1)*100
    df['V12'] = (df['趋势'] - df['趋势'].shift(1)) / df['趋势'].shift(1) * 100

    # BBx 系列：底部买入信号
    df['BB1'] = (df['趋势'].shift(1) < 11) & (df['趋势'].shift(1) > 6) & (df['趋势'] > 11) & (df['close'] < df['中线'])
    df['BB2'] = (df['趋势'].shift(1) < 6) & (df['趋势'].shift(1) > 3) & (df['趋势'] > 6) & (df['close'] < df['中线'])
    df['BB3'] = (df['趋势'].shift(1) < 3) & (df['趋势'].shift(1) > 1) & (df['趋势'] > 3) & (df['close'] < df['中线'])
    df['BB4'] = (df['趋势'].shift(1) < 1) & (df['趋势'].shift(1) > 0) & (df['趋势'] > 1) & (df['close'] < df['中线'])
    df['BB5'] = (df['趋势'].shift(1) < 0) & (df['趋势'] > 0) & (df['close'] < df['中线'])

    df['BB'] = df[['BB1', 'BB2', 'BB3', 'BB4', 'BB5']].any(axis=1)

    # 准备买入条件
    df['准备买入'] = df['趋势'] < 11

    # AA := (趋势<11) AND FILTER((趋势<=11),15) AND C<中线
    df['AA'] = (df['趋势'] < 11) & (df['趋势'] <= 11).rolling(window=15).apply(lambda x: x.any(), raw=True) & (
                df['close'] < df['中线'])

    # 抄底信号
    df['抄底'] = df['AA'] | df['BB']

    # DDx 系列：顶部卖出信号
    df['DD1'] = (df['趋势'].shift(1) > 89) & (df['趋势'].shift(1) < 94) & (df['趋势'] < 89) & (df['close'] > df['中线'])
    df['DD2'] = (df['趋势'].shift(1) > 94) & (df['趋势'].shift(1) < 97) & (df['趋势'] < 94) & (df['close'] > df['中线'])
    df['DD3'] = (df['趋势'].shift(1) > 97) & (df['趋势'].shift(1) > 99) & (df['趋势'] < 97) & (df['close'] > df['中线'])
    df['DD4'] = (df['趋势'].shift(1) > 99) & (df['趋势'].shift(1) < 100) & (df['趋势'] < 99) & (df['close'] > df['中线'])
    df['DD5'] = (df['趋势'].shift(1) > 100) & (df['趋势'] < 100) & (df['close'] > df['中线'])

    df['DD'] = df[['DD1', 'DD2', 'DD3', 'DD4', 'DD5']].any(axis=1)

    # 超买见顶信号
    df['超买见顶'] = (df['趋势'] > 89) & (df['趋势'].rolling(window=15).apply(lambda x: x.any(), raw=True)) & (
                df['close'] > df['中线'])

    # 合并所有信号
    return df[['open', 'high', 'low', 'close', '趋势', '支撑', '阻力', '中线', '抄底', '超买见顶', 'BB', 'DD']]
