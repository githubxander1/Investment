import requests

# 第一张图片对应的请求URL和头部
url1 = "https://eq.10jqka.com.cn/gateway/iwc - web - business - center/executor/execute/?code = 300010&interface_name = company_brightpoint"
headers1 = {
    "Host": "eq.10jqka.com.cn",
    "Connection": "keep - alive",
    "Accept": "application/json, text/plain, */*",
    "User - Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QQQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.6.10 (Royal Flush) hxtheme/1 innver/ G037.08.980.1.32 followPhoneSystemTheme/ 1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaotOldSetting/0",
    "X - Requested - With": "com.hexin.plat.android",
    "Sec - Fetch - Site": "same - origin",
    "Sec - Fetch - Mode": "cors",
    "Sec - Fetch - Dest": "empty",
    "Referer": "https://eq.10jqka.com.cn/stockViewPoints/index.html?stockCode = 300010&marketId = 33",
    "Accept - Encoding": "gzip, deflate",
    "Accept - Language": "zh - CN,zh;q = 0.9,en - US;q = 0.8,en;q = 0.7"
}

# 第二张图片对应的请求URL和头部
url2 = "https://eq.10jqka.com.cn/stockViewPoints/index.html?stockCode = 300010&marketId = 33"
headers2 = {
    "Host": "eq.10jqka.com.cn",
    "Connection": "keep - alive",
    "Accept": "text/html,application/xhtml + xml,application/xml;q = 0.9,image/webp,image/apng,*/*;q = 0.8,application/signed - exchange;v = b3;q = 0.9",
    "User - Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QQQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.6.10 (Royal Flush) hxtheme/1 innver/ G037.08.980.1.32 followPhoneSystemTheme/ 1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaotOldSetting/0",
    "X - Requested - With": "com.hexin.plat.android",
    "Sec - Fetch - Site": "same - origin",
    "Sec - Fetch - Mode": "navigate",
    "Sec - Fetch - User": "?1",
    "Sec - Fetch - Dest": "document",
    "Referer": "https://eq.10jqka.com.cn/",
    "Accept - Encoding": "gzip, deflate",
    "Accept - Language": "zh - CN,zh;q = 0.9,en - US;q = 0.8,en;q = 0.7"
}

# 发送请求（第一张图片对应的请求）
response1 = requests.get(url1, headers = headers1)
print(response1.text)

# 发送请求（第二张图片对应的请求）
response2 = requests.get(url2, headers = headers2)
print(response2.text)