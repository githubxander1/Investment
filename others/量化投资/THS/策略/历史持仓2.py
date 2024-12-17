import requests
import pandas as pd
from pprint import pprint

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

# 存储所有策略的历史持仓数据
all_position_data = []

# 遍历每个策略ID
for strategy_id in strategy_ids:
    page = 2
    while True:
        url = f"{base_url}strategyId={strategy_id}&page={page}&pageSize=10"

        # 发送GET请求
        response = requests.get(url, headers=headers)

        # 判断请求是否成功（状态码为200）
        if response.status_code == 200:
            data = response.json()
            pprint(data)
            position_data_list = data.get("result", {}).get("datas", [])

            # 如果没有更多数据，退出循环
            if not position_data_list:
                break

            # 提取关键信息
            for entry in position_data_list:
                position_date = entry.get('positionDate')
                for stock in entry.get('positionStocks', []):
                    all_position_data.append({
                        'Strategy ID': strategy_id,
                        'Position Date': position_date,
                        'Stock Code': stock.get('code'),
                        'HQ Code': stock.get('hqCode'),
                        'Industry': stock.get('industry'),
                        'Market': stock.get('market'),
                        'Market Code': stock.get('marketCode'),
                        'Position Ratio': stock.get('positionRatio'),
                        'Price': stock.get('price'),
                        'Profit and Loss Ratio': stock.get('profitAndLossRatio'),
                        'Standard Code': stock.get('standardCode'),
                        'STK Code': stock.get('stkCode'),
                        'Stock Name': stock.get('stkName')
                    })
        else:
            print(f"请求失败，策略ID: {strategy_id}, 页面: {page}, 状态码: {response.status_code}")
            break

        # # 增加页面计数
        # page += 1


# 打印到控制台
for item in all_position_data:
    pprint(item)

# 保存到Excel
df = pd.DataFrame(all_position_data)
df.to_excel('策略历史持仓111.xlsx', index=False)
print("数据已保存到 history_positions_info.xlsx")
