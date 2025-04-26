import asyncio
import csv
import datetime
import os
from pprint import pprint

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
    # pprint(data)
    for item in data:
        createAt = item.get('createAt', None)
        content = item.get('content', '')
        relocateList = item.get('relocateList', [])

        for infos in relocateList:
            name = infos.get('name', None)
            code = infos.get('code', None)
            if '***' in name:
                print(f"未订阅或标的名称显示异常 -组合id:{portfolio_id} 股票代码: {code}, 时间: {createAt}")
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
                '名称': combination_name,
                '操作': operation,
                '标的名称': name,
                '代码': str(code).zfill(6),  # 提前统一格式
                '最新价': infos.get('finalPrice'),
                # '当前比例%': round(current_ratio * 100, 2),
                '新比例%': round(new_ratio * 100, 2),
                '市场': market,
                '时间': createAt,
                '理由': content
            }
            # 今天更新的
            today = datetime.date.today().strftime('%Y-%m-%d')
            if today == createAt.split()[0]:
                today_trades.append(history_post)

    return today_trades

# async def read_existing_data(file_path):
#     expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间']
#
#     # try:
#     if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
#         # 添加dtype参数强制代码列为字符串
#         existing_df = pd.read_csv(file_path, dtype={'代码': str})
#         print(f'{len(existing_df)} 条历史更新数据, 如下：\n {existing_df}')
#         # # 检查列名是否匹配
#         # if not set(expected_columns).issubset(existing_df.columns):
#         #     print("列名不匹配，创建新文件")
#         #     return pd.DataFrame(columns=expected_columns)
#         return existing_df
        # else:
        #     # 创建带有正确列名的空文件
        #     pd.DataFrame(columns=expected_columns).to_csv(file_path, index=False)
        #     print("创建新的历史数据文件")
        #     return pd.DataFrame(columns=expected_columns)
    # except pd.errors.EmptyDataError:
    #     print("历史数据为空")
        # pd.DataFrame(columns=expected_columns).to_csv(file_path, index=False)
        # return pd.DataFrame(columns=expected_columns)

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

    all_today_trades = etf_today_trades_all + stock_today_trades_all # 整合两个表数据
    all_today_trades = sorted(all_today_trades, key=lambda x: x['时间'], reverse=True) # 倒序排序

    # 转换成pd表格样式
    all_today_trades_df = pd.DataFrame(all_today_trades)
    all_today_trades_df = all_today_trades_df.reset_index(drop=True).set_index(all_today_trades_df.index + 1) #从1开始
    #去掉‘理由’列
    all_today_trades_df_without_content = all_today_trades_df.drop(columns=['理由'])
    if not all_today_trades_df.empty:
        print(f'{len(all_today_trades_df)} 条今天更新数据, 如下：\n {all_today_trades_df_without_content}\n')

    #读取历史数据
    existing_data_file = ETF_Combination_TODAY_ADJUSTMENT_FILE
    existing_data = pd.read_csv(existing_data_file) if os.path.exists(existing_data_file) else pd.DataFrame()

    if not existing_data.empty:
        #找出新增的更新数据
        mask = ~all_today_trades_df['时间'].isin(existing_data['时间'])
        new_data = all_today_trades_df[mask].copy()
        if not new_data.empty:
            print(f'{len(new_data)} 条新增数据, 如下：\n {new_data}')
            pd.DataFrame(new_data).to_csv(existing_data_file, mode='a', header=False, index=False)
        else:
            print("没有新增数据")
    else:
        print("没有历史数据")


if __name__ == '__main__':
    asyncio.run(ETF_Combination_main())
