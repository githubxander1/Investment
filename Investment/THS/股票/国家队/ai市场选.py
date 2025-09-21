from datetime import datetime

import pandas as pd
import requests
import json

import fake_useragent
ua = fake_useragent.UserAgent()


def get_ai_strategy_xuangu():
    """
    获取AI市场跟随选股数据
    对应请求: AI市场跟随按照数量从高到低排序
    """
    # 请求URL
    url = "https://eq.10jqka.com.cn/gateway/iwc-web-business-center/strategy_unify/ai_strategy_xuangu"

    # URL参数
    params = {
        "limit": "22",
        "query": "AI市场跟随按照数量从高到低排序"  # 原始查询字符串，无需URL编码，requests会自动处理
    }

    # 请求头
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "priority": "u=1, i",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "referrer": "https://bowerbird.10jqka.com.cn/",
        "User-Agent": ua.random
    }
    # headers = {}

    try:
        # 发送GET请求，credentials: omit 对应不发送cookie
        response = requests.get(
            url,
            params=params,
            headers=headers,
            cookies=None,  # 不携带cookie
            verify=True
        )
        response.raise_for_status()  # 检查响应状态码
        response_json = response.json()
        # 保存 数据
        with open ("ai_strategy_xuangu.json", "w", encoding="utf-8") as f:
            json.dump(response_json, f, ensure_ascii=False, indent=4)
        return response_json
    except requests.exceptions.RequestException as e:
        print(f"请求AI策略选股数据失败: {e}")
        return None

def extract_data(data):
    datas = data["datas"]
    # model_sql = data["model_sql"]

    all_data = []
    for item in datas:
        all_data.append({
            "股票代码": item.get("股票代码", "").split(".")[0],
            "股票简称": item.get("股票简称", ""),
            "最新价": item.get("最新价", ""),
            "最新涨跌幅": item.get("最新涨跌幅", ""),
            "所属概念": item.get("所属概念", ""),
            "概念解析": item.get("概念解析", ""),
            "所属概念数量": item.get("所属概念数量", ""),
            "所属概念数量排名": item.get("所属概念数量排名", ""),
            "所属概念数量排名名次": item.get("所属概念数量排名名次", ""),
            "所属概念数量排名基数": item.get("所属概念数量排名基数", "")
            # "code": "301236",
            # "market_code": "33" # 33:深圳,17:上海
        })
    all_data_df = pd.DataFrame(all_data)
    today = datetime.now()
    # 昨天
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    all_data_df.to_excel("ai_strategy_xuangu.xlsx", sheet_name= f'{yesterday}', index=False)
    print(all_data_df)




# 测试函数
if __name__ == "__main__":
    ai_data = get_ai_strategy_xuangu()
    extract_data(ai_data)
    # if ai_data:
    #     print("AI市场跟随选股数据:")
    #     print(json.dumps(ai_data, indent=2, ensure_ascii=False))