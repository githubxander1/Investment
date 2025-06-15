import pandas as pd
import requests
from fake_useragent import UserAgent


def fetch_data():
    """
    获取北向资金 ETF 股票数据（原始 JSON 响应）
    """
    url = "https://apigate.10jqka.com.cn/d/hq/hshkconnect/etf/v1/list"
    params = {
        "type": "north",
        "sort_field": "rise",
        "sort_mode": "desc",
        "start_row": 0,
        "row_count": 10
    }

    headers = {
        "User-Agent": UserAgent().random
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求过程中发生错误: {e}")
        return None


def extract_data(data):
    """
    从原始数据中提取所需字段并返回 DataFrame
    """
    if not data or 'data' not in data or 'list' not in data['data']:
        print("未提取到有效数据")
        return pd.DataFrame()  # 返回空 DataFrame

    etf_list = data['data']['list']
    etf_datas = []

    for etf in etf_list:
        rise = etf.get("rise", 0)
        etf_data = {
            "代码": etf.get("code"),
            "市场": etf.get("market"),
            "名称": etf.get("name"),
            "价格": etf.get("price"),
            "涨幅": f'{rise:.2f}%',
            "成交总额": etf.get("total_amount")
        }
        etf_datas.append(etf_data)

    df = pd.DataFrame(etf_datas)
    return df


# 主程序入口
if __name__ == "__main__":
    raw_data = fetch_data()
    df = extract_data(raw_data)

    if not df.empty:
        print(df)
    else:
        print("未提取到有效数据")
