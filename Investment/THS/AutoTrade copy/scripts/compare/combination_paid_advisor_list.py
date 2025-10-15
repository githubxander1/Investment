from pprint import pprint

import requests
import pandas as pd
from datetime import datetime

from config.settings import Combination_headers, combination_paid_advisor_list_file


def fetch_portfolio_data(block_id):
    """发送GET请求并获取投资组合数据"""
    # 定义请求URL和headers
    url = "https://dq.10jqka.com.cn/fuyao/portfolio_game/portfolio/v1/all_income_rank_list"
    headers = Combination_headers
    params = {
        "offset": 0,
        "page_size": 20,
        "block_id": block_id,
        "list_type": 4,
        "match_id": -1
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.RequestException as e:
        print(f"请求数据时出错: {e}")
        return None


def extract_key_data(json_data, block_name):
    """从JSON数据中提取关键信息，并添加block_name"""
    if not json_data or "data" not in json_data or "list" not in json_data["data"]:
        print("数据格式不正确或缺少关键字段")
        return []

    portfolios = json_data["data"]["list"]
    # print(f"获取 {block_name} 的投资组合数据")
    # pprint(portfolios)
    key_data = []
    # update_time = portfolios["update_time"]
    # print(f"数据更新时间: {update_time}")

    for portfolio in portfolios:
        # 提取基础信息，并添加block_name
        portfolio_info = {
            "排名": portfolio.get("rank"),
            "投资组合ID": portfolio.get("portfolio_id"),
            "投资组合名称": portfolio.get("portfolio_name"),
            "总收益率": round(portfolio.get("income_rate") * 100, 2),
            "更新时间": json_data["data"]["update_time"],
            "板块名称": block_name,  # 添加block_name
            "累计抓涨停次数": next((label.get("label") for label in portfolio.get("portfolio_labels", [])
                                    if "累计抓涨停" in label.get("label", "")), "0次"),
            "用户名称": portfolio.get("user_info", {}).get("user_name"),
            # "用户ID": portfolio.get("user_info", {}).get("user_id"),
        }

        # 提取最佳持仓信息
        best_holding = portfolio.get("bestHolding", {})
        if best_holding:
            portfolio_info["最佳持仓股票"] = best_holding.get("stockName", "无")
            portfolio_info["最佳持仓收益率"] = best_holding.get("profitRate", 0)
            portfolio_info["最佳持仓代码"] = best_holding.get("stockCode", "无")

        # 提取最近调仓信息
        # relocation = portfolio.get("relocation", {})
        # portfolio_info["调仓时间"] = relocation.get("date", "无") if relocation else "无"
        # portfolio_info["调仓价格"] = relocation.get("price", "无") if relocation else "无"
        # portfolio_info["调仓类型"] = relocation.get("type", "无") if relocation else "无"
        # portfolio_info["调仓股票"] = relocation.get("stock_name", "无") if relocation else "无"
        # portfolio_info["标的代码"] = relocation.get("stock_code", "无") if relocation else "无"
        # portfolio_info["调仓理由"] = relocation.get("reason", "无") if relocation else "无"
        # portfolio_info["调仓收益率"] = round(relocation.get("profit_loss_rate", 0) * 100, 2) if relocation else "无"

        # 提取最近的收益数据
        income_echarts = portfolio.get("income_echarts", [])
        if income_echarts:
            portfolio_info["最新收益日期"] = income_echarts[-1].get("date", "无")
            portfolio_info["最新收益率"] = income_echarts[-1].get("income_rate", 0)

        key_data.append(portfolio_info)

    return key_data


def main():
    # 发送请求并获取数据
    block_id = {
        "精选": 0,
        "可控核聚变": 886065,
        "中国A50": 886102,
        "固态电池": 886032,
        "芯片概念": 885756,
        "人形机器人": 886069,
    }
    all_data = []  # 用于存储所有数据的列表

    for name, id in block_id.items():
        print(f"正在获取{name}投资组合数据...")
        json_data = fetch_portfolio_data(id)
        # pprint(json_data)

        # 提取关键数据，传入block_name
        key_data = extract_key_data(json_data, name)
        if not key_data:
            print("未提取到有效数据")
            continue

        # 将提取的数据直接添加到all_data列表中
        all_data.extend(key_data)  # 使用extend将列表中的每个元素都添加进去

    # 如果有数据，则进行排序和保存
    if all_data:
        # 将所有数据转换为DataFrame
        df = pd.DataFrame(all_data)

        # 按总收益率倒序排序
        df = df.sort_values(by="总收益率", ascending=False)

        # 保存到xlsx文件，使用固定的sheet_name
        filename = combination_paid_advisor_list_file
        df.to_excel(filename, sheet_name="所有投资组合排名", index=False)
        print(f"\n数据已保存至 {filename}")
        print("\n==== 投资组合排名关键数据 (按总收益率倒序) ====")
        print(df)
    else:
        print("没有获取到任何有效数据")


if __name__ == "__main__":
    main()
