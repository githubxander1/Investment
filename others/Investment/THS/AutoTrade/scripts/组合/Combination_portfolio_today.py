import asyncio
import csv
import datetime
import os
import re
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
    Combination_ids_to_name, Combination_portfolio_today, Combination_headers, all_ids, id_to_name, \
    OPRATION_RECORD_DONE_FILE
from others.Investment.THS.AutoTrade.utils.determine_market import determine_market
from others.Investment.THS.AutoTrade.utils.notification import send_notification
# from others.Investment.THS.AutoTrade.utils.excel_handler import save_to_excel, clear_sheet, read_excel, \
#     create_empty_excel

# logger = setup_print(ETF_ADJUSTMENT_LOG_FILE)

def fetch_and_extract_data(portfolio_id):
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
    data = response_json.get('data', [])
    # pprint(data)
    for item in data:
        createAt = item.get('createAt', '') or '' # 防止空值
        raw_content = item.get('content', '') or '' #防止空值
        relocateList = item.get('relocateList', [])

        # 优化内容提取逻辑
        def clean_content(text):
            """清洗HTML内容并提取关键信息"""
            # 移除HTML标签
            clean_text = re.sub(r'<[^>]+>', '', text)
            # 提取调仓理由模式
            # 增加空值检查
            if not isinstance(text, str):
                return '无'

            # 预处理内容
            text = text.replace('\n', ' ').replace('\r', ' ')
            # 提取结构化理由
            reasons = re.findall(
                r'<div class="change_reason">([^<]*)</div>\s*<div class="change_content">([^<]*)</div>',
                text
            )
            # 合并多个理由
            if reasons:
                return '\n'.join([f"{title.strip()}：{content.strip()}"
                                for title, content in reasons])
            # 降级处理：移除所有HTML标签
            return re.sub(r'<[^>]+>', '', text).strip() or '无'

        # 使用安全的内容清洗
        clean_reason = clean_content(raw_content)

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
            # # 获取组合名称
            # if is_etf:
            #     combination_name = ETF_ids_to_name.get(portfolio_id, '未知ETF组合')
            # else:
            #     combination_name = Combination_ids_to_name.get(portfolio_id, '未知股票组合')

            history_post = {
                '名称': id_to_name.get(str(portfolio_id), '未知组合'),
                '操作': operation,
                '标的名称': name,
                '代码': str(code).zfill(6),  # 提前统一格式
                '最新价': infos.get('finalPrice'),
                # '当前比例%': round(current_ratio * 100, 2),
                '新比例%': round(new_ratio * 100, 2),
                '市场': market,
                '时间': createAt,
                '理由': clean_reason
            }
            # 今天更新的
            # today = datetime.date.today().strftime('%Y-%m-%d')
            #昨天
            # yesterday \
            today= (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')


            if today == createAt.split()[0]:
                today_trades.append(history_post)

    return today_trades


async def Combination_main():
    all_today_trades = []
    for portfolio_id in all_ids:
        # print(all_ids)
        # print(f"正在处理组合ID: {portfolio_id}")
        today_trades = fetch_and_extract_data(portfolio_id)
        all_today_trades.extend(today_trades)

    all_today_trades = sorted(all_today_trades, key=lambda x: x['时间'], reverse=True)  # 倒序排序

    # 转换成pd表格样式
    all_today_trades_df = pd.DataFrame(all_today_trades)

    def normalize_time(time_str):
        # 保留到分钟级别
        return " ".join(time_str.split())[:16]  # 截断至 'YYYY-MM-DD HH:MM'

    # 只有在非空的情况下才进行字段处理
    if not all_today_trades_df.empty:
        all_today_trades_df['时间'] = all_today_trades_df['时间'].apply(normalize_time)
        all_today_trades_df = all_today_trades_df.reset_index(drop=True).set_index(
            all_today_trades_df.index + 1
        )  # 从1开始
    else:
        # print("今日无任何交易更新")
        print("⚠️ 当前无今日交易数据")
        return

    # 打印时去掉‘理由’列
    all_today_trades_df_without_content = all_today_trades_df.drop(columns=['理由'], errors='ignore')
    print(all_today_trades_df_without_content)

    # 读取历史数据
    existing_data_file = Combination_portfolio_today
    expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间', '理由']

    try:
        existing_data = pd.read_csv(existing_data_file)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # 显式创建带列名的空DataFrame
        existing_data = pd.DataFrame(columns=expected_columns)
        existing_data.to_csv(existing_data_file, index=False)
        print(f'初始化历史记录文件: {existing_data_file}')

    # 确保列结构一致
    existing_data = existing_data.reindex(columns=expected_columns, fill_value=None)

    # 标准化历史数据格式：代码补零 + 时间标准化
    if not existing_data.empty:
        existing_data['代码'] = existing_data['代码'].astype(str).str.zfill(6)
        existing_data['时间'] = existing_data['时间'].apply(normalize_time)
        existing_data['_id'] = existing_data['时间'].astype(str) + '_' + existing_data['代码'].astype(str)
        # print("existing_data _id:", existing_data['_id'].tolist())

    # 处理 today_trades 数据
    if not all_today_trades_df.empty:
        # 添加唯一标识 _id
        all_today_trades_df['_id'] = all_today_trades_df['时间'].astype(str) + '_' + all_today_trades_df['代码'].astype(str)
        # print("all_today_trades_df _id:", all_today_trades_df['_id'].tolist())

        new_mask = ~all_today_trades_df['_id'].isin(existing_data['_id']) if not existing_data.empty else []
        new_data = all_today_trades_df[new_mask].copy().drop(columns=['_id']) if not existing_data.empty else all_today_trades_df.copy().drop(columns=['_id'])

        # 保存新增数据
        if not new_data.empty:
            with open(OPRATION_RECORD_DONE_FILE, 'w') as f:
                f.write('1')
            print(f'发现{len(new_data)}条新增交易:')
            new_data_without_content = new_data.drop(columns=['理由'], errors='ignore')
            print(new_data_without_content)
            header = not os.path.exists(existing_data_file) or os.path.getsize(existing_data_file) == 0
            new_data.to_csv(existing_data_file, mode='a', header=header, index=False)
            #通知时不要显示标题行
            # new_data_print_without_header = new_data.drop(columns=['理由'], errors='ignore').to_string(index=False)
            new_data_print_without_header = new_data_without_content.drop(columns=['理由'], errors='ignore').to_string(index=False)
            send_notification(f"{len(new_data)} 条新增交易，\n {new_data_print_without_header}")
            #创建标志文件
        else:
            print("---------------今日无新增交易数据----------------")
    else:
        print("---------今日无任何交易更新-----------")




if __name__ == '__main__':
    asyncio.run(Combination_main())
