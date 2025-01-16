import requests
from pprint import pprint
import pandas as pd
import openpyxl

# 接口的URL模板


def fetch_history_trade_data(pages):
    url = 'https://ms.10jqka.com.cn/iwencai/iwc - web - business - center/strategy_unify/history_trade'

    # 请求头，按照原始请求信息设置
    headers = {
        'Host': 'ms.10jqka.com.cn',
        'Connection': 'keep - alive',
        'User - Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0',
        'Accept': '*/*',
        'Origin': 'https://bowerbird.10jqka.com.cn',
        'X - Requested - With': 'com.hexin.plat.android',
        'Sec - Fetch - Site': 'same - site',
        'Sec - Fetch - Mode': 'cors',
        'Sec - Fetch - Dest': 'empty',
        'Referer': 'https://bowerbird.10jqka.com.cn/thslc/editor/view/fbea94598C?strategyId=155680',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN,zh;q = 0.9,en - US;q = 0.8,en;q = 0.7'
    }
    all_history_data = []

    for page in range(pages):
        params = {
            'strategyId': '155680',
            'page': pages,
            'pageSize': '20'
        }
        response = requests.get(url, headers=headers, params=params)

        # 判断请求是否成功（状态码为200）
        if response.status_code == 200:
            data = response.json()
            print(data)
            history_data = data["result"]["datas"]
            all_history_data.extend(history_data)
        else:
            print(f"请求失败，状态码: {response.status_code}")
            break

    return all_history_data

def organize_trade_data(history_data):
    trade_date_dict = {}

    for trade_data in history_data:
        trade_date = trade_data["tradeDate"]
        if trade_date not in trade_date_dict:
            trade_date_dict[trade_date] = []
        trade_date_dict[trade_date].extend(trade_data["tradeStocks"])

    return trade_date_dict

def print_trade_data(trade_date_dict):
    print("tradeDate\toperation_tradeDate\tcode\tstkName\toperationType\ttradePrice\ttradeAmount\tposition")
    for trade_date, stocks in trade_date_dict.items():
        for stock in stocks:
            operation_tradeDate = stock['tradeDate']
            print(f"{trade_date}\t{operation_tradeDate}\t{stock['code']}\t{stock['stkName']}\t{stock['operationType']}\t{stock['tradePrice']}\t{stock['tradeAmount']}\t{stock['position']}")

def save_trade_data_to_excel(trade_date_dict, file_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "调仓信息"

    # 写入表头
    ws.append(["tradeDate", "operation_tradeDate", "code", "stkName", "operationType", "tradePrice", "tradeAmount", "position"])

    # 写入数据
    for trade_date, stocks in trade_date_dict.items():
        for stock in stocks:
            operation_tradeDate = stock['tradeDate']
            ws.append([trade_date, operation_tradeDate, stock['code'], stock['stkName'], stock['operationType'], stock['tradePrice'], stock['tradeAmount'], stock['position']])

    wb.save(file_path)
    print(f"调仓信息已成功保存到 '{file_path}' 文件中。")

def main():
    pages_to_download = 1  # 例如，下载1页数据
    history_data = fetch_history_trade_data(pages_to_download)
    pprint(history_data)

    trade_date_dict = organize_trade_data(history_data)
    print_trade_data(trade_date_dict)

    file_path = r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\策略\策略保存的数据\历史买卖_无最新.xlsx"
    save_trade_data_to_excel(trade_date_dict, file_path)

if __name__ == '__main__':
    main()
