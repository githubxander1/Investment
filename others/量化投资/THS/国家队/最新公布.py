from pprint import pprint

import pandas as pd
import requests

# 接口的URL
url = "https://data.hexin.cn/gjd/team/type/1/page/1/"

# 请求头，按照你提供的原始请求信息设置
headers = {
    "Host": "data.hexin.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "hexin-v": "Aybh7_FzfdB79il0WsY4SDDyfpeoB2rLPE-eJRDPEn0kiMkNeJe60Qzb7j_j",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Referer": "https://data.hexin.cn/gjd/index/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "v=A0WC0sa2jqWkK6p5raMLXZ9_XYp_AvmeQ7Ld6EeqAciLxWrwD1IJZNMG7bPU"
}

def fetch_data(url, headers):
    """
    发送GET请求并返回解析后的JSON数据
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 若请求不成功，抛出异常
        return response.json()  # 返回解析后的JSON数据
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

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

def save_to_excel(data, filename):
    """
    将数据保存到Excel文件
    """
    if data:
        df = pd.DataFrame(data)
        print(df)
        df.to_excel(filename, index=False)
    else:
        print("未提取到有效数据")

def main():
    data = fetch_data(url, headers)
    if data:
        pprint(data)
        extracted_result = extract_result(data)
        save_to_excel(extracted_result, '国家队持股.xlsx')
    else:
        print("未获取到数据")

if __name__ == "__main__":
    main()
