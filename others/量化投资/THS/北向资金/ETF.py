import requests

# 请求的URL
url = "https://apigate.10jqka.com.cn/d/hq/hshkconnect/etf/v1/list?type=north&sort_field=rise&sort_mode=desc&start_row=0&row_count=20"

# 请求头
headers = {
    "Host": "apigate.10jqka.com.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://eq.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont/1 isVip/0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "Referer": "https://eq.10jqka.com.cn/webpage/hsgt-project/index.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "X-Requested-With": "com.hexin.plat.android"
}

# 发送GET请求
response = requests.get(url, headers=headers)
# 确保请求成功，状态码为200
if response.status_code == 200:
    data = response.json()
    etf_list = data["data"]["list"]
    for etf in etf_list:
        print("代码:", etf["code"])
        print("市场:", etf["market"])
        print("名称:", etf["name"])
        print("价格:", etf["price"])
        print("涨幅:", etf["rise"])
        print("成交总额:", etf["total_amount"])
        print("-" * 30)
else:
    print(f"请求失败，状态码: {response.status_code}")