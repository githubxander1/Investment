import pandas as pd
import requests
from others.Investment.THS.AutoTrade.utils.determine_market import determine_market

from others.Investment.THS.AutoTrade.config.settings import ETF_ids, ETF_ids_to_name, ETF_adjustment_holding_file, \
    all_ids, id_to_name


def get_portfolio_holding_data(id):
    url = f"https://t.10jqka.com.cn/portfolio/relocate/user/getPortfolioHoldingData?id={id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://t.10jqka.com.cn/portfolio/relocate/user/index?id=6994",
        'cookie': 'hxmPid=cot_mkt_conf_20240416_63095; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM1Nzk4NTQxOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTkzMWYxMzQxYzIwODVlNTZkZDE2NmFjNDdhNzA5NmE1Ojox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c5bc8d322763afbfb6bdc4c9f43381ce; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; v=A97ICdweNXX3q2GRIhA9tWEUJn8gn6IQNGNW_YhnSiEcq3El8C_yKQTzph5b'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # pprint(testdata)
        positions = data["result"]["positions"]
        total_funds = data["result"]["totalFunds"]

        # code = [position.get("code", "") for position in positions]

        for position in positions:
            code = position.get("code", "")
            market = determine_market(code)  # 每个 code 都是字符串
            # 构造每一行的数据
            df = pd.DataFrame({
                "组合名称": id_to_name.get(id, '未知组合'),
                "股票代码": str(code).zfill(6),
                "股票名称": position.get("name", ""),
                "市场": market,
                "成本价": position["costPrice"],
                "当前价格": position["price"],
                "收益率(%)": position.get("incomeRate", 0) * 100,
                "盈亏比例(%)": position.get("profitLossRate", 0) * 100,
                "实际持仓比例(%)": position.get("positionRealRatio", 0) * 100,
            }, index=[0])  # 添加 index=[0] 以避免空索引警告
            all_dfs.append(df)
        # market = determine_market(code)
        # df = pd.DataFrame({
        #     # "id": [id] * len(positions),
        #     "组合名称": id_to_name.get(id, '未知组合'),
        #     "股票代码": str(code).zfill(6),
        #     "股票名称": [position.get("name", "") for position in positions],
        #     "市场": market,
        #     "成本价": [position["costPrice"] for position in positions],
        #     "当前价格": [position["price"] for position in positions],
        #     "收益率(%)": [position.get("incomeRate", 0) * 100 for position in positions],
        #     "盈亏比例(%)": [position.get("profitLossRate", 0) * 100 for position in positions],
        #     "实际持仓比例(%)": [position.get("positionRealRatio", 0) * 100 for position in positions],
        #     # "持仓比例(%)": [position.get("positionRelocatedRatio", 0) * 100 for position in positions],
        #     # "市场代码": [position["marketCode"] for position in positions],
        #     # "冻结比例": [position["freezeRatio"] for position in positions],
        #     # "状态": [position["state"] for position in positions],
        #     # "类型": [position["type"] for position in positions],
        #     # "总资金": [total_funds] * len(positions),
        # })
        #
        # all_dfs.append(df)
    else:
        print(f"请求失败，状态码: {response.status_code}，id: {id}")

if __name__ == '__main__':
    # 多个id
    # combination_ids = [6994, 7152, 18710, 16281, 19347, 13081, 14980]
    # combination_ids = [6994]

    # id_to_name = {
    #     13081:'好赛道出牛股',
    #     16281:'每天进步一点点',
    #     18565:'龙头一年三倍',
    #     7152:'中线龙头',
    #     6994:'梦想一号' ,
    #     11094:'低位题材',
    #     14980:'波段突击',
    #     19347:'超短稳定复利',
    #     18710:'用收益率征服您'}
    # 存储所有结果的列表
    all_dfs = []

    for id in all_ids:
        get_portfolio_holding_data(id)
    # 合并所有DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)

    # 保存为Excel文件
    file_path = ETF_adjustment_holding_file
    final_df.to_excel(file_path, index=False)
    print("数据已保存到Excel文件：", file_path)

    # 打印最终的DataFrame
    print(final_df)