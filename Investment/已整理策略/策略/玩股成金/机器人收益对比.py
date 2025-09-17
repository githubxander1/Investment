import requests
import json
import pandas as pd
from datetime import datetime

# 工具函数：时间戳转换
def convert_timestamp(timestamp):
    if timestamp and timestamp > 0:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
    return None

# 通用请求函数
def fetch_data(url, headers, data):
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 获取机器人列表
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
    return fetch_data(url, headers, payload)

# 获取机器人详情（不包括持仓）
def fetch_robot_detail(robot_id):
    url = "http://ai.api.traderwin.com/api/ai/robot/get.json"
    headers = {
        "Content-Type": "application/json",
        "token": "5a66427c4cc7054622909acafc31d2a6",
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Accept": "*/*",
        "Host": "ai.api.traderwin.com",
        "Connection": "keep-alive"
    }
    payload = {
        "cmd": "9015",
        "robotId": robot_id
    }
    return fetch_data(url, headers, payload)

# 提取机器人基础信息
def extract_robot_base_info(data):
    if not data or 'data' not in data:
        return None

    robot_data = data['data']
    startFunds = robot_data.get("startFunds")
    todayTotalRate  = robot_data.get("todayTotalRate")
    winRate = round(((todayTotalRate - startFunds)/startFunds) * 100, 2)
    gain = todayTotalRate - startFunds
    return {
        "机器人ID": robot_data.get("robotId"),
        "名称": robot_data.get("name"),
        "总收益": gain,
        "总收益率": winRate,
        "今日收益率": round(robot_data.get("todayRate"),2),
        "总资产": robot_data.get("todayTotalRate"),
        "当前可用资金": robot_data.get("funds"),
        "本月资产": robot_data.get("amountOfMonth"),
        "本年资产": robot_data.get("amountOfYear"),
        # "风险等级": robot_data.get("risk"),
        "初始资金": robot_data.get("startFunds"),
        "总市值": robot_data.get("marketValue"),
        "卖出收益": robot_data.get("sellGains"),
        "止损比例": robot_data.get("stopLost"),
        "止盈比例": robot_data.get("stopWin"),
        "收益更新时间": convert_timestamp(robot_data.get("gainDate")),
        "创建时间": convert_timestamp(robot_data.get("created"))

    }

# 保存所有机器人基础信息到 Excel
def save_all_robots_details_to_excel(robot_ids):
    all_robots_df = pd.DataFrame()

    total = len(robot_ids)
    for idx, robot_id in enumerate(robot_ids, 1):
        print(f"正在获取第 {idx} / {total} 个机器人详情... robot_id={robot_id}")
    # with pd.ExcelWriter('所有机器人基础信息详情.xlsx', engine='openpyxl') as writer:
    #     for robot_id in robot_ids:
        detail_data = fetch_robot_detail(robot_id)
        base_info = extract_robot_base_info(detail_data)
        if base_info:
            df = pd.DataFrame([base_info])
            all_robots_df = pd.concat([all_robots_df, df], ignore_index=True)
            # 按总收益率降序排序
            all_robots_df = all_robots_df.sort_values(by='总收益率', ascending=False)
            # sheet_name = f"Robot_{robot_id[-6:]}"  # 避免sheet名过长

            # df.to_excel(writer, sheet_name=sheet_name, index=False)
    if not all_robots_df.empty:
        output_path = '所有机器人对比.xlsx'
        all_robots_df.to_excel(output_path, index=False, sheet_name='机器人对比')
        print("✅ 所有机器人基础信息已保存到 Excel 文件")
    else:
        print("没有提取到任何机器人数据")

# 主流程
if __name__ == "__main__":
    result = robot_list()
    if result and result.get("message", {}).get("state") == 0:
        data = result.get("data", [])
        robot_ids = [robot.get("robotId") for robot in data if robot.get("robotId")]
        if robot_ids:
            save_all_robots_details_to_excel(robot_ids)
        else:
            print("未获取到机器人ID列表")
    else:
        print("未收到有效响应或状态码错误")
