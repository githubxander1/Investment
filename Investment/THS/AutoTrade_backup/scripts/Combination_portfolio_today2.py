# Combination_portfolio_today2.py
import asyncio
import datetime
import re
from pprint import pprint

import pandas as pd
import requests

import sys
import os

from Investment.THS.AutoTrade.scripts.data_process2 import read_today_portfolio_record,save_to_operation_history_excel
from Investment.THS.AutoTrade.utils.logger import setup_logger

# # 获取根目录
others_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
# # 将others目录添加到模块搜索路径中
sys.path.append(others_dir)
# print(f'包路径：{sys.path}')

from Investment.THS.AutoTrade.config.settings import Combination_portfolio_today_file, Combination_headers, all_ids, \
    id_to_name
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe, get_new_records, normalize_time, \
    determine_market

# 使用setup_logger获取统一的logger实例
logger = setup_logger("组合_调仓日志.log")

from bs4 import BeautifulSoup

def clean_content(text):
    if not isinstance(text, str):
        return '无', '无'

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(text, 'lxml')

    # 移除 HTML 标签，获取纯文本
    clean_text = soup.get_text().strip()

    # 如果没有结构化 div 标签，返回 clean_text 作为理由，'无' 作为名称
    if not soup.find('div', class_='change_reason') and not soup.find('div', class_='change_content'):
        return ('无', clean_text or '无')

    # 提取 change_content 内容（基础理由）
    content_div = soup.find('div', class_='change_content')
    base_reasons = content_div.get_text(strip=True) if content_div else '无'

    # 提取 change_quota_content 内容（附加理由）
    quota_content_div = soup.find('div', class_='change_quota_content')
    additional_reasons = quota_content_div.get_text(strip=True) if quota_content_div else ''

    # 合并基础理由和附加理由
    clean_reasons = f"{base_reasons} {additional_reasons}".strip()

    # 提取标的名称：匹配 "调仓理由" 前面的内容
    reason_div = soup.find('div', class_='change_reason')
    if reason_div:
        name_match = re.search(r'^(.+?)\s*调仓理由', reason_div.get_text(strip=True))
        extracted_name = name_match.group(1).strip() if name_match else '无'
        logger.warning(f"从content提取标的名称: {extracted_name}")
        # send_notification(f"从content提取标的名称: {extracted_name} 为 无")
    else:
        # 新增二级提取方案：尝试从纯文本中提取
        fallback_match = re.search(r'^(.+?)\s*调仓理由', clean_text)
        extracted_name = fallback_match.group(1).strip() if fallback_match else '无'

    return (extracted_name, clean_reasons)

def fetch_and_extract_data(portfolio_id):
    url = "https://t.10jqka.com.cn/portfolio/post/v2/get_relocate_post_list"
    headers = Combination_headers
    params = {"id": portfolio_id, "dynamic_id": 0}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        logger.info(f"组合 获取数据成功 id:{portfolio_id} {id_to_name.get(str(portfolio_id), '未知组合')} ")
        # pprint(response_json)
    except requests.RequestException as e:
        logger.error(f"请求出错 (ID: {portfolio_id}): {e}")
        return []

    today_trades = []
    data = response_json.get('data', [])
    # pprint(data)
    for item in data:
        createAt = item.get('createAt', '') or ''  # 防止空值
        # print(f"时间: {createAt}")
        raw_content = item.get('content', '') or ''  # 防止空值
        relocateList = item.get('relocateList', [])  # 用于获取标的名称，比例等

        # 使用安全的内容清洗
        extracted_name, clean_reason= clean_content(raw_content)
        # print(clean_content(raw_content))

        for infos in relocateList:
            code = str(infos.get('code', '')).zfill(6)
            name = (infos.get('name') or '').replace('\n', '').strip() or '无'

            # 如果名称被隐藏，使用提取的名称
            if '***' in name:
                name = extracted_name
                logger.warning(
                    f"标的名称被隐藏，使用提取的名称: {name} - 组合id:{portfolio_id} 股票代码: {code}, 时间: {createAt}")
                    # f"从content提取标的名称: {name} - 组合id:{portfolio_id} 股票代码: {code}, 时间: {createAt}"
                # continue

            # 计算操作类型
            current_ratio = infos.get('currentRatio', 0)
            new_ratio = infos.get('newRatio', 0)
            operation = infos.get('operation', '')
            operation = '买入' if operation == 1 else '卖出'
            # if operation == 1:
            #     operation = '买入'
            # elif operation == 2:
            #     operation = '卖出'
            # operation = '买入' if new_ratio > current_ratio else '卖出'
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
            today = datetime.datetime.now().strftime('%Y-%m-%d')

            if today == createAt.split()[0]:
            # if today == createAt:
                # print(f"提取{createAt.split()[0]}")
                # print(f"今天{today}")
                today_trades.append(history_post)
            # print(f"组合id:{portfolio_id} {id_to_name.get(str(portfolio_id), '未知组合')} 时间: {createAt} 提取{createAt.split()[0]} 今天{today} {today_trades}")
    # print(f"组合id:{portfolio_id} {id_to_name.get(str(portfolio_id), '未知组合')} 时间: {createAt} {today_trades}")

    return today_trades


