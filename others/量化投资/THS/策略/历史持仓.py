from pprint import pprint

import requests
import openpyxl

# 基础的接口URL，后续通过改变page参数获取不同页的数据
base_url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/history_position?"

# 请求头，按照原始请求信息设置
headers = {
    "Host": "ms.10jqka.com.cn",
    "Connection": "keep-alive",
    "Origin": "https://bowerbird.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme=0 innerversion=G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "Accept": "*/*",
    "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/7C958511F8?strategyId=155259",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "X-Requested-With": "com.hexin.plat.android"
}

# 多个策略ID
strategy_ids = ['155259', '155680', '138036', '138386', '155270', '118188', '137789', '138006', '136567', '138127']

# 用于存储所有页按operationDate分类的持仓股票信息
all_data_dict = {}

# 循环获取每个策略ID的数据
for strategy_id in strategy_ids:
    # 重置每种策略的数据字典
    all_data_dict[strategy_id] = {}
    for page in range(10):
        url = f"{base_url}strategyId={strategy_id}&page={page}&pageSize=10"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                trade_data_list = data["result"]["datas"]
                pprint(trade_data_list)
                for trade_data in trade_data_list:
                    operation_date = trade_data["tradeDate"]  # 分类时间
                    trade_stocks = trade_data["tradeStocks"]
                    for stock in trade_stocks:
                        if operation_date not in all_data_dict[strategy_id]:
                            all_data_dict[strategy_id][operation_date] = []
                        stock_info = {
                            "code": stock["code"],
                            "stkName": stock["stkName"],
                            "positionRatio": stock["position"],
                            "profitAndLossRatio": stock.get("profitAndLossRatio", ""),
                            "price": stock["tradePrice"],
                            "industry": stock.get("industry", ""),
                            "operationDate": stock["tradeDate"]  # 操作时间
                        }
                        all_data_dict[strategy_id][operation_date].append(stock_info)
            except KeyError as e:
                print(f"解析JSON数据时出错: {e}, 响应内容: {response.text}")
                break
        else:
            print(f"请求策略ID {strategy_id} 第{page + 1}页数据失败，状态码: {response.status_code}")
            break

# 在控制台展示分类后的持仓股票信息
print("strategyId\toperationDate\tcode\tstkName\tpositionRatio\tprofitAndLossRatio\tprice\tindustry")
for strategy_id, date_dict in all_data_dict.items():
    for operation_date, stocks in date_dict.items():
        for stock in stocks:
            pprint(f"{strategy_id}\t{operation_date}\t{stock['code']}\t{stock['stkName']}\t{stock['positionRatio']}\t{stock['profitAndLossRatio']}\t{stock['price']}\t{stock['industry']}")

# 将分类后的持仓股票信息保存到Excel文件
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "历史持仓信息"

# 写入表头
ws.append(["strategyId", "operationDate", "code", "stkName", "positionRatio", "profitAndLossRatio", "price", "industry"])

# 写入数据
for strategy_id, date_dict in all_data_dict.items():
    for operation_date, stocks in date_dict.items():
        for stock in stocks:
            ws.append([strategy_id, operation_date, stock['code'], stock['stkName'], stock['positionRatio'], stock['profitAndLossRatio'], stock['price'], stock['industry']])

wb.save("历史持仓信息.xlsx")
print("历史持仓信息已成功保存到 '历史持仓信息.xlsx' 文件中。")
