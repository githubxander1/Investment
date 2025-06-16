import pandas as pd
import requests
import json


def fetch_strongest_board(date="20250303"):
    """
    获取涨停最强风口板块数据

    参数:
        date (str): 查询日期，格式为YYYYMMDD，默认为20250613

    返回:
        dict: 请求返回的JSON数据

    异常:
        可能抛出requests库的异常
    """
    # 接口URL
    url = "https://data.10jqka.com.cn/dataapi/limit_up/block_top"

    # 请求参数
    params = {
        "filter": "HS,GEM2STAR",
        "date": date
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
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ5NjkzMjg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTVjNGY3MWViY2M0YmQwNDBkNGU1MDEzYzdmM2Q0NWRmOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=536749b3c84105bd1c392b267cb5d589; IFUserCookieKey={\"userid\":\"641926488\",\"escapename\":\"mo_641926488\",\"custid\":\"\"); _clck=a5x9j2%7C2%7Cfwp%7C0%7C0; hxmPid=free_ztjj; v=A-5diHKNCpSlon7wHk9gJe-WPU-w77LoxLJmzRi3WkGsvYH1gH8C-ZRDttbr"
    }

    try:
        # 发送GET请求
        response = requests.get(url, params=params, headers=headers, timeout=15)

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
def extract_top_n_blocks(json_data, block_limit=3, stock_limit=3):
    """
    提取前 N 个板块及其前 M 只股票
    """
    if json_data.get('status_code') != 0:
        print("接口返回错误，状态码：", json_data.get('status_code'))
        return []

    blocks = json_data.get('data', [])[:block_limit]  # 前3个板块
    all_extracted_data = []

    for block in blocks:
        block_name = block['name']
        stock_list = block.get('stock_list', [])[:stock_limit]  # 每个板块前3只股票

        for item in stock_list:
            all_extracted_data.append({
                '所属板块': block_name,
                '股票代码': item['code'],
                '股票名称': item['name'],
                '涨停原因': item['reason_type'],
                '最新价': item['latest'],
                '涨跌幅(%)': round(item['change_rate'], 2),
                '是否首板': '是' if item['high'] == '首板' else '否',
                '涨停天数': item['continue_num'],
                '涨停时间戳': item['first_limit_up_time']
            })

    return all_extracted_data



# 调用函数获取2025年6月13日的数据
if __name__ == "__main__":
    data = fetch_strongest_board(date="20250613")
    print("涨停_最强风口数据:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # 提取前3个板块的各前3只股票
    cleaned_data = extract_top_n_blocks(data, block_limit=3, stock_limit=3)

    # 创建 DataFrame
    df = pd.DataFrame(cleaned_data)

    # 控制台展示表格
    print("\n📊 涨停股票信息表（前3个板块 × 各前3只）：")
    print(df)

    # 写入 Excel
    output_file = '涨停风口数据.xlsx'
    df.to_excel(output_file, sheet_name='最强风口', index=False, engine='openpyxl')
    print(f"\n✅ 数据已保存至 {output_file}")