async def Combination_main():
    all_today_trades = []
    portfolio_stats = {}
    for portfolio_id in all_ids:
        today_trades = fetch_and_extract_data(portfolio_id)
        trade_count = len(today_trades)
        portfolio_stats[portfolio_id] = trade_count
        logger.info(f"组合ID: {portfolio_id} - 获取到 {trade_count} 条交易数据")
        all_today_trades.extend(today_trades)

        # print(f"组合id:{portfolio_id} {id_to_name.get(str(portfolio_id), '未知组合')} 数据：{today_trades}")

    # 输出每个组合的数据统计
    # logger.info("📊 每个组合的数据统计:")
    # for pid, count in portfolio_stats.items():
    #     logger.info(f"组合ID: {pid}, 名称: {id_to_name.get(str(pid), '未知组合')}, 数据条数: {count}")

    all_today_trades = sorted(all_today_trades, key=lambda x: x['时间'], reverse=True)  # 倒序排序
    all_today_trades_df = pd.DataFrame(all_today_trades)
    # 打印各列数据类型
    # print(f"今日数据列的数据类型:{all_today_trades_df.dtypes}")
    # print(f"[调试] 合并后数据: {all_today_trades_df.to_string()}")
    # logger.info(f"今日交易数据（DataFrame）:\n{all_today_trades_df}")

    # 只有在非空的情况下才进行字段处理
    if not all_today_trades_df.empty:
        all_today_trades_df['时间'] = all_today_trades_df['时间'].astype(str).apply(normalize_time)
        # print(f"[调试] 时间标准化后: {all_today_trades_df[['时间', '市场']]}")
        all_today_trades_df = all_today_trades_df.reset_index(drop=True).set_index(
            all_today_trades_df.index + 1
        )  # 从1开始
    else:
        # print("⚠️ 无今日交易数据")
        logger.info("⚠️ 今日无交易数据")
        return False, None

    # 去掉科创板和创业板的股票
    # all_today_trades_df = all_today_trades_df[
    #     ~all_today_trades_df['市场'].str.contains('科创板|创业板')
    #     ]
    # all_today_trades_df = all_today_trades_df[all_today_trades_df['市场'].isin(['沪深A股']) == True]
    all_today_trades_df = all_today_trades_df[all_today_trades_df['市场'] == '沪深A股']
    # 如果标的名称有无得，去掉标的名称为‘无’的，并通知有无的已去除
    if '无' in all_today_trades_df['标的名称'].unique():
        send_notification('标的名称无的已去除')
    all_today_trades_df = all_today_trades_df[all_today_trades_df['标的名称'] != '无']

    # 打印时去掉‘理由’列
    all_today_trades_df_without_content = all_today_trades_df.drop(columns=['理由'], errors='ignore')

    logger.info(f'今日交易数据 {len(all_today_trades_df_without_content)} 条\n{all_today_trades_df_without_content}')

    # 读取历史数据
    history_df_file = Combination_portfolio_today_file
    # history_df_file_hash = get_file_hash(history_df_file)
    expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间', '理由']

    try:
        history_df = read_today_portfolio_record(history_df_file)
        # print(f'历史数据各列数据类型: {history_df.dtypes}')
        # 获取新增数据前
        # logger.info(f"历史数据（DataFrame）:\n{history_df}")

        # ✅ 显式转换关键列类型
        history_df['代码'] = history_df['代码'].astype(str).str.zfill(6)
        history_df['新比例%'] = history_df['新比例%'].astype(float).round(2)
        history_df['最新价'] = history_df['最新价'].astype(float).round(2)

    except (FileNotFoundError, pd.errors.EmptyDataError):
        # 显式创建带列名的空DataFrame
        history_df = pd.DataFrame(columns=expected_columns)
        # history_df.to_csv(history_df_file, index=False)
        today = normalize_time(datetime.date.today().strftime('%Y%m%d'))
        save_to_operation_history_excel(history_df, history_df_file, f'{today}', index=False)
        logger.info(f'初始化历史记录文件: {history_df_file}')

    # 标准化数据格式
    all_today_trades_df = standardize_dataframe(all_today_trades_df)
    history_df = standardize_dataframe(history_df)
    # logger.info(f'标准化数据格式: \n{history_df}')

    # 获取新增数据
    new_data = get_new_records(all_today_trades_df, history_df)
    # logger.info(f'提取新增数据: \n{new_data}')
    # pprint(new_data)

    # 保存新增数据
    if not new_data.empty:
        # with open(OPRATION_RECORD_DONE_FILE, 'w') as f:
        #     f.write('1')

        new_data_without_content = new_data.drop(columns=['理由'], errors='ignore')
        # logger.info(new_data_without_content)

        header = not os.path.exists(history_df_file) or os.path.getsize(history_df_file) == 0
        today = normalize_time(datetime.date.today().strftime('%Y-%m-%d'))
        save_to_operation_history_excel(new_data, history_df_file, f'{today}', index=False)
        # logger.info(f"保存新增数据到文件：{history_df_file}")
        # 添加这一行：更新文件状态
        # from Investment.THS.AutoTrade.utils.file_monitor import update_file_status
        # update_file_status(history_df_file)
        # new_file_hash = get_file_hash(history_df_file)
        # 写入成功后，触发自动化交易


        # 发送通知
        new_data_print_without_header = new_data_without_content.to_string(index=False)
        send_notification(f" 新增交易 {len(new_data)}条：\n{new_data_print_without_header}")
        # logger.info(f"✅ 保存新增调仓数据成功 \n{history_df}")
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
    # text1 = '<div class="change_reason">保利发展调仓理由</div><div class="change_content">调仓换票</div><div class="change_quota">引用</div><div class="change_quota_content" user-data="https://news.10jqka.com.cn/20250710/c669540344.shtml">国泰海通：上半年存量土地收购有序推进 多地收购存量商品房项目落地</div>'
    # text2 = '<div class="change_reason">新亚强调仓理由</div><div class="change_content">有机硅</div><div class="change_quota">引用</div><div class="change_quota_content" user-data="https://www.iwencai.com/unifiedmobile/?q=603155.SH%E4%B8%BB%E5%8A%9B%E8%B5%84%E9%87%91%E6%B5%81%E5%90%91">新亚强2025年07月11日主力资金流出</div>'
    # text3 = '<div class="change_reason">粤宏远Ａ调仓理由</div><div class="change_content">减仓</div><div class="change_quota">引用</div><div class="change_quota_content" user-data="https://www.iwencai.com/unifiedmobile/?q=000573.SZ%E4%B8%BB%E5%8A%9B%E8%B5%84%E9%87%91%E6%B5%81%E5%90%91">粤宏远A2025年07月10日主力资金流</div>'
    # print(clean_content(text3))
