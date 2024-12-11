import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from plyer import notification
import talib as ta
import tushare as ts

# 设置Tushare Pro的API Token
ts.set_token('2e9a7a0827b4c655aa6c267dc00484c6e76ab1022b5717092b44573e')
pro = ts.pro_api()


def fetch_stock_data(stock_code, start_date, end_date):
    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.sort_values(by='trade_date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def calculate_indicators(df):
    # 计算通达信指标
    A1 = df[['close', 'high']].max(axis=1)
    B1 = df[['close', 'low']].min(axis=1)
    C1 = A1 - B1
    df['阻力'] = B1 + C1 * 7 / 8
    df['支撑'] = B1 + C1 * 0.5 / 8
    df['中线'] = (df['支撑'] + df['阻力']) / 2

    # 动态信息
    df['DYNAINFO_3'] = df['close']
    df['DYNAINFO_5'] = df['high']
    df['DYNAINFO_6'] = df['low']

    # 其他指标计算...
    HHV_H_55 = df['high'].rolling(window=55).max()
    LLV_L_55 = df['low'].rolling(window=55).min()
    RSV = ((df['close'] - LLV_L_55) / (HHV_H_55 - LLV_L_55)) * 100
    V11 = 3 * ta.SMA(RSV, timeperiod=5, matype=1) - 2 * ta.SMA(ta.SMA(RSV, timeperiod=5, matype=1), timeperiod=3,
                                                               matype=1)
    df['趋势'] = ta.EMA(V11, timeperiod=3)
    df['V12'] = (df['趋势'] - df['趋势'].shift(1)) / df['趋势'].shift(1) * 100

    df['准备买入'] = np.where((df['趋势'] < 11), df['趋势'], np.nan)
    df['AA'] = (df['趋势'] < 11) & ((df['趋势'] <= 11).rolling(window=15).sum() >= 1) & (df['close'] < df['中线'])
    df['BB0'] = (df['趋势'].shift(1) < 11) & (df['趋势'] > 11) & (df['close'] < df['中线'])
    df['BB'] = ((df['趋势'].shift(1) < 11) & (df['趋势'].shift(1) > 6) & (df['趋势'] > 11)) | \
               ((df['趋势'].shift(1) < 6) & (df['趋势'].shift(1) > 3) & (df['趋势'] > 6)) | \
               ((df['趋势'].shift(1) < 3) & (df['趋势'].shift(1) > 1) & (df['趋势'] > 3)) | \
               ((df['趋势'].shift(1) < 1) & (df['趋势'].shift(1) > 0) & (df['趋势'] > 1)) | \
               ((df['趋势'].shift(1) < 0) & (df['趋势'] > 0))

    df['下单买入'] = np.where((df['BB'] == True) & (df['close'] < df['中线']), 52, np.nan)
    df['准备卖出'] = np.where((df['趋势'] > 89), df['趋势'], np.nan)
    df['CC'] = (df['趋势'] > 89) & ((df['趋势'] > 89).rolling(window=15).sum() >= 1) & (df['close'] > df['中线'])
    df['DD0'] = (df['趋势'].shift(1) > 89) & (df['趋势'] < 89) & (df['close'] > df['中线'])
    df['DD'] = ((df['趋势'].shift(1) > 89) & (df['趋势'].shift(1) < 94) & (df['趋势'] < 89)) | \
               ((df['趋势'].shift(1) > 94) & (df['趋势'].shift(1) < 97) & (df['趋势'] < 94)) | \
               ((df['趋势'].shift(1) > 97) & (df['趋势'].shift(1) > 99) & (df['趋势'] < 97)) | \
               ((df['趋势'].shift(1) > 99) & (df['趋势'].shift(1) < 100) & (df['趋势'] < 99)) | \
               ((df['趋势'].shift(1) > 100) & (df['趋势'] < 100))

    df['下单卖出'] = np.where((df['DD'] == True) & (df['close'] > df['中线']), 49, np.nan)

    return df


def check_signals_and_notify(df, stock_code):
    last_row = df.iloc[-1]

    if not pd.isna(last_row['下单买入']):
        message = f"【{stock_code}】出现买入信号！"
        print(message)
        notification.notify(
            title="股票交易提醒",
            message=message,
            app_name="Stock Alert",
            timeout=10
        )

    if not pd.isna(last_row['下单卖出']):
        message = f"【{stock_code}】出现卖出信号！"
        print(message)
        notification.notify(
            title="股票交易提醒",
            message=message,
            app_name="Stock Alert",
            timeout=10
        )


if __name__ == "__main__":
    stock_code = "000001.SZ"  # 示例股票代码，替换为你想要监控的股票代码
    today = datetime.today().strftime('%Y%m%d')
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

    df = fetch_stock_data(stock_code, yesterday, today)
    df = calculate_indicators(df)
    check_signals_and_notify(df, stock_code)