# Combination_portfolio_today.py
import asyncio
import datetime
import re
# from pprint import pprint

import pandas as pd
import requests

import sys
import os

from Investment.THS.AutoTrade.scripts.data_process import read_portfolio_record_history, save_to_excel
from Investment.THS.AutoTrade.utils.logger import setup_logger

# # 获取根目录
others_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
# # 将others目录添加到模块搜索路径中
sys.path.append(others_dir)
# print(f'包路径：{sys.path}')

from Investment.THS.AutoTrade.config.settings import Combination_portfolio_today, Combination_headers, all_ids, \
    id_to_name
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe, get_new_records, normalize_time, \
    determine_market

# 使用setup_logger获取统一的logger实例
logger = setup_logger("组合_调仓日志.log")


def fetch_and_extract_data(portfolio_id):
    url = "https://t.10jqka.com.cn/portfolio/post/v2/get_relocate_post_list"
    headers = Combination_headers
    params = {"id": portfolio_id, "dynamic_id": 0}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        logger.info(f"组合 获取数据成功id:{portfolio_id} {id_to_name.get(str(portfolio_id), '未知组合')} ")
        # pprint(response_json)
    except requests.RequestException as e:
        logger.error(f"请求出错 (ID: {portfolio_id}): {e}")
        return []

    today_trades = []
    data = response_json.get('data', [])
    # pprint(data)
    for item in data:
        createAt = item.get('createAt', '') or ''  # 防止空值
        raw_content = item.get('content', '') or ''  # 防止空值
        relocateList = item.get('relocateList', [])

        # 优化内容提取逻辑
        def clean_content(text):
            """清洗HTML内容并提取多个调仓理由"""
            if not isinstance(text, str):
                return '无'

            # 移除HTML标签
            clean_text = re.sub(r'<[^>]+>', '', text).strip()

            # 如果没有结构化 div 标签，则返回纯文本
            if 'class="change_reason"' not in text:
                return clean_text or '无'

            # 使用正则提取所有 reason + content
            pattern = r'<div class="change_reason">(.*?)</div>\s*<div class="change_content">(.*?)</div>'
            matches = re.findall(pattern, text, re.DOTALL)

            # 合并多个理由
            result = '\n'.join([f"{title.strip()}：{content.strip()}" for title, content in matches])

            return result or '无'


        # 使用安全的内容清洗
        clean_reason = clean_content(raw_content)

        for infos in relocateList:
            name = infos.get('name', None).replace('\n', '').strip() or '无'

            code = infos.get('code', None)

            if '***' in name:
                logger.warning(
                    f"未订阅或标的名称显示异常 -组合id:{portfolio_id} 股票代码: {code}, 时间: {createAt}")
                continue

            # 计算操作类型
            current_ratio = infos.get('currentRatio', 0)
            new_ratio = infos.get('newRatio', 0)
            operation = '买入' if new_ratio > current_ratio else '卖出'
            # # 计算操作比例，并转换成股数
            # operation_ratio = (new_ratio - current_ratio) * 100
            # stock_num = round(operation_ratio / 100 * 10000)

            market = determine_market(code)

            history_post = {
                '名称': id_to_name.get(str(portfolio_id), '未知组合'),
                '操作': operation,
                '标的名称': name,
                '代码': str(code).zfill(6),  # 提前统一格式
                '最新价': infos.get('finalPrice'),
                # '旧比例%': round(current_ratio * 100, 2),
                '新比例%': round(new_ratio * 100, 2),
                '市场': market,
                '时间': createAt,
                '理由': clean_reason
            }

            # 昨天日期
            # today = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            today = datetime.date.today().strftime('%Y-%m-%d')

            if today == createAt.split()[0]:
                today_trades.append(history_post)

    return today_trades


