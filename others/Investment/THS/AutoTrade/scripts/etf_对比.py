from pprint import pprint

import pandas as pd
import requests

from others.Investment.THS.AutoTrade.config.settings import ETF_ids, ETF_ids_to_name, \
    ETF_info_file


def send_request(id):
    url = 'https://t.10jqka.com.cn/portfolio/v2/position/get_position_income_info'
    params = {
        'id': id
    }
    headers = {
        'Host': 't.10jqka.com.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'com.hexin.plat.android',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=29617',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY4MTkyNjQ4ODoxNzM3MzM4ODA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTJiMmY0NGE2ODgxYjg0Nzc1YzY2MzM2MGM2NGUxZjMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=ee119caec220dd3e984ad47c01216b5f; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; hxmPid=hqMarketPkgVersionControl; v=A4NGpYxA4H6qFqyKSI--Yjh4EEwt-Bc6UYxbbrVg3-JZdKw2PcinimFc67DG'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

def extract_result(data, id):
    if not data or 'data' not in data:
        print(f"ID: {id} 无数据")
        return []

    item = data['data']
    return [{
        'ETF组合': ETF_ids_to_name.get(id, '未知'),
        '创建时间': item.get('createAt', None),
        '最大回撤%': round(item.get('maxDrawdownRate', None) * 100, 2),
        '日收益率%': round(item.get('dailyIncomeRate', None) * 100, 2),
        '总收益率%': round(item.get('totalIncomeRate', None) * 100, 2)
    }]

def save_results_to_xlsx(results, filename ,sheetname):
    df = pd.DataFrame(results)
    print(df)
    df.to_excel(filename, sheet_name=sheetname, index=False)
    print(f"结果已保存到 {filename}")

def main():
    all_results = []
    for id in ETF_ids:
        result = send_request(id)
        pprint(result)
        if result:
            extracted_result = extract_result(result, id)
            all_results.extend(extracted_result)
        else:
            print(f"未获取到有效数据 (ID: {id})")
    save_path =ETF_info_file
    save_results_to_xlsx(all_results, save_path , sheetname='ETF组合对比')

if __name__ == "__main__":
    main()
