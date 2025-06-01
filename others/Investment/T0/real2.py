import numpy as np
import pandas as pd


def indicator2(close, volume, high, low, date, window=480):
    """
    第二个指标函数：多周期分析与资金流向计算

    参数：
    close: 收盘价序列 (pd.Series)
    volume: 成交量序列 (pd.Series)
    high: 最高价序列 (pd.Series)
    low: 最低价序列 (pd.Series)
    date: 日期序列 (pd.Series, 格式为datetime)
    window: 长期高点窗口 (默认480)

    返回：
    dict: 包含计算结果的字典
    """
    # 480日最高价
    XG = high.rolling(window).max()

    # 计算当月第几天
    rq = date.dt.day

    # 移动平均线（按自然月周期）
    month_change = rq != rq.shift()
    jy = month_change.groupby(month_change.cumsum()).cumcount() + 1
    MA1 = close.shift(jy)
    MA2 = MA1.shift(jy)
    MA3 = MA2.shift(jy)

    # 阻力与支撑（基于动态高低点）
    H1 = high.ewm(com=0.1).mean()
    L1 = low.ewm(com=0.1).mean()
    P1 = H1 - L1
    resistance = L1 + P1 * 8 / 9
    support = L1 + P1 * 0.5 / 9

    # MACD计算
    DIF = pd.ewma(close, 12) - pd.ewma(close, 26)
    DEA = pd.ewma(DIF, 9)
    MACD = (DIF - DEA) * 10

    # 量价比与资金流向
    A1 = (volume / close) / 3
    A2 = np.cumsum(np.where((A1 > 40) & (close > close.shift(1)), A1, 0))
    A3 = np.cumsum(np.where((A1 > 40) & (close < close.shift(1)), A1, 0))
    A4 = np.cumsum(np.where((A1 < 40) & (close > close.shift(1)), A1, 0))
    A5 = np.cumsum(np.where((A1 < 40) & (close < close.shift(1)), A1, 0))
    A6 = A2 + A3 + A4 + A5

    # 买卖信号
    buy_signal = (close > support) & (close.shift(1) < support.shift(1))
    sell_signal = (close < resistance) & (close.shift(1) > resistance.shift(1))

    return {
        'XG': XG,
        'MA1': MA1,
        'resistance': resistance,
        'support': support,
        'MACD': MACD,
        'institutional_buy': A2,
        'institutional_sell': A3,
        'retail_buy': A4,
        'retail_sell': A5,
        'buy_signal': buy_signal,
        'sell_signal': sell_signal
    }