async def Combination_main():
    all_today_trades = []
    for portfolio_id in all_ids:
        today_trades = fetch_and_extract_data(portfolio_id)
        all_today_trades.extend(today_trades)

    all_today_trades = sorted(all_today_trades, key=lambda x: x['时间'], reverse=True)  # 倒序排序
    all_today_trades_df = pd.DataFrame(all_today_trades)

    # 只有在非空的情况下才进行字段处理
    if not all_today_trades_df.empty:
        all_today_trades_df['时间'] = all_today_trades_df['时间'].astype(str).apply(normalize_time)

        all_today_trades_df = all_today_trades_df.reset_index(drop=True).set_index(
            all_today_trades_df.index + 1
        )  # 从1开始
    else:
        # print("⚠️ 无今日交易数据")
        logger.info("⚠️ 今日无交易数据")
        return False, None

    # 去掉科创板和创业板的股票
    all_today_trades_df = all_today_trades_df[
        ~all_today_trades_df['标的名称'].str.contains('科创板|创业板')
        ]
    # 打印时去掉‘理由’列
    all_today_trades_df_without_content = all_today_trades_df.drop(columns=['理由'], errors='ignore')

    logger.info(f'今日交易数据 {len(all_today_trades_df_without_content)} 条\n{all_today_trades_df_without_content}')

    # 读取历史数据
    existing_data_file = Combination_portfolio_today
    # existing_data_file_hash = get_file_hash(existing_data_file)
    expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间', '理由']

    try:
        existing_data = read_portfolio_record_history(existing_data_file)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # 显式创建带列名的空DataFrame
        existing_data = pd.DataFrame(columns=expected_columns)
        # existing_data.to_csv(existing_data_file, index=False)
        today = normalize_time(datetime.date.today().strftime('%Y%m%d'))
        save_to_excel(existing_data, existing_data_file, f'{today}', index=False)
        logger.info(f'初始化历史记录文件: {existing_data_file}')

    # 标准化数据格式
    all_today_trades_df = standardize_dataframe(all_today_trades_df)
    existing_data = standardize_dataframe(existing_data)
    # logger.info(f'标准化数据格式: \n{existing_data}')

    # 获取新增数据
    new_data = get_new_records(all_today_trades_df, existing_data)
    # logger.info(f'提取新增数据: \n{new_data}')
    # pprint(new_data)

    # 保存新增数据
    if not new_data.empty:
        # with open(OPRATION_RECORD_DONE_FILE, 'w') as f:
        #     f.write('1')

        new_data_without_content = new_data.drop(columns=['理由'], errors='ignore')
        # logger.info(new_data_without_content)

        header = not os.path.exists(existing_data_file) or os.path.getsize(existing_data_file) == 0
        today = normalize_time(datetime.date.today().strftime('%Y-%m-%d'))
        save_to_excel(new_data, existing_data_file, f'{today}', index=False)
        # logger.info(f"保存新增数据到文件：{existing_data_file}")
        # 添加这一行：更新文件状态
        # from Investment.THS.AutoTrade.utils.file_monitor import update_file_status
        # update_file_status(existing_data_file)
        # new_file_hash = get_file_hash(existing_data_file)
        # 写入成功后，触发自动化交易


        # 发送通知
        new_data_print_without_header = new_data_without_content.to_string(index=False)
        send_notification(f" 新增交易 {len(new_data)}条：\n{new_data_print_without_header}")
        # logger.info(f"✅ 保存新增调仓数据成功 \n{existing_data}")
        # from Investment.THS.AutoTrade.utils.event_bus import event_bus
        # event_bus.publish('new_trades_available', new_data)
        # from Investment.THS.AutoTrade.utils.trade_utils import mark_new_trades_as_scheduled
        #
        # mark_new_trades_as_scheduled(new_data, OPERATION_HISTORY_FILE)

        return True, new_data
    else:
        logger.info("---------------组合 无新增交易数据----------------")
        return False, None

if __name__ == '__main__':
    asyncio.run(Combination_main())
