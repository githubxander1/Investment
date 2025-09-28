from pprint import pprint

from Investment.T0.real1 import indicator1
from Investment.T0.real2 import indicator2
from Investment.T0_NewSystem.real3 import indicator3


def evaluate_indicators(df):
    """
    统一评估所有指标函数，返回包含买卖信号的结果

    参数：
    df: DataFrame，包含 ['close', 'high', 'low', 'volume', 'datetime'] 列

    返回：
    dict: {'symbol': [signals]}
    """
    signals = {}

    # indicator1
    ind1 = indicator1(df['close'], df['volume'], df['high'], df['low'])
    signals.update({
        'indicator1_buy': ind1['buy_signal'],
        'indicator1_sell': ind1['sell_signal']
    })

    # indicator2 (需要日期列)
    ind2 = indicator2(
        df['close'], df['volume'], df['high'], df['low'], df['datetime']
    )
    signals.update({
        'indicator2_buy': ind2['buy_signal'],
        'indicator2_sell': ind2['sell_signal']
    })

    # indicator3
    ind3 = indicator3(df['close'], df['high'], df['low'])
    signals.update({
        'indicator3_buy': ind3['buy_signal'],
        'indicator3_sell': ind3['sell_signal']
    })

    return signals

import akshare as ak
import pandas as pd
from datetime import time, datetime


def fetch_realtime_data(symbols):
    """
    使用 akshare 获取指定股票列表的实时行情数据

    参数：
    symbols: list of str, e.g., ['sh600000', 'sz300001']

    返回：
    dict: {symbol: DataFrame}
    """
    data = {}
    stock_zh_a_spot_df = ak.stock_zh_a_spot()

    for symbol in symbols:
        symbol_info = stock_zh_a_spot_df[stock_zh_a_spot_df["代码"] == symbol[2:]]
        pprint (symbol_info)

        if not symbol_info.empty:
            close = float(symbol_info["最新价"].values[0])
            high = float(symbol_info["最高"].values[0])
            low = float(symbol_info["最低"].values[0])
            volume = float(symbol_info["成交量"].values[0])
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data[symbol] = pd.DataFrame([{
                "datetime": current_time,
                "open": close,  # 假设开盘价等于收盘价
                "high": high,
                "low": low,
                "close": close,
                "volume": volume
            }])
    return data

def is_trading_time():
    now = datetime.now().time()
    morning_start = time(9, 30)
    morning_end = time(11, 30)
    afternoon_start = time(13, 30)
    afternoon_end = time(14, 50)

    return ((morning_start <= now <= morning_end) or
            (afternoon_start <= now <= afternoon_end))

import requests
import json

def send_dingtalk_notification(msg):
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=ad751f38f241c5088b291765818cfe294c2887198b93655e0e20b1605a8cd6a2"
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    print("钉钉通知发送结果：", response.text)

import time as t

def monitor_stocks(symbols):
    while True:
        if is_trading_time():
            try:
                all_data = fetch_realtime_data(symbols)
                for symbol, df in all_data.items():
                    signals = evaluate_indicators(df)

                    # 检查是否有任何信号被触发
                    triggered_signals = [
                        k for k, v in signals.items() if v.any()
                    ]
                    if triggered_signals:
                        message = f"【{symbol}】触发信号: {triggered_signals}"
                        print(message)
                        # send_dingtalk_notification(message)
            except Exception as e:
                print(f"错误发生：{e}")

        t.sleep(60)  # 每分钟执行一次

if __name__ == "__main__":
    symbols = ["sh600900"]  # 自定义股票/ETF列表
    # monitor_stocks(symbols)
    # fetch_realtime_data(symbols)
    # print(fetch_realtime_data(symbols))
    #保存到csv
    df = pd.DataFrame(fetch_realtime_data(symbols))
    print(df)
    df.to_csv('stock_data.csv', index=False)
