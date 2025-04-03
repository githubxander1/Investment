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
    Combination_ids_to_name, ETF_Combination_TODAY_ADJUSTMENT_FILE
from others.Investment.THS.AutoTrade.utils.determine_market import determine_market
from others.Investment.THS.AutoTrade.utils.notification import send_notification
from others.Investment.THS.AutoTrade.utils.excel_handler import save_to_excel, clear_sheet, read_excel, \
    create_empty_excel



# logger = setup_print(ETF_ADJUSTMENT_LOG_FILE)

def fetch_and_extract_data(portfolio_id, is_etf=True):
    url = "https://t.10jqka.com.cn/portfolio/post/v2/get_relocate_post_list"
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQxMzEyNzkzOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWRlZGQ2ZWU3MDFlOGM0YWM0MWM3ZWYyOGVkNTM5OTZjOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=5fc67f8e0b1358794365b561cebf49ab; user_status=0; hxmPid=sns_topic_T0xv0pp.vote.show; v=A2KnimVLcWWWZ205M4HOL2F3sePEs2bNGLda8az7jlWAfw1ZlEO23ehHqgV_; hxmPid=sns_live_p_435998200; v=A98ascgcxE1b9cBRFbcb1BSobDhpRDPmTZg32nEsew7VAPAieRTDNl1oxzqC"
    }
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

async def check_data(today_trade_df, file_path, sheet_name):
    '''
    读取历史数据
    对比历史数据和所有今天调仓数据
    找出新增
    附加到历史数据中
    通知
    '''
    # existing_df = f"ETF和组合_今天调仓.csv"
    existing_df = read_excel(file_path, sheet_name)
    print(existing_df)
    if existing_df is not None and not existing_df.empty:
        print(f'{len(existing_df)} 条历史数据：\n {existing_df}')
    else:
        existing_df = pd.DataFrame(columns=['组合名称', '股票名称', '代码', '操作', '新比例%', '时间'])
        print("历史数据为空")

    # 复合键生成逻辑保持不变...
    existing_df = existing_df.reset_index(drop=True)

    # 新增去重逻辑（考虑所有关键字段）
    compare_columns = ['代码', '新比例%']
    if not existing_df.empty:
        new_data = today_trade_df[~today_trade_df[compare_columns].apply(tuple, axis=1).isin(existing_df[compare_columns].apply(tuple, axis=1))]
    else:
        new_data = today_trade_df

    if not new_data.empty:
        print(f'{len(new_data)} 条新增数据，如下：\n {new_data}')

        # 重置索引以确保唯一性
        new_data = new_data.reset_index(drop=True)

        # 生成通知消息
        # notification_msg = f"\n> " + "\n".join(
        #     [f"{row['组合名称']} {row['操作']} {row['股票名称']} {row['代码']} {row['新比例%']}% {row['最新价']} \n{row['时间']}"
        #      for _, row in new_data.iterrows()])
        # send_notification(notification_msg)
        # print(f"新增{len(new_data)}条唯一调仓记录")

        # 保存新增数据到文件
        existing_df = f"ETF和组合_今天调仓.csv"
        if not os.path.exists(existing_df):
            with open(f"{existing_df}", "w", encoding="utf-8") as f:
                f.write(f"{new_data.to_csv(index=False)}\n")
        else:
            with open(f"{existing_df}", "a", encoding="utf-8") as f:
                f.write(f"{new_data.to_csv(index=False)}\n")
                print(f"新增{len(new_data)}条唯一调仓记录")
                # send_notification(f"没有新增调仓数据")
        # save_to_excel(new_data, file_path, sheet_name, mode='a')
    else:
        pprint("没有新增调仓数据")

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
    #索引倒序，比如5,4,3,2,1
    # all_today_trades_df = all_today_trades_df[::-1]
    print(f'{len(all_today_trades_df)} 条今天调仓数据, 如下：\n {all_today_trades_df}\n')

    existing_data_file = ETF_Combination_TODAY_ADJUSTMENT_FILE

    # 检查文件是否存在且不为空
    if os.path.exists(existing_data_file) and os.path.getsize(existing_data_file) > 0:
        with open(existing_data_file, 'r', encoding="utf-8") as f:
            existing_df = pd.read_csv(f)
            existing_df['代码'] = existing_df['代码'].astype(str).str.zfill(6)
            print(f'{len(existing_df)} 历史数据：\n{existing_df}')
    else:
        existing_df = pd.DataFrame(columns=['组合名称', '股票名称', '代码', '操作', '新比例%', '时间'])
        print("历史数据文件不存在或为空，创建新的历史数据文件。")

    def check_new_data(all_today_trades_df, existing_df, file_path):
        if existing_df.empty:
            combined_df = all_today_trades_df
            combined_df.to_csv(file_path, index=False)
        else:
            combined_df = pd.concat([all_today_trades_df, existing_df], ignore_index=True)
        new_data = combined_df.drop_duplicates(subset=['代码', '时间'], keep=False)
        if not new_data.empty:
            print(f'\n{len(new_data)} 条新增数据，如下：\n {new_data}')
            # 检查文件是否已经存在
            file_exists = os.path.isfile(file_path)
            with open(file_path, "a", encoding="utf-8") as f:
                new_data.to_csv(f, index=False, header=not file_exists)
                print(f"新增{len(new_data)}条唯一调仓记录成功，\n{len(existing_df)} 条新历史数据 \n{existing_df}")

            # 生成通知消息
            notification_msg = f"\n> " + "\n".join(
                [f"\n{row['组合名称']} {row['操作']} {row['股票名称']} {row['代码']} {row['新比例%']}% {row['最新价']} \n{row['时间']}"
                 for _, row in new_data.iterrows()])
            send_notification(notification_msg)

    check_new_data(all_today_trades_df, existing_df, existing_data_file)

if __name__ == '__main__':
    asyncio.run(ETF_Combination_main())
