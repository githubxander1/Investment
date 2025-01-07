from pprint import pprint

import pandas as pd
import requests

def gjd_zjc(operation):
    # 接口URL
    url = f"https://data.hexin.cn/zjc/zjcApi/method/zcjc/cate/{operation}"

    # 请求头，按照给定的原始请求信息进行设置
    headers = {
        "Host": "data.hexin.cn",
        "Connection": "keep-alive",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "hexin-v": "A0KFW_2HkXw_yo0goOrkVPS-mkOkE0Y0-B86UYxbbrVg3-35dKOWPcinimVf",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Referer": "https://data.hexin.cn/zjc/index/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "v=A0KFW_2HkXw_yo0goOrkVPS-mkOkE0Y0-B86UYxbbrVg3-35dKOWPcinimVf"
    }

    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 判断请求是否成功（状态码为200）
    if response.status_code == 200:
        data = response.json()
        # 先简单打印出整个JSON数据内容，后续可根据实际情况进一步提取详细信息
        df = pd.DataFrame(data)
        print(df)
    else:
        print(f"请求失败，状态码: {response.status_code}")
# operation = 'jc'
for operation in ['jc', 'zc']:
    print(gjd_zjc(operation))
# operation = 'zc'
# print(gjd_zjc(operation))