import time
from datetime import datetime, timedelta
import json
import pandas as pd
import requests
from pprint import pprint

# 时间转换工具
def convert_timestamp(timestamp):
    """将毫秒时间戳转为可读日期"""
    if timestamp and timestamp > 0:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return None

# 获取交易记录
def get_trade_records(robot_id, index=1, page_size=20, req_type=0):
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
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 获取成交明细
def get_trade_details(robot_id):
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
        "index": 1,
        "pageSize": 5,
        "cmd": "9013",
        "robotId": robot_id,
        "type": -1  # 查询全部交易
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 提取交易记录
def extract_trade_records(robots):
    all_trades = []
    for robot_name, robot_id in robots.items():
        result = get_trade_records(robot_id)

        if result and result.get("message", {}).get("state") == 0:
            data_list = result.get("data", {}).get("data", [])

            for trade in data_list:
                buy_price = trade.get("buyPrice")
                sale_price = trade.get("price")
                # 避免除零错误
                if buy_price and buy_price > 0:
                    profit_rate = round((sale_price - buy_price) / buy_price * 100, 2)
                else:
                    profit_rate = 0

                trade_info = {
                    "机器人": robot_name,
                    "交易ID": trade.get("logId"),
                    "机器人ID": trade.get("robotId"),
                    "股票代码": trade.get("symbol"),
                    "股票名称": trade.get("symbolNmae"),  # 注意：原数据中字段名可能为symbolName
                    "交易额": trade.get("balance"),
                    "交易数量": trade.get("shares"),
                    "买入价": buy_price,
                    "买入时间": convert_timestamp(trade.get("buyDate")),
                    "卖出价": sale_price,
                    "卖出时间": convert_timestamp(trade.get("created")),
                    "利润率%": profit_rate,
                    "类型": trade.get("type")
                }
                all_trades.append(trade_info)
        else:
            print(f"⚠️ 获取 {robot_name} 交易记录失败")

    return pd.DataFrame(all_trades)

# 提取成交明细
def extract_trade_details(robots):
    all_today_trades = []
    for robot_name, robot_id in robots.items():
        result = get_trade_details(robot_id)

        if result and result.get("message", {}).get("state") == 0:
            data_list = result.get("data", {}).get("data", [])

            for trade in data_list:
                trade_date = convert_timestamp(trade.get("tradeDate"))
                if trade_date:
                    trade_date = datetime.strptime(trade_date, '%Y-%m-%d %H:%M:%S').date()

                trade_info = {
                    "机器人": robot_name,
                    "交易ID": trade.get("logId"),
                    "机器人ID": trade.get("robotId"),
                    "操作方向": "买入" if trade.get("type") == 1 else "卖出" if trade.get("type") == 0 else "已取消",
                    "股票代码": trade.get("symbol"),
                    "股票名称": trade.get("symbolNmae"),  # 注意：原数据中字段名可能为symbolName
                    "交易数量": trade.get("shares"),
                    "成交价格": trade.get("price"),
                    "买入价格": trade.get("buyPrice"),
                    "交易金额": trade.get("balance"),
                    "买入时间": convert_timestamp(trade.get("buyDate")),
                    "创建时间": convert_timestamp(trade.get("created")),
                    "交易日期": trade_date
                }
                all_today_trades.append(trade_info)

                # 通知格式输出
                print(f"[{datetime.now().strftime('%Y-%m-%d')}] "
                      f"机器人：{trade_info['机器人']}，"
                      f"股票：{trade_info['股票名称']}，"
                      f"方向：{trade_info['操作方向']}，"
                      f"数量：{trade_info['交易数量']}，"
                      f"成交价格：{trade_info['成交价格']}，"
                      f"买入价格：{trade_info['买入价格']}，"
                      f"买入时间：{trade_info['买入时间']}")

        else:
            print(f"⚠️ 获取 {robot_name} 成交记录失败")

    return pd.DataFrame(all_today_trades)

# 整合保存交易记录和成交明细
def save_combined_data(robots, output_file="机器人交易数据.xlsx"):
    print("正在获取交易记录...")
    trade_records_df = extract_trade_records(robots)

    print("正在获取成交明细...")
    trade_details_df = extract_trade_details(robots)

    # 保存到同一个Excel文件的不同工作表
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 保存交易记录到"交易记录"工作表
        if not trade_records_df.empty:
            trade_records_df.to_excel(writer, sheet_name='交易记录', index=False)
            print(f"✅ 交易记录已保存到 {output_file} 的'交易记录'工作表")
        else:
            print("⚠️ 无交易记录数据")

        # 保存成交明细到"成交明细"工作表
        if not trade_details_df.empty:
            trade_details_df.to_excel(writer, sheet_name='成交明细', index=False)
            print(f"✅ 成交明细已保存到 {output_file} 的'成交明细'工作表")
        else:
            print("⚠️ 无成交明细数据")

    print(f"🎉 所有数据已整合保存到: {output_file}")
    return trade_records_df, trade_details_df

# 启动整合任务
if __name__ == "__main__":
    # 机器人列表
    robots = {
        "有色金属": "8afec86a-e573-411a-853f-5a9a044d89ae",
        "钢铁": "89c1be35-08a6-47f6-a8c9-1c64b405dab6",
        "建筑行业": "ca2d654c-ab95-448e-9588-cbc89cbb7a9e"
    }

    # 执行整合并保存数据
    trade_records, trade_details = save_combined_data(robots)

    print("\n=== 交易记录预览 ===")
    if not trade_records.empty:
        print(trade_records.head())
    else:
        print("无交易记录")

    print("\n=== 成交明细预览 ===")
    if not trade_details.empty:
        print(trade_details.head())
    else:
        print("无成交明细")
