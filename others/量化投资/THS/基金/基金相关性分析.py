import requests
import pandas as pd
import numpy as np
from pprint import pprint

# 定义函数用于获取基金持仓股票信息
def get_fund_hold_stock(trade_code):
    url = "https://basic.10jqka.com.cn/fuyao/fund_trans/fund/v1/hold_stock"
    params = {"tradeCode": trade_code}
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://eq.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Referer": "https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.3.html?tabid=cpbd&code=562500&marketid=20",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    cookies = {
        "user_status": "0",
        "user": "MDptb18yNDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox",
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "ticket": "c9840d8b7eefc37ee4c5aa8dd6b90656",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "hxmPid": "sns_service_video_choice_detail_85853",
        "v": "A4aQAbRGHc0mqsmpTGjYaNAS3ncI58qhnCv-BXCvcqmEcykt2HcasWy7ThpD"
    }

    try:
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求发生异常: {e}")
        return None

# 定义函数用于获取基金名称
def get_fund_name(trade_code):
    """
    发送GET请求获取ETF基础信息的函数
    """
    url = "https://basic.10jqka.com.cn/fundf10/etf/v1/base"
    params = {
        "trade_code": trade_code,
        "group": "baseInfo"
    }
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://eq.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Referer": f"https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.3.html?tabid=cpbd&code={trade_code}&marketid=20",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb18yNDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0,ExLDQwOzYsMSw0MDs1,ExsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1,ExsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=sns_service_video_choice_detail_85853; v=A9jOG5agC-ekJCdjLsiu8hJsoA1qwTxLniUQzxLJJJPGrXc3utEM2-414Fxh",
        "X-Requested-With": "com.hexin.plat.android"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        info = data['data']
        simpleName = info.get('simpleName')
        return simpleName
    except requests.RequestException as e:
        print(f"请求发生异常: {e}")
        return None

# 提取基金持仓股票的证券代码
def extract_sec_codes(data):
    sec_codes = set()
    if 'data' in data and isinstance(data['data'], list):
        for stock in data['data']:
            if 'secCode' in stock:
                sec_codes.add(stock['secCode'])
    return sec_codes

# 计算两个基金持仓股票的重叠度
def calculate_overlap(sec_codes1, sec_codes2):
    intersection = sec_codes1.intersection(sec_codes2)
    union = sec_codes1.union(sec_codes2)
    overlap = len(intersection) / len(union) if len(union) > 0 else 0
    return overlap

# 计算多个基金之间的相关性矩阵
def calculate_correlation_matrix(trade_codes):
    sec_codes_dict = {}
    fund_names_dict = {}

    for code in trade_codes:
        result = get_fund_hold_stock(code)
        if result:
            sec_codes_dict[code] = extract_sec_codes(result)
        else:
            sec_codes_dict[code] = set()

        # 获取基金名称
        fund_name = get_fund_name(code)
        if fund_name:
            fund_names_dict[code] = fund_name
        else:
            fund_names_dict[code] = code

    correlation_matrix = pd.DataFrame(index=trade_codes, columns=trade_codes)

    for i, code1 in enumerate(trade_codes):
        for j, code2 in enumerate(trade_codes):
            if i <= j:
                overlap = calculate_overlap(sec_codes_dict[code1], sec_codes_dict[code2])
                correlation_matrix.at[code1, code2] = overlap
                correlation_matrix.at[code2, code1] = overlap

    # 确保数据类型为浮点数
    correlation_matrix = correlation_matrix.astype(float)
    return correlation_matrix, fund_names_dict

# 将相关性矩阵保存到CSV文件
def save_correlation_matrix_to_excel(correlation_matrix, fund_names_dict, filename="基金相关性分析.xlsx"):
    labels = [fund_names_dict[code] for code in correlation_matrix.index]
    correlation_matrix.index = labels
    correlation_matrix.columns = labels
    correlation_matrix.to_excel(filename, index=True)
    print(f"相关性矩阵已保存到 {filename}")

if __name__ == "__main__":
    trade_codes = ["159300", "159925", "515310", "159673"]
    correlation_matrix, fund_names_dict = calculate_correlation_matrix(trade_codes)
    save_correlation_matrix_to_excel(correlation_matrix, fund_names_dict)
