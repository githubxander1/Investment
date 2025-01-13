import requests

def options_api_request():
    url = "https://data.10jqka.com.cn/dataapi/performance_forecast/v2/notice_query"
    headers = {
        "Host": "data.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
        "Origin": "https://eq.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Sec-Fetch-Mode": "cors",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.5.html?token=KEENjkwNwB5&source=juhelist&performance_type=%E6%89%AD%E4%BA%8F%E4%B8%BA%E7.9B.88&report=2024-4",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    try:
        response = requests.options(url, headers=headers)
        response.raise_for_status()  # 若请求不成功，抛出异常
        return response.headers  # 返回响应头信息
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

if __name__ == "__main__":
    result = options_api_request()
    if result:
        print(result)