from pprint import pprint

import pandas as pd
import requests


def send_request(id):
    url = 'https://t.10jqka.com.cn/portfolioedge/calculate/v1/get_portfolio_profitability'
    params = {'id': id}
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
        'Cookie': 'user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ4ODA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTJiMmY0NGE2ODgxYjg0Nzc1YzY2MzM2MGM2NGUxZjMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=ee119caec220dd3e984ad47c01216b5f; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; hxmPid=hqMarketPkgVersionControl; v=A0SBYHcl_6Mx20vv4_DxD_OlF8k2XWjUKoH8C17l0I_Sievzhm04V3qRzI-t'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错 (ID: {id}): {e}")
        return None

def extract_result(data):
    data = data.get('data', {})
    profitabilityDataList = data.get('profitabilityDataList', [])
    profitabilityLevel = data.get('profitabilityLevel', '')
    extract_data = []
    for item in profitabilityDataList:
        extract_data.append({
            'hs300收益%': round(item.get('hs300Income', 0) * 100, 2),
            '收益%': round(item.get('portfolioIncome', 0) * 100, 2),
            '周期': item.get('timeSpan', '')
        })
    return extract_data

def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"结果已保存到 {filename}")

def main():
    ids = [27122, 29617, 29665, 29671, 29656, 29734, 29714, 29646]
    all_results = []
    for id in ids:
        result = send_request(id)
        pprint(result)
        if result:
            extracted_result = extract_result(result)
            all_results.extend(extracted_result)
        else:
            print(f"未获取到有效数据 (ID: {id})")
    save_results_to_csv(all_results, 'etf组合收益.csv')

if __name__ == "__main__":
    main()
