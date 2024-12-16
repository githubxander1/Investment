from pprint import pprint

import requests
import pandas as pd

# 请求的URL
url = "https://t.10jqka.com.cn/portfolioedge/calculate/v1/get_portfolio_profit_probability?id=14533"
# 请求头，直接复制提供的内容
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
    pprint(result)
    # 翻译字段
    translated_result = {
        "状态码": result["status_code"],
        "数据": {
            "盈利水平": result["data"]["profitLevel"],
            "跟踪天数": result["data"]["followDay"],
            "盈利概率": result["data"]["profitProbability"],
            "跟踪盈利数据列表": [
                {
                    "跟踪天数": item["followDay"],
                    "平均收益": item["averageIncome"],
                    "盈利概率": item["profitProbability"]
                }
                for item in result["data"]["followProfitDataList"]
            ]
        },
        "状态消息": result["status_msg"]
    }
    pprint(translated_result)

    # 将翻译后的数据转换为DataFrame格式，方便后续保存为Excel
    df = pd.DataFrame(translated_result["数据"]["跟踪盈利数据列表"])
    # 添加盈利水平、跟踪天数、盈利概率这几个总体数据到DataFrame中
    df["盈利水平"] = translated_result["数据"]["盈利水平"]
    df["总跟踪天数"] = translated_result["数据"]["跟踪天数"]
    df["总盈利概率"] = translated_result["数据"]["盈利概率"]
    # 保存为Excel文件
    df.to_excel("portfolio_profit_probability.xlsx", index=False)
else:
    print(f"请求失败，状态码: {response.status_code}")