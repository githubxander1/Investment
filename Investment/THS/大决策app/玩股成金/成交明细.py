from pprint import pprint
import requests
import json
import pandas as pd
from datetime import datetime

def convert_timestamp(timestamp):
    """将毫秒时间戳转为可读日期"""
    if timestamp and timestamp > 0:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return None

def 成交明细(robot_id="9a09cbd9-be78-469c-b3d2-b2d07ad50862", index=1, page_size=20, req_type=-1):
    url = "http://ai.api.traderwin.com/api/ai/robot/history.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "27129c04fb43a33723a9f7720f280ff9",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    payload = {
        "index": index,
        "pageSize": page_size,
        "cmd": "9013",
        "robotId": robot_id,
        "type": req_type
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        pprint(response_data)
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 请求数据
result = 成交明细()

if result and result.get("message", {}).get("state") == 0:
    data_list = result.get("data", {}).get("data", [])

    trade_records = []

    for trade in data_list:
        trade_info = {
            "交易ID": trade.get("id"),
            "机器人ID": trade.get("robotId"),
            "股票ID": trade.get("stockId"),
            "股票代码": trade.get("symbol"),
            "股票名称": trade.get("symbolName"),
            "交易方向": "买入" if trade.get("buy") == 1 else "卖出" if trade.get("buy") == 0 else "未知",
            "交易数量": trade.get("shares"),
            "交易价格": trade.get("price"),
            "交易时间": convert_timestamp(trade.get("created")),
            "完成时间": convert_timestamp(trade.get("updated")),
            "状态": "已完成" if trade.get("status") == 1 else "进行中" if trade.get("status") == 0 else "已取消",
            "委托类型": trade.get("orderType"),
            "成交金额": trade.get("amount"),
            "手续费": trade.get("fee"),
            "市场类型": trade.get("marketType"),
            "备注": trade.get("remark")
        }
        trade_records.append(trade_info)

    # 转换为 DataFrame
    df_trades = pd.DataFrame(trade_records)

    # 保存到 Excel 文件
    output_path = r"D:\1document\Investment\Investment\THS\大决策app\玩股成金\成交明细数据.xlsx"
    df_trades.to_excel(output_path, sheet_name='成交明细', index=False)

    print(f"✅ 数据已成功保存到：{output_path}")

else:
    print("未收到有效响应或状态码错误")
