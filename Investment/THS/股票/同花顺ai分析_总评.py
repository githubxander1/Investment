import requests
# url = "https://dq.10jqka.com.cn/fuyao/stock_diagnosis/finance/v1/ability_history?code=300010&market=333&type=stock&ability_id=final_score&industry_type="
# headers = {
#     "User-Agent": ua.random
# }

# response = requests.get(url, headers=headers)
# print(response.text)

import requests
from fake_useragent import UserAgent

ua = UserAgent()
url = "https://dq.10jqka.com.cn/fuyao/stock_diagnosis/finance/v1/analysis?code=300010&market=333&type=stock&industry_type=stock_ths&report="
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


try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查请求是否成功
    data = response.json()

    if data["status_code"] == 0:
        # 提取关键信息
        overview = data["testdata"]["overview"]
        reports = data["testdata"]["reports"]
        highlights = data["testdata"]["highlight"]
        code = data["testdata"]["code"]
        name = data["testdata"]["name"]
        industry = data["testdata"]["industry"]

        # 打印提取的信息
        print(f"股票代码: {code}")
        print(f"股票名称: {name}")
        print(f"行业: {industry}")
        print(f"总评: {overview}")
        print(f"报告列表: {reports}")

        print("\n亮点信息:")
        for highlight in highlights:
            print(f"  - {highlight['name']}: {highlight['comment']}")
    else:
        print(f"请求失败: {data['status_msg']}")

except requests.RequestException as e:
    print(f"请求出现错误: {e}")
