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

    # 提取重要信息
    extracted_data = []
    for item in data['data']:
        stock_info = {
            '股票代码': item['code'],
            '股票名称': item['name'],
            '报告期': item['report'],
            '持仓总规模': item['scale'],
            '持仓变动规模': item['sqScale'],
            '进入时间': item['entry'],
            '持有期': item['period'],
            '主要股东': []
        }
        for holder in item['holders']:
            holder_info = {
                '股东名称': holder['name'],
                '持仓规模': holder['scale'],
                '股东类型': holder['tag']
            }
            stock_info['主要股东'].append(holder_info)
        extracted_data.append(stock_info)

    # 将提取的数据转换为DataFrame
    # 创建一个空的DataFrame
    df = pd.DataFrame(columns=[
        '股票代码', '股票名称', '报告期', '持仓总规模', '持仓变动规模',
        '进入时间', '持有期', '股东名称_1', '持仓规模_1', '股东类型_1',
        '股东名称_2', '持仓规模_2', '股东类型_2',
        '股东名称_3', '持仓规模_3', '股东类型_3',
        '股东名称_4', '持仓规模_4', '股东类型_4',
        '股东名称_5', '持仓规模_5', '股东类型_5'
    ])

    for stock in extracted_data:
        row = {
            '股票代码': stock['股票代码'],
            '股票名称': stock['股票名称'],
            '报告期': stock['报告期'],
            '持仓总规模': stock['持仓总规模'],
            '持仓变动规模': stock['持仓变动规模'],
            '进入时间': stock['进入时间'],
            '持有期': stock['持有期']
        }
        for i, holder in enumerate(stock['主要股东']):
            row[f'股东名称_{i+1}'] = holder['股东名称']
            row[f'持仓规模_{i+1}'] = holder['持仓规模']
            row[f'股东类型_{i+1}'] = holder['股东类型']
        df = df.append(row, ignore_index=True)

    # 保存为Excel文件
    df.to_excel('持有最久.xlsx', index=False)
    print(df)
else:
    print(f"请求失败，状态码: {response.status_code}")
