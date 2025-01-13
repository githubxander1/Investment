from datetime import datetime
from pprint import pprint

import pandas as pd
import requests

# 请求的URL
url = "https://dataq.10jqka.com.cn/fetch-data-server/fetch/v1/specific_data"

# 请求头
headers = {
    "Host": "dataq.10jqka.com.cn",
    "Connection": "keep-alive",
    "Content-Length": "954",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://eq.10jqka.com.cn",
    "Platform": "mobileweb",
    "Source-id": "hsgt-project",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "Content-Type": "application/json",
    "Referer": "https://eq.10jqka.com.cn/webpage/hsgt-project index.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY1MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=juece_new; v=A_PlyoFJkPs_8lyvgzlFs10li_wdKIf5QbjLHqWQTw9IjhzmLfgXOlGMW3S2",
    "X-Requested-With": "com.hexin.plat.android"
}

def fetch_data(url, headers, payload):
    """
    发送POST请求并返回解析后的JSON数据
    """
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # 若请求不成功，抛出异常
        return response.json()  # 返回解析后的JSON数据
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def extract_result(data):
    """
    从接口返回数据中提取结果
    """
    if data and 'data' in data and 'data' in data['data']:
        result_data = data['data']['data']
        parsed_data = []
        for item in result_data:
            parsed_item = {}
            for value in item['values']:
                idx = str(value['idx'])
                parsed_item[idx] = value['value']
            parsed_data.append(parsed_item)
        return parsed_data
    return []

def save_to_csv(data, filename):
    """
    将数据保存到CSV文件
    """
    if data:
        # 创建一个映射字典，将index_id映射到中文标题
        index_to_chinese = {
            "0": "股票名称",
            "1": "价格变化百分比之和",
            "2": "财务指标",
            "3": "新增持股比例",
            "4": "持股数量",
            "5": "持股市值",
            "6": "可交易持股比例",
            "7": "连续持股季度数",
            "8": "总持股比例",
            "9": "所属行业"
        }

        # 替换表头为中文
        df = pd.DataFrame(data)
        df.columns = [index_to_chinese[col] for col in df.columns]

        print(df)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
    else:
        print("未提取到有效数据")

