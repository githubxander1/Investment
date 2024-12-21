import requests

# 请求的URL
url = "https://ms.10jqka.com.cn/index/robotindex/"
# 请求参数
params = {
    "tag": "策略详情页评论区",
    "code": "6w5aqh",
    "market_code": "100002",
    "page": 1,
    "size": 3
}
# 请求头，直接复制提供内容
headers = {
    "Host": "ms.10jqka.com.cn",
    "Connection": "keep-alive",
    "Origin": "https://bowerbird.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Accept": "*/*",
    "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/15f2E0a579?strategyId=155259",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "X-Requested-With": "com.hexin.plat.android"
}

# 发送GET请求
response = requests.get(url, params=params, headers=headers)

# 判断请求是否成功（状态码为200表示成功）
if response.status_code == 200:
    result = response.json()
    print(result)
    # 这里可以进一步对返回的结果进行处理，例如提取评论内容、用户信息等
    for comment in result["answer"]["components"][0]["data"]["datas"]:
        print(f"用户名: {comment['userName']}")
        print(f"评论时间: {comment['time']}")
        print(f"评论内容: {comment['content']}")
        print("-" * 50)
else:
    print(f"请求失败，状态码: {response.status_code}")