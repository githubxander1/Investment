from pprint import pprint
import pandas as pd
import requests

# 接口URL
url = "https://data.hexin.cn/gjd/team/type/3/page/1/"

# 请求头，按照原始请求信息进行设置
headers = {
    "Host": "data.hexin.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "hexin-v": "A-UisqbW7oVEywpZTAprPf9f_aofIpm449B9COfKoUoq4ArQr3KphHMmjdV0",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "Referer": "https://data.hexin.cn/gjd/index/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "v=A-UisqbW7oVEywpZTAprPf9f_aofIpm449B9COfKoUoq4ArQr3KphHMmjdV0"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 判断请求是否成功（状态码为200）
if response.status_code == 200:
    data = response.json()
    # 这里先简单打印出整个返回的JSON数据，后续你可以根据实际情况提取具体字段进行分析
    pprint(data)

    # 提取重要信息
    extracted_data = []
    for item in data['data']:
        stock_info = {
            '股票代码': item['code'],
            '股票名称': item['name'],
            '报告期': item['report'],
            '持仓总规模': item['scale'],
            '持仓变动规模': item['sqScale']
        }
        for i, holder in enumerate(item['holders']):
            stock_info[f'股东名称_{i+1}'] = holder['name']
            stock_info[f'持仓规模_{i+1}'] = holder['scale']
            stock_info[f'股东类型_{i+1}'] = holder['tag']
        extracted_data.append(stock_info)

    # 转换为DataFrame
    df = pd.DataFrame(extracted_data)
    df.to_excel('增持最多.xlsx', index=False)
    print(df)
else:
    print(f"请求失败，状态码: {response.status_code}")
