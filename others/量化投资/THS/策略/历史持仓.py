from pprint import pprint

import requests
import pandas as pd

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

def fetch_history_position_data(strategy_id, pages):
    all_position_data = []

    for page in range(pages):
        url = f"{base_url}strategyId={strategy_id}&page={page}&pageSize=10"
        response = requests.get(url, headers=headers)

        # 判断请求是否成功（状态码为200）
        if response.status_code == 200:
            data = response.json()
            pprint(data)
            position_data = data["result"]["datas"]
            all_position_data.extend(position_data)
        else:
            print(f"请求失败，状态码: {response.status_code}")
            break

    return all_position_data

def determine_market(stock_code):
    # 根据股票代码判断市场
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('300'):
        return '创业板'
    elif stock_code.startswith(('4', '8')):
        return '北交所'
    else:
        return '其他'

def extract_important_info(position_data):
    important_info = []

    for position in position_data:
        position_date = position["positionDate"]
        for stock in position["positionStocks"]:
            stkCode = stock['stkCode']
            # strategy_id = strategy_id
            important_info.append({
                "strategyId": strategy_id,
                "positionDate": position_date,
                "stkCode": stock["stkCode"],
                "stkName": stock["stkName"],
                "industry": stock["industry"],
                "market": determine_market(stkCode),
                "positionRatio": f'{stock["positionRatio"] * 100:.2f}%',
                "price": stock["price"],
                "profitAndLossRatio": f'{stock["profitAndLossRatio"] * 100:.2f}%'
            })

    return important_info

# 指定要下载的页数
pages_to_download = 2  # 例如，下载2页数据

all_important_info = []

for strategy_id in strategy_ids:
    position_data = fetch_history_position_data(strategy_id, pages_to_download)
    important_info = extract_important_info(position_data)
    all_important_info.extend(important_info)

# 将数据转换为DataFrame
df = pd.DataFrame(all_important_info)

# 打印DataFrame
print(df)

# 将数据保存到Excel文件
df.to_excel("历史持仓信息.xlsx", index=False)
print("历史持仓信息已成功保存到 '历史持仓信息.xlsx' 文件中。")
