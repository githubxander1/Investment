# scripts/strategy_portfolio_today.py
import datetime
import os
from pprint import pprint

import pandas as pd
import requests
from fake_useragent import UserAgent

from Investment.THS.AutoTrade.config.settings import STRATEGY_TODAY_ADJUSTMENT_LOG_FILE, \
    Strategy_portfolio_today_file, Strategy_id_to_name, Strategy_ids
from Investment.THS.AutoTrade.scripts.data_process import save_to_excel, read_portfolio_record_history
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
        # pprint(data)
    except requests.RequestException as e:
        logger.error(f"请求失败 (Strategy ID: {strategy_id}): {e}")
        return []

    latest_trade = data.get('result', {}).get('latestTrade', {})
    trade_date = normalize_time(latest_trade.get('tradeDate', ''))
    # print(f"原始日期: {trade_date}，格式化后的：{normalize_time(str(trade_date))}")
    trade_stocks = latest_trade.get('tradeStocks', [])

    result = []
    for trade_info in trade_stocks:
        code = str(trade_info.get('code', '').zfill(6))
        # name = trade_info.get('stkName', '')
        # operation = '买入' if trade_info.get('operationType', '') == 'BUY' else '卖出'
        # price = trade_info.get('tradePrice', '')
        # ratio = round(trade_info.get('position', 0) * 100, 2)
        # market = determine_market(code)
        # 显式转换时间戳为整数
        timestamp = trade_info.get('tradeDate', '')
        if isinstance(timestamp, (int, float)):
            timestamp = str(int(timestamp))  #
        # stock_trade_date = normalize_time(timestamp)

        # stock_trade_date = normalize_time(trade_info.get('tradeDate', ''))
        # print(f"原始日期: {stock_trade_date}，格式化后的：{normalize_time(str(stock_trade_date))}")

        # 只保留当天记录
        # 昨天
        today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
        # today = normalize_time((datetime.datetime.now() - datetime.timedelta(days=4)).strftime('%Y-%m-%d'))
        # print(today)
        if trade_date == today:
                result.append({
                '名称': Strategy_id_to_name.get(strategy_id, '未知策略'),
                '操作': '买入' if trade_info.get('operationType') == 'BUY' else '卖出',
                '标的名称': trade_info.get('stkName', ''),
                '代码': str(trade_info.get('code', '')).zfill(6),
                '最新价': round(float(trade_info.get('tradePrice', 0)), 2),
                '新比例%': round(float(trade_info.get('position', 0)) * 100, 2),
                '市场': determine_market(trade_info.get('code', '')),
                '时间': normalize_time(trade_info.get('tradeDate', ''))
            })

    return result


async def Strategy_main():
    all_today_trades = []
    for strategy_id in Strategy_ids:
        trades = await get_latest_position_and_trade(strategy_id)
        # pprint(trades)
        all_today_trades.extend(trades)

    # all_today_trades = sorted(all_today_trades, key=lambda x: x['时间'], reverse=True)  # 倒序排序
    all_today_trades_df = pd.DataFrame(all_today_trades)
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
        # 打印数据列的数据类型
        history_data_df = read_portfolio_record_history(history_data_file)
        # print(f'历史数据列的数据类型:\n{history_data_df.dtypes}')
        if not history_data_df.empty:
            history_data_df['代码'] = history_data_df['代码'].astype(str).str.zfill(6)  # 立即转为 str
            history_data_df['新比例%'] = history_data_df['新比例%'].round(2).astype(float)
        else:
            history_data_df = pd.DataFrame(columns=expected_columns)
    except Exception: #读取历史数据失败，初始化保存一个
        history_data_df = pd.DataFrame(columns=expected_columns)
        today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
        save_to_excel(history_data_df, history_data_file, f'{today}', index=False)
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
    header = not os.path.exists(history_data_file) or os.path.getsize(history_data_file) == 0
    save_to_excel(new_data_df,history_data_file,f'{today}')
    # logger.info(f"✅ 保存新增调仓数据成功 \n{new_data_df}")
    # from Investment.THS.AutoTrade.utils.file_monitor import update_file_status
    # update_file_status(history_data_df_file)

    # 发送通知
    new_data_df_print_without_header = all_today_trades_df.to_string(index=False)
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
