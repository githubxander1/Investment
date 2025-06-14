import json
from pprint import pprint

import pandas as pd
import requests


def fetch_data(type,page=1):
    """
    发送GET请求获取团队数据

    参数:
        page (int): 页码，默认为1

    返回:
        dict: 请求返回的JSON数据

    异常:
        可能抛出requests库的异常
    """
    # 构建请求URL
    url = f"https://data.hexin.cn/gjd/team/type/{type}/page/{page}/"

    # 请求头信息
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

    try:
        # 发送GET请求
        response = requests.get(url, headers=headers, timeout=10)

        # 检查响应状态码
        if response.status_code == 200:
            # 尝试解析JSON响应
            try:
                return response.json()
            except json.JSONDecodeError:
                print("响应不是有效的JSON格式")
                return {"error": "Invalid JSON response", "text": response.text}
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return {"error": f"Request failed with status code {response.status_code}"}

    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return {"error": f"Request exception: {str(e)}"}

def extract_result(data):
    """
    从接口返回数据中提取结果
    """
    if data and 'data' in data:
        result_list = data['data']
        extracted_data = []
        for item in result_list:
            holders_info = ', '.join([f"{holder['name']} ({holder['scale']}%)" for holder in item.get('holders', [])])
            extracted_data.append({
                '股票代码': item.get('code'),
                '股票名称': item.get('name'),
                '报告期': item.get('report'),
                '公告日期': item.get('declare'),
                '总持股比例': item.get('scale'),
                '持有人信息': holders_info,
                '社保': item.get('sb'),
                '养老金': item.get('ylj'),
                '证金': item.get('zj'),
                '汇金': item.get('hj')
            })
        return extracted_data
    return []

def save_to_excel(data, type, filename):
    """
    将数据保存到Excel文件
    """
    if data:
        df = pd.DataFrame(data)
        print(df)
        df.to_excel(filename, sheet_name=type, index=False)
    else:
        print("未提取到有效数据")

def main():
    types = {
        1: '最新公布',
        2: '持有最多',
        3: '增持最多',
        4: '持有最久'
    }

    for type_key in types:
        data = fetch_data(type_key, page=1)

        if data:
            pprint(data)
            extracted_result = extract_result(data)
            print(extracted_result)

            if extracted_result:  # 防止空数据写入
                extracted_df = pd.DataFrame(extracted_result)
                sheet_name = types[type_key]

                # 使用 ExcelWriter 确保多个 sheet 能共存
                with pd.ExcelWriter('国家队持股.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                    extracted_df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"已成功写入 {sheet_name} 到 Excel")
            else:
                print(f"{types[type_key]} - 提取到空数据，未写入Excel")
        else:
            print(f"{types[type_key]} - 请求失败或返回空数据")

if __name__ == "__main__":
    main()
