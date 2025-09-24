from pprint import pprint

import requests
import pandas as pd
from datetime import datetime

from Investment.THS.AutoTrade.config.settings import Combination_headers

# 定义请求URL和headers
url = "https://dq.10jqka.com.cn/fuyao/portfolio_game/portfolio/v1/all_income_rank_list"
# headers = {
#     "accept": "application/json, text/plain, */*",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "content-type": "application/x-www-form-urlencoded",
#     "sec-ch-ua": "\"Chromium\";v=\"129\", \"Not=A?Brand\";v=\"8\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site",
#     "referrer": "https://t.10jqka.com.cn/",
#     "referrerPolicy": "strict-origin-when-cross-origin"
# }
headers = Combination_headers
params = {
    "offset": 0,
    "page_size": 8,
    "block_id": 0,
    "list_type": 4,
    "match_id": -1
}

def fetch_portfolio_data(url, headers, params):
    """发送GET请求并获取投资组合数据"""
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.RequestException as e:
        print(f"请求数据时出错: {e}")
        return None

def extract_key_data(json_data):
    """从JSON数据中提取关键信息"""
    if not json_data or "data" not in json_data or "list" not in json_data["data"]:
        print("数据格式不正确或缺少关键字段")
        return []

    portfolios = json_data["data"]["list"]
    key_data = []
    # update_time = portfolios["update_time"]
    # print(f"数据更新时间: {update_time}")


    for portfolio in portfolios:
        # 提取基础信息
        portfolio_info = {
            "排名": portfolio.get("rank"),
            "投资组合ID": portfolio.get("portfolio_id"),
            "投资组合名称": portfolio.get("portfolio_name"),
            "总收益率": round(portfolio.get("income_rate") * 100, 2),
            "更新时间": json_data["data"]["update_time"],
            # "用户名称": portfolio.get("user_info", {}).get("user_name"),
            # "用户ID": portfolio.get("user_info", {}).get("user_id"),
            "累计抓涨停次数": next((label.get("label") for label in portfolio.get("portfolio_labels", [])
                                    if "累计抓涨停" in label.get("label", "")), "0次"),
        }

        # 提取最佳持仓信息
        # best_holding = portfolio.get("bestHolding", {})
        # portfolio_info["最佳持仓股票"] = best_holding.get("stockName", "无")
        # portfolio_info["最佳持仓收益率"] = best_holding.get("profitRate", 0)
        # portfolio_info["最佳持仓代码"] = best_holding.get("stockCode", "无")

        # 提取最近调仓信息
        relocation = portfolio.get("relocation", {})
        portfolio_info["调仓类型"] = relocation.get("type", "无") if relocation else "无"
        portfolio_info["调仓股票"] = relocation.get("stock_name", "无") if relocation else "无"
        portfolio_info["标的代码"] = relocation.get("stock_code", "无") if relocation else "无"
        portfolio_info["调仓收益率"] = round(relocation.get("profit_loss_rate", 0) * 100, 2) if relocation else "无"

        # 提取最近的收益数据
        income_echarts = portfolio.get("income_echarts", [])
        if income_echarts:
            portfolio_info["最新收益日期"] = income_echarts[-1].get("date", "无")
            portfolio_info["最新收益率"] = income_echarts[-1].get("income_rate", 0)

        key_data.append(portfolio_info)

    return key_data

def main():
    # 发送请求并获取数据
    json_data = fetch_portfolio_data(url, headers, params)
    # pprint(json_data)
    if not json_data:
        return

    # 提取关键数据
    key_data = extract_key_data(json_data)
    if not key_data:
        print("未提取到有效数据")
        return

    # 将数据转换为DataFrame
    df = pd.DataFrame(key_data)

    # 展示DataFrame
    print("\n==== 投资组合排名关键数据 ====")
    print(df)

    # 保存数据到CSV文件（可选）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"portfolio_ranking_{timestamp}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"\n数据已保存至 {filename}")

if __name__ == "__main__":
    main()
