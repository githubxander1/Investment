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

def fetch_position_data(strategy_id, page):
    url = f"{base_url}strategyId={strategy_id}&page={page}&pageSize=10"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"请求失败，策略ID: {strategy_id}, 页面: {page}, 状态码: {response.status_code}")
        return None

def extract_position_data(data, strategy_id):
    position_data_list = data.get("result", {}).get("datas", [])
    extracted_data = []
    for entry in position_data_list:
        position_date = entry.get('positionDate')
        for stock in entry.get('positionStocks', []):
            extracted_data.append({
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
    return extracted_data

def fetch_all_position_data(strategy_ids):
    all_position_data = []
    for strategy_id in strategy_ids:
        page = 1
        while True:
            data = fetch_position_data(strategy_id, page)
            if not data:
                break
            position_data = extract_position_data(data, strategy_id)
            if not position_data:
                break
            all_position_data.extend(position_data)
            page += 1
    return all_position_data

def print_position_data(all_position_data):
    for item in all_position_data:
        pprint(item)

def save_position_data_to_excel(all_position_data, file_path):
    df = pd.DataFrame(all_position_data)
    df.to_excel(file_path, index=False)
    print(f"数据已保存到 {file_path}")

def main():
    all_position_data = fetch_all_position_data(strategy_ids)
    print_position_data(all_position_data)
    file_path = '策略历史持仓111.xlsx'
    save_position_data_to_excel(all_position_data, file_path)

if __name__ == '__main__':
    main()
