import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def calculate_support_resistance(df, prev_close):
    """
    计算支撑位、阻力位和买卖信号
    """
    # 计算H1和L1
    df['H1'] = np.maximum(prev_close, df['最高'])
    df['L1'] = np.minimum(prev_close, df['最低'])

    # 计算P1、阻力位和支撑位
    df['P1'] = df['H1'] - df['L1']
    df['阻力'] = df['L1'] + df['P1'] * 7 / 8
    df['支撑'] = df['L1'] + df['P1'] * 0.5 / 8

    # 计算穿越信号
    # 买入信号: 连续2根K线收盘价在支撑位上方，当前K线收盘价跌破支撑位
    df['longcross_support'] = (df['收盘'].shift(2) > df['支撑'].shift(2)) & \
                              (df['收盘'].shift(1) > df['支撑'].shift(1)) & \
                              (df['收盘'] < df['支撑'])

    # 卖出信号: 连续2根K线收盘价在阻力位下方，当前K线收盘价突破阻力位
    df['longcross_resistance'] = (df['收盘'].shift(2) < df['阻力'].shift(2)) & \
                                 (df['收盘'].shift(1) < df['阻力'].shift(1)) & \
                                 (df['收盘'] > df['阻力'])

    # 交叉信号: 当前K线收盘价跌破支撑位
    df['cross_support'] = (df['收盘'].shift(1) > df['支撑'].shift(1)) & (df['收盘'] < df['支撑'])

    return df

def get_prev_close(stock_code, trade_date):
    """
    获取昨收价（从日线数据）
    """
    try:
        # 转换交易日期格式
        trade_date_dt = datetime.strptime(trade_date, '%Y%m%d')
        prev_date = (trade_date_dt - timedelta(days=7)).strftime('%Y%m%d')

        # 获取最近7个交易日的日线数据
        daily_df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=prev_date,
            end_date=trade_date,
            adjust=""
        )

        # 按日期排序
        daily_df = daily_df.sort_values('日期', ascending=False)

        # 找到交易日前一日的收盘价
        trade_date_str = trade_date_dt.strftime('%Y-%m-%d')
        if trade_date_str in daily_df['日期'].values:
            # 如果包含交易日数据，取前一天的收盘价
            trade_idx = daily_df.index[daily_df['日期'] == trade_date_str].tolist()[0]
            if trade_idx > 0:
                prev_close = daily_df.iloc[trade_idx + 1]['收盘']
            else:
                prev_close = daily_df.iloc[1]['收盘'] if len(daily_df) > 1 else daily_df.iloc[0]['开盘']
        else:
            # 如果不包含交易日数据，取最近一天的收盘价
            prev_close = daily_df.iloc[1]['收盘'] if len(daily_df) > 1 else daily_df.iloc[0]['开盘']

        print(f"昨收价: {prev_close}")
        return prev_close
    except Exception as e:
        print(f"获取昨收价失败: {e}")
        # 使用分时数据开盘价作为替代
        return None

