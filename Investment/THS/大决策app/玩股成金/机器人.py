import json
from pprint import pprint

import requests

def fetch_data(url, headers, params):
    """发送请求并获取数据"""
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None
import pandas as pd

def extract_data(response_data):
    """提取数据并转换为 DataFrame"""
    if not response_data or 'data' not in response_data:
        print("无效的响应数据")
        return pd.DataFrame()

    data = response_data['data']

    # 提取组合基本信息
    extracted_item = {
        "组合名称": data.get('name', ''),
        "总收益率": data.get('currentTotalRate', ''),
        "今日盈亏": data.get('todayGains', ''),
        "今日收益率": data.get('todayRate', ''),
        "累计盈亏": data.get('totalGains', ''),
        "累计收益率": data.get('totalRate', ''),
        "最新价": data.get('nowPrice', ''),
        "成本价": data.get('costPrice', ''),
        "创建时间": data.get('createTime', '')
    }

    # 提取持仓股票信息
    stocks_data = []
    for log in data.get('logs', []):
        stock_item = {
            "股票代码": log.get('symbol', ''),
            "股票名称": log.get('symbolName', ''),
            "最新价": log.get('price', ''),
            "成本价": log.get('basePrice', ''),
            "持仓量": log.get('shares', ''),
            "市值": log.get('marketValue', ''),
            "今日盈亏": log.get('todayGains', ''),
            "累计盈亏": log.get('totalGains', ''),
            "今日收益率": (log.get('todayGains', 0) / log.get('todayCost', 1)) * 100 if log.get('todayCost', 0) != 0 else 0,
            "累计收益率": (log.get('totalGains', 0) / log.get('lockCost', 1)) * 100 if log.get('lockCost', 0) != 0 else 0,
        }
        stocks_data.append(stock_item)

    # 将提取的数据转换为 DataFrame
    combo_df = pd.DataFrame([extracted_item])
    stocks_df = pd.DataFrame(stocks_data)

    return combo_df, stocks_df

def main():
    # 请求参数
    url = "http://ai.api.traderwin.com/api/ai/robot/get.json?token=5a66427c4cc7054622909acafc31d2a6"

    payload = json.dumps({
        "cmd": "9015",
        "robotId": "2"
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'ai.api.traderwin.com',
        'Connection': 'keep-alive'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = response.json()
    pprint(response_data)

    if response_data:
        # 提取数据
        combo_df, stocks_df = extract_data(response_data)
        combo_df.to_csv('combo_data.csv', index=False)
        stocks_df.to_csv('stocks_data.csv', index=False)

        if not combo_df.empty:
            # 展示组合信息
            print("组合信息如下：")
            print(combo_df)
        else:
            print("未提取到组合有效数据")

        if not stocks_df.empty:
            # 展示持仓股票信息
            print("持仓股票信息如下：")
            print(stocks_df)
        else:
            print("未提取到持仓股票有效数据")
    else:
        print("请求失败或响应数据为空")

# 运行主函数
if __name__ == "__main__":
    main()
