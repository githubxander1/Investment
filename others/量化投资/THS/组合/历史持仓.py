from pprint import pprint

import requests
import pandas as pd


# 请求的URL
url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/history_trade"
# 请求参数
params = {
    "strategyId": 155259,
    "page": 0,
    "pageSize": 10
}

# 请求头，直接复制原请求中的请求头信息
headers = {
    "Host": "ms.10jqka.com.cn",
    "Connection": "keep-alive",
    "Origin": "https://bowerbird.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Accept": "**",
    "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/fbea94598C?strategyId=155259",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "X-Requested-With": "com.hexin.plat.android"
}

# 发送GET请求
response = requests.get(url, params=params, headers=headers)
# 确保请求成功，状态码为200
if response.status_code == 200:
    data = response.json()
    pprint(data)
    result_data = data["result"]["datas"]

    # 用于存储最终整理后的数据
    all_data = []
    for item in result_data:
        trade_date = item["tradeDate"]
        trade_stocks = item["tradeStocks"]
        for stock in trade_stocks:
            extracted_data = {
                "tradeDate": trade_date,
                "marketCode": stock["marketCode"],
                "operationType": stock["operationType"],
                "position": stock["position"],
                "stkCode": stock["stkCode"],
                "stkName": stock["stkName"],
                "tradeAmount": stock["tradeAmount"],
                "tradePrice": stock["tradePrice"]
            }
            all_data.append(extracted_data)

    # 将数据转换为DataFrame
    df = pd.DataFrame(all_data)
    # 按照tradeDate分组显示在控制台（表格形式）
    print(df.groupby('tradeDate').apply(lambda x: x[['marketCode', 'operationType', 'position', 'stkCode', 'stkName', 'tradeAmount', 'tradePrice']]))
    # 保存到Excel文件
    df.to_excel(r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\trade_data.xlsx", index=False)
else:
    print(f"请求失败，状态码: {response.status_code}")