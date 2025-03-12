from pprint import pprint

import requests


def get_fund_data():
    """
    调用指定接口获取基金相关数据的函数
    """
    # 接口地址
    url = "https://basic.10jqka.com.cn/fundf10/etf/v1/base"

    # 请求参数
    params = {
        "trade_code": "562500",
        "group": "fundholder",
        "limit": 10
    }

    # 请求头，按照你提供的信息原样设置
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

    # Cookie信息，按照你提供的原样设置（不过实际中如果Cookie有隐私相关内容需要谨慎处理）
    cookies = {
        "user_status": "0",
        "user": "MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox",
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "ticket": "c9840d8b7eefc37ee4c5aa8dd6b90656",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "hxmPid": "sns_service_video_choice_detail_85853",
        "v": "A3FnQPcfslwVsx5IL0SnmaPbifYLXuXQj9KJ5FOGbThXep5sm671oB8imb3g"
    }

    try:
        # 发送GET请求
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        # 如果请求成功（状态码为200），则处理返回的数据
        if response.status_code == 200:
            return response.json()  # 假设返回的数据是JSON格式，进行解析并返回
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求发生异常: {e}")
        return None


if __name__ == "__main__":
    result = get_fund_data()
    if result:
        pprint(result)