def plot_tdx_indicator(stock_code, period="1", trade_date=None):
    """
    绘制通达信风格的分时指标图

    参数:
    stock_code: 股票代码 (e.g., '600900')
    period: 分钟周期 ('1' 或 '5')
    trade_date: 交易日期 (YYYYMMDD), 默认为当天
    """
    try:
        # 获取当前日期
        today = datetime.now().strftime('%Y%m%d')
        trade_date = trade_date or today

        print(f"获取分时数据: 股票代码={stock_code}, 日期={trade_date}")
        # 获取分时数据
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period=period,
            start_date=trade_date,
            end_date=trade_date,
            adjust=''
        )

        if df.empty:
            print(f"未获取到分时数据: 股票代码={stock_code}, 日期={trade_date}")
            return None

        print(f"分时数据:\n{df.head()}")

        # 获取昨收价
        prev_close = get_prev_close(stock_code, trade_date)

        # 如果无法获取昨收价，使用分时数据开盘价作为替代
        if prev_close is None:
            prev_close = df['开盘'].iloc[0]
            print(f"使用开盘价作为昨收价替代: {prev_close}")

        # 计算指标
        df = calculate_support_resistance(df, prev_close)

        # 处理时间格式
        df['时间'] = pd.to_datetime(df['时间'])
        df.set_index('时间', inplace=True)

        # 过滤交易时间 (9:30-11:30, 13:00-15:00)
        morning_mask = (df.index.time >= pd.to_datetime('09:30:00').time()) & \
                       (df.index.time <= pd.to_datetime('11:30:00').time())
        afternoon_mask = (df.index.time >= pd.to_datetime('13:00:00').time()) & \
                         (df.index.time <= pd.to_datetime('15:00:00').time())
        df = df[morning_mask | afternoon_mask]

        # 创建图表
        plt.figure(figsize=(16, 9))
        # plt.style.use('dark_background')  # 深色背景类似通达信

        # 绘制价格线
        plt.plot(df.index, df['收盘'], label='现价', color='white', linewidth=1.5)

        # 绘制支撑位和阻力位
        plt.plot(df.index, df['阻力'], label='阻力', color='#00DD00', linestyle='--', linewidth=1.2)
        plt.plot(df.index, df['支撑'], label='支撑', color='#00DD00', linestyle='--', linewidth=1.2)

        # 标记买入信号 (LONGCROSS(支撑,现价,2))
        buy_signals = df[df['longcross_support']]
        if not buy_signals.empty:
            for idx, row in buy_signals.iterrows():
                buy_price = row['支撑'] * 1.001
                plt.scatter(idx, buy_price, marker='^', color='red', s=100, zorder=5)
                plt.text(idx, buy_price, '买',
                         color='red', fontsize=12, ha='center', va='bottom', fontweight='bold')

        # 标记卖出信号 (LONGCROSS(现价,阻力,2))
        sell_signals = df[df['longcross_resistance']]
        if not sell_signals.empty:
            for idx, row in sell_signals.iterrows():
                sell_price = row['收盘']
                plt.scatter(idx, sell_price, marker='v', color='green', s=100, zorder=5)
                plt.text(idx, sell_price, '卖',
                         color='green', fontsize=12, ha='center', va='top', fontweight='bold')

        # 绘制黄色柱状线 (CROSS(支撑,现价))
        cross_signals = df[df['cross_support']]
        if not cross_signals.empty:
            for idx, row in cross_signals.iterrows():
                plt.plot([idx, idx], [row['支撑'], row['阻力']],
                         color='yellow', linewidth=3, alpha=0.7, solid_capstyle='round')

        # 设置时间格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
        plt.xticks(rotation=45)
        plt.xlabel('时间')

        # 设置价格标签
        min_price = min(df['最低'].min(), df['支撑'].min())
        max_price = max(df['最高'].max(), df['阻力'].max())
        price_range = np.linspace(min_price, max_price, 10)
        plt.yticks(price_range, [f'{price:.2f}' for price in price_range])
        plt.ylabel('价格')

        # 添加标题和图例
        plt.title(f'{stock_code} 分时阻力支撑指标 - {trade_date}', fontsize=14)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # 添加网格线
        plt.grid(True, linestyle='--', alpha=0.3)

        # 添加水平线表示昨收价
        plt.axhline(y=prev_close, color='gray', linestyle='-', linewidth=0.8, alpha=0.5)
        plt.text(df.index[0], prev_close * 1.001, f'昨收: {prev_close:.2f}',
                 color='gray', fontsize=10, ha='left', va='bottom')

        plt.show()

        return df

    except Exception as e:
        print(f"绘图错误: {e}")
        import traceback
        traceback.print_exc()
        return None

# 使用示例
if __name__ == "__main__":
    # 设置股票代码和日期
    stock_code = '600900'  # 长江电力
    trade_date = '20250612'  # 指定日期，或使用None表示当天

    # 绘制分时图
    result_df = plot_tdx_indicator(stock_code, period="1", trade_date=trade_date)

    # 如果需要保存结果
    if result_df is not None:
        result_df.to_csv(f'{stock_code}_{trade_date}_分时指标.csv', encoding='utf-8-sig')
        print(f"结果已保存到: {stock_code}_{trade_date}_分时指标.csv")