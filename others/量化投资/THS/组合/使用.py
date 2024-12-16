import requests
import time
from datetime import datetime

# 请求的URL
url = "https://t.10jqka.com.cn/portfolio/relocate/v2/get_relocate_data_summary?id=14533"
# 请求头，直接复制你提供的内容
headers = {
    "Host": "t.10jqka.com.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://t.10jqka.com.cn/portfolioFront/historyTransfer.html?id=14533",
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
            "利润率": result["data"]["profitMargin"],
            "总利润": result["data"]["profitTotal"],
            "迁移总数": result["data"]["relocateTotal"],
            "汇总日期": datetime.fromtimestamp(result["data"]["summaryDate"]).strftime('%Y-%m-%d %H:%M:%S')  # 将时间戳转换为正常时间格式
        },
        "状态消息": result["status_msg"]
    }
    print(translated_result)
else:
    print(f"请求失败，状态码: {response.status_code}")