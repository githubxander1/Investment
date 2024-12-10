from pprint import pprint
import requests
from fake_useragent import UserAgent
import pandas as pd
import schedule
import time
from datetime import datetime, timedelta
from plyer import notification
import os

# 手动创建策略ID到策略名称的映射
strategy_id_to_name = {
    '155259': 'TMT资金流入战法',
    '155680': 'GPT定期精选',
    '138036': '低价小盘股战法',
    '138386': '主力控盘低价股战法',
    '118188': '均线粘合平台突破',
}

def fetch_strategy_profit(strategy_id):
    ua = UserAgent()
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
    params = {"strategyId": strategy_id}
    headers = {"User-Agent": ua.random}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # 提取 latestTrade 和 positionStocks 信息
        latest_trade = data.get('result', {}).get('latestTrade', {})
        trade_stocks = latest_trade.get('tradeStocks', [])
        position_stocks = data.get('result', {}).get('positionStocks', [])

        trades_info = [
            {
                '策略ID': strategy_id,
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '操作': trade.get('operationType', 'N/A'),
                '名称': trade.get('stkName', 'N/A'),
                '价格': trade.get('tradePrice', 'N/A'),
                '数量': trade.get('tradeAmount', 'N/A'),
                '时间': trade.get('tradeDate', 'N/A'),
            }
            for trade in trade_stocks
        ]

        positions_info = [
            {
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '名称': position.get('stkName', 'N/A'),
                '行业': position.get('industry', 'N/A'),
                '价格': position.get('price', 'N/A'),
                '持仓日期': position.get('positionDate', 'N/A'),
                '持仓比例': f"{position.get('positionRatio', 0) * 100:.2f}%",
                '盈亏比例': f"{position.get('profitAndLossRatio', 0) * 100:.2f}%",
            }
            for position in position_stocks
        ]

        return trades_info, positions_info
    else:
        print(f"请求失败，状态码: {response.status_code}，策略ID: {strategy_id}")
        return [], []

def check_today_trades(trades_info):
    today = datetime.now().strftime('%Y-%m-%d')
    return [trade for trade in trades_info if trade['时间'].startswith(today)]

def notify_trades(trades):
    if trades:
        message = "\n".join([
            f"{trade['操作']} {trade['名称']} 价格: {trade['价格']} 数量: {trade['数量']} 时间: {trade['时间']}"
            for trade in trades
        ])
        notification.notify(
            title="今日交易通知",
            message=message,
            app_name="策略监控",
            timeout=10
        )

def job():
    all_trades_info = []
    all_positions_info = []

    for strategy_id in strategy_ids:
        trades_info, positions_info = fetch_strategy_profit(strategy_id)
        all_trades_info.extend(trades_info)
        all_positions_info.extend(positions_info)

    today_trades = check_today_trades(all_trades_info)
    notify_trades(today_trades)

# 要查询的策略ID列表
strategy_ids = ['155259', '155680', '138036', '138386', '118188']

# 设置定时任务，每个工作日早上9点32运行
schedule.every().monday.at("09:32").do(job)
schedule.every().tuesday.at("09:32").do(job)
schedule.every().wednesday.at("09:32").do(job)
schedule.every().thursday.at("09:32").do(job)
schedule.every().friday.at("09:32").do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)