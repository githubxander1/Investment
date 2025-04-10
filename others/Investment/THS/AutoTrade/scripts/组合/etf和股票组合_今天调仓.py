import asyncio
import datetime
import os
from pprint import pprint

import openpyxl
import pandas as pd
import requests

import sys
import os

# # 获取根目录
others_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
# # 将others目录添加到模块搜索路径中
sys.path.append(others_dir)
# print(f'包路径：{sys.path}')

from others.Investment.THS.AutoTrade.config.settings import ETF_ids, ETF_ids_to_name, \
    ETF_ADJUSTMENT_LOG_FILE, Combination_ids, \
    Combination_ids_to_name, ETF_Combination_TODAY_ADJUSTMENT_FILE, Combination_headers
from others.Investment.THS.AutoTrade.utils.determine_market import determine_market
from others.Investment.THS.AutoTrade.utils.notification import send_notification
from others.Investment.THS.AutoTrade.utils.excel_handler import save_to_excel, clear_sheet, read_excel, \
    create_empty_excel



# logger = setup_print(ETF_ADJUSTMENT_LOG_FILE)

def fetch_and_extract_data(portfolio_id, is_etf=True):
    url = "https://t.10jqka.com.cn/portfolio/post/v2/get_relocate_post_list"
    headers = Combination_headers
    params = {"id": portfolio_id, "dynamic_id": 0}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        # pprint(response_json)
    except requests.RequestException as e:
        print(f"请求出错 (ID: {portfolio_id}): {e}")
        return []

    today_trades = []
    today = datetime.date.today().strftime('%Y-%m-%d')

    data = response_json.get('data', [])
    for item in data:
        createAt = item.get('createAt', None)
        content = item.get('content', '')
        relocateList = item.get('relocateList', [])

        for infos in relocateList:
            name = infos.get('name', None)
            code = infos.get('code', None)
            if '***' in name:
                print(f"未订阅或股票名称显示异常 -组合id:{portfolio_id} 股票代码: {code}, 时间: {createAt}")
                continue

            # 计算操作类型
            current_ratio = infos.get('currentRatio', 0)
            new_ratio = infos.get('newRatio', 0)
            operation = '买入' if new_ratio > current_ratio else '卖出'

            market = determine_market(code)
            # 获取组合名称
            if is_etf:
                combination_name = ETF_ids_to_name.get(portfolio_id, '未知ETF组合')
            else:
                combination_name = Combination_ids_to_name.get(portfolio_id, '未知股票组合')

            history_post = {
                '组合名称': combination_name,
                '代码': str(code).zfill(6),  # 提前统一格式
                '股票名称': name,
                '市场': market,
                '操作': operation,
                '最新价': infos.get('finalPrice'),
                '当前比例%': round(current_ratio * 100, 2),
                '新比例%': round(new_ratio * 100, 2),
                '时间': createAt,
                # '理由': content
            }
            # 今天调仓的
            today = datetime.date.today().strftime('%Y-%m-%d')
            if today == createAt.split()[0]:
                today_trades.append(history_post)

    return today_trades

async def read_existing_data(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            existing_df = pd.read_csv(file_path)
            # existing_df['代码'] = existing_df['代码'].astype(str).str.zfill(6)
            return existing_df
        except pd.errors.EmptyDataError:
            print("文件为空，创建一个空的DataFrame")
            return pd.DataFrame(columns=['组合名称', '股票名称', '代码', '操作', '最新价',  '新比例%', '时间'])
    else:
        print("历史数据文件不存在或为空，创建新的历史数据文件。")
        return pd.DataFrame(columns=['组合名称', '股票名称', '代码', '操作', '最新价', '新比例%', '时间'])

async def save_new_data(new_data, file_path):
    if not new_data.empty:
        file_exists = os.path.isfile(file_path)
        with open(file_path, "a", encoding="utf-8") as f:
            new_data.to_csv(f, index=False, header=not file_exists)
        print(f"新增{len(new_data)}条唯一调仓记录")
        notification_msg = f"\n> " + "\n".join(
            [f"\n{row['组合名称']} {row['操作']} {row['股票名称']} {row['代码']} {row['新比例%']}% {row['最新价']} \n{row['时间']}"
             for _, row in new_data.iterrows()])
        send_notification(notification_msg)
    else:
        print("没有新增调仓数据")

async def ETF_Combination_main():
    # 处理 ETF 组合
    etf_today_trades_all = []
    for etf_id in ETF_ids:
        etf_today_trades = fetch_and_extract_data(etf_id, is_etf=True)
        etf_today_trades_all.extend(etf_today_trades)

    # 处理股票组合
    stock_today_trades_all = []
    for stock_id in Combination_ids:
        stock_today_trades = fetch_and_extract_data(stock_id, is_etf=False)
        stock_today_trades_all.extend(stock_today_trades)
    # pprint(f'股票组合的今日调仓：\n {stock_today_trades_all}')

    all_today_trades = etf_today_trades_all + stock_today_trades_all

    # 倒序排序
    all_today_trades = sorted(all_today_trades, key=lambda x: x['时间'], reverse=True)

    # 合并两个表数据
    all_today_trades_df = pd.DataFrame(all_today_trades)
    all_today_trades_df = all_today_trades_df.reset_index(drop=True).set_index(all_today_trades_df.index + 1)
    # all_today_trades_df['代码'] = all_today_trades_df['代码'].astype(str).str.zfill(6)
    #索引倒序，比如5,4,3,2,1
    # all_today_trades_df = all_today_trades_df[::-1]
    print(f'{len(all_today_trades_df)} 条今天调仓数据, 如下：\n {all_today_trades_df}\n')

    existing_data_file = ETF_Combination_TODAY_ADJUSTMENT_FILE
    existing_df = await read_existing_data(existing_data_file)

    # 确保两个DataFrame的列一致
    if existing_df.empty:
        existing_df = pd.DataFrame(columns=all_today_trades_df.columns)

    combined_df = pd.concat([all_today_trades_df, existing_df], ignore_index=True)
    combined_df.drop_duplicates(subset=['代码', '时间'], inplace=True)

    new_data = combined_df[~combined_df.index.isin(existing_df.index)]
    await save_new_data(new_data, existing_data_file)

if __name__ == '__main__':
    asyncio.run(ETF_Combination_main())
