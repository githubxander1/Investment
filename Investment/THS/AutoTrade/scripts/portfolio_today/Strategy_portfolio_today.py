# scripts/strategy_portfolio_today.py
import datetime
import os
from pprint import pprint

import pandas as pd
import requests
from fake_useragent import UserAgent

from Investment.THS.AutoTrade.config.settings import STRATEGY_TODAY_ADJUSTMENT_LOG_FILE, \
    Strategy_portfolio_today_file, Strategy_id_to_name, Strategy_ids, Strategy_holding_file
from Investment.THS.AutoTrade.scripts.data_process import save_to_operation_history_excel, read_today_portfolio_record, \
    write_to_excel_append, read_portfolio_or_operation_data
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe, get_new_records, normalize_time, \
    determine_market

logger = setup_logger(STRATEGY_TODAY_ADJUSTMENT_LOG_FILE)

ua = UserAgent()

async def get_latest_position_and_trade(strategy_id):
    """单接口：获取并提取保存今日数据"""
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit?strategyId={strategy_id}"
    headers = {"User-Agent": ua.random}

    try:
        data = requests.get(url, headers=headers, timeout=10)
        data.raise_for_status()
        data = data.json()
        logger.info(f"策略 获取数据成功id:{strategy_id} {Strategy_id_to_name.get(strategy_id, '未知策略')} ")
        pprint(data)
    except requests.RequestException as e:
        logger.error(f"请求失败 (Strategy ID: {strategy_id}): {e}")
        return []

    result = data.get('result', {})
    latest_trade_infos = result.get('latestTrade', {})
    position_stocks = result.get('positionStocks', {})
    lastest_trade_date = normalize_time(latest_trade_infos.get('tradeDate', ''))
    # print(f"原始日期: {trade_date}，格式化后的：{normalize_time(str(trade_date))}")
    trade_stocks = latest_trade_infos.get('tradeStocks', [])

    trade_results = []
    for trade_stock_info in trade_stocks:
        # 显式转换时间戳为整数
        timestamp = trade_stock_info.get('tradeDate', '')
        if isinstance(timestamp, (int, float)):
            timestamp = str(int(timestamp))  #
        # stock_trade_date = normalize_time(trade_info.get('tradeDate', ''))
        # print(f"原始日期: {stock_trade_date}，格式化后的：{normalize_time(str(stock_trade_date))}")

        # 只保留当天记录
        # 昨天
        today = (datetime.datetime.now().strftime('%Y-%m-%d'))
        # print(f'今天{today}')
        # today = normalize_time((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
        if lastest_trade_date == today:
            trade_results.append({
            '名称': Strategy_id_to_name.get(strategy_id, '未知策略'),
            '操作': '买入' if trade_stock_info.get('operationType') == 'BUY' else '卖出',
            '标的名称': trade_stock_info.get('stkName', ''),
            '代码': str(trade_stock_info.get('stkCode', '').split('.')[0]).zfill(6),
            '最新价': round(float(trade_stock_info.get('tradePrice', 0)), 2),
            '新比例%': round(float(trade_stock_info.get('position', 0)) * 100, 2),
            '交易数量': trade_stock_info.get('tradeAmount', 0),
            '市场': determine_market(trade_stock_info.get('code', '')),
            '时间': normalize_time(trade_stock_info.get('tradeDate', ''))
            })

    position_stocks_results = []
    for position_stock_info in position_stocks:
        stk_code = str(position_stock_info.get('stkCode', '').split('.')[0]).zfill(6)
        position_stocks_results.append({
            '名称': Strategy_id_to_name.get(strategy_id, '未知策略'),
            '标的名称': position_stock_info.get('stkName', ''),
            '代码': str(position_stock_info.get('stkCode', '').split('.')[0]).zfill(6),
            '市场': determine_market(stk_code),
            '最新价': round(float(position_stock_info.get('price', 0)), 2),
            '盈亏比例%': round(float(position_stock_info.get('profitAndLossRatio', 0)) * 100, 2),
            '持仓比例%': round(float(position_stock_info.get('positionRatio', 0)) * 100, 2),
            '持仓时间': position_stock_info.get('positionDate', ''),
            '行业': position_stock_info.get('industry', ''),
        })


    return trade_results, position_stocks_results


