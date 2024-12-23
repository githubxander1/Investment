import logging

# import logger
import os
from pprint import pprint
import requests
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
from plyer import notification
import schedule
import time

from others.量化投资.THS.自动化交易_同花顺.ths_logger import setup_logger
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

ua = UserAgent()

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

    if response.status_code == 200:
        data = response.json()
        # logger.debug(f"成功获取策略ID: {strategy_id} 的数据")

        # 提取 latestTrade 信息
        latest_trade = data.get('result', {}).get('latestTrade', {})
        trade_date = latest_trade.get('tradeDate', 'N/A')
        trade_stocks = latest_trade.get('tradeStocks', [])

        # 提取latestTrade所需字段
        latest_trade_info = []
        today_trades_info = []
        for trade_info in trade_stocks:
            code = trade_info.get('stkCode', 'N/A').split('.')[0]  # 提取股票代码

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
            # pprint(latest_trade_info)
            # logger.debug(f"提取交易信息: {trade_entry}")
            # logger.info(f'最新交易信息 (策略ID: {strategy_id}):{latest_trade_info}')

        # 当前日期
        current_date = datetime.now().date().strftime('%Y%m%d')
        # logger.debug(f"当前日期: {current_date}")

        # 提取当天的交易信息
        today_trades = [trade for trade in latest_trade_info if trade['时间'] == current_date]
        today_trades_info.extend(today_trades)
        # logger.info(f"当天交易信息 (策略ID: {strategy_id}): {today_trades}")

        # 过滤掉创业板股票的交易信息
        today_trades_info_without_cyb = [trade for trade in today_trades_info if not trade['市场'] == '创业板']
        # logger.info(f"过滤后的当天交易信息 (策略ID: {strategy_id}): {today_trades_info}")
        #
        return trade_date, latest_trade_info, today_trades_info, today_trades_info_without_cyb
    else:
        # logger.error(f"请求失败，状态码: {response.status_code}，策略ID: {strategy_id}")
        return None, [], []

def determine_market(stock_code):
    # 根据股票代码判断市场
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

def save_to_excel(df, filename, sheet_name, index=False):
    # 保存DataFrame到Excel文件
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
        logger.info(f"成功保存数据到Excel文件: {filename}, 表名称: {sheet_name}")
    except Exception as e:
        pass
        logger.error(f"保存数据到Excel文件失败: {e}")


def main():
    # global today_trades_info
    # 要查询的策略ID列表

    strategy_ids = ['138006', '137789','155259', '155270',
                    '155680',  '118188']
    '''
'155259': 'TMT资金流入战法',
'155680': GPT精选
'138006': '连续五年优质股战法',
137789  高现金高毛利战法
'138036': '低价小盘股战法',
'155270': '中字头概念',
'118188': '均线粘合平台突破'

'136567','净利润同比大增低估值战法'
138220 高roic低市盈率战法
'''

    all_latest_trade_info = []
    all_today_trades_info = []
    all_today_trades_info_without_cyb = []

    logger.info("开始处理策略调仓信息")

    # 存储所有策略的交易信息
    for strategy_id in strategy_ids:
        # logger.info(f"处理策略ID: {strategy_id}")
        trade_date, latest_trade_info, today_trades_info, today_trades_info_without_cyb = get_latest_position_and_trade(strategy_id)
        # print(latest_trade_info)


        if latest_trade_info:
            all_latest_trade_info.extend(latest_trade_info)
            # print(all_latest_trade_info)
            # logger.debug(f"添加最新交易信息: {latest_trade_info}")

        if today_trades_info:
            all_today_trades_info.extend(today_trades_info)
            # print(all_today_trades_info)
            # logger.debug(f"添加当天交易信息: {today_trades_info}")

        if today_trades_info_without_cyb:
            all_today_trades_info_without_cyb.extend(today_trades_info_without_cyb)
            # print(all_today_trades_info_without_cyb)


    # 创建DataFrame
    # last_trades_df = pd.DataFrame(latest_trade_info)
    # print(last_trades_df)
    today_trades_info_df = pd.DataFrame(all_today_trades_info)
    today_trades_without_cyb_df = pd.DataFrame(all_today_trades_info_without_cyb)
    print(today_trades_without_cyb_df)

    # 检查是否有数据并保存
    if not today_trades_without_cyb_df.empty:
        save_to_excel(today_trades_without_cyb_df, today_trades_without_cyb_file_path, '策略今天调仓')
    else:
        logger.info("No today's trade data to save.")

    # 打印当天交易信息到控制台
    # logger.info("\n当天交易信息:")
    # logger.info(f'今日交易信息汇总\n{today_trades_info_df}')
    if not today_trades_without_cyb_df.empty:
        logger.info(f'去除创业板的今天交易信息\n{today_trades_without_cyb_df}')
        # 发送系统通知
        notification.notify(
            title="今日调仓提醒",
            message="发现今日有新的调仓操作！策略",
            app_name="量化投资监控",
            timeout=10
        )
    else:
        logger.info("No today's trade data available.")

    logger.info("策略调仓信息处理完成")

if __name__ == '__main__':
    # schedule.every().monday.at("09:32").do(main)
    # schedule.every().tuesday.at("09:32").do(main)
    # schedule.every().wednesday.at("09:32").do(main)
    # schedule.every().thursday.at("09:32").do(main)
    # schedule.every().friday.at("09:32").do(main)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # 配置日志记录
    logger = setup_logger(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\保存的数据\策略_今天调仓.log')
    today_trades_without_cyb_file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\保存的数据\策略今天调仓.xlsx'

    try:
        main()
    except:
        logging.shutdown()
