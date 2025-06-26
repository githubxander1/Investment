# scripts/strategy_portfolio_today.py
import datetime
import os
from pprint import pprint

import pandas as pd
import requests
from fake_useragent import UserAgent

from Investment.THS.AutoTrade.config.settings import STRATEGY_TODAY_ADJUSTMENT_LOG_FILE, \
    Strategy_portfolio_today, Strategy_id_to_name, Strategy_ids, OPRATION_RECORD_DONE_FILE, OPERATION_HISTORY_FILE
from Investment.THS.AutoTrade.utils.determine_market import determine_market
from Investment.THS.AutoTrade.utils.file_monitor import get_file_hash
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.utils.excel_handler import save_to_excel, clear_csv
from Investment.THS.AutoTrade.utils.data_processor import standardize_dataframe, get_new_records, normalize_time
# from Investment.THS.AutoTrade.scripts.自动化交易 import logger
logger = setup_logger(STRATEGY_TODAY_ADJUSTMENT_LOG_FILE)

ua = UserAgent()

async def get_latest_position_and_trade(strategy_id):
    """获取策略的最新持仓和交易信息"""
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit?strategyId={strategy_id}"
    headers = {"User-Agent": ua.random}

    try:
        data = requests.get(url, headers=headers, timeout=10)
        data.raise_for_status()
        data = data.json()
        # pprint(data)
        logger.info(f"策略id:{strategy_id} {Strategy_id_to_name.get(strategy_id, '未知策略')} 获取数据成功")
        # pprint(data)
    except requests.RequestException as e:
        print(f"请求失败 (Strategy ID: {strategy_id}): {e}")
        return []

    latest_trade = data.get('result', {}).get('latestTrade', {})
    trade_date = latest_trade.get('tradeDate', 'N/A')
    # print(f"原始日期: {trade_date}，格式化后的：{normalize_time(str(trade_date))}")
    trade_stocks = latest_trade.get('tradeStocks', [])

    today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
    # 昨天
    # today = normalize_time((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
    # print(today)

    result = []
    for trade_info in trade_stocks:
        code = str(trade_info.get('stkCode', 'N/A').split('.')[0].zfill(6))
        name = trade_info.get('stkName', 'N/A')
        operation = '买入' if trade_info.get('operationType', 'N/A') == 'BUY' else '卖出'
        price = trade_info.get('tradePrice', 'N/A')
        ratio = round(trade_info.get('position', 0) * 100, 2)
        market = determine_market(code)
        stock_trade_date = trade_info.get('tradeDate', 'N/A')
        # print(f"原始日期: {stock_trade_date}，格式化后的：{normalize_time(str(stock_trade_date))}")

        # 只保留当天记录
        if normalize_time(str(trade_date)) == today:
            result.append({
                '名称': Strategy_id_to_name.get(strategy_id, '未知策略'),
                '操作': operation,
                '标的名称': name,
                '代码': code,
                '最新价': price,
                '新比例%': ratio,
                '市场': market,
                '时间': normalize_time(str(stock_trade_date)),
            })

    return result


async def Strategy_main():
    all_today_trades = []
    for strategy_id in Strategy_ids:
        trades = await get_latest_position_and_trade(strategy_id)
        all_today_trades.extend(trades)

    all_today_trades = sorted(all_today_trades, key=lambda x: x['时间'], reverse=True)  # 倒序排序

    # 转换为 DataFrame
    all_today_trades_df = pd.DataFrame(all_today_trades)

    # 只有在非空的情况下才进行字段处理
    if not all_today_trades_df.empty:
        # all_today_trades_df['时间'] = all_today_trades_df['时间'].apply(normalize_time)
        all_today_trades_df['时间'] = all_today_trades_df['时间'].astype(str).apply(normalize_time)

        all_today_trades_df = all_today_trades_df.reset_index(drop=True).set_index(
            all_today_trades_df.index + 1
        )  # 从1开始
    else:
        print("⚠️ 今日无交易数据")
        return

    # 标准化时间字段
    # all_trades_df['时间'] = all_trades_df['时间'].apply(normalize_time)

    # 过滤掉创业板、科创板股票的交易信息
    all_today_trades_df_without_sc = all_today_trades_df[all_today_trades_df['市场'].isin(['创业板', '科创板']) == False]
    # all_trades_df = [~(all_trades_df[all_trades_df['市场'].isin(['创业板', '科创板'])]
    logger.info(f'今日交易数据：\n{all_today_trades_df_without_sc}')

    # # 排序
    # all_trades_df = all_trades_df.sort_values(by='时间', ascending=False).reset_index(drop=True)
    # all_trades_df.index += 1

    # 读取历史数据
    existing_data_file = Strategy_portfolio_today
    expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间']

    try:
        existing_data = pd.read_csv(existing_data_file)
        # 强制清理异常值
        # existing_data['代码'] = existing_data['代码'].astype(str).str.zfill(6)
        # existing_data['时间'] = existing_data['时间'].astype(str).apply(normalize_time)
        # existing_data = existing_data[existing_data['时间'].notna() & (existing_data['时间'] != '')]
    except (FileNotFoundError, pd.errors.EmptyDataError):
        existing_data = pd.DataFrame(columns=expected_columns)
        existing_data.to_csv(existing_data_file, index=False)
        # print(f'初始化历史记录文件: {existing_data_file}')

    # 标准化数据格式
    all_today_trades_df = standardize_dataframe(all_today_trades_df_without_sc)
    existing_data = standardize_dataframe(existing_data)
    # print(f'读取历史记录: {existing_data}')

    # 获取新增数据
    new_data = get_new_records(all_today_trades_df, existing_data)
    # print(f'获取新增数据: new_data)')

    # 保存新增数据并通知
    if not new_data.empty:
        # with open(OPRATION_RECORD_DONE_FILE, 'w') as f:
        #     f.write('1')
        # 打印并保存新增数据
        # new_data_without_sc = new_data.drop(columns=['理由'], errors='ignore')
        # print(new_data_without_sc)

        header = not os.path.exists(existing_data_file) or os.path.getsize(existing_data_file) == 0
        new_data.to_csv(existing_data_file, mode='a', header=header, index=False)
        logger.info(f"✅ 保存新增调仓数据成功 {existing_data}")
        # from Investment.THS.AutoTrade.utils.file_monitor import update_file_status
        # update_file_status(existing_data_file)

        # 发送通知
        new_data_print_without_header = all_today_trades_df_without_sc.to_string(index=False)
        send_notification(f"{len(new_data)} 条新增策略调仓：\n{new_data_print_without_header}")
        logger.info("✅ 检测到新增策略调仓，准备启动自动化交易")
        # from Investment.THS.AutoTrade.utils.event_bus import event_bus
        # event_bus.publish('new_trades_available', new_data)
        # from Investment.THS.AutoTrade.utils.trade_utils import mark_new_trades_as_scheduled
        #
        # mark_new_trades_as_scheduled(new_data, OPERATION_HISTORY_FILE)

        return True, new_data
    else:
        print("---------------策略 无新增交易数据----------------")
        return False



if __name__ == '__main__':
    import asyncio
    asyncio.run(Strategy_main())
