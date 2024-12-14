import requests


def get_etf_fin_fund_share():
    """
    发送GET请求获取ETF基金份额相关信息的函数
    """
    url = "https://basic.10jqka.com.cn/fundf10/etf/v1/base"
    params = {
        "trade_code": "562500",
        "group": "finFundShare"
    }
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://eq.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Referer": "https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.3.html?tabid=cpbd&code=562500&marketid=20",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0,ExLDQwOzYsMSw0MDs1,ExsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1,ExsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=sns_service_video_choice_detail_85853; v=A3FnQPcfslwVsx5IL0SnmaPbifYLXuXQj9KJ5FOGbThXep5sm671oB8imb3g",
        "X-Requested-With": "com.hexin.plat.android"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()  # 假设返回的数据是JSON格式，返回解析后的内容
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


if __name__ == "__main__":
    # 调用函数获取ETF基金份额相关信息
    result = get_etf_fin_fund_share()
    if result:
        print("获取到的ETF基金份额相关信息:")
        print(result)
        # 这里可以根据业务需求进一步处理返回的数据，例如提取特定字段进行分析或存储等
        share_info = result.get('result', {})
        print("基金份额相关数据:", share_info)
    else:
        print("获取数据失败")