def main():
    # 用户输入起始日期和结束日期
    # start_date_str = input("请输入起始日期 (格式: YYYY-MM-DD): ")
    start_date_str = "2024-12-10"
    # end_date_str = input("请输入结束日期 (格式: YYYY-MM-DD): ")
    end_date_str = "2025-01-15"
    # 将日期字符串转换为时间戳
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
    except ValueError:
        print("日期格式不正确，请使用 YYYY-MM-DD 格式")
        return

    # 定义不同的payload
    payload_increasing_holding = {
        "code_selectors": {
            "include": [
                {
                    "type": "tag",
                    "values": ["lgt_stock_holding_list"],
                    "start": start_timestamp,
                    "end": end_timestamp
                }
            ]
        },
        "indexes": [
            {"index_id": "security_name"},
            {"index_id": "inr-price_change_ratio_pct-sum", "time_type": "DAY_1", "timestamp": start_timestamp, "attribute": {"win_size": "60"}},
            {"index_id": "hq-fncdict-3475914"},
            {"index_id": "lgt_stock_add_hold_per", "time_type": "QUARTER_1", "timestamp": start_timestamp},
            {"index_id": "lgt_stock_hold_num", "time_type": "QUARTER_1", "timestamp": start_timestamp},
            {"index_id": "lgt_stock_hold_market_value", "time_type": "QUARTER_1", "timestamp": start_timestamp},
            {"index_id": "lgt_stock_hold_tradeable_per", "time_type": "QUARTER_1", "timestamp": start_timestamp},
            {"index_id": "lgt_stock_hold_continous_num", "time_type": "QUARTER_1", "timestamp": start_timestamp},
            {"index_id": "lgt_stock_hold_total_per", "time_type": "QUARTER_1", "timestamp": start_timestamp},
            {"index_id": "lgt_stock_industry_name"}
        ],
        "page_info": {"page_begin": 0, "page_size": 20},
        "sort": [{"idx": 3, "type": "desc"}]
    }

    payload_heavy_holding = {
        "code_selectors": {
            "include": [
                {
                    "type": "tag",
                    "values": ["lgt_stock_holding_list"],
                    "start": start_timestamp,
                    "end": end_timestamp
                }
            ]
        },
        "indexes": [
            {"index_id": "security_name"},
            {"index_id": "lgt_stock_hold_market_value", "time_type": "SNAPSHOT"},
            {"index_id": "lgt_stock_hold_tradeable_per", "time_type": "SNAPSHOT"},
            {"index_id": "inr-price_change_ratio_pct-sum", "time_type": "DAY_1", "timestamp": start_timestamp, "attribute": {"win_size": "1"}},
            {"index_id": "lgt_stock_add_hold_per", "time_type": "SNAPSHOT"},
            {"index_id": "lgt_stock_hold_total_per", "time_type": "SNAPSHOT"},
            {"index_id": "lgt_stock_industry_name"}
        ],
        "page_info": {"page_begin": 0, "page_size": 20},
        "sort": [{"idx": 1, "type": "desc"}]
    }

    payload_individual_stocks = {
        "code_selectors": {
            "include": [
                {
                    "type": "tag",
                    "values": ["lgt_top_deal_list"],
                    "start": start_timestamp,
                    "end": end_timestamp
                }
            ]
        },
        "indexes": [
            {"index_id": "security_name"},
            {"index_id": "inr-price_change_ratio_pct-sum", "time_type": "DAY_1", "timestamp": start_timestamp, "attribute": {"win_size": "1"}},
            {"index_id": "lgt_stock_industry_name"},
            {"index_id": "lgt_stock_turnover", "attribute": {"start": start_timestamp, "end": end_timestamp}},
            {"index_id": "lgt_stock_market_turnover", "attribute": {"start": start_timestamp, "end": end_timestamp}},
            {"index_id": "lgt_stock_turnover_per", "attribute": {"start": start_timestamp, "end": end_timestamp}},
            {"index_id": "lgt_stock_hold_num", "attribute": {"start": start_timestamp, "end": end_timestamp}},
            {"index_id": "lgt_stock_hold_tradeable_per", "attribute": {"start": start_timestamp, "end": end_timestamp}},
            {"index_id": "lgt_stock_list_top_deal_tag", "attribute": {"start": start_timestamp, "end": end_timestamp}}
        ],
        "page_info": {"page_begin": 0, "page_size": 20},
        "sort": [{"idx": 3, "type": "desc"}]
    }

    # 用户选择payload
    payload_choice = input("请输入要查询的数据类型 (1: 增持, 2: 重仓, 3: 北向个股): ")
    if payload_choice == '1':
        payload = payload_increasing_holding
        field_mapping = {
            "0": "股票名称",
            "1": "价格变化百分比之和",
            "2": "财务指标",
            "3": "新增持股比例",
            "4": "持股数量",
            "5": "持股市值",
            "6": "可交易持股比例",
            "7": "连续持股季度数",
            "8": "总持股比例",
            "9": "所属行业"
        }
        filename = '增持.xlsx'
    elif payload_choice == '2':
        payload = payload_heavy_holding
        field_mapping = {
            "0": "股票名称",
            "1": "持股市值",
            "2": "可交易持股比例",
            "3": "价格变化百分比之和",
            "4": "新增持股比例",
            "5": "总持股比例",
            "6": "所属行业"
        }
        filename = '重仓.xlsx'
    elif payload_choice == '3':
        payload = payload_individual_stocks
        field_mapping = {
            "0": "证券名称",
            "1": "价格变动百分比",
            "2": "行业名称",
            "3": "成交量",
            "4": "市场成交量",
            "5": "成交量占比",
            "6": "持仓数量",
            "7": "可交易持仓占比",
            "8": "顶级交易标签"
        }
        filename = '北向个股.xlsx'
    else:
        print("无效的选择，请输入 1, 2 或 3")
        return

    data = fetch_data(url, headers, payload)
    if data:
        pprint(data)
        extracted_result = extract_result(data)
        save_to_csv(extracted_result, filename)
    else:
        print("未获取到数据")


if __name__ == "__main__":
    main()