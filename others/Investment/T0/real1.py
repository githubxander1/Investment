import pandas as pd
import numpy as np

from others.Investment.T0.monitor import logger


def indicator1(close, volume, high, low, window=240):
    """
    第一个指标函数：量价分析与支撑阻力计算

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
    window: 均价计算窗口 (默认240)

    返回：
    dict: 包含计算结果的字典
    """
    try:
        # 输入验证和类型转换
        close = pd.Series(close).fillna(method='ffill').astype(np.float32)
        volume = pd.Series(volume).fillna(0).astype(np.float32)
        high = pd.Series(high).fillna(method='ffill').astype(np.float32)
        low = pd.Series(low).fillna(method='ffill').astype(np.float32)

        # 量价计算 - 优化为向量化操作
        with np.errstate(divide='ignore', invalid='ignore'):
            vol_price = (volume.values / close.values) / 3

        # 条件累加 - 使用NumPy实现更快的条件运算
        up_mask = (vol_price > 0.2) & (close.values[1:] > close.values[:-1])
        down_mask = (vol_price > 0.2) & (close.values[1:] < close.values[:-1])

        # 处理边界情况
        A2 = np.zeros_like(close)
        A3 = np.zeros_like(close)

        if len(up_mask) > 0:
            A2[1:][up_mask] = vol_price[up_mask]
            A3[1:][down_mask] = vol_price[down_mask]

        A2 = np.cumsum(A2)
        A3 = np.cumsum(A3)
        A6 = A2 + A3

        # 计算比例 - 添加防除零
        non_zero = A6 != 0
        buy_ratio = np.zeros_like(A6)
        sell_ratio = np.zeros_like(A6)
        diff_ratio = np.zeros_like(A6)

        if np.any(non_zero):
            buy_ratio[non_zero] = (A2[non_zero] / A6[non_zero]) * 100
            sell_ratio[non_zero] = (A3[non_zero] / A6[non_zero]) * 100
            diff_ratio[non_zero] = ((A2[non_zero] - A3[non_zero]) / A6[non_zero]) * 100

        # 支撑阻力计算 - 优化为滚动窗口计算
        H1 = high.rolling(window=window, min_periods=1).max()
        L1 = low.rolling(window=window, min_periods=1).min()

        P1 = H1 - L1
        support = L1 + P1 * 1 / 8
        resistance = L1 + P1 * 7 / 8

        # 均价计算 - 使用预分配数组优化性能
        avg_price = np.zeros_like(close)
        cum_price_volume = 0
        cum_volume = 0

        for i in range(len(close)):
            cum_price_volume += close[i] * volume[i]
            cum_volume += volume[i]

            if i >= window:
                # 减去窗口外的数据
                cum_price_volume -= close[i - window] * volume[i - window]
                cum_volume -= volume[i - window]

            if cum_volume != 0:
                avg_price[i] = cum_price_volume / cum_volume

        # 买卖信号 - 向量化操作
        shifted_close = np.roll(close, 2)
        shifted_close[:2] = np.nan

        support_cross = (shifted_close < support) & (close > support)
        resistance_cross = (shifted_close > resistance) & (close < resistance)

        return {
            'buy_ratio': pd.Series(buy_ratio, index=close.index),
            'sell_ratio': pd.Series(sell_ratio, index=close.index),
            'diff_ratio': pd.Series(diff_ratio, index=close.index),
            'support': pd.Series(support, index=close.index),
            'resistance': pd.Series(resistance, index=close.index),
            'avg_price': pd.Series(avg_price, index=close.index),
            'buy_signal': pd.Series(support_cross, index=close.index),
            'sell_signal': pd.Series(resistance_cross, index=close.index)
        }

    except Exception as e:
        logger.error(f"indicator1计算错误: {e}")
        # 返回安全的默认值
        return {
            'buy_ratio': pd.Series([], dtype=np.float32),
            'sell_ratio': pd.Series([], dtype=np.float32),
            'diff_ratio': pd.Series([], dtype=np.float32),
            'support': pd.Series([], dtype=np.float32),
            'resistance': pd.Series([], dtype=np.float32),
            'avg_price': pd.Series([], dtype=np.float32),
            'buy_signal': pd.Series([], dtype=bool),
            'sell_signal': pd.Series([], dtype=bool)
        }
