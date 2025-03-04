from pprint import pprint

import pandas as pd
import requests

from others.量化投资.THS.自动化交易_同花顺.config.settings import ETF_adjustment_holding_file, ETF_ids, Combination_ids, \
    Combination_ids_to_name, ETF_ids_to_name


def get_portfolio_holding_data(id, id_to_name):
    url = f"https://t.10jqka.com.cn/portfolio/relocate/user/getPortfolioHoldingData?id={id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://t.10jqka.com.cn/portfolio/relocate/user/index?id=6994",
        'cookie': 'hxmPid=cot_mkt_conf_20240416_63095; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM1Nzk4NTQxOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTkzMWYxMzQxYzIwODVlNTZkZDE2NmFjNDdhNzA5NmE1Ojox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c5bc8d322763afbfb6bdc4c9f43381ce; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; v=A97ICdweNXX3q2GRIhA9tWEUJn8gn6IQNGNW_YhnSiEcq3El8C_yKQTzph5b'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        positions = data["result"]["positions"]
        total_funds = data["result"]["totalFunds"]

        df = pd.DataFrame({
            '组合名称': id_to_name.get(id, '未知ETF'),
            "股票代码": [position.get("code", "") for position in positions],
            "股票名称": [position.get("name", "") for position in positions],
            "成本价": [position["costPrice"] for position in positions],
            "当前价格": [position["price"] for position in positions],
            "收益率(%)": [position.get("incomeRate", 0) * 100 for position in positions],
            "盈亏比例(%)": [position.get("profitLossRate", 0) * 100 for position in positions],
            "实际持仓比例(%)": [position.get("positionRealRatio", 0) * 100 for position in positions],
            # "持仓比例(%)": [position.get("positionRelocatedRatio", 0) * 100 for position in positions],
            # "市场代码": [position["marketCode"] for position in positions],
            # "冻结比例": [position["freezeRatio"] for position in positions],
            # "状态": [position["state"] for position in positions],
            # "类型": [position["type"] for position in positions],
            # "总资金": [total_funds] * len(positions),
        })

        all_dfs.append(df)
    else:
        print(f"请求失败，状态码: {response.status_code}，id: {id}")

def save_results_to_xlsx(relocation_data, holding_data, filename):
    # 检查文件是否存在
    try:
        with pd.ExcelFile(filename) as _:
            # 文件存在，追加模式
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                if relocation_data:
                    df_relocation = pd.DataFrame(relocation_data)
                    # print(df_relocation)
                    df_relocation.to_excel(writer, sheet_name='ETF组合调仓', index=False)
                    print(f"调仓结果已保存到 {filename}")
                else:
                    print("没有调仓数据")

                if holding_data:
                    df_holding = pd.DataFrame(holding_data)
                    # print(df_holding)
                    df_holding.to_excel(writer, sheet_name='ETF组合持仓', index=False)
                    print(f"持仓结果已保存到 {filename}")
                else:
                    print("没有持仓数据")
    except FileNotFoundError:
        # 文件不存在，创建新文件
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            if relocation_data:
                df_relocation = pd.DataFrame(relocation_data)
                # print(df_relocation)
                df_relocation.to_excel(writer, sheet_name='ETF组合调仓', index=False)
                print(f"调仓结果已保存到 {filename}")
            else:
                print("没有调仓数据")

            if holding_data:
                df_holding = pd.DataFrame(holding_data)
                # print(df_holding)
                df_holding.to_excel(writer, sheet_name='ETF组合持仓', index=False)
                print(f"持仓结果已保存到 {filename}")
            else:
                print("没有持仓数据")
# def main():
#     # all_relocation_data = []
#     # all_holding_data = []
#     all_dfs = []
#     for id in ETF_ids:
#     # for id in Combination_ids:
#         result = get_portfolio_holding_data(id)
#         pprint(result)
#         if not result or not result.get('result'):
#             print(f"ID {id} 返回无效数据")
#             continue  # 跳过无效数据
#
#         try:
#             relocation_data, holding_data, holding_count = extract_result(result, id)
#             # print(relocation_data)
#             # print(holding_data)
#             if relocation_data:
#                 all_dfs.extend(relocation_data)
#             if holding_data:
#                 all_holding_data.extend(holding_data)
#                 all_holding_data.extend(relocation_data)
#         except Exception as e:
#             print(f"处理ID {id} 时发生异常: {str(e)}")
#             continue
#
#     df = pd.DataFrame(all_holding_data)
#     print(df)
#
#     save_path = ETF_adjustment_holding_file
#     save_results_to_xlsx(all_relocation_data, all_holding_data, save_path)

if __name__ == '__main__':

    all_dfs = []

    # 处理ETF组合持仓数据
    for id in ETF_ids:
        get_portfolio_holding_data(id , ETF_ids_to_name)
    # 合并所有DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)

    # 保存为Excel文件
    file_path = ETF_adjustment_holding_file
    final_df.to_excel(ETF_adjustment_holding_file, sheet_name='ETF持仓',index=False)
    print("数据已保存到Excel文件：", file_path)

    # 处理股票组合持仓数据
    for id in Combination_ids:
        get_portfolio_holding_data(id, Combination_ids_to_name)
    # 合并所有DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)

    # 保存为Excel文件
    file_path = ETF_adjustment_holding_file
    final_df.to_excel(ETF_adjustment_holding_file, sheet_name='股票持仓',index=False)
    print("数据已保存到Excel文件：", file_path)
    # 打印最终的DataFrame
    print(final_df)