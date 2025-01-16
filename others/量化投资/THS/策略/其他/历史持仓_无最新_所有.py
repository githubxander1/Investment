import logging
from pprint import pprint
import os
import requests
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(levelname)s-%(message)s")

def get_strategy_details_by_id(strategy_id):
    """
    根据策略ID获取策略详情信息
    """
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/detail"
    headers = {
        "Host": "ms.10jqka.com.cn",
        "Connection": "keep-alive",
        "Origin": "https://bowerbird.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Accept": "*/*",
        "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/15f2E0a579?strategyId=155259",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    params = {
        "strategyId": strategy_id,
    }
    response = requests.get(url, headers=headers, params=params)

    # 判断请求是否成功（状态码为200表示成功）
    if response.status_code != 200:
        logging.warning(f"Failed to fetch data for strategy ID {strategy_id}. Status code: {response.status_code}")
        return {}

    try:
        # extract_data = []
        result = response.json()['result']
        # pprint(result)
        if not result:
            logging.warning(f"Failed to fetch data for strategy ID {strategy_id}. Status code: {response.status_code}")
            return {}
        return {
            "策略ID": strategy_id,
            "策略名称": result["strategyName"],
            "描述": result["description"],
            "说明": result["investIdea"],
            "周期": result["investPeriod"],
            "风格": result["investStyle"],
            "子风格": result["subType"],
        }
    except Exception as e:
        logging.error(f"Error processing data for strategy ID {strategy_id}: {str(e)}")
        return {}

# pprint(get_strategy_details_by_id(155259))

def fetch_history_position_data(strategy_id, pages):
    """
    根据策略ID和页数获取历史持仓位置数据
    """
    base_url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/history_position?"
    headers = {
        "Host": "ms.10jqka.com.cn",
        "Connection": "keep-alive",
        "Origin": "https://bowerbird.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme=0 innerversion=G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Accept": "*/*",
        "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/7C958511F8?strategyId=155259",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    all_position_data = []
    for page in range(pages):
        url = f"{base_url}strategyId={strategy_id}&page={page}&pageSize=10"
        response = requests.get(url, headers=headers)

        # 判断请求是否成功（状态码为200）
        if response.status_code == 200:
            data = response.json()
            position_data = data["result"]["datas"]
            all_position_data.extend(position_data)
        else:
            logging.warning(f"请求失败，状态码: {response.status_code}")
            break
    return all_position_data

def determine_market(stock_code):
    """
    根据股票代码判断所属市场
    """
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('300'):
        return '创业板'
    elif stock_code.startswith(('4', '8')):
        return '北交所'
    else:
        return '其他'

def extract_important_info(position_data, strategy_id):
    """
    从持仓位置数据中提取重要信息，并结合策略详情信息
    """
    important_info = []
    strategy_details = get_strategy_details_by_id(strategy_id)
    for position in position_data:
        position_date = position["positionDate"]

        for stock in position["positionStocks"]:
            profitAndLossRatio = round(stock['profitAndLossRatio'] * 100, 2)

            stkCode = stock['stkCode']
            important_info.append({
                "策略ID": strategy_id,
                "策略名称": strategy_details.get("策略名称"),
                "描述": strategy_details.get("描述"),
                "说明": strategy_details.get("说明"),
                "周期": strategy_details.get("周期"),
                "风格": strategy_details.get("风格"),
                "子风格": strategy_details.get("子风格"),
                "持仓日期": position_date,
                "股票代码": stock["stkCode"],
                "股票名称": stock["stkName"],
                "行业": stock["industry"],
                "市场": determine_market(stkCode),
                "持仓比例%": round(stock["positionRatio"] * 100, 2),
                "价格": stock["price"],
                "收益率%": profitAndLossRatio,
            })
    return important_info

def calculate_strategy_stats(all_important_info):
    """
    计算每个策略的收益率大于0和小于0的个数以及胜率
    """
    strategy_stats = {}
    for info in all_important_info:
        strategy_id = info["策略ID"]
        if strategy_id not in strategy_stats:
            strategy_stats[strategy_id] = {
                "策略名称": info["策略名称"],
                "收益>0个数": 0,
                "收益<0个数": 0,
                "总股票数": 0,
            }
        if info["收益率%"] > 0:
            strategy_stats[strategy_id]["收益>0个数"] += 1
        elif info["收益率%"] < 0:
            strategy_stats[strategy_id]["收益<0个数"] += 1
        strategy_stats[strategy_id]["总股票数"] += 1

    for strategy_id, stats in strategy_stats.items():
        total_stocks = stats["总股票数"]
        positive_count = stats["收益>0个数"]
        negative_count = stats["收益<0个数"]
        win_rate = (positive_count / total_stocks) * 100 if total_stocks > 0 else 0
        stats["胜率%"] = round(win_rate, 2)

    return list(strategy_stats.values())

def save_data_to_excel(all_important_info, strategy_ids, file_path):
    """
    将整合好的重要信息保存到Excel文件中，每个策略的数据存为一个工作表，并添加一个统计工作表
    """
    with pd.ExcelWriter(file_path) as writer:
        for strategy_id in strategy_ids:
            df = pd.DataFrame([info for info in all_important_info if info["策略ID"] == strategy_id])
            strategy_details = get_strategy_details_by_id(strategy_id)
            if strategy_details:
                sheet_name = strategy_details.get("策略名称", f'Strategy_{strategy_id}')
            else:
                sheet_name = f'Strategy_{strategy_id}'
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # 添加统计信息工作表
        strategy_stats = calculate_strategy_stats(all_important_info)
        df_stats = pd.DataFrame(strategy_stats)
        df_stats.to_excel(writer, sheet_name='策略统计', index=False)

def main():
    """
    主函数，整合各个功能函数，完成数据获取、处理和保存的整体流程
    """
    strategy_ids = ['155259', '155270', '137789', '118188',
                    '155680', '138006', '138036', '138127']
    pages_to_download = 10  # 例如，下载2页数据
    all_important_info = []

    for strategy_id in strategy_ids:
        position_data = fetch_history_position_data(strategy_id, pages_to_download)
        important_info = extract_important_info(position_data, strategy_id)
        all_important_info.extend(important_info)

    file_path = r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\策略\策略保存的数据\历史持仓信息_所有.xlsx"
    save_data_to_excel(all_important_info, strategy_ids, file_path)
    print("历史持仓信息已成功保存到 '历史持仓信息_所有.xlsx' 文件中。")

if __name__ == "__main__":
    main()
