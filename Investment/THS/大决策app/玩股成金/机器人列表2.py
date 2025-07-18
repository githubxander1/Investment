from pprint import pprint

import requests
import json
import pandas as pd
from datetime import datetime

def convert_timestamp(timestamp):
    """将毫秒时间戳转为可读日期"""
    if timestamp and timestamp > 0:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
    return None

def robot_list():
    url = "http://ai.api.traderwin.com/api/ai/robot/list.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "27129c04fb43a33723a9f7720f280ff9",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    payload = {
        "industryId": "CN",
        "cmd": "9012",
        "userId": "0",
        "version": "2",
        "marketType": "CN"
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
result = robot_list()

if result and result.get("message", {}).get("state") == 0:
    data = result.get("data", [])

    # 提取机器人基本信息
    robot_basic_info = []
    # 提取持仓股票信息
    robot_stock_logs = []

    for robot in data:
        robot_info = {
            "机器人ID": robot.get("robotId"),
            "名称": robot.get("name"),
            "备注": robot.get("remark"),
            "当前资金": robot.get("funds"),
            "初始资金": robot.get("startFunds"),
            "止损比例": robot.get("stopLost"),
            "止盈比例": robot.get("stopWin"),
            "创建时间": convert_timestamp(robot.get("created")),
            "收益更新时间": convert_timestamp(robot.get("gainDate")),
            "标记": robot.get("flag"),
            "今日收益率": robot.get("todayRate"),
            "今日总资产": robot.get("todayTotalRate"),
            "卖出收益": robot.get("sellGains"),
            "卖出时间": convert_timestamp(robot.get("sellDate")),
            "卖出市值": robot.get("sellMarketValue"),
            "当日成本": robot.get("todayCost"),
            "市场类型": robot.get("marketType"),
            "参考指数": robot.get("consult"),
            "本月资产": robot.get("amountOfMonth"),
            "本年资产": robot.get("amountOfYear"),
            "参考月份": robot.get("refMonth"),
            "参考年份": robot.get("refYear"),
            "版本号": robot.get("version"),
            "风险等级": robot.get("risk"),
            "资产总值": robot.get("marketValue")
        }
        robot_basic_info.append(robot_info)

        logs = robot.get("logs", [])
        for log in logs:
            stock_info = {
                "机器人ID": robot.get("robotId"),
                "股票ID": log.get("stockId"),
                "股票代码": log.get("symbol"),
                "股票名称": log.get("symbolName"),
                "持有数量": log.get("shares"),
                "买入价格": log.get("price"),
                "建仓时间": convert_timestamp(log.get("created")),
                "当前价格": log.get("nominal"),
                "前收盘价": log.get("prvClose"),
                "当日收益": log.get("todayGains"),
                "总收益": log.get("totalGains"),
                "市值": log.get("marketValue"),
                "锁定数量": log.get("locks"),
                "成本价": log.get("basePrice"),
                "锁定时间": convert_timestamp(log.get("lockDate")),
                "更新时间": convert_timestamp(log.get("updated")),
                "最高价": log.get("high"),
                "锁定成本": log.get("lockCost"),
                "卖出时间": convert_timestamp(log.get("sellDate")),
                "卖出锁定数": log.get("sellLocks"),
                "卖出收益": log.get("sellGains"),
                "当日成本": log.get("todayCost"),
                "市场类型": log.get("marketType"),
                "成本价值": log.get("costValue"),
                "收益": log.get("gains"),
                "累计收益": log.get("totalGains"),
                "累计市值": log.get("totalMarketValue")
            }
            robot_stock_logs.append(stock_info)

    # 转换为 DataFrame
    df_robots = pd.DataFrame(robot_basic_info)
    df_stocks = pd.DataFrame(robot_stock_logs)

    # 保存到 Excel 文件的不同 sheet
    output_path = r"D:\1document\Investment\Investment\THS\大决策app\玩股成金\机器人数据.xlsx"
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_robots.to_excel(writer, sheet_name='机器人基本信息', index=False)
        df_stocks.to_excel(writer, sheet_name='持仓股票信息', index=False)

    print(f"✅ 数据已成功保存到：{output_path}")

else:
    print("未收到有效响应或状态码错误")


# # 示例调用
# if __name__ == "__main__":
#     result = robot_list()
#     if result:
#         print("响应数据：")
#         print(json.dumps(result, indent=4, ensure_ascii=False))
#     else:
#         print("未收到有效响应")
