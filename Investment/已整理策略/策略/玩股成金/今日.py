from pprint import pprint
import requests
import json
import pandas as pd

# 定义不同信号的请求参数
requests_params = {
    "止损信号": {
        "flag": 0,
        "pageSize": 10,
        "index": "1",
        "cmd": "9022",
        "marketType": ""
    },
    "买入信号": {
        "flag": 3,
        "pageSize": 10,
        "index": "1",
        "cmd": "9023",
        "marketType": ""
    },
    "最优收益排行": {
        "flag": 1,
        "pageSize": 10,
        "index": "1",
        "cmd": "9021",
        "marketType": ""
    },
    "最近一年收益排行": {
        "flag": 2,
        "pageSize": 10,
        "index": "1",
        "cmd": "9025",
        "marketType": ""
    }
}

url = "http://ai.api.traderwin.com/api/ai/signal/rank.json"
headers = {
    'token': '5a66427c4cc7054622909acafc31d2a6',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Host': 'ai.api.traderwin.com',
    'Connection': 'keep-alive'
}

# 存储每个信号对应的 DataFrame
data_frames = {}

# 时间戳转换函数
def convert_timestamp(timestamp):
    return pd.to_datetime(timestamp, unit='ms').strftime('%Y-%m-%d')

# 遍历所有信号参数，发起请求
for sheet_name, params in requests_params.items():
    payload = json.dumps(params)
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    pprint(result)

    if result.get('message', {}).get('state') == 0:
        data_list = result.get('data', {}).get('data', [])
        # 提取并处理数据
        cleaned_data = []
        for item in data_list:
            cleaned_item = {
                '股票名称': item.get('stockName'),
                '代码': item.get('symbol'),
                '行业': item.get('industry'),
                '日期': convert_timestamp(item.get('date')),
                '前收盘价': item.get('prvClose'),
                '当前价格': item.get('nominal')
            }
            cleaned_data.append(cleaned_item)

        # 创建 DataFrame
        df = pd.DataFrame(cleaned_data)
        data_frames[sheet_name] = df
    else:
        print(f"请求 {sheet_name} 失败: {result.get('message')}")

# 保存到 Excel 文件的不同 sheet
# output_path = r"D:\1document\Investment\Investment\已整理策略\玩股成金\AI神经元信号数据.xlsx"
output_path = "今日AI神经元信号数据.xlsx"
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    for sheet_name, df in data_frames.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"✅ 数据已成功保存到：{output_path}")
