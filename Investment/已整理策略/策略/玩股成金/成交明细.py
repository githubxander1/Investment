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
        pprint(response_data)
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 检查当天交易并通知
def extract_trades(robots):
    all_today_trades = []
    for robot_name, robot_id in robots.items():
        result = get_trade_details(robot_id)
        pprint(result)
        if result and result.get("message", {}).get("state") == 0:
            data_list = result.get("data", {}).get("data", [])

            for trade in data_list:
                trade_date = convert_timestamp(trade.get("tradeDate")).strftime('%Y-%m-%d')
                # if trade_date and trade_date.startswith(today):
                trade_info = {
                    "交易ID": trade.get("logId"),
                    "机器人ID": trade.get("robotId"),
                    "机器人": robot_name,
                    "操作方向": "买入" if trade.get("type") == 1 else "卖出" if trade.get("type") == 0 else "已取消",
                    "股票代码": trade.get("symbol"),
                    "股票名称": trade.get("symbolNmae"),
                    "交易数量": trade.get("shares"),
                    "成交价格": trade.get("price"),
                    "买入价格": trade.get("buyPrice"),
                    "交易金额": trade.get("balance"),
                    "买入时间": convert_timestamp(trade.get("buyDate")),
                    "创建时间": convert_timestamp(trade.get("created")),
                    '交易日期': trade_date
                    # "完成时间": convert_timestamp(trade.get("tradeTime"))
                }
                all_today_trades.append(trade_info)
                #通知格式输出
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

    all_today_trades_df  = pd.DataFrame(all_today_trades)
    all_today_trades_df.to_excel(f"机器人成交明细.xlsx", index=False)
    return all_today_trades_df

# 定时执行函数
# def schedule_daily_check(target_time="09:31"):
#     while True:
#         now = datetime.now()
#         today_time = now.strftime("%H:%M")
#         if today_time == target_time:
#             print(f"⏰ 正在检查 {now.strftime('%Y-%m-%d')} 的交易记录...")
#             check_trades_today()
#             time.sleep(60)  # 避免重复执行
#         else:
#             time.sleep(30)  # 每30秒检查一次时间

# 启动定时任务
if __name__ == "__main__":
    # print("⏰ 启动定时任务，等待每天 09:31 检查交易...")
    # schedule_daily_check()
    # 机器人列表
    robots = {
        "有色金属": "8afec86a-e573-411a-853f-5a9a044d89ae",
        "钢铁": "89c1be35-08a6-47f6-a8c9-1c64b405dab6",
        "建筑行业": "ca2d654c-ab95-448e-9588-cbc89cbb7a9e"
    }

    print(extract_trades(robots))
