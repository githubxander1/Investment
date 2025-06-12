# scripts/strategy_portfolio_today.py
import datetime
import os
from pprint import pprint

import pandas as pd
import requests
from fake_useragent import UserAgent

from others.Investment.THS.AutoTrade.config.settings import STRATEGY_TODAY_ADJUSTMENT_LOG_FILE, \
    STRATEGY_TODAY_ADJUSTMENT_FILE, Strategy_id_to_name, Strategy_ids
from others.Investment.THS.AutoTrade.utils.determine_market import determine_market
from others.Investment.THS.AutoTrade.utils.logger import setup_logger
from others.Investment.THS.AutoTrade.utils.notification import send_notification
from others.Investment.THS.AutoTrade.utils.excel_handler import save_to_excel, clear_sheet


logger = setup_logger(STRATEGY_TODAY_ADJUSTMENT_LOG_FILE)
ua = UserAgent()


def normalize_time(time_str):
    """统一时间格式为 YYYY-MM-DD"""
    if not time_str:
        return ''
    try:
        # 若是整数日期格式（如20250507）
        if isinstance(time_str, int) or (time_str.isdigit() and len(time_str) == 8):
            return f"{time_str[:4]}-{time_str[4:6]}-{time_str[6:8]}"
        # 若已有标准格式
        elif '-' in time_str:
            return time_str.split(' ')[0]
        else:
            return time_str
    except Exception:
        return ''


async def get_latest_position_and_trade(strategy_id):
    """获取策略的最新持仓和交易信息"""
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit?strategyId={strategy_id}"
    headers = {"User-Agent": ua.random}

    try:
        data = requests.get(url, headers=headers, timeout=10).json()
    except requests.RequestException as e:
        print(f"请求失败 (Strategy ID: {strategy_id}): {e}")
        return []

    latest_trade = data.get('result', {}).get('latestTrade', {})
    trade_date = latest_trade.get('tradeDate', 'N/A')
    trade_stocks = latest_trade.get('tradeStocks', [])

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    result = []
    for trade_info in trade_stocks:
        code = trade_info.get('stkCode', 'N/A').split('.')[0].zfill(6)
        name = trade_info.get('stkName', 'N/A')
        operation = trade_info.get('operationType', 'N/A')
        price = trade_info.get('tradePrice', 'N/A')
        ratio = round(trade_info.get('position', 0) * 100, 2)
        market = determine_market(code)

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
                '时间': normalize_time(str(trade_date)),
            })

    return result


async def strategy_main():
    all_trades = []
    for strategy_id in Strategy_ids:
        trades = await get_latest_position_and_trade(strategy_id)
        all_trades.extend(trades)

    # 转换为 DataFrame
    all_trades_df = pd.DataFrame(all_trades)
    expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间']

    if all_trades_df.empty:
        print("今日无任何策略调仓更新")
        return

    # 标准化时间字段
    all_trades_df['时间'] = all_trades_df['时间'].apply(normalize_time)

    # 过滤掉创业板股票的交易信息
    # all_today_trades_info_without_sc = [trade for trade in all_today_trades_info if trade['市场'] not in ['创业板', '科创板']]
    # 排除创业板、科创板
    all_trades_df = all_trades_df[all_trades_df['市场'].isin(['创业板', '科创板']) == False]

    # 排序 & 打印
    all_trades_df = all_trades_df.sort_values(by='时间', ascending=False).reset_index(drop=True)
    all_trades_df.index += 1
    # print(all_trades_df.drop(columns=['时间'], errors='ignore'))
    # pprint("去掉参考价大于30的")
    # all_today_trades_info_without_sc = [trade for trade in all_today_trades_info_without_sc if trade['参考价'] < 30]

    # today_trades_without_sc_df = pd.DataFrame(all_today_trades_info_without_sc)
    # print(f'{len(today_trades_without_sc_df)}条 策略今日调仓：\n {today_trades_without_sc_df}')


    # 检查新增流程
    # 读取历史数据
    existing_data_file = STRATEGY_TODAY_ADJUSTMENT_FILE
    try:
        existing_data = pd.read_csv(existing_data_file)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        existing_data = pd.DataFrame(columns=expected_columns)
        existing_data.to_csv(existing_data_file, index=False)
        print(f'初始化历史记录文件: {existing_data_file}')

    # 列对齐
    existing_data = existing_data.reindex(columns=expected_columns, fill_value=None)

    # 标准化历史数据
    if not existing_data.empty:
        existing_data['代码'] = existing_data['代码'].astype(str).str.zfill(6)
        existing_data['时间'] = existing_data['时间'].apply(normalize_time)
        existing_data['_id'] = existing_data['时间'].astype(str) + '_' + existing_data['代码'].astype(str)

    # 处理当前数据
    all_trades_df['_id'] = all_trades_df['时间'].astype(str) + '_' + all_trades_df['代码'].astype(str)

    # print("all_trades_df _id:", all_trades_df['_id'].tolist())
    # print("existing_data _id:", existing_data['_id'].tolist() if not existing_data.empty else [])

    # 筛选新增数据
    new_mask = ~all_trades_df['_id'].isin(existing_data['_id']) if not existing_data.empty else []
    new_data = all_trades_df[new_mask].copy().drop(columns=['_id'])

    # 写入 CSV 并通知
    if not new_data.empty:
        header = not os.path.exists(existing_data_file) or os.path.getsize(existing_data_file) == 0
        new_data.to_csv(existing_data_file, mode='a', header=header, index=False)
        msg = f"{len(new_data)} 条新增策略调仓：\n{new_data.drop(columns=['理由'], errors='ignore')}"
        send_notification(msg)
        print(f'发现{len(new_data)}条新增策略调仓:')
        print(new_data.drop(columns=['理由'], errors='ignore'))
    else:
        print("今日无新增策略调仓")

if __name__ == '__main__':
    import asyncio
    asyncio.run(strategy_main())
