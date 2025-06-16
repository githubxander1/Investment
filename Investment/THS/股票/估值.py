from pprint import pprint
import requests
import json
import pandas as pd
import os

def fetch_data(url, headers, payload, data_type):
    """通用数据获取函数"""
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            return response.json(), data_type
        else:
            print(f"{data_type}请求失败，状态码: {response.status_code}")
            print(response.text)
            return None, data_type
    except Exception as e:
        print(f"{data_type}请求异常: {e}")
        return None, data_type

def process_response(data, data_type):
    """处理响应数据并转换为DataFrame"""
    if not data:
        return pd.DataFrame()

    # 提取索引定义
    indexes = data.get("data", {}).get("indexes", [])
    if not indexes:
        return pd.DataFrame()

    # 创建字段映射：index_id -> 字段名
    field_map = {i: item["index_id"] for i, item in enumerate(indexes)}

    # 提取记录数据
    records = data.get("data", {}).get("data", [])
    if not records:
        return pd.DataFrame()

    # 处理每条记录
    processed_records = []
    for record in records:
        record_data = {}
        values = record.get("values", [])

        # 处理每个值项
        for value_item in values:
            idx = value_item.get("idx")
            value = value_item.get("value")

            # 如果是嵌套对象，提取关键信息
            if isinstance(value, dict):
                # 提取标签和估值描述
                tags = value.get("tag_name_list", [])
                comment = value.get("valuation_comment", "")

                # 将嵌套对象转换为可存储的格式
                record_data[field_map.get(idx)] = ", ".join(tags) if tags else comment
            else:
                # 普通值直接存储
                field_name = field_map.get(idx)
                if field_name:
                    record_data[field_name] = value

        # 添加数据类型标识
        record_data["data_type"] = data_type
        processed_records.append(record_data)

    # 转换为DataFrame
    return pd.DataFrame(processed_records)

def save_to_excel(dfs, file_path):
    """将多个DataFrame保存到Excel不同工作表"""
    with pd.ExcelWriter(file_path) as writer:
        for data_type, df in dfs.items():
            if not df.empty:
                # 简化列名以便阅读
                df.columns = df.columns.str.replace("_", " ").str.title()
                df.to_excel(writer, sheet_name=data_type, index=False)
    print(f"数据已保存至: {file_path}")

