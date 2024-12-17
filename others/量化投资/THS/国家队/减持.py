from pprint import pprint

import pandas as pd
import requests

# 接口的URL
url = "https://data.hexin.cn/zjc/zjcApi/method/zcjc/cate/jc/"

# 请求头，按照给定的原始请求信息设置
headers = {
    "Host": "data.hexin.cn",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "hexin-v": "A6tsHKz0SJM-SZTHFqMNa1UdM8SVwL9aOdKD9h0oh-pBvMS-pZBPkkmkE0Uu",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "Referer": "https://data.hexin.cn/zjc/index/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "v=A6tsHKz0SJM-SZTHFqMNa1UdM8SVwL9aOdKD9h0oh-pBvMS-pZBPkkmkE0Uu"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 判断请求是否成功（状态码为200）
if response.status_code == 200:
    data = response.json()
    # 这里先简单打印出整个返回的JSON数据，你可以根据实际返回的数据结构进一步提取所需信息
    pprint(data)
    df = pd.DataFrame(data['data']['list'])
    df.to_excel('减持.xlsx', index=False)
    print(df)
else:
    print(f"请求失败，状态码: {response.status_code}")