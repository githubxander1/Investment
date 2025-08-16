from pprint import pprint

import pandas as pd
import requests
import json
from urllib.parse import urlencode


def fetch_limit_up_data(type_key, date, page=1, limit=5):
    """
    发送GET请求获取股票涨停池数据

    参数:
        page (int): 页码，默认为1
        limit (int): 每页数据条数，默认为15

    返回:
        dict: 请求返回的JSON数据

    异常:
        可能抛出requests库的异常
    """
    # 基础URL
    base_url = f"https://data.10jqka.com.cn/dataapi/limit_up/{type_key}"

    # 请求参数
    params = {
        "page": page,
        "limit": limit,
        "field": "199112,10,9001,330323,330324,330325,9002,330329,133971,133970,1968584,3475914,9003,9004",
        "filter": "HS,GEM2STAR",
        "order_field": "330324",#119112为冲刺涨停，330329为连板池，
        "order_type": "0",
        "date": date,
        # "_": "1749898676743"
    }

    # 请求头信息
    headers = {
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Android WebView";v="116"',
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; V2353A Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 Hexin_Gphone/11.30.02 (Royal Flush) hxtheme/1 innerversion/G037.09.033.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "sec-ch-ua-platform": '"Android"',
        "X-Requested-With": "com.hexin.plat.android",
        "Referer": "https://data.10jqka.com.cn/datacenterph/limitup/limtupInfo.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ5NjkzMjg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTVjNGY3MWViY2M0YmQwNDBkNGU1MDEzYzdmM2Q0NWRmOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=536749b3c84105bd1c392b267cb5d589; IFUserCookieKey={\"userid\":\"641926488\",\"escapename\":\"mo_641926488\",\"custid\":\"\"); _clck=a5x9j2%7C2%7Cfwp%7C0%7C0; hxmPid=free_ztjj; v=AwCzQhCrfI5n3ACKfzWWz20Y04XSieRThm04V3qRzJuu9a-_Ipm049Z9COPJ"
    }

    try:
        # 发送GET请求，自动处理参数编码
        response = requests.get(base_url, params=params, headers=headers, timeout=15)

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
            print(f"响应内容: {response.text}")
            return {"error": f"Request failed with status code {response.status_code}"}

    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return {"error": f"Request exception: {str(e)}"}

def extract_limit_up_pool(json_data):
    """
    提取【涨停强度】中的股票信息
    """
    stock_list = json_data.get('data', {}).get('info', [])
    extracted_data = []

    for item in stock_list:
        extracted_data.append({
            '股票代码': item['code'],
            '股票名称': item['name'],
            '涨跌幅(%)': round(item['change_rate'], 2),
            '涨停原因': item.get('reason_type', ''),
            '最新价': item['latest'],
            '涨停类型': item.get('limit_up_type', ''),
            '是否首板': '是' if item['high_days'] == '首板' else '否',
            '换手率(%)': item.get('turnover_rate', 0)
        })

    return extracted_data


def extract_strongest_block(json_data):
    """
    提取【最强风口】中的股票信息
    """
    blocks = json_data.get('data', [])
    extracted_data = []

    for block in blocks:
        block_name = block['name']
        stock_list = block.get('stock_list', [])

        for item in stock_list:
            extracted_data.append({
                '所属板块': block_name,
                '股票代码': item['code'],
                '股票名称': item['name'],
                '涨跌幅(%)': round(item['change_rate'], 2),
                '涨停原因': item.get('reason_type', ''),
                '最新价': item['latest'],
                '是否首板': '是' if item['high'] == '首板' else '否'
            })

    return extracted_data


def extract_continuous_limit_up(json_data):
    """
    提取【连板天梯】中的股票信息
    """
    heights = json_data.get('data', [])
    extracted_data = []

    for height_info in heights:
        height = height_info['height']
        stocks = height_info.get('code_list', [])

        for item in stocks:
            extracted_data.append({
                '涨停高度': height,
                '股票代码': item['code'],
                '股票名称': item['name'],
                '连续涨停天数': item['continue_num']
            })

    return extracted_data

# 调用函数获取第一页数据
if __name__ == "__main__":
    date = "20240613"
    types = {
        'limit_up_pool': '涨停强度',
        'block_top': '最强风口',
        'continuous_limit_up': '连板天梯',
    }

    all_dfs = {}

    for type_key, type_name in types.items():
        print(f"正在获取 {type_name} 数据...")
        data = fetch_limit_up_data(type_key,date)
        pprint(data)

        if type_key == 'limit_up_pool':
            df = pd.DataFrame(extract_limit_up_pool(data))
        elif type_key == 'block_top':
            df = pd.DataFrame(extract_strongest_block(data))
        elif type_key == 'continuous_limit_up':
            df = pd.DataFrame(extract_continuous_limit_up(data))

        # 控制台打印
        print(f"\n📊 {type_name} 数据表：")
        print(df)

        # 存入字典，便于后续写入多个sheet
        all_dfs[type_name] = df

    # 写入 Excel
    output_file = '涨停综合数据.xlsx'

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df in all_dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"\n✅ 所有数据已保存至 {output_file}")
