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

def trade_record(robot_id, index=1, page_size=20, req_type=0):
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


def extract_trades(robots):
    """从机器人列表中提取交易记录"""
    trade_records = []
    for robot_name,robot_id in robots.items():
        result = trade_record(robot_id)

        if result and result.get("message", {}).get("state") == 0:
            data_list = result.get("data", {}).get("data", [])
            totalRecord = result.get("totalRecord")
            totalPage = result.get("totalPage")
            pageSize = result.get("pageSize")

            trade_records = []

            for trade in data_list:
                buy_price = trade.get("buyPrice")
                sale_price = trade.get("price")
                profit_rate = round((sale_price - buy_price) / buy_price * 100,2)
                trade_info = {
                    "交易ID": trade.get("logId"),
                    "机器人ID": trade.get("robotId"),
                    "股票代码": trade.get("symbol"),
                    "股票名称": trade.get("symbolNmae"),
                    # "交易方向": "买入" if trade.get("buy") == 1 else "卖出" if trade.get("buy") == 0 else "未知",
                    "交易额": trade.get("balance"),
                    "交易数量": trade.get("shares"),
                    "买入价": trade.get("buyPrice"),
                    "买入时间": convert_timestamp(trade.get("buyDate")),
                    "卖出价": trade.get("price"),
                    "卖出时间": convert_timestamp(trade.get("created")),
                    "利润率": profit_rate,
                    "类型": trade.get("type")
                }
                trade_records.append(trade_info)

            # 转换为 DataFrame
            df_trades = pd.DataFrame(trade_records)
            print(df_trades)

            # 保存到 Excel 文件
            output_path = "交易记录数据.xlsx"
            df_trades.to_excel(output_path, sheet_name='交易记录', index=False)

            print(f"✅ 数据已成功保存到：{output_path}")

        else:
            print("未收到有效响应或状态码错误")
    return trade_records

if __name__ == '__main__':
    robots = {
        "有色金属": "8afec86a-e573-411a-853f-5a9a044d89ae",
        "钢铁": "89c1be35-08a6-47f6-a8c9-1c64b405dab6",
        "建筑行业": "ca2d654c-ab95-448e-9588-cbc89cbb7a9e"
    }
    print(extract_trades(robots))