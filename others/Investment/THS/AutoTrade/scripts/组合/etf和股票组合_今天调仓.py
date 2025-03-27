import asyncio
import datetime
import os
from pprint import pprint

import openpyxl
import pandas as pd
import requests

from others.Investment.THS.AutoTrade.config.settings import ETF_ids, ETF_ids_to_name, \
    ETF_ADJUSTMENT_LOG_FILE, Combination_ids, \
    Combination_ids_to_name, ETF_Combination_TODAY_ADJUSTMENT_FILE
from others.Investment.THS.AutoTrade.utils.determine_market import determine_market
from others.Investment.THS.AutoTrade.utils.notification import send_notification
from others.Investment.THS.AutoTrade.utils.excel_handler import save_to_excel, clear_sheet, read_excel
# from others.Investment.THS.AutoTrade.zothers.tes import exists_data


# print = setup_print(ETF_ADJUSTMENT_LOG_FILE)

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
    existing_df = read_excel(file_path, sheet_name)
    if existing_df is None:
        existing_df = pd.DataFrame(columns=today_trade_df.columns)

    print(f'历史数据：\n {existing_df}')

    # 找出新增的记录
    new_records = today_trade_df[~today_trade_df.apply(tuple, axis=1).isin(existing_df.apply(tuple, axis=1))]

    print("\n新增的记录:")
    print(new_records)

    if not new_records.empty:
        # 生成通知消息
        notification_msg = f"\n> " + "\n".join(
            [f"{row['组合名称']} {row['操作']} {row['股票名称']} {row['代码']} {row['新比例%']}% {row['最新价']} \n{row['时间']}"
             for _, row in new_records.iterrows()])
        send_notification(notification_msg)
        print(f"新增{len(new_records)}条唯一调仓记录")

        # 合并数据并保存
        # updated_df = pd.concat([existing_df, new_records], ignore_index=True)
        # updated_df = updated_df.sort_values('时间', ascending=False).reset_index(drop=True)
        save_to_excel(new_records, file_path, sheet_name)
    else:
        pprint("没有新增调仓数据")

async def ETF_Combination_main():
    # 处理 ETF 组合
    etf_today_trades_all = []
    for etf_id in ETF_ids:
        etf_today_trades = fetch_and_extract_data(etf_id, is_etf=True)
        etf_today_trades_all.extend(etf_today_trades)

    # pprint(f'ETF的今日调仓：\n {etf_today_trades_all}')

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
    # all_today_trades_df.to_excel(ETF_Combination_TODAY_ADJUSTMENT_FILE, sheet_name='所有今天调仓', index=False)
    print(f'所有今天调仓：\n {all_today_trades_df}')
    print(f'今天总共有{len(all_today_trades_df)}条调仓数据')

    # 倒序排序并重置索引
    if not all_today_trades_df.empty:
        exists_data = read_excel(ETF_Combination_TODAY_ADJUSTMENT_FILE, '所有今天调仓')
        exists_data['代码'] = all_today_trades_df['代码'].astype(str).str.zfill(6)
        print(f'历史数据：\n {exists_data}')

        exists_data_count = len(exists_data)
        print(f'历史数据的数量：{exists_data_count}')

        #如果所有今天调仓的数据数量大于历史数据的数据，则附加新数据到Excel中，并通知
        if exists_data_count < len(all_today_trades_df):
            # 找出新增数据
            # new_data1 = all_today_trades_df[~all_today_trades_df['strict_id'].isin(exists_data['strict_id'])]
            new_data = all_today_trades_df[~all_today_trades_df].isin(exists_data)# 解释：找出all_today_trades_df中，不在exists_data中的数据

            save_to_excel(new_data, ETF_Combination_TODAY_ADJUSTMENT_FILE, '所有今天调仓')
            # new_data = all_today_trades_df.iloc[-1]
            print(f'新增数据：\n {new_data}')

            #通知
            send_notification(f"新调仓，{new_data['组合名称']} {new_data['操作']} {new_data['股票名称']} {new_data['代码']} {new_data['新比例%']}% {new_data['最新价']} \n{new_data['时间']}")
            # return new_data
        else:
            print('没有新增数据')
            # return exists_data
    # else:
    #     print('今天没有ETF和股票组合调仓数据')

        # 检查并保存数据
    #     await check_data(all_today_trades_df)
    #     save_to_excel(all_today_trades_df, ETF_Combination_TODAY_ADJUSTMENT_FILE, '所有今天调仓')
    # else:
    #     print('今天没有ETF和股票组合调仓数据')

if __name__ == "__main__":
    # clear_sheet(ETF_Combination_TODAY_ADJUSTMENT_FILE, '所有今天调仓')
    asyncio.run(ETF_Combination_main())
