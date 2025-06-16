import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import Combination_holding_file, ETF_ids, Combination_ids, \
    Combination_ids_to_name, ETF_ids_to_name
from Investment.THS.AutoTrade.utils.determine_market import determine_market


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

        holding_data = []
        for position in positions:
            code = position.get("code", "")
            market = determine_market(code)
            holding_info = {
                '组合名称': id_to_name.get(id, '未知ETF'),
                "股票代码": code,
                "股票名称": position.get("name", ""),
                "市场": market,
                "成本价": position["costPrice"],
                "当前价格": position["price"],
                "收益率(%)": position.get("incomeRate", 0) * 100,
                "盈亏比例(%)": position.get("profitLossRate", 0) * 100,
                "实际持仓比例(%)": position.get("positionRealRatio", 0) * 100,
            }
            holding_data.append(holding_info)

        df = pd.DataFrame(holding_data)
        return df
    else:
        print(f"请求失败，状态码: {response.status_code}，id: {id}")
        return pd.DataFrame()


def save_results_to_csv(holding_data, filename, mode='a', header=True):
    if mode == 'a' and os.path.exists(filename):
        header = False
    holding_data.to_csv(filename, mode=mode, header=header, index=False)
    print(f"持仓结果已保存到 {filename}")


if __name__ == '__main__':
    all_dfs = []

    # 处理ETF组合持仓数据
    for id in ETF_ids:
        df = get_portfolio_holding_data(id, ETF_ids_to_name)
        if not df.empty:
            all_dfs.append(df)

    # 合并所有DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)

    # 保存为CSV文件
    file_path = Combination_holding_file.replace('.xlsx', '.csv')
    save_results_to_csv(final_df, file_path, mode='w', header=True)

    # 处理股票组合持仓数据
    all_dfs = []  # 重置 all_dfs
    for id in Combination_ids:
        df = get_portfolio_holding_data(id, Combination_ids_to_name)
        if not df.empty:
            all_dfs.append(df)

    # 合并所有DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)

    # 保存为CSV文件
    save_results_to_csv(final_df, file_path, mode='a', header=False)

    # 打印最终的DataFrame
    print(final_df)
