import requests

def get_fund_top_holders():
    """
    该函数用于向指定接口发送请求，获取基金（562500）各年十大持有人的相关信息。
    """
    # 接口的URL地址，用于获取特定基金的各年十大持有人数据，这里的562500是基金代码，group=fundholder表示获取持有人信息，limit=10可能表示获取的数量限制（这里推测为获取最近几年每年的十大持有人信息）。
    url = "https://basic.10jqka.com.cn/fundf10/etf/v1/base?trade_code=562500&group=fundholder&limit=10"
    # 请求头信息，包含了诸如浏览器标识、来源页面等多种信息，用于模拟正常的浏览器请求，使得服务器能够正确响应。
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://eq.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme=0 innerversion=G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Referer": "https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.3.html?code=562500&marketid=20&tabid=3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    # Cookie信息，通常包含了用户相关的一些标识、会话等信息，可能用于服务器识别用户、维持会话状态等（要注意其中隐私相关内容）。
    cookies = {
        "user_status": "0",
        "user": "MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox",
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "ticket": "c9840d8b7eefc37ee4c5aa8dd6b90656",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "hxmPid": "free_stock_600188.dstx",
        "v": "A-371FvrdhDtkxJ8ZojjxQen9YJnSiEcq36F8C_yKQTzpgL495ox7DvOlcK8"
    }

    try:
        # 发送GET请求，向指定接口发起获取数据的请求，携带了相应的请求头和Cookie信息。
        response = requests.get(url, headers=headers, cookies=cookies)
        # 如果请求成功，即服务器返回的状态码为200，表示获取数据正常。
        if response.status_code == 200:
            # 尝试将返回的数据解析为JSON格式，方便后续对数据进行处理和分析，然后返回解析后的数据。
            return response.json()
        else:
            # 如果请求失败，打印出具体的失败状态码信息，方便排查问题，同时返回None，表示没有获取到有效数据。
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        # 如果在请求过程中发生了其他异常（比如网络问题等），打印出异常信息，同样返回None。
        print(f"请求发生异常: {e}")
        return None

if __name__ == "__main__":
    # 调用函数来获取基金各年十大持有人信息。
    result = get_fund_top_holders()
    if result:
        # 如果获取到了数据（即result不为None），则可以在这里根据具体需求对数据进行进一步的处理，比如分析持有人的类型、持有份额的变化趋势等，这里暂时只是简单打印出来查看。
        print(result)