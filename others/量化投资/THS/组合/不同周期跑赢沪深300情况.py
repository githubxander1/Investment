import requests
import pandas as pd

# 请求的URL
url = "https://t.10jqka.com.cn/portfolioedge/calculate/v1/get_portfolio_profitability?id=14533"
# 请求头，直接复制你提供的内容
headers = {
    "Host": "t.10jqka.com.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=14533",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "X-Requested-With": "com.hexin.plat.android"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 判断请求是否成功（状态码为200表示成功）
if response.status_code == 200:
    result = response.json()
    # 翻译字段
    translated_result = {
        "状态码": result["status_code"],
        "数据": {
            "盈利水平": result["data"]["profitabilityLevel"],
            "时间跨度": result["data"]["timeSpan"],
            "盈利数据列表": [
                {
                    "时间跨度": item["timeSpan"],
                    "投资组合收益": item["portfolioIncome"],
                    "沪深300收益": item["hs300Income"]
                }
                for item in result["data"]["profitabilityDataList"]
            ]
        },
        "状态消息": result["status_msg"]
    }
    print(translated_result)

    # 将翻译后的数据转换为DataFrame格式，方便后续保存为Excel
    df = pd.DataFrame(translated_result["数据"]["盈利数据列表"])
    # 保存为Excel文件
    df.to_excel("portfolio_profitability.xlsx", index=False)
else:
    print(f"请求失败，状态码: {response.status_code}")