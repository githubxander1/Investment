from pprint import pprint

import fake_useragent
import requests

ua = fake_useragent.UserAgent()
def get_latest_position_and_trade(strategy_id):
    """单接口：获取并提取保存今日数据"""
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit?strategyId={strategy_id}"
    headers = {"User-Agent": ua.random}

    try:
        data = requests.get(url, headers=headers, timeout=10)
        data.raise_for_status()
        data = data.json()
        # logger.info(f"策略 获取数据成功id:{strategy_id} {Strategy_id_to_name.get(strategy_id, '未知策略')} ")
        pprint(data)
    except requests.RequestException as e:
        # logger.error(f"请求失败 (Strategy ID: {strategy_id}): {e}")
        return []
if __name__ == '__main__':
    # get_latest_position_and_trade(strategy_id=156275)
    get_latest_position_and_trade(strategy_id=155680)