import requests

# 请求的URL
url = "https://ms.10jqka.com.cn/iwencai/userinfo/iwc/userinfo/strategy_unify_subscribe/is_subscribe"
# 请求参数
params = {"strategyId": 155259}
# 请求头，直接复制提供内容
headers = {
    "Host": "ms.10jqka.com.cn",
    "Connection": "keep-alive",
    "Origin": "https://bowerbird.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Accept": "*/*",
    "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/15f2E0a579?strategyId=155259",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=free_stock_600188.dstx; v=A2J0tXgyceLuTm2-ZPbEtNQeuuPEs2a_GLFa8az7jwuBEw1ZlEO23ehHqhZ_",
    "X-Requested-With": "com.hexin.plat.android"
}

# 发送GET请求
response = requests.get(url, params=params, headers=headers)

# 判断请求是否成功（状态码为200表示成功）
if response.status_code == 200:
    result = response.json()
    # 翻译字段
    translated_result = {
        "状态码": result["status_code"],
        "状态消息": result["status_msg"],
        "耗时": result["cost_time"],
        "是否订阅": result["result"],
        "调试信息": result["debug_info"]
    }
    print(translated_result)
else:
    print(f"请求失败，状态码: {response.status_code}")