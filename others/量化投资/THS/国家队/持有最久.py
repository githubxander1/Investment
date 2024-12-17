from pprint import pprint

import pandas as pd
import requests

# 接口的URL
url = "https://data.hexin.cn/gjd/team/type/4/page/1/"

# 请求头，按照给定的原始请求信息进行设置
headers = {
    "Host": "data.hexin.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "hexin-v": "A4lOhnqCCllAN_atgDcPUXvTkb7j1n0F582hnCv-BAGuZqYkcyaN2HcasWK4",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "Referer": "https://data.hexin.cn/gjd/index/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "v=A4lOhnqCCllAN_atgDcPUXvTkb7j1n0F582hnCv-BAGuZqYkcyaN2HcasWK4"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 判断请求是否成功（状态码为200）
if response.status_code == 200:
    data = response.json()
    # 先简单打印出整个返回的JSON数据，后续可根据实际情况提取具体字段
    pprint(data)
    df = pd.DataFrame(data['data']['list'])
    df.to_excel('减持.xlsx', index=False)
    print(df)
else:
    print(f"请求失败，状态码: {response.status_code}")