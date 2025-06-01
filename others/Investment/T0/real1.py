import pandas as pd
import numpy as np


def indicator1(close, volume, high, low, window=240):
    """
    第一个指标函数：量价分析与支撑阻力计算

    参数：
    close: 收盘价序列 (pd.Series)
    volume: 成交量序列 (pd.Series)
    high: 最高价序列 (pd.Series)
    low: 最低价序列 (pd.Series)
    window: 均价计算窗口 (默认240)

    返回：
    dict: 包含计算结果的字典
    """
    # 量价计算
    vol_price = (volume / close) / 3

    # 条件累加
    A2 = np.cumsum(np.where((vol_price > 0.20) & (close > close.shift(1)), vol_price, 0))
    A3 = np.cumsum(np.where((vol_price > 0.20) & (close < close.shift(1)), vol_price, 0))
    A6 = A2 + A3

    # 比例计算
    buy_ratio = (A2 / A6) * 100 if A6 != 0 else 0
    sell_ratio = (A3 / A6) * 100 if A6 != 0 else 0
    diff_ratio = ((A2 - A3) / A6) * 100 if A6 != 0 else 0

    # 支撑阻力计算
    H1 = high.max()
    L1 = low.min()
    P1 = H1 - L1
    support = L1 + P1 * 1 / 8
    resistance = L1 + P1 * 7 / 8

    # 均价计算
    avg_price = (close * volume).rolling(window).sum() / volume.rolling(window).sum()

    # 买卖信号（LONGCROSS转换为连续两天交叉）
    support_cross = (close.shift(2) < support) & (close.shift(1) > support)
    resistance_cross = (close.shift(2) > resistance) & (close.shift(1) < resistance)

    return {
        'buy_ratio': buy_ratio,
        'sell_ratio': sell_ratio,
        'diff_ratio': diff_ratio,
        'support': support,
        'resistance': resistance,
        'avg_price': avg_price,
        'buy_signal': support_cross,
        'sell_signal': resistance_cross
    }