async def Strategy_main():
    today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
    # today = normalize_time((datetime.datetime.now() - datetime.timedelta(days=6)).strftime('%Y-%m-%d'))
    logger.info(f'今天日期: {today}')
    all_today_trades = []
    all_positions = []
    for strategy_id in Strategy_ids:
        lastest_trade_results, position_stocks_results = await get_latest_position_and_trade(strategy_id)
        # pprint(trades)
        all_today_trades.extend(lastest_trade_results)
        all_positions.extend(position_stocks_results)

    all_today_trades_df = pd.DataFrame(all_today_trades)
    position_stocks_results_df = pd.DataFrame(all_positions)
    # logger.info(f'保存今日持仓数据:\n{position_stocks_results_df}')
    # position_stocks_results_df.to_excel(Strategy_holding_file, sheet_name=today,index=False)
    # print('今日数据:', all_today_trades_df)
    # print('持仓数据:', position_stocks_results_df)
    # 筛选今天的
    # all_today_trades_df = all_today_trades_df[all_today_trades_df['时间'] == today]

    # 打印所有列的数据类型
    # print(f'今日数据列的数据类型:\n{all_today_trades_df.dtypes}')

    if all_today_trades_df.empty:
        logger.info("⚠️ 今日无交易数据")
        return False, None

    # 根据时间列倒序
    all_today_trades_df = all_today_trades_df.sort_values(by='时间', ascending=False)
    all_today_trades_df = all_today_trades_df.reset_index(drop=True).set_index(all_today_trades_df.index + 1)  # 从1开始

    # 去重处理
    all_today_trades_df = all_today_trades_df.drop_duplicates(
        subset=['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间'],
        keep='first')

    # 过滤掉创业板、科创板股票的交易信息
    all_today_trades_df = all_today_trades_df[all_today_trades_df['市场'].isin(['沪深A股']) == True]
    # 去掉标的名称含st的
    all_today_trades_df = all_today_trades_df[~all_today_trades_df['标的名称'].str.contains('ST')]
    logger.info(f'今日交易数据：{len(all_today_trades_df)}条 \n{all_today_trades_df}')


    # 读取历史数据
    history_data_file = Strategy_portfolio_today_file
    expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间']
    try:
        # 修复：正确传递参数给 read_portfolio_or_operation_data
        today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 修复：使用 read_today_portfolio_record 而不是 read_portfolio_or_operation_data 保持一致性
        history_data_df = read_today_portfolio_record(history_data_file)
        # print(f'历史数据列的数据类型:\n{history_data_df.dtypes}')
        if not history_data_df.empty:
            history_data_df['代码'] = history_data_df['代码'].astype(str).str.zfill(6)  # 立即转为 str
            history_data_df['新比例%'] = history_data_df['新比例%'].round(2).astype(float)
        else:
            history_data_df = pd.DataFrame(columns=expected_columns)
    except Exception: #读取历史数据失败，初始化保存一个
        history_data_df = pd.DataFrame(columns=expected_columns)
        today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 修复：保持函数一致性
        save_to_operation_history_excel(history_data_df, history_data_file, f'{today}', index=False)
        # history_data_df.to_csv(history_data_df_file, index=False)
        # print(f'初始化历史记录文件: {history_data_df_file}')

    # 标准化数据格式
    all_today_trades_df = standardize_dataframe(all_today_trades_df)
    history_data_df = standardize_dataframe(history_data_df)
    # print(f'读取历史记录: {history_data_df}')

    # 获取新增数据
    new_data_df = get_new_records(all_today_trades_df, history_data_df)
    # print(f'获取新增数据: new_data_df)')

    # 保存新增数据并通知
    if new_data_df.empty:
        logger.info("---------------策略 无新增交易数据----------------")
        return False, None
    # with open(OPRATION_RECORD_DONE_FILE, 'w') as f:
    #     f.write('1')
    # 打印并保存新增数据
    # new_data_df_without_sc = new_data_df.drop(columns=['理由'], errors='ignore')
    # print(new_data_df_without_sc)

    today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
    # 修复：保持函数一致性
    save_to_operation_history_excel(new_data_df, history_data_file, f'{today}', index=False)
    position_stocks_results_df.to_excel(Strategy_holding_file, sheet_name=today, index=False)
    logger.info(f'保存今日持仓数据:\n{position_stocks_results_df}')
    # logger.info(f"✅ 保存新增调仓数据成功 \n{new_data_df}")
    # from Investment.THS.AutoTrade.utils.file_monitor import update_file_status
    # update_file_status(history_data_df_file)

    # 发送通知 - 修复：只发送新增数据而不是所有今日数据
    new_data_df_print_without_header = new_data_df.to_string(index=False)
    # print(f"新增的数据各列数据类型：\n{all_today_trades_df.dtypes}")
    send_notification(f"{len(new_data_df)} 条新增策略调仓：\n{new_data_df_print_without_header}")
    # logger.info("✅ 检测到新增策略调仓，准备启动自动化交易")
    # from Investment.THS.AutoTrade.utils.event_bus import event_bus
    # event_bus.publish('new_trades_available', new_data_df)
    # from Investment.THS.AutoTrade.utils.trade_utils import mark_new_trades_as_scheduled
    #
    # mark_new_trades_as_scheduled(new_data_df, OPERATION_HISTORY_FILE)

    return True, new_data_df
    # else:



if __name__ == '__main__':
    import asyncio
    asyncio.run(Strategy_main())
