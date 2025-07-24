import akshare as ak
import pandas as pd
import time
import datetime
import logging
from Investment.THS.AutoTrade.utils.notification import send_notification

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 获取中国交易日历（用于判断是否为交易日）
def is_trading_day(date: datetime.date) -> bool:
    """
    判断是否为中国股市的交易日（简单实现，可替换为真实数据）
    :param date: 日期
    :return: 是否是交易日
    """
    # 忽略周六周日
    if date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        return False

    # 可以在此添加节假日列表进行排除
    holidays = [
        (1, 1),     # 元旦
        (2, 10),    # 春节
        (4, 5),     # 清明
        (5, 1),     # 劳动节
        (6, 22),    # 端午
        (9, 30),    # 国庆
    ]

    return not ((date.month, date.day) in holidays)

# 获取 ETF 历史行情数据
def fetch_etf_data(code: str, period=30):
    """
    获取 ETF 历史行情数据
    :param code: ETF 代码（如 '508011'）
    :param period: 获取最近多少天的数据
    :return: DataFrame
    """
    try:
        symbol = f"sh{code}" if code.startswith("5") else f"sz{code}"
        df = ak.fund_etf_hist_sina(symbol=symbol)
        df.columns = ['日期', '开盘价', '最高价', '最低价', '收盘价', '成交量']
        df['日期'] = pd.to_datetime(df['日期'])
        df.set_index('日期', inplace=True)
        df.sort_index(inplace=True)
        return df.tail(period)
    except Exception as e:
        logger.error(f"获取 ETF {code} 数据失败: {e}")
        return pd.DataFrame()
def fetch_stock_data(code, period):
    """获取指定股票的历史行情数据"""
    try:
        df = ak.stock_zh_a_hist(symbol=code[2:], period="daily", adjust="qfq")
        df.columns = ['日期', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
        df['日期'] = pd.to_datetime(df['日期'])
        df.set_index('日期', inplace=True)
        return df.tail(period)  # 取最近20天数据计算均线
    except Exception as e:
        logger.error(f"获取股票 {code} 数据失败: {e}")
        return pd.DataFrame()

def check_strategy_5_ma(df: pd.DataFrame, window=5, days_threshold=3):
    """
    判断是否连续 N 天收盘价上穿或下穿20日均线
    :param df: 行情数据 DataFrame
    :param window: 计算均线的窗口大小（默认20日）
    :param days_threshold: 连续满足条件的天数阈值
    :return: "up" 上穿 / "down" 下穿 / None 无信号
    """
    if df.empty or len(df) < window + days_threshold:
        return None

    df['5日均线'] = df['收盘价'].rolling(window=window).mean()
    df['信号'] = df['收盘价'] > df['5日均线']

    # 找出最近连续满足条件的天数
    last_signal = df.iloc[-1]['信号']
    count = 0
    for i in range(1, days_threshold + 1):
        if df.iloc[-i]['信号'] == last_signal:
            count += 1
        else:
            break

    if count >= days_threshold:
        return "up" if last_signal else "down"
    return None

# 判断均线突破策略
def check_strategy_20_ma(df: pd.DataFrame, window=20, days_threshold=3):
    """
    判断是否连续 N 天收盘价上穿或下穿20日均线
    :param df: 行情数据 DataFrame
    :param window: 计算均线的窗口大小（默认20日）
    :param days_threshold: 连续满足条件的天数阈值
    :return: "up" 上穿 / "down" 下穿 / None 无信号
    """
    if df.empty or len(df) < window + days_threshold:
        return None

    df['20日均线'] = df['收盘价'].rolling(window=window).mean()
    df['信号'] = df['收盘价'] > df['20日均线']

    # 找出最近连续满足条件的天数
    last_signal = df.iloc[-1]['信号']
    count = 0
    for i in range(1, days_threshold + 1):
        if df.iloc[-i]['信号'] == last_signal:
            count += 1
        else:
            break

    if count >= days_threshold:
        return "up" if last_signal else "down"
    return None
def daily_stock_check():
    today = datetime.date.today()
    if not is_trading_day(today):
        logger.info(f"{today} 是非交易日，跳过股票策略检查")
        return

    logger.info("开始执行股票策略检查")

    for code, name in MONITORED_STOCKS.items():
        df = fetch_stock_data(code,30)
        signal = check_strategy_5_ma(df)

        if signal == "up":
            msg = f"{name}({code}) 收盘价今日上穿5日均线，建议关注！"
            send_notification(msg)
            logger.info(msg)
        elif signal == "down":
            msg = f"{name}({code}) 近 3 天收盘价持续下穿5日均线，建议关注卖出机会！"
            send_notification(msg)
            logger.info(msg)
        else:
            logger.info(f"{name}({code}) 当前未出现明显趋势信号")
def daily_monitor(MONITORED_ids=None):
    today = datetime.date.today()
    if not is_trading_day(today):
        logger.info(f"{today} 是非交易日，跳过本次监控")
        return

    logger.info(f"开始执行每日策略监控任务：{today}")

    for code, name in MONITORED_ids.items():
        df = fetch_etf_data(code, period=30)
        signal = check_strategy_20_ma(df, window=20, days_threshold=3)

        if signal == "up":
            msg = f"{name}({code}) 近 3 天收盘价持续上穿20日均线，建议关注买入机会！"
            send_notification(msg)
            logger.info(msg)
        elif signal == "down":
            msg = f"{name}({code}) 近 3 天收盘价持续下穿20日均线，建议关注卖出机会！"
            send_notification(msg)
            logger.info(msg)
        else:
            logger.info(f"{name}({code}) 当前未出现明显趋势信号")

    # for code, name in MONITORED_ids.items():
    #     df = fetch_stock_data(code, period=30)
    #     signal = check_strategy_20_ma(df, window=20, days_threshold=3)
    #
    #     if signal == "up":
    #         msg = f"{name}({code}) 近 3 天收盘价持续上穿20日均线，建议关注买入机会！"
    #         send_notification(msg)
    #         logger.info(msg)
    #     elif signal == "down":
    #         msg = f"{name}({code}) 近 3 天收盘价持续下穿20日均线，建议关注卖出机会！"
    #         send_notification(msg)
    #         logger.info(msg)
    #     else:
    #         logger.info(f"{name}({code}) 当前未出现明显趋势信号")

# 定时执行器（每天15:00执行）
def schedule_daily_task(target_time="15:00"):
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time == target_time:
            try:
                daily_monitor()
            except Exception as e:
                logger.error(f"执行监控任务时发生异常: {e}")

            # 防止重复执行
            time.sleep(60)

        time.sleep(10)  # 每10秒检查一次时间
        logger.info(f"当前时间：{current_time}, 等待下一次执行...")

if __name__ == '__main__':
    # 要监控的股票
    # MONITORED_STOCKS = {
    #     "sh000573": "粤宏远A",
    #     "sz600570": "恒生电子"
    # }
    # 要监控的 ETF
    MONITORED_ETFS = {
        "508011": "嘉实物美消费REIT",
        "508005": "华夏首创奥莱REIT",
        # 可添加更多 ETF
    }
    schedule_daily_task()
    # daily_monitor()
    # daily_stock_check()