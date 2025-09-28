import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import akshare as ak

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def calculate_rsi(close, window=14):
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(close, short_window=12, long_window=26, signal_window=9):
    short_ema = close.ewm(span=short_window, adjust=False).mean()
    long_ema = close.ewm(span=long_window, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    return macd_line, signal_line, macd_line - signal_line


def calculate_support_resistance(df, window=50, multiplier=1.5):
    """
    计算支撑位和阻力位，并生成买卖信号

    参数:
    df: DataFrame，包含股票数据(开盘价、最高价、最低价、收盘价)
    window: 布林带窗口长度
    multiplier: 标准差倍数

    返回:
    df: 处理后的DataFrame，包含计算结果和信号
    """
    # 确保数据包含所需列
    required_columns = ['开盘', '最高', '最低', '收盘']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"数据缺少必要的列: {required_columns}")

    # 计算布林带
    df['middle_band'] = df['收盘'].rolling(window=window).mean()
    df['upper_band'] = df['middle_band'] + multiplier * df['收盘'].rolling(window=window).std()
    df['lower_band'] = df['middle_band'] - multiplier * df['收盘'].rolling(window=window).std()

    # 使用布林带确定支撑位和阻力位
    df['阻力'] = df['upper_band']
    df['支撑'] = df['lower_band']

    # 生成买卖信号
    df['buy_signal'] = (df['收盘'] < df['支撑']) & (df['收盘'].shift(1) >= df['支撑'].shift(1))
    df['sell_signal'] = (df['收盘'] > df['阻力']) & (df['收盘'].shift(1) <= df['阻力'].shift(1))

    # 增加最小信号间隔时间（例如 30 分钟）
    df['buy_signal'] = df['buy_signal'] & (df['buy_signal'].rolling('30T').sum() == 0)
    df['sell_signal'] = df['sell_signal'] & (df['sell_signal'].rolling('30T').sum() == 0)

    # 引入 RSI 和 MACD 过滤信号
    df['rsi'] = calculate_rsi(df['收盘'])
    macd_line, signal_line, _ = calculate_macd(df['收盘'])
    df['macd_uptrend'] = macd_line > signal_line

    df['buy_signal'] = df['buy_signal'] & (df['rsi'] < 30) & df['macd_uptrend']
    df['sell_signal'] = df['sell_signal'] & (df['rsi'] > 70) & ~df['macd_uptrend']

    return df



def plot_support_resistance(df, title='分时支撑位阻力位'):
    """
    绘制支撑位、阻力位和买卖信号

    参数:
    df: DataFrame，包含计算结果和信号
    title: 图表标题
    """
    plt.figure(figsize=(14, 7))

    # 绘制价格线
    plt.plot(df.index, df['收盘'], label='现价', color='white', linewidth=1, alpha=0.7)

    # 绘制布林带
    plt.plot(df.index, df['upper_band'], label='上轨', color='green', linestyle='--')
    plt.plot(df.index, df['lower_band'], label='下轨', color='green', linestyle='--')
    plt.plot(df.index, df['middle_band'], label='中轨', color='green', linestyle='-')

    # 绘制买卖信号
    buy_points = df[df['buy_signal']]
    sell_points = df[df['sell_signal']]

    plt.scatter(buy_points.index, buy_points['支撑'], marker='^', color='red', s=100, label='买入')
    plt.scatter(sell_points.index, sell_points['阻力'], marker='v', color='green', s=100, label='卖出')

    # 设置图表属性

    plt.title(title)
    plt.xlabel('时间')
    plt.ylabel('价格')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # 设置x轴日期格式
    if isinstance(df.index, pd.DatetimeIndex):
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gcf().autofmt_xdate()

    plt.tight_layout()
    return plt


# 使用示例
if __name__ == "__main__":
    import akshare as ak
    today = datetime.date.today().strftime('%Y%m%d')
    symbol = '600900'
    # data = ak.stock_zh_a_hist_min_em(symbol=symbol, period="1", start_date=today, end_date=today)
    data = ak.stock_zh_a_hist_min_em(symbol=symbol, period="1", start_date='20250924', end_date='20250924')
    print(data)

    # 重命名列以匹配函数需求
    data.rename(columns={
        '开盘': '开盘',
        '最高': '最高',
        '最低': '最低',
        '收盘': '收盘',
        'volume': 'volume'
    }, inplace=True)

    # 将时间列转换为datetime并设置为索引
    data['time'] = pd.to_datetime(data['时间'])
    data.set_index('time', inplace=True)

    # 计算支撑位和阻力位
    df = calculate_support_resistance(data)

    # 绘制图表
    plot = plot_support_resistance(df, f'{symbol}分时支撑阻力位')
    plot.show()
