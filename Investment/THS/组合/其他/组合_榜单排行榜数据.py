import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import Combination_list_file, Combination_headers


def get_all_portfolio_rank_data(match_id):
    # url = "https://t.10jqka.com.cn/portfoliolist/tgserv/v1/subTab?match_id=0"
    url = "https://t.10jqka.com.cn/portfoliolist/tgserv/v2/block_list"

    headers = Combination_headers

    params = {
        "match_id": match_id,#0 为全国总榜 14为ETF，15为智投杯投顾比赛
        "offset": 0,
        "page_size": 20,
        "block_id": 0,
        "list_type": 4
    }

    # 发送GET请求
    response = requests.get(url, params=params, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"接口请求失败，状态码: {response.status_code}")

def extract_data(data):
    list_data = data["data"]["list"]
    # pprint(list_data)

    extract_data = []
    for item in list_data:
        portfolio_labels = item["portfolio_labels"]
        # 判断 portfolio_labels 的长度
        if len(portfolio_labels) > 1:
            grab_tzt_count = portfolio_labels[1].get("label")
        elif len(portfolio_labels) == 1:
            grab_tzt_count = portfolio_labels[0].get("label")  # 或者设置默认值，如 None 或 ""
        else:
            grab_tzt_count = None  # 如果没有 label，设置为 None
        extract_data.append(
            {
                "排名": item["rank"],
                # "排名变化": item["rank_change"],
                "组合id": item["portfolio_id"],
                "组合名称": item["portfolio_name"],
                "组合作者": item["user_info"].get("user_name"),
                "作者id": item["user_info"].get("user_id"),
                "组合收益": f'{item["income_rate"] * 100:.2f}%',
                "标签": grab_tzt_count
            }
        )
    return extract_data

# 使用 ExcelWriter 将数据写入同一个 Excel 文件的不同 Sheet
# 定义 listType 和对应的 Sheet 名称
print("开始爬取数据...")

# def save_to_excel(df, writer, sheet_name):
#     """Helper function to save DataFrame to Excel with a given sheet name."""
#     try:
#         df.to_excel(writer, sheet_name=sheet_name, index=False)
#         print(f"{sheet_name} 数据已保存")
#     except Exception as e:
#         print(f"保存 {sheet_name} 数据时出错: {e}")

def process_and_save_data(file_path, match_ids):
    """
    将多个 match_id 的数据写入同一个 Excel 文件的不同 Sheet 中

    :param file_path: 输出文件路径（.xlsx）
    :param match_ids: {match_id: sheet_name} 字典
    """
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        for match_id, sheet_name in match_ids.items():
            raw_data = get_all_portfolio_rank_data(match_id)
            out_put_data = extract_data(raw_data)

            if out_put_data:
                df = pd.DataFrame(out_put_data)
                print(df)
                # df.to_excel(writer, sheet_name=sheet_name, index=False)
                # print(f"✅ [{sheet_name}] 数据已保存")
            else:
                print(f"❌ 请求失败，{sheet_name} 数据未保存")




if __name__ == '__main__':
    file_path = Combination_list_file.replace('.csv', '.xlsx')  # 修改为 .xlsx 格式
    print(f'数据保存地址: {file_path}')

    match_ids = {
        0: "全国总榜",
        14: "ETF",
        15: "智投杯"
    }

    process_and_save_data(file_path, match_ids)

    # 示例：获取智投杯前20组合ID
    raw_data = get_all_portfolio_rank_data(15)  # 获取智投杯数据
    extract_da = extract_data(raw_data)
    portfolio_ids = [item["组合id"] for item in extract_da][:20]
    print("Top 20 组合ID:", portfolio_ids)


