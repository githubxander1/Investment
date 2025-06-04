import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import akshare as ak


def calculate_support_resistance(df):
    """
    计算支撑位和阻力位，并生成买卖信号

    参数:
    df: DataFrame，包含股票数据(开盘价、最高价、最低价、收盘价)

    返回:
    df: 处理后的DataFrame，包含计算结果和信号
    """
    # 确保数据包含所需列
    required_columns = ['开盘', '最高', '最低', '收盘']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"数据缺少必要的列: {required_columns}")

    # 计算布林带
    window = 20
    multiplier = 2
    df['middle_band'] = df['收盘'].rolling(window=window).mean()
    df['upper_band'] = df['middle_band'] + multiplier * df['收盘'].rolling(window=window).std()
    df['lower_band'] = df['middle_band'] - multiplier * df['收盘'].rolling(window=window).std()

    # 使用布林带确定支撑位和阻力位
    df['阻力'] = df['upper_band']
    df['支撑'] = df['lower_band']

    # 生成买卖信号
    df['buy_signal'] = (df['收盘'] < df['支撑']) & (df['收盘'].shift(1) >= df['支撑'].shift(1))
    df['sell_signal'] = (df['收盘'] > df['阻力']) & (df['收盘'].shift(1) <= df['阻力'].shift(1))

    return df


def plot_support_resistance(df, title='支撑位和阻力位分析'):
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

    plt.scatter(buy_points.index, buy_points['支撑'], marker='^', color='red', s=100, label='买入信号')
    plt.scatter(sell_points.index, sell_points['阻力'], marker='v', color='green', s=100, label='卖出信号')

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
    data = ak.stock_zh_a_hist_min_em(symbol='600900', period="1", start_date=today, end_date=today)
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
    plot = plot_support_resistance(df, '支撑位和阻力位分析示例')
    plot.show()
