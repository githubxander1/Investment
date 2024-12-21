import os
from pprint import pprint
import pandas as pd
from datetime import datetime
from latest_position_and_trade_api import get_latest_position_and_trade
from data_processor import extract_latest_trade_info, extract_latest_positions_info, determine_market
from file_operations import save_to_excel
from notification import send_notification

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

def main():
    strategy_ids = ['155259', '155270', '137789', '155680', '138006', '118188']

    all_latest_trade_info = []
    all_positions_info = []
    all_today_trades_info = []

    for strategy_id in strategy_ids:
        data = get_latest_position_and_trade(strategy_id)
        if data:
            latest_trade_info = extract_latest_trade_info(data, strategy_id, strategy_id_to_name)
            positions_info = extract_latest_positions_info(data, strategy_id, strategy_id_to_name)

            all_latest_trade_info.extend(latest_trade_info)
            all_positions_info.extend(positions_info)

            # 处理今天的交易信息
            current_date = datetime.now().date().strftime('%Y%m%d')
            today_trades = [trade for trade in latest_trade_info if trade['时间'] == current_date]
            all_today_trades_info.extend(today_trades)

            # 移除创业板
            # all_latest_trade_info = [trade for trade in all_latest_trade_info if not trade['市场'] == '创业板']
            all_today_trades_info = [trade for trade in all_today_trades_info if not trade['市场'] == '创业板']

    last_trades_df = pd.DataFrame(all_latest_trade_info)
    last_positions_df = pd.DataFrame(all_positions_info)
    today_trades_df = pd.DataFrame(all_today_trades_info)

    # 保存数据
    file_path = r'策略最新持仓和调仓_所有.xlsx'
    if not last_positions_df.empty:
        positions_file_path = os.path.join(os.getcwd(), '策略保存的数据', '策略最新持仓_所有.xlsx')
        save_to_excel(last_positions_df, positions_file_path, '策略最新持仓')
    else:
        print("No position data to save.")

    if not last_trades_df.empty:
        trades_file_path = os.path.join(os.getcwd(), '策略保存的数据', '策略最新调仓_所有.xlsx')
        save_to_excel(last_trades_df, trades_file_path, '策略最新调仓')
    else:
        print("No trade data to save.")

    if not today_trades_df.empty:
        today_trades_file_path = os.path.join(os.getcwd(), '策略保存的数据', '策略今天调仓.xlsx')
        save_to_excel(today_trades_df, today_trades_file_path, '策略今天调仓')
    else:
        print("No today's trade data to save.")

    print("\n当天交易信息:")
    if not today_trades_df.empty:
        print(today_trades_df)
        send_notification("今日调仓提醒", "发现今日有新的调仓操作！策略")
    else:
        print("今日无调仓操作")
