# 修改后的 Robot_holding.py
import pandas as pd
import akshare as ak
import os
from datetime import datetime
import time
import random
import requests
import json

# 所有股票信息文件路径
ALL_STOCKS_FILE = 'all_stocks.xlsx'

# 全局变量存储股票信息
all_stocks_df = None

def load_all_stocks():
    """加载所有股票信息到内存中"""
    global all_stocks_df

    # 首先尝试从本地Excel文件加载股票信息
    if os.path.exists(ALL_STOCKS_FILE):
        try:
            print("正在从本地Excel文件加载股票信息...")
            all_stocks_df = pd.read_excel(ALL_STOCKS_FILE)
            print(f"从本地Excel文件成功加载 {len(all_stocks_df)} 条股票信息")
            return
        except Exception as e:
            print(f"从本地Excel文件加载股票信息失败: {e}")

    # 如果本地文件不存在或加载失败，则从网络获取
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"正在尝试通过 stock_zh_a_spot 获取所有股票信息... (第 {attempt + 1} 次尝试)")
            # 添加随机延迟，避免请求过于频繁
            time.sleep(random.uniform(1, 2))

            # 使用stock_zh_a_spot获取所有股票信息
            all_stocks_df = ak.stock_zh_a_spot()

            # 保存到Excel文件供以后使用
            all_stocks_df.to_excel(ALL_STOCKS_FILE, index=False)
            print(f"已保存所有股票信息到 {ALL_STOCKS_FILE}")
            print(f"通过 stock_zh_a_spot 成功获取 {len(all_stocks_df)} 条股票信息")
            return

        except Exception as e:
            print(f"第 {attempt + 1} 次尝试获取股票信息失败: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            continue

    print("所有方法都失败，无法获取股票信息")
    all_stocks_df = pd.DataFrame()

def get_stock_name_by_code(code):
    """根据股票代码获取股票名称"""
    global all_stocks_df

    if all_stocks_df is None or all_stocks_df.empty:
        return f"未知股票({code})"

    # 查找匹配的股票代码
    matching_stocks = all_stocks_df[all_stocks_df['代码'] == code]
    if not matching_stocks.empty:
        return matching_stocks.iloc[0]['名称']

    # 如果6位代码没找到，尝试添加市场前缀查找
    if not code.startswith(('sh', 'sz')):
        # 尝试上海市场
        sh_code = f"sh{code}" if code.startswith('6') else f"sz{code}"
        matching_stocks = all_stocks_df[all_stocks_df['代码'] == sh_code]
        if not matching_stocks.empty:
            return matching_stocks.iloc[0]['名称']

    return f"未知股票({code})"

def fetch_robot_data(robot_id, token="27129c04fb43a33723a9f7720f280ff9"):
    """获取单个机器人的数据"""
    url = "http://ai.api.traderwin.com/api/ai/robot/get.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": token,
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    payload = {
        "cmd": "9015",
        "robotId": robot_id
    }

    # 增加重试机制
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            response.raise_for_status()
            response_json = response.json()
            # pprint(response_json)
            return response_json
        except requests.RequestException as e:
            print(f"第 {attempt + 1} 次尝试，请求机器人 {robot_id} 数据失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                return None

def extract_robot_data(response_data):
    """提取机器人数据并转换为 DataFrame"""
    if not response_data or 'data' not in response_data:
        print("无效的响应数据")
        return pd.DataFrame(), pd.DataFrame()

    data = response_data['data']

    # 提取组合基本信息
    combo_info = {
        "组合名称": data.get('name', ''),
        "总收益率": data.get('currentTotalRate', ''),
        "今日盈亏": data.get('todayGains', ''),
        "今日收益率": data.get('todayRate', ''),
        "累计盈亏": data.get('totalGains', ''),
        "累计收益率": data.get('totalRate', ''),
        "最新价": data.get('nowPrice', ''),
        "成本价": data.get('costPrice', ''),
        "创建时间": data.get('createTime', '')
    }

    # 提取持仓股票信息
    stocks_data = []
    for log in data.get('logs', []):
        symbol = log.get('symbol', '')
        symbol_name = log.get('symbolName', None)

        # 获取股票名称
        if symbol_name and symbol_name.strip() and symbol_name != 'None':
            stock_name = symbol_name.strip()
        else:
            # 从股票代码中提取纯数字部分用于查找名称
            code = symbol.replace('sh', '').replace('sz', '') if symbol.startswith(('sh', 'sz')) else symbol
            stock_name = get_stock_name_by_code(code)

        stock_item = {
            "股票代码": symbol,
            "股票名称": stock_name,
            "最新价": log.get('price', ''),
            "成本价": log.get('basePrice', ''),
            "持仓量": log.get('shares', ''),
            "市值": log.get('marketValue', ''),
            "今日盈亏": log.get('todayGains', ''),
            "累计盈亏": log.get('totalGains', ''),
            "今日收益率": (log.get('todayGains', 0) / log.get('todayCost', 1)) * 100 if log.get('todayCost', 0) != 0 else 0,
            "累计收益率": (log.get('totalGains', 0) / log.get('lockCost', 1)) * 100 if log.get('lockCost', 0) != 0 else 0,
        }
        stocks_data.append(stock_item)

    # 将提取的数据转换为 DataFrame
    combo_df = pd.DataFrame([combo_info])
    stocks_df = pd.DataFrame(stocks_data)

    return combo_df, stocks_df

def main():
    # 加载所有股票信息
    load_all_stocks()

    # 机器人列表
    robots = {
        "有色金属": "8afec86a-e573-411a-853f-5a9a044d89ae",
        "钢铁": "89c1be35-08a6-47f6-a8c9-1c64b405dab6",
        "建筑行业": "ca2d654c-ab95-448e-9588-cbc89cbb7a9e"
    }

    # 创建一个Excel写入器
    with pd.ExcelWriter('机器人详情.xlsx', engine='openpyxl') as writer:
        # 遍历所有机器人
        for robot_name, robot_id in robots.items():
            print(f"正在获取 {robot_name} 的数据...")

            # 获取机器人数据
            response_data = fetch_robot_data(robot_id)

            if response_data and response_data.get("message", {}).get("state") == 0:
                # 提取数据
                combo_df, stocks_df = extract_robot_data(response_data)

                # 以机器人的名称作为工作表名保存数据
                # 确保工作表名称不超过31个字符
                combo_sheet_name = f"{robot_name}_组合信息"[:31]
                stocks_sheet_name = f"{robot_name}_持仓信息"[:31]

                # 保存到Excel的不同工作表
                if not combo_df.empty:
                    combo_df.to_excel(writer, sheet_name=combo_sheet_name, index=False)
                    print(f"已保存 {robot_name} 的组合信息到工作表 {combo_sheet_name}")

                if not stocks_df.empty:
                    stocks_df.to_excel(writer, sheet_name=stocks_sheet_name, index=False)
                    print(f"已保存 {robot_name} 的持仓信息到工作表 {stocks_sheet_name}")
            else:
                print(f"获取 {robot_name} 数据失败")

    print("所有机器人的数据已保存到 '机器人详情.xlsx' 文件中")

# 运行主函数
if __name__ == "__main__":
    main()
    name = get_stock_name_by_code("bj430017")
    print(name)
