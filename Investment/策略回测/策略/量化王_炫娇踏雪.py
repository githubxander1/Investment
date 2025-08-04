# 量化王_炫娇踏雪.py
import asyncio
import datetime
import time
import pandas as pd
import requests
from pprint import pprint

# 导入必要的工具函数和配置
from Investment.THS.AutoTrade.scripts.data_process import read_today_portfolio_record, save_to_operation_history_excel
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe, get_new_records, normalize_time, determine_market
from Investment.THS.AutoTrade.config.settings import Strategy_portfolio_today_file

# 使用setup_logger获取统一的logger实例
logger = setup_logger("量化王_炫娇踏雪.log")

# 策略配置
STRATEGY_ID = "8001"
STRATEGY_NAME = "量化王_炫娇踏雪"

def fetch_strategy_data():
    """
    获取量化王策略数据
    """
    url = "https://prod-lhw-strategy-data-center.ydtg.com.cn/lhwDataCenter/getQSChangeByIdAndDateNew"

    # 计算日期范围（最近30天）
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")

    params = {
        "poolId": STRATEGY_ID,
        "startDate": start_date,
        "endDate": end_date,
        "by": "date",
        "ascOrDesc": "DESC",
        "startIndex": "0",
        "pageSize": "50"  # 增加获取的数据量
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTY4MjA1NzgsImlhdCI6MTc1NDE0MjE3OH0.yKBdHg0gGPzkbEbX2_stiSXAY5uQxgQueL4rI7IlnOU",
        "Host": "prod-lhw-strategy-data-center.ydtg.com.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.12.0"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            response_json = response.json()
            logger.info(f"量化王策略数据获取成功: {STRATEGY_NAME}")
            return response_json.get('data', [])
        except requests.RequestException as e:
            logger.warning(f"请求出错, 第{attempt+1}次重试: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                logger.error(f"请求最终失败: {e}")
                return []

def process_strategy_data(raw_data):
    """
    处理策略数据，提取今日交易
    """
    today_trades = []
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    for item in raw_data:
        trade_date = item.get('date', '')
        sec_code = item.get('sec_code', '')
        sec_name = item.get('sec_name', '')
        transaction_price = item.get('transaction_price', 0)
        operation = item.get('type', '')

        # 提取股票代码（去除SH/SZ前缀）
        if sec_code.startswith('SH'):
            code = sec_code[2:]
        elif sec_code.startswith('SZ'):
            code = sec_code[2:]
        else:
            code = sec_code

        code = str(code).zfill(6)  # 格式化为6位数字

        # 确定市场
        market = determine_market(code)

        # 构造交易记录
        trade_record = {
            '名称': STRATEGY_NAME,
            '操作': operation,
            '标的名称': sec_name,
            '代码': code,
            '最新价': transaction_price,
            '新比例%': None,  # 策略数据中没有比例信息
            '市场': market,
            '时间': trade_date,
            '理由': f"量化王策略信号 - {operation}"
        }

        # 只保留今天的交易
        if today == trade_date:
            today_trades.append(trade_record)
            logger.info(f"提取到今日交易: {sec_name}({code}) {operation} @ {transaction_price}")

    return today_trades

async def Strategy_main():
    """
    主函数，获取并处理量化王策略数据
    """
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    logger.info(f'开始处理量化王策略数据，日期: {today}')

    # 获取策略数据
    raw_data = fetch_strategy_data()
    if not raw_data:
        logger.warning("未能获取到策略数据")
        return False, None

    logger.info(f"共获取到 {len(raw_data)} 条策略数据")

    # 处理数据，提取今日交易
    today_trades = process_strategy_data(raw_data)

    if not today_trades:
        logger.info("---------------量化王策略 今日无交易数据----------------")
        return False, None

    # 转换为DataFrame
    today_trades_df = pd.DataFrame(today_trades)
    today_trades_df = today_trades_df.sort_values('时间', ascending=False)  # 按时间倒序排序

    # 标准化数据格式
    today_trades_df = standardize_dataframe(today_trades_df)

    # 打印时去掉'理由'列
    today_trades_df_without_content = today_trades_df.drop(columns=['理由'], errors='ignore')
    logger.info(f'今日交易数据 {len(today_trades_df_without_content)} 条\n{today_trades_df_without_content}')

    # 读取历史数据
    history_df_file = Strategy_portfolio_today_file
    expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间', '理由']

    try:
        history_df = read_today_portfolio_record(history_df_file)

        # 显式转换关键列类型
        if not history_df.empty:
            history_df['代码'] = history_df['代码'].astype(str).str.zfill(6)
            if '新比例%' in history_df.columns:
                history_df['新比例%'] = history_df['新比例%'].astype(float).round(2)
            if '最新价' in history_df.columns:
                history_df['最新价'] = history_df['最新价'].astype(float).round(2)

    except Exception as e:
        # 显式创建带列名的空DataFrame
        history_df = pd.DataFrame(columns=expected_columns)
        today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
        save_to_operation_history_excel(history_df, history_df_file, f'{today}', index=False)
        logger.info(f'初始化历史记录文件: {history_df_file}')

    # 标准化数据格式
    history_df = standardize_dataframe(history_df)

    # 获取新增数据
    new_data = get_new_records(today_trades_df, history_df)

    # 过滤掉科创板和创业板的股票
    new_data = new_data[new_data['市场'] == '沪深A股']

    # 保存新增数据
    if not new_data.empty:
        new_data_without_content = new_data.drop(columns=['理由'], errors='ignore')

        today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 保存到文件
        save_to_operation_history_excel(new_data, history_df_file, f'{today}', index=False)

        # 发送通知
        new_data_print_without_header = new_data_without_content.to_string(index=False)
        send_notification(f"量化王策略 新增交易 {len(new_data)}条：\n{new_data_print_without_header}")

        logger.info(f"✅ 保存新增策略数据成功")
        return True, new_data
    else:
        logger.info("---------------量化王策略 无新增交易数据----------------")
        return False, None

if __name__ == '__main__':
    # 测试代码
    asyncio.run(Strategy_main())

    # 测试数据解析
    # test_data = [
    #     {
    #         'date': '2025-07-24',
    #         'sec_code': 'SZ002956',
    #         'sec_name': '西麦食品',
    #         'stockpool_id': '8001',
    #         'time_stamp': 1753320600000,
    #         'transaction_price': 20.42,
    #         'type': '买入'
    #     }
    # ]
    # pprint(process_strategy_data(test_data))
