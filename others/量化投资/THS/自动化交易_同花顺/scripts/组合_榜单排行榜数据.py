import pandas as pd
import requests


def get_all_portfolio_rank_data(list_type):
    url = "https://t.10jqka.com.cn/portfoliolist/tgserv/v1/blockList"

    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/tgactivity/portfolioSquare.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0,ExLDQwOzYsMS,0MDs1,ExsNDA7MS,xMDEsNDA7Mi,xLDQwOzMs,ExsNDA7NS,ExsNDA7OC,wwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIs,ExsNDAoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=hqMarketPkgVersionControl; v=A8nfSB_XyhoyhrZuY3TPETuT0f4jFr1OJw_h3Gs-RF3vQeZks2bNGLda8aP4",
        "X-Requested-With": "com.hexin.plat.android"
    }

    params = {
        "offset": 0,
        "pageSize": 50,
        "matchId": 0,
        "blockId": 0,
        "listType": list_type
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
    list_data = data["result"]["list"]
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

def save_to_excel(df, writer, sheet_name):
    """Helper function to save DataFrame to Excel with a given sheet name."""
    try:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"{sheet_name} 数据已保存")
    except Exception as e:
        print(f"保存 {sheet_name} 数据时出错: {e}")

def process_and_save_data(file_path, list_types):
    """Process and save portfolio rank testdata to an Excel file."""

    with pd.ExcelWriter(file_path) as writer:
        for list_type, sheet_name in list_types.items():
            # 获取并处理数据
            raw_data = get_all_portfolio_rank_data(list_type)
            out_put_data = extract_data(raw_data)

            if out_put_data:
                # 将数据转换为 DataFrame 并保存到 Excel
                df = pd.DataFrame(out_put_data)
                save_to_excel(df, writer, sheet_name)

                # 提取前二十条数据
                # pprint(raw_data)
                top20_data = out_put_data[:20]
                # out_put_data20 = extract_data(top20_data)
                # 处理所有前二十条数据
                if top20_data:
                    df20 = pd.DataFrame(top20_data)
                    save_to_excel(df20, writer, f"{sheet_name} 前二十")
                else:
                    print(f"{sheet_name} 前二十条数据保存失败")
            else:
                print(f"请求失败，listType: {list_type}, {sheet_name} 数据保存失败")


# 示例调用
if __name__ == '__main__':
    file_path = r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\data\榜单排行榜数据.xlsx"
    list_types = {
        # 1: "日收益",
        # 2: "周收益",
        3: "月收益",
        4: "总收益"
    }
    # process_and_save_data(file_path, list_types)

    extract_da = extract_data(get_all_portfolio_rank_data(4))
    portfolio_ids = [item["组合id"] for item in extract_da][:20]
    print(portfolio_ids)
