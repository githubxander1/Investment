import requests
from fake_useragent import UserAgent

ua = UserAgent()
url = "https://dq.10jqka.com.cn/fuyao/stock_diagnosis/finance/v1/ability_history?code=300010&market=333&type=stock&ability_id=final_score&industry_type="
headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QQQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.6.10 (Royal Flush) hxtheme/1 innver/ G037.08.980.1.32 followPhoneSystemTheme/ 1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaotOldSetting/0",
    "Accept": "*/*",
    "Origin": "https://vaservice.10jqka.com.cn",
    "X-Requested-With": "com.hexin.plat.android",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://vaservice.10jqka.com.cn/advancediagnosestock/html/300010/index.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(url, headers=headers)
data = response.json()["testdata"]
print(response.text)