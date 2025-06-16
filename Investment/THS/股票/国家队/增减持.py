from pprint import pprint

import pandas as pd
import requests



def zjc(type):
    # 接口的URL
    url = f"https://data.hexin.cn/zjc/zjcApi/method/zcjc/cate/{type}/"

    # 请求头，按照给定的原始请求信息设置
    headers = {
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Android WebView";v="116"',
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "hexin-v": "A4KIJ4yxXhAvn0LMtKo0IeNy0YPkU4ZtOFd6kcybrvWgHy05tOPWfQjnyqKf",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; V2353A Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 Hexin_Gphone/11.30.02 (Royal Flush) hxtheme/1 innerversion/G037.09.033.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
            "sec-ch-ua-platform": '"Android"',
            "Referer": "https://data.hexin.cn/gjd/index/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": "v=A4KIJ4yxXhAvn0LMtKo0IeNy0YPkU4ZtOFd6kcybrvWgHy05tOPWfQjnyqKf"
        }

    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 判断请求是否成功（状态码为200）
    if response.status_code == 200:
        data = response.json()
        # 这里先简单打印出整个返回的JSON数据，你可以根据实际返回的数据结构进一步提取所需信息
        # pprint(data)
        # df = pd.DataFrame(data['data']['list'])
        # df.to_excel('减持.xlsx', index=False)
        print(data)
        return data
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None

def extract_data(data):
    """
    提取并格式化数据，避免 tag 字段中的列表导致 to_excel 错误
    """
    for item in data:
        # 将 tag 列表转换为字符串，便于写入 Excel
        if isinstance(item.get('tag'), list):
            item['tag'] = ', '.join(filter(None, item['tag']))  # 过滤空值
    return data

if __name__ == '__main__':
    types = {
        'jc': '减持',
        'zc': '增持'
    }

    filename = '增减持.xlsx'

    with pd.ExcelWriter(filename, mode='w', engine='openpyxl') as writer:
        for type_key, sheet_name in types.items():
            print(f"正在获取 {sheet_name} 数据...")
            raw_data = zjc(type_key)

            if not raw_data:
                print(f"{sheet_name} - 未获取到有效数据")
                continue

            cleaned_data = extract_data(raw_data)
            df = pd.DataFrame(cleaned_data)
            print(df)

            # 写入 Excel 不同 sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"{sheet_name} 数据已写入 Excel")