def main():
    # 公共参数
    url = "http://dataq.10jqka.com.cn/fetch-data-server/fetch/v1/specific_data"
    headers = {
        "Host": "dataq.10jqka.com.cn",
        "Connection": "keep-alive",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Android WebView\";v=\"116\"",
        "sec-ch-ua-mobile": "?1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; V2353A Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 Hexin_Gphone/11.30.02 (Royal Flush) hxtheme/1 innerversion/G037.09.033.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Platform": "mobileweb",
        "Source-id": "kamis-7933",
        "sec-ch-ua-platform": "Android",
        "Origin": "https://eq.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://eq.10jqka.com.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ5NjkzMjg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTVjNGY3MWViY2M0YmQwNDBkNGU1MDEzYzdmM2Q0NWRmOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=536749b3c84105bd1c392b267cb5d589; _clck=a5x9j2%7C2%7Cfws%7C0%7C0; _clsk=1psigrs%7C1749956074262%7C2%7C1%7C; IFUserCookieKey={\"userid\":\"641926488\",\"escapename\":\"mo_641926488\",\"custid\":\"100113495581\"}; hxmPid=ths_jeton_show; v=A0f0F5Ou45CvQGccxVO5wt5F1PARTBtLdSWfohk0Ykz92GjqIRyrfoXwL_Qq"
    }

    # 三种数据类型的请求参数
    request_params = [
        {
            "data_type": "精选",
            "payload": {
                "code_selectors": {"intersection": [{"type": "tag", "values": ["picked_index"]}]},
                "indexes": [
                    {"index_id": "security_name"},
                    {"index_id": "security_ths_code"},
                    {"index_id": "last_price"},
                    {"index_id": "price_change_ratio_pct"},
                    {"index_id": "total_market_value"},
                    {"index_id": "valuation_tag", "time_type": "DAY_1", "timestamp": 0}
                ],
                "page_info": {"page_begin": 0, "page_size": 20},
                "sort": [{"idx": 4, "type": "DESC"}]
            }
        },
        {
            "data_type": "行业",
            "payload": {
                "code_selectors": {"intersection": [{"type": "tag", "values": ["second_industry"]}]},
                "indexes": [
                    {"index_id": "security_name"},
                    {"index_id": "security_ths_code"},
                    {"index_id": "security_valuation_pep", "attribute": {"win_size": 1}},
                    {"index_id": "F10-pe_ttm"},
                    {"index_id": "security_valuation_pbp", "attribute": {"win_size": 1}},
                    {"index_id": "F10-pb_mrq"},
                    {"index_id": "security_valuation_psp", "attribute": {"win_size": 1}},
                    {"index_id": "F10-ps_ttm"},
                    {"index_id": "security_valuation_pcfp", "attribute": {"win_size": 1}},
                    {"index_id": "F10-pcf_ttm"},
                    {"index_id": "F10-roe_ttm"},
                    {"index_id": "F10-dividend_yield_ratio"},
                    {"index_id": "F10-predict_peg"},
                    {"index_id": "valuation-predict_pe", "time_type": "DAY_1", "timestamp": 0},
                    {"index_id": "valuation-total_market_value", "time_type": "DAY_1", "timestamp": 0}
                ],
                "follow": {"idx": "4"},
                "page_info": {"page_begin": 0, "page_size": 20},
                "sort": [{"idx": 14, "type": "DESC"}]
            }
        },
        {
            "data_type": "指数",
            "payload": {
                "code_selectors": {"intersection": [{"type": "tag", "values": ["all_index"]}]},
                "indexes": [
                    {"index_id": "security_name"},
                    {"index_id": "security_ths_code"},
                    {"index_id": "security_valuation_suitable_val"},
                    {"index_id": "security_valuation_pep", "attribute": {"win_size": 1}},
                    {"index_id": "F10-pe_ttm"},
                    {"index_id": "security_valuation_pbp", "attribute": {"win_size": 1}},
                    {"index_id": "F10-pb_mrq"},
                    {"index_id": "security_valuation_psp", "attribute": {"win_size": 1}},
                    {"index_id": "F10-ps_ttm"},
                    {"index_id": "security_valuation_pcfp", "attribute": {"win_size": 1}},
                    {"index_id": "F10-pcf_ttm"},
                    {"index_id": "F10-roe_ttm"},
                    {"index_id": "F10-dividend_yield_ratio"},
                    {"index_id": "F10-predict_peg"},
                    {"index_id": "valuation-predict_pe", "time_type": "DAY_1", "timestamp": 0},
                    {"index_id": "valuation-total_market_value", "time_type": "DAY_1", "timestamp": 0}
                ],
                "follow": {"idx": "3"},
                "page_info": {"page_begin": 0, "page_size": 20},
                "sort": [{"idx": 15, "type": "DESC"}]
            }
        }
    ]

    # 存储结果的DataFrame字典
    dfs = {}

    # 依次发送三种请求
    for params in request_params:
        data, data_type = fetch_data(url, headers, params["payload"], params["data_type"])
        pprint(data)
        df = process_response(data, data_type)
        dfs[data_type] = df
        print(f"{data_type}数据获取完成，共{len(df)}条记录")

        # 打印前几条数据预览
        if not df.empty:
            print("数据预览:")
            print(df.head().to_string(index=False))
            print("\n")

    # 保存到Excel
    today = pd.Timestamp.now().strftime("%Y%m%d")
    file_path = f"估值数据_{today}.xlsx"
    save_to_excel(dfs, file_path)

if __name__ == "__main__":
    main()
