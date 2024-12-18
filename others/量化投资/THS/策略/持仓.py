from pprint import pprint
import pandas as pd
import requests
import openpyxl

# 接口的URL
url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/history_trade?strategyId=138006&page=0&pageSize=10"

# 请求头，按照原始请求信息设置
headers = {
    "Host": "ms.10jqka.com.cn",
    "Connection": "keep-alive",
    "Origin": "https://bowerbird.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme=0 innerversion=G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "Accept": "*/*",
    "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/fbea94598C?strategyId=138006",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "X-Requested-With": "com.hexin.plat.android"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 判断请求是否成功（状态码为200）
if response.status_code == 200:
    data = response.json()
    historyData = data["result"]["datas"]
    print('所有调仓数据：')
    pprint(historyData)

    # 用于存储按tradeDate分类的调仓信息
    trade_date_dict = {}

    for trade_data in historyData:
        trade_date = trade_data["tradeDate"]
        if trade_date not in trade_date_dict:
            trade_date_dict[trade_date] = []
        trade_date_dict[trade_date].extend(trade_data["tradeStocks"])

    # 在控制台以表格形式输出调仓信息
    print("tradeDate\tcode\tstkName\toperationType\ttradePrice\ttradeAmount\tposition")
    for trade_date, stocks in trade_date_dict.items():
        for stock in stocks:
            print(f"{trade_date}\t{stock['code']}\t{stock['stkName']}\t{stock['operationType']}\t{stock['tradePrice']}\t{stock['tradeAmount']}\t{stock['position']}")

    # 将调仓信息保存到Excel文件
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "调仓信息"

    # 写入表头
    ws.append(["tradeDate", "code", "stkName", "operationType", "tradePrice", "tradeAmount", "position"])

    # 写入数据
    for trade_date, stocks in trade_date_dict.items():
        for stock in stocks:
            ws.append([trade_date, stock['code'], stock['stkName'], stock['operationType'], stock['tradePrice'], stock['tradeAmount'], stock['position']])

    wb.save("调仓信息.xlsx")
    print("调仓信息已成功保存到 '调仓信息.xlsx' 文件中。")
else:
    print(f"请求失败，状态码: {response.status_code}")
