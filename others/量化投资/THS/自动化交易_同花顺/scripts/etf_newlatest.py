import requests


def send_request():
    url = 'https://t.10jqka.com.cn/portfolio/post/v2/get_newest_relocate_post'
    params = {
        'id': 29617
    }
    headers = {
        'Host': 't.10jqka.com.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'com.hexin.plat.android',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=29617',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ4ODA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTJiMmY0NGE2ODgxYjg0Nzc1YzY2MzM2MGM2NGUxZjMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=ee119caec220dd3e984ad47c01216b5f; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; hxmPid=hqMarketPkgVersionControl; v=AxLXmrX7oTmTPd1F4fgfxZGDYdP0Ixa0SCcK4dxrPkWw771JxLNmzRi3WuOv'
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
    # 假设返回数据中有'newestRelocatePost'字段，提取它
    newest_post = data.get('newestRelocatePost', None)
    return newest_post


def main():
    result = send_request()
    extracted_result = extract_result(result)
    print(extracted_result)


if __name__ == "__main__":
    main()
