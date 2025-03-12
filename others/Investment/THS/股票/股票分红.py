import requests

def get_stock_dividend_event_remind():
    """
    该函数用于获取指定股票（600188）分红相关的大事提醒信息。
    """
    # 接口URL，用于获取股票分红大事提醒数据，600188是股票代码，0/10是分页参数（从第0条开始取10条）
    url = "https://basic.10jqka.com.cn/mapp/600188/dividend/0/10/stock_event_remind.json"
    # 请求头，包含了用于标识请求的各种信息，如浏览器类型、来源页面等
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "hexin-v": "A8XTXOMjaUQz5irExQKL3R__3Qr_gnkVwzddaMcqgScLSepwj9KJ5FOGbQVU",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Referer": "https://basic.10jqka.com.cn/astockph/briefinfo/index.html?code=600188&marketid=17",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    # Cookie信息，可能用于用户身份识别、会话管理等（注意隐私问题）
    cookies = {
        "user_status": "0",
        "user": "MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox",
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "ticket": "c9840d8b7eefc37ee4c5aa8dd6b90656",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "hxmPid": "free_stock_600188.dstx",
        "v": "A8XTXOMjaUQz5irExQKL3R__3Qr_gnkVwzddaMcqgScLSepwj9KJ5FOGbQVU"
    }

    try:
        # 发送GET请求，携带请求头和Cookie信息
        response = requests.get(url, headers=headers, cookies=cookies)
        # 如果请求成功（状态码为200）
        if response.status_code == 200:
            # 解析JSON数据并返回
            return response.json()
        else:
            # 打印请求失败状态码
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        # 打印请求异常信息
        print(f"请求发生异常: {e}")
        return None

if __name__ == "__main__":
    # 调用函数获取分红大事提醒信息
    result = get_stock_dividend_event_remind()
    if result:
        # 如果获取到数据，可进行进一步处理（这里简单打印）
        print(result)