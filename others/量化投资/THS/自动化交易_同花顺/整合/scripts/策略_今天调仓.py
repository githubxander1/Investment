# scripts/策略_今天调仓.py
import logging
import datetime
import pandas as pd

# from utils.notification import send_notification
# from utils.ths_logger import setup_logger
# from config.settings import STRATEGY_TODAY_ADJUSTMENT_LOG_FILE, STRATEGY_TODAY_ADJUSTMENT_FILE, API_URL, HEADERS
import requests
from fake_useragent import UserAgent

from others.量化投资.THS.自动化交易_同花顺.整合.utils.api_client import APIClient
from others.量化投资.THS.自动化交易_同花顺.整合.utils.notification import send_notification
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import STRATEGY_TODAY_ADJUSTMENT_LOG_FILE, API_URL, HEADERS, \
    STRATEGY_TODAY_ADJUSTMENT_FILE, STRATEGY_ID_TO_NAME, OPRATION_RECORD_DONE_FILE
from others.量化投资.THS.自动化交易_同花顺.整合.utils.ths_logger import setup_logger

logger = setup_logger(STRATEGY_TODAY_ADJUSTMENT_LOG_FILE)

api_client = APIClient()

ua = UserAgent()
# 手动创建策略ID到策略名称的映射
strategy_id_to_name = {
    '155259': 'TMT资金流入战法',
    '155680': 'GPT定期精选',
    '138036': '低价小盘股战法',
    '155270': '中字头概念',
    '137789': '高现金毛利战法',
    '138006': '连续五年优质股战法',
    '136567': '净利润同比大增低估值战法',
    '138127': '归母净利润高战法',
    '118188': '均线粘合平台突破'
}

def determine_market(stock_code):
    """根据股票代码判断市场"""
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('30'):
        return '创业板'
    elif stock_code.startswith(('4', '8')):
        return '北交所'
    else:
        return '其他'

def get_latest_position_and_trade(strategy_id):
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
    params = {"strategyId": strategy_id}

    headers = {
        "User-Agent": ua.random,
        "Accept": "*/*",
        "Origin": "https://bowerbird.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://bowerbird.10jqka.com.cn/thsic/editor/view/15f2E0a579?strategyId={{strategy_id}}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    # logger.debug(f"正在请求策略ID: {strategy_id}")
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        latest_trade = data.get('result', {}).get('latestTrade', {})
        trade_date = latest_trade.get('tradeDate', 'N/A')
        trade_stocks = latest_trade.get('tradeStocks', [])

        latest_trade_info = []
        today_trades_info = []
        for trade_info in trade_stocks:
            code = trade_info.get('stkCode', 'N/A').split('.')[0]
            trade_entry = {
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '时间': trade_date,
                '操作': trade_info.get('operationType', 'N/A'),
                '股票名称': trade_info.get('stkName', 'N/A'),
                '市场': determine_market(code),
                '参考价': trade_info.get('tradePrice', 'N/A'),
                '数量': trade_info.get('tradeAmount', 'N/A'),
            }
            latest_trade_info.append(trade_entry)
            today_trades = [trade for trade in latest_trade_info if trade['时间'] == datetime.datetime.now().date().strftime('%Y%m%d')]
            today_trades_info.extend(today_trades)

        today_trades_info_without_cyb = [trade for trade in today_trades_info if not trade['市场'] == '创业板']
        return trade_date, latest_trade_info, today_trades_info, today_trades_info_without_cyb
    else:
        return None, [], []

def save_to_excel(df, filename, sheet_name, index=False):
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
        logger.info(f"成功保存数据到Excel文件: {filename}, 表名称: {sheet_name}")
    except Exception as e:
        logger.error(f"保存数据到Excel文件失败: {e}")

def main():
    strategy_ids = ['138006', '137789', '155259', '155270', '155680', '118188']
    all_today_trades_info_without_cyb = []

    logger.info("开始处理策略调仓信息")
    for strategy_id in strategy_ids:
        combination_name = STRATEGY_ID_TO_NAME.get(strategy_id, '未知策略')
        _, _, today_trades_info, today_trades_info_without_cyb = get_latest_position_and_trade(strategy_id)
        if today_trades_info_without_cyb:
            all_today_trades_info_without_cyb.extend(today_trades_info_without_cyb)

    today_trades_without_cyb_df = pd.DataFrame(all_today_trades_info_without_cyb)
    if not today_trades_without_cyb_df.empty:
        save_to_excel(today_trades_without_cyb_df, STRATEGY_TODAY_ADJUSTMENT_FILE, '策略今天调仓')
        send_notification( "今天有新的调仓操作！策略")
        # 创建标志文件
        with open(f"{OPRATION_RECORD_DONE_FILE}", "w") as f:
            f.write("组合调仓已完成")
        logger.info(f'去除创业板的今天交易信息\n{today_trades_without_cyb_df}')
    else:
        logger.info("No today's trade data available.")

    logger.info("策略调仓信息处理完成")


if __name__ == '__main__':
    main()
