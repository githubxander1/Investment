import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import Combination_headers, Combination_list_file
from Investment.THS.组合.其他.组合_榜单排行榜数据 import extract_data


def fetch_and_save_to_sheet(writer, match_id, sheet_name):
    """
    获取榜单数据并写入 Excel 的指定 Sheet

    :param writer: pd.ExcelWriter 对象
    :param match_id: 榜单类型 ID（0=全球总榜，14=ETF，15=新比赛）
    :param sheet_name: sheet 名称
    """
    raw_data = get_all_portfolio_rank_data(match_id)
    if not raw_data:
        print(f"❌ {sheet_name} 数据获取失败")
        return

    out_put_data = extract_data(raw_data)

    if out_put_data:
        df = pd.DataFrame(out_put_data)
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"✅ [{sheet_name}] 数据已保存")

        # 保存前20条数据
        # top20_data = out_put_data[:20]
        # if top20_data:
        #     df_top20 = pd.DataFrame(top20_data)
        #     top20_sheet_name = f"{sheet_name}_前二十"
        #     df_top20.to_excel(writer, sheet_name=top20_sheet_name, index=False)
        #     print(f"✅ [{top20_sheet_name}] 数据已保存")
    else:
        print(f"❌ {sheet_name} 数据为空")


def get_all_portfolio_rank_data(match_id):
    """
    请求组合排行榜数据（支持不同 match_id）

    :param match_id: 比赛ID
    :return: JSON 响应数据或 None
    """
    url = "https://t.10jqka.com.cn/portfoliolist/tgserv/v2/block_list"

    headers = Combination_headers

    params = {
        "offset": 0,
        "page_size": 100,
        "match_id": match_id,
        "block_id": 0,
        "list_type": 4
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"接口请求失败，状态码: {response.status_code}")
        return None


# 示例调用
if __name__ == '__main__':
    file_path = Combination_list_file
    print(f'数据保存地址: {file_path}')

    list_config = {
        0: "全球总榜",
        14: "ETF榜单",
        15: "新比赛"
    }
    # pd.writer = pd.ExcelWriter(file_path, engine='openpyxl')
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for match_id, sheet_name in list_config.items():
            fetch_and_save_to_sheet(writer, match_id, sheet_name)
