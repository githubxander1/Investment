# scripts/strategy_portfolio_today.py
import datetime
import os
from pprint import pprint

# import UserAgent
import pandas as pd
import requests
from fake_useragent import UserAgent

from others.Investment.THS.AutoTrade.config.settings import STRATEGY_TODAY_ADJUSTMENT_LOG_FILE, \
    STRATEGY_TODAY_ADJUSTMENT_FILE, Strategy_id_to_name, Strategy_ids, \
    ETF_Combination_TODAY_ADJUSTMENT_FILE
from others.Investment.THS.AutoTrade.utils.api_client import APIClient
# from z_others.Investment.THS.AutoTrade.utils.api_client import APIClient
# from utils.api_client import APIClient
from others.Investment.THS.AutoTrade.utils.determine_market import determine_market
# from utils.determine_market import determine_market
from others.Investment.THS.AutoTrade.utils.logger import setup_logger
# from utils.logger import setup_logger
from others.Investment.THS.AutoTrade.utils.notification import send_notification, send_email
from others.Investment.THS.AutoTrade.utils.excel_handler import save_to_excel, clear_sheet

logger = setup_logger(STRATEGY_TODAY_ADJUSTMENT_LOG_FILE)

api_client = APIClient()

ua = UserAgent()


async def get_latest_position_and_trade(strategy_id):
    """获取策略的最新持仓和交易信息"""
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit?strategyId={strategy_id}"
    # params = {"strategyId": strategy_id}

    headers = {
        "User-Agent": ua.random
    }

    data = requests.get(url, headers=headers)
    data = data.json()
    # pprint(data)
    latest_trade = data.get('result', {}).get('latestTrade', {})
    trade_date = latest_trade.get('tradeDate', 'N/A')
    trade_stocks = latest_trade.get('tradeStocks', [])

    latest_trade_info = []
    for trade_info in trade_stocks:
        code = trade_info.get('stkCode', 'N/A').split('.')[0]
        latest_trade_info.append({
            '名称': Strategy_id_to_name.get(strategy_id, '未知策略'),
            '操作': trade_info.get('operationType', 'N/A'),
            # '代码': trade_info.get('code', 'N/A'),
            '股票名称': trade_info.get('stkName', 'N/A'),
            '最新价': trade_info.get('tradePrice', 'N/A'),
            '新比例%': round(trade_info.get('position', 'N/A') * 100,2),
            '市场': determine_market(code),
            '时间': trade_date,#注意：有两个时间，格式不同
        })
        return latest_trade_info, trade_date
    else:
        return [], 'N/A'

async def read_existing_data(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            existing_df = pd.read_csv(file_path, on_bad_lines='skip')
            # 确保列名一致
            expected_columns = ['名称', '操作', '股票名称', '最新价', '新比例%', '市场', '时间']
            if not all(column in existing_df.columns for column in expected_columns):
                print("文件列名不匹配，创建一个空的DataFrame")
                return pd.DataFrame(columns=expected_columns)
            return existing_df
        except pd.errors.EmptyDataError:
            print("文件为空，创建一个空的DataFrame")
            return pd.DataFrame(columns=['名称', '操作', '股票名称', '最新价', '新比例%', '市场', '时间'])
    else:
        print("历史数据文件不存在或为空，创建新的历史数据文件。")
        return pd.DataFrame(columns=['名称', '操作', '股票名称', '最新价', '新比例%', '市场', '时间'])

async def save_new_data(new_data, file_path):
    if not new_data.empty:
        file_exists = os.path.isfile(file_path)
        with open(file_path, "a", encoding="utf-8", newline='') as f:
            new_data.to_csv(f, index=False, header=not file_exists)
        print(f"新增{len(new_data)}条唯一调仓记录")
        notification_msg = f"\n> " + "\n".join(
            [f"\n{row['名称']} {row['操作']} {row['股票名称']} {row['最新价']} {row['新比例%']}% \n{row['时间']}"
             for _, row in new_data.iterrows()])
        send_notification(notification_msg)
    else:
        print("没有新增调仓数据")

async def strategy_main():
    all_today_trades_info = []
    all_latest_trade_info = []

    pprint("开始处理策略调仓信息")
    for strategy_id in Strategy_ids:
        latest_trade_info, trade_date = await get_latest_position_and_trade(strategy_id)
        if latest_trade_info:
            all_latest_trade_info.extend(latest_trade_info)
            today_trades = [trade for trade in latest_trade_info if trade['时间'] == datetime.datetime.now().date().strftime('%Y%m%d')]
            all_today_trades_info.extend(today_trades)
            # print(all_today_trades_info)

    # 过滤掉创业板股票的交易信息
    all_today_trades_info_without_sc = [trade for trade in all_today_trades_info if trade['市场'] not in ['创业板', '科创板']]
    # pprint("去掉参考价大于30的")
    # all_today_trades_info_without_sc = [trade for trade in all_today_trades_info_without_sc if trade['参考价'] < 30]

    today_trades_without_sc_df = pd.DataFrame(all_today_trades_info_without_sc)
    print(f'{len(today_trades_without_sc_df)}条 策略今日调仓：\n {today_trades_without_sc_df}')


    # 检查新增流程
    existing_data_file = STRATEGY_TODAY_ADJUSTMENT_FILE
    existing_df = await read_existing_data(existing_data_file)

    # 确保两个DataFrame的列一致
    if existing_df.empty:
        existing_df = pd.DataFrame(columns=today_trades_without_sc_df.columns)

    combined_df = pd.concat([today_trades_without_sc_df, existing_df], ignore_index=True)
    combined_df = combined_df.dropna(how='all')  # 排除全为空值的行
    combined_df.drop_duplicates(subset=['时间'], inplace=True)

    if combined_df.empty:
        logger.warning("合并后的数据为空，无需保存新数据")
    else:
        new_data = combined_df[~combined_df.index.isin(existing_df.index)]
        if not new_data.empty:
            await save_new_data(new_data, existing_data_file)
            logger.info(f"新增 {len(new_data)} 条唯一调仓记录")
        else:
            logger.info("无新增调仓记录")

    pprint("策略调仓信息处理完成")

if __name__ == '__main__':
    # strategy_id_to_name = Strategy_id_to_name
    import asyncio

    asyncio.run(strategy_main())

    # try:
    #     scheduler = Scheduler(interval=0.25,
    #                           callback=main,
    #                           start_time=dt_time(9, 29),
    #                           end_time=dt_time(10, 33))
    #     scheduler.start()
    # except Exception as e:
    #     logger.error(f"调度器启动失败: {e}", exc_info=True)

