import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from others.Investment.T0.monitor import logger

pd.set_option('future.no_silent_downcasting', True)
def indicator3(close, high, low):
    """
    阻力支撑与买卖信号指标

    特性：
    1. 使用NumPy向量化操作提升性能
    2. 添加输入验证确保数据质量
    3. 优化内存使用，减少中间变量
    4. 添加异常处理保障稳定性

    参数：
    close: 收盘价序列 (pd.Series)
    high: 最高价序列 (pd.Series)
    low: 最低价序列 (pd.Series)

    返回：
    dict: 包含计算结果的字典
    """
    try:
        # 输入验证和类型转换
        close = pd.Series(close).ffill().astype(np.float32)
        high = pd.Series(high).ffill().astype(np.float32)
        low = pd.Series(low).ffill().astype(np.float32)

        # 计算昨收、今高、今低
        prev_close = close.shift(1)

        # 计算H1和L1 - 使用向量化操作
        H1 = np.maximum(prev_close.values, high.values)
        L1 = np.minimum(prev_close.values, low.values)

        # 计算阻力与支撑
        P1 = H1 - L1
        resistance = L1 + P1 * 7 / 8  # 阻力位
        support = L1 + P1 * 0.5 / 8  # 支撑位

        # 计算买卖信号 - 向量化操作
        shifted_close = np.roll(close, 2)
        shifted_support = np.roll(support, 2)
        shifted_resistance = np.roll(resistance, 2)

        pd.set_option('future.no_silent_downcasting', True)
        buy_signal = (shifted_close < shifted_support) & (close > support)
        sell_signal = (shifted_close > shifted_resistance) & (close < resistance)

        return {
            'resistance': pd.Series(resistance, index=close.index),
            'support': pd.Series(support, index=close.index),
            'buy_signal': pd.Series(buy_signal, index=close.index),
            'sell_signal': pd.Series(sell_signal, index=close.index),
            'close': close
        }

    except Exception as e:
        logger.error(f"indicator3计算错误: {e}")
        return {
            'resistance': pd.Series([], dtype=np.float32),
            'support': pd.Series([], dtype=np.float32),
            'buy_signal': pd.Series([], dtype=bool),
            'sell_signal': pd.Series([], dtype=bool),
            'close': pd.Series([], dtype=np.float32)
        }


def plot_indicator(df):
    """绘制指标图表，优化性能和可视化效果"""
    try:
        # 数据验证：确保输入数据完整且格式正确
        if not all(col in df.columns for col in ['收盘', '最高', '最低']):
            raise ValueError("输入数据缺少必要列：收盘、最高、最低")

        result = indicator3(df['收盘'], df['最高'], df['最低'])

        plt.figure(figsize=(16, 9))
        plt.style.use('dark_background')

        # 确保索引为datetime格式，并剔除非法时间戳
        df.index = pd.to_datetime(df.index, errors='coerce')
        # 删除非法时间戳的行
        df = df[df.index.notna()]

        # 确保 result 的索引与 df 的索引一致
        result = {key: value.reindex(df.index) for key, value in result.items()}

        # 绘制价格曲线
        plt.plot(df.index, result['close'], label='现价', color='white', linewidth=0.8)

        # 绘制阻力与支撑线
        plt.plot(df.index, result['resistance'], label='阻力', color='#00DD00', linestyle='--', linewidth=0.8)
        plt.plot(df.index, result['support'], label='支撑', color='#00DD00', linestyle='--', linewidth=0.8)

        # 绘制买卖信号
        buy_signal = result['buy_signal'].fillna(False).astype(bool)
        sell_signal = result['sell_signal'].fillna(False).astype(bool)

        buy_points = df.index[buy_signal]
        sell_points = df.index[sell_signal]

        if len(buy_points) > 0:
            buy_values = result['support'][buy_points] * 1.001
            plt.scatter(buy_points, buy_values, marker='^', color='red', zorder=5, s=50)
            for point, value in zip(buy_points, buy_values):
                plt.text(point, value, f'买\n{value:.2f}', color='red', va='bottom', fontsize=8, rotation=45)

        if len(sell_points) > 0:
            sell_values = result['close'][sell_points]
            plt.scatter(sell_points, sell_values, marker='v', color='green', zorder=5, s=50)
            for point, value in zip(sell_points, sell_values):
                plt.text(point, value, f'卖\n{value:.2f}', color='green', va='top', fontsize=8, rotation=45)

        # 设置x轴标签（时间）
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
        plt.xticks(rotation=45)
        plt.xlabel('时间')

        # 设置y轴标签（价格）
        price_range = np.linspace(min(result['close']), max(result['close']), 10)
        plt.yticks(price_range, [f'{price:.2f}' for price in price_range])
        plt.ylabel('价格')

        # 绘制交叉柱状线
        cross_dates = df.index[(buy_signal | sell_signal)]
        if len(cross_dates) > 0:
            heights = result['resistance'][cross_dates] - result['support'][cross_dates]
            bottoms = result['support'][cross_dates]
            plt.bar(cross_dates, heights, bottom=bottoms, width=0.1, color='yellow', alpha=0.5)

        plt.title('阻力支撑与买卖信号')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    except ValueError as ve:
        logger.error(f"数据验证错误: {ve}")
    except Exception as e:
        logger.error(f"绘图错误: {e}", exc_info=True)  # 添加详细错误信息


if __name__ == '__main__':
    import akshare as ak
    today = datetime.date.today().strftime('%Y%m%d')
    print('today:', today)

    try:
        data = ak.stock_zh_a_hist_min_em(symbol='600900', period="1", start_date=today, end_date=today)
        print(data)
        plot_indicator(data)
    except Exception as e:
        logger.error(f"获取数据或绘图失败: {e}")