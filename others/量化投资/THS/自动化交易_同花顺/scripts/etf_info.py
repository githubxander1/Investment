from pprint import pprint

import requests


def send_request():
    url = 'https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_portfolio_infos'
    params = {
        'product_id': 29617,
        'product_type': 'portfolio'
    }
    headers = {
        'Host': 'dq.10jqka.com.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://t.10jqka.com.cn',
        'X-Requested-With': 'com.hexin.plat.android',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=29617',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM3MzM4ODA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTJiMmY0NGE2ODgxYjg0Nzc1YzY2MzM2MGM2NGUxZjMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=ee119caec220dd3e984ad47c01216b5f; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; hxmPid=hqMarketPkgVersionControl; v=A2KnimVLcSmXyW11P_nPtcEzsePEs2bNGLda8az7jlWAfw1ZlEO23ehHqgN_'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

def extract_result(data):
    if not data:
        return None

    baseinfo = data.get('data', {}).get('baseInfo', {})
    chargeInfo = data.get('data', {}).get('chargeInfo', {})
    userInfo = data.get('data', {}).get('userInfo', {})

    if not baseinfo:
        return None

    extracted_data = {
        '组合id': baseinfo.get('portfolioId', 0),
        '组合名称': baseinfo.get('productName', ''),
        '介绍': baseinfo.get('productDesc', ''),
        '状态': baseinfo.get('productState', 0),
        '是否收费': baseinfo.get('isCharge', 0),
        '服务价格': chargeInfo.get('servicePrice', 0),
        '是否顾问': userInfo.get('isAdviser', False),
        '用户id': userInfo.get('userId', 0)
    }

    return extracted_data

def main():
    result = send_request()
    pprint(result)
    extracted_result = extract_result(result)
    pprint(extracted_result)

if __name__ == "__main__":
    main()
