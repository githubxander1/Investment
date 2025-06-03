import numpy as np
import pandas as pd

from others.Investment.T0.monitor import logger


def indicator2(close, volume, high, low, date, window=480):
    """
    第二个指标函数：多周期分析与资金流向计算

    特性：
    1. 使用NumPy向量化操作提升性能
    2. 添加输入验证确保数据质量
    3. 优化内存使用，减少中间变量
    4. 添加异常处理保障稳定性

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
    try:
        # 输入验证和类型转换
        close = pd.Series(close).fillna(method='ffill').astype(np.float32)
        volume = pd.Series(volume).fillna(0).astype(np.float32)
        high = pd.Series(high).fillna(method='ffill').astype(np.float32)
        low = pd.Series(low).fillna(method='ffill').astype(np.float32)

        if date is None or len(date) != len(close):
            date = pd.date_range(end=datetime.today(), periods=len(close), freq='D')
        else:
            date = pd.Series(date).fillna(method='ffill')

        # 480日最高价 - 使用滚动窗口优化
        XG = high.rolling(window=window, min_periods=1).max()

        # 计算当月第几天 - 使用向量化操作
        rq = date.dt.day

        # 移动平均线（按自然月周期）- 优化计算
        month_change = rq != rq.shift()
        jy = month_change.groupby(month_change.cumsum()).cumcount() + 1

        MA1 = close.shift(jy)
        MA2 = MA1.shift(jy)
        MA3 = MA2.shift(jy)

        # 阻力与支撑（基于动态高低点）- 使用EWM优化
        H1 = high.ewm(com=0.1, min_periods=1).mean()
        L1 = low.ewm(com=0.1, min_periods=1).mean()

        P1 = H1 - L1
        resistance = L1 + P1 * 8 / 9
        support = L1 + P1 * 0.5 / 9

        # MACD计算 - 使用向量化操作
        DIF = close.ewm(span=12, min_periods=12).mean() - close.ewm(span=26, min_periods=26).mean()
        DEA = DIF.ewm(span=9, min_periods=9).mean()
        MACD = (DIF - DEA) * 10

        # 量价比与资金流向 - 使用向量化操作
        with np.errstate(divide='ignore', invalid='ignore'):
            A1 = (volume.values / close.values) / 3

        up_mask1 = (A1 > 40) & (close.values[1:] > close.values[:-1])
        down_mask1 = (A1 > 40) & (close.values[1:] < close.values[:-1])
        up_mask2 = (A1 < 40) & (close.values[1:] > close.values[:-1])
        down_mask2 = (A1 < 40) & (close.values[1:] < close.values[:-1])

        # 处理边界情况
        A2 = np.zeros_like(close)
        A3 = np.zeros_like(close)
        A4 = np.zeros_like(close)
        A5 = np.zeros_like(close)

        if len(up_mask1) > 0:
            A2[1:][up_mask1] = A1[up_mask1]
            A3[1:][down_mask1] = A1[down_mask1]
            A4[1:][up_mask2] = A1[up_mask2]
            A5[1:][down_mask2] = A1[down_mask2]

        A2 = np.cumsum(A2)
        A3 = np.cumsum(A3)
        A4 = np.cumsum(A4)
        A5 = np.cumsum(A5)
        A6 = A2 + A3 + A4 + A5

        # 买卖信号 - 向量化操作
        shifted_close = np.roll(close, 1)
        shifted_close[0] = np.nan

        buy_signal = (close.values > support.values) & (shifted_close < support.values)
        sell_signal = (close.values < resistance.values) & (shifted_close > resistance.values)

        return {
            'XG': pd.Series(XG, index=close.index),
            'MA1': pd.Series(MA1, index=close.index),
            'resistance': pd.Series(resistance, index=close.index),
            'support': pd.Series(support, index=close.index),
            'MACD': pd.Series(MACD, index=close.index),
            'institutional_buy': pd.Series(A2, index=close.index),
            'institutional_sell': pd.Series(A3, index=close.index),
            'retail_buy': pd.Series(A4, index=close.index),
            'retail_sell': pd.Series(A5, index=close.index),
            'buy_signal': pd.Series(buy_signal, index=close.index),
            'sell_signal': pd.Series(sell_signal, index=close.index)
        }

    except Exception as e:
        logger.error(f"indicator2计算错误: {e}")
        # 返回安全的默认值
        return {
            'XG': pd.Series([], dtype=np.float32),
            'MA1': pd.Series([], dtype=np.float32),
            'resistance': pd.Series([], dtype=np.float32),
            'support': pd.Series([], dtype=np.float32),
            'MACD': pd.Series([], dtype=np.float32),
            'institutional_buy': pd.Series([], dtype=np.float32),
            'institutional_sell': pd.Series([], dtype=np.float32),
            'retail_buy': pd.Series([], dtype=np.float32),
            'retail_sell': pd.Series([], dtype=np.float32),
            'buy_signal': pd.Series([], dtype=bool),
            'sell_signal': pd.Series([], dtype=bool)
        }
