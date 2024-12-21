import requests
from pprint import pprint
import pandas as pd
import openpyxl

# 接口的URL模板
url_template = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/history_trade?strategyId=118188&page={}&pageSize=10"

# 请求头，按照原始请求信息设置
headers = {
    "Host": "ms.10jqka.com.cn",
    "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/fbea94598C?strategyId=138006",
}

def fetch_history_trade_data(pages):
    all_history_data = []

    for page in range(pages):
        url = url_template.format(page)
        response = requests.get(url, headers=headers)

        # 判断请求是否成功（状态码为200）
        if response.status_code == 200:
            data = response.json()
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
