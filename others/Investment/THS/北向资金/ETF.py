import pandas as pd
import requests

# 请求的URL
from fake_useragent import UserAgent

url = "https://apigate.10jqka.com.cn/d/hq/hshkconnect/etf/v1/list?type=north&sort_field=rise&sort_mode=desc&start_row=0&row_count=30"

ua = UserAgent()
# 请求头
headers = {
    # "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont/1 isVip/0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "User-Agent": ua.random
}

# 发送GET请求
response = requests.get(url, headers=headers)
# 确保请求成功，状态码为200
if response.status_code == 200:
    data = response.json()
    etf_list = data["testdata"]["list"]

    etf_datas = []
    for etf in etf_list:
        rise = etf["rise"]

        etf_data = {
        "代码": etf["code"],
        "市场": etf["market"],
        "名称": etf["name"],
        "价格": etf["price"],
        "涨幅": f'{rise:.2f}%',
        "成交总额": etf["total_amount"]
        }
        etf_datas.append(etf_data)
    df = pd.DataFrame(etf_datas)
    print(df)
else:
    print(f"请求失败，状态码: {response.status_code}")