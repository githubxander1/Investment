import time
from datetime import datetime, timedelta
import json
import pandas as pd
import requests
from pprint import pprint

from Investment.THS.AutoTrade.utils.format_data import determine_market


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
        # pprint(response_data)
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 检查当天交易并通知
def check_trades_today():
    # 机器人列表
    robots = {
        "有色金属": "8afec86a-e573-411a-853f-5a9a044d89ae",
        "钢铁": "89c1be35-08a6-47f6-a8c9-1c64b405dab6",
        "建筑行业": "ca2d654c-ab95-448e-9588-cbc89cbb7a9e"
    }

    today = datetime.now().date().strftime("%Y-%m-%d")

    all_today_trades = []
    for robot_name, robot_id in robots.items():
        result = get_trade_details(robot_id)
        if result and result.get("message", {}).get("state") == 0:
            data_list = result.get("data", {}).get("data", [])

            for trade in data_list:
                code = trade.get("symbol")
                market = determine_market(code)
                trade_date = convert_timestamp(trade.get("tradeDate"))
                if trade_date and trade_date.startswith(today):
                    trade_info = {
                        # "交易ID": trade.get("logId"),
                        # "机器人ID": trade.get("robotId"),
                        "名称": robot_name,
                        "操作": "买入" if trade.get("type") == 1 else "卖出" if trade.get("type") == 0 else "已取消",
                        "标的名称": trade.get("symbolNmae"),
                        "代码": code,
                        "最新价": trade.get("price"),#原成交价格
                        "新比例%": 0,
                        "市场": market,
                        "时间": convert_timestamp(trade.get("buyDate")),#原买入时间
                        "交易数量": trade.get("shares"),
                        "买入价格": trade.get("buyPrice"),
                        "交易金额": trade.get("balance"),
                        "创建时间": convert_timestamp(trade.get("created")),
                        "完成时间": convert_timestamp(trade.get("tradeTime"))
                    }
                    all_today_trades.append(trade_info)
                    # 通知格式输出
                    print(f"[{datetime.now().strftime('%Y-%m-%d')}] "
                          f"名称：{trade_info['名称']}，"
                          f"操作：{trade_info['操作']}，"
                          f"标的名称：{trade_info['标的名称']}，"
                          f"市场：{trade_info['市场']}，"
                          f"最新价：{trade_info['最新价']}，"
                          f"时间：{trade_info['时间']},"
                          f"新比例%：{trade_info['新比例%']}")
                          # f"代码：{trade_info['代码']}，"
                          # f"数量：{trade_info['交易数量']}，"
                          # f"买入价格：{trade_info['买入价格']}，"

        else:
            print(f"⚠️ 获取 {robot_name} 成交记录失败")

    all_today_trades_df  = pd.DataFrame(all_today_trades)
    all_today_trades_df.to_excel(f"机器人今日成交明细.xlsx", index=False)
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
    print("⏰ 启动定时任务，等待每天 09:31 检查交易...")
    # schedule_daily_check()
    print(check_trades_today())
