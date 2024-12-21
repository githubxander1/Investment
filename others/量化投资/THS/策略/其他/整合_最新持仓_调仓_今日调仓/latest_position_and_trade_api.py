from pprint import pprint

import requests
from fake_useragent import UserAgent

# 获取策略最新持仓和调仓
def get_latest_position_and_trade(strategy_id):
    ua = UserAgent()
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
    params = {
        "strategyId": strategy_id
    }
    headers = {
        "User-Agent": ua.random
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"请求失败，状态码: {response.status_code}，策略ID: {strategy_id}")
        return None

# pprint(get_strategy_profit(155680))