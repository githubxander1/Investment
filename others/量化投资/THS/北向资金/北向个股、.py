from json import JSONDecodeError
import requests
import pandas as pd
from datetime import datetime, timezone

# 请求的URL
url = "https://dataq.10jqka.com.cn/fetch-data-server/fetch/v1/specific_data"

# 请求头，直接复制原请求中的请求头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=juece_new; v=A5uNwnmxeEOXqoS3aOMdO8VtI_QFcK9-qYdzJo3Yd5WxwrTuFUA_wrlUA2ae"
}

def get_current():
    # 获取当前时间戳
    return int(datetime.now(timezone.utc).timestamp())

def fetch_data():
    # 动态设置 start 和 end 时间为当前时间
    current = get_current()

    # 请求体数据，直接复制原请求中的请求体信息
    payload = {
        "code_selectors": {
            "include": [
                {
                    "type": "tag",
                    "values": ["lgt_top_deal_list"],
                    # "values": ["lgt_stock_holding_list"],
                    "start": 1734278400,
                    "end": current
                }
            ]
        },
        "indexes": [
            {"index_id": "security_name"},
            {"index_id": "inr-price_change_ratio_pct-sum", "time_type": "DAY_1", "timestamp": 1734278400, "attribute": {"win_size": "1"}},
            {"index_id": "lgt_stock_industry_name"},
            {"index_id": "lgt_stock_turnover", "attribute": {"start": 1734278400, "end": current}},
            {"index_id": "lgt_stock_market_turnover", "attribute": {"start": 1734278400, "end": current}},
            {"index_id": "lgt_stock_turnover_per", "attribute": {"start": 1734278400, "end": current}},
            {"index_id": "lgt_stock_hold_num", "attribute": {"start": 1734278400, "end": current}},
            {"index_id": "lgt_stock_hold_tradeable_per", "attribute": {"start": 1734278400, "end": current}},
            {"index_id": "lgt_stock_list_top_deal_tag", "attribute": {"start": 1734278400, "end": current}}
        ],
        "page_info": {"page_begin": 0, "page_size": 20},
        "sort": [{"idx": 3, "type": "desc"}]
    }

    # 发送POST请求
    response = requests.post(url, json=payload, headers=headers)

    # 确保请求成功，状态码为200
    if response.status_code == 200:
        try:
            data = response.json()
            # 尝试提取data下的data信息
            result_data = data.get('data', {}).get('data', [])

            # 定义字段名映射
            field_mapping = {
                "security_name": "证券名称",
                "inr-price_change_ratio_pct-sum": "价格变动百分比",
                "lgt_stock_industry_name": "行业名称",
                "lgt_stock_turnover": "成交量",
                "lgt_stock_market_turnover": "市场成交量",
                "lgt_stock_turnover_per": "成交量占比",
                "lgt_stock_hold_num": "持仓数量",
                "lgt_stock_hold_tradeable_per": "可交易持仓占比",
                "lgt_stock_list_top_deal_tag": "顶级交易标签"
            }

            # 解析数据
            parsed_data = []
            for item in result_data:
                parsed_item = {}
                for value in item['values']:
                    idx = value['idx']
                    field_name = field_mapping.get(idx, idx)  # 使用映射的字段名，如果没有映射则使用原始字段名
                    parsed_item[field_name] = value['value']
                parsed_data.append(parsed_item)

            # 转换为DataFrame
            df = pd.DataFrame(parsed_data)
            df.to_csv('data.csv', index=False, encoding='utf-8-sig')
            print(df)
        except (ValueError, JSONDecodeError) as e:
            print(f"解析 JSON 失败: {e}")
        except KeyError as e:
            print(f"键不存在: {e}")
    else:
        print(f"请求失败，状态码: {response.status_code}")

# 调用函数获取当前时间的数据
fetch_data()
