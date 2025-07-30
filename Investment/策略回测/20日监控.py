# 优化后的 20日监控.py
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

def fetch_stock_data(code, period=30):
    """
    获取指定股票的历史行情数据
    优化版本：改进错误处理和数据获取逻辑
    """
    try:
        # 根据代码前缀确定市场
        if code.startswith('sh') or code.startswith('sz'):
            symbol = code
        elif code.startswith("6"):
            symbol = f"sh{code}"
        else:
            symbol = f"sz{code}"

        today = datetime.date.today().strftime("%Y%m%d")
        # 从today往前30天的日期
        start_date = (datetime.datetime.strptime(today, "%Y%m%d") - datetime.timedelta(days=period)).strftime("%Y%m%d")

        # 获取股票历史数据
        df = ak.stock_zh_a_hist(symbol=symbol[2:] if symbol.startswith(('sh', 'sz')) else symbol,
                               period="daily",
                               adjust="qfq",
                               start_date=start_date,
                               end_date=today)

        if df.empty:
            logger.warning(f"获取股票 {code} 数据为空")
            return pd.DataFrame()

        # 数据处理
        df['日期'] = pd.to_datetime(df['日期'])
        df.set_index('日期', inplace=True)
        df.sort_index(inplace=True)

        return df.tail(period)  # 取最近period天数据

    except Exception as e:
        logger.error(f"获取股票 {code} 数据失败: {e}")
        return pd.DataFrame()

def check_strategy_ma(df: pd.DataFrame, window=20, days_threshold=3):
    """
    判断是否连续 N 天收盘价上穿或下穿均线
    :param df: 行情数据 DataFrame
    :param window: 计算均线的窗口大小（默认20日）
    :param days_threshold: 连续满足条件的天数阈值
    :return: "up" 上穿 / "down" 下穿 / None 无信号
    """
    if df.empty or len(df) < window + days_threshold:
        return None

    # 如果收盘价列不存在，尝试用收盘列
    if '收盘价' not in df.columns:
        df['收盘价'] = df['收盘']
        df.drop('收盘', axis=1, inplace=True)
        # print(df.columns)

    # 检查是否有足够的数据
    if len(df) < window + days_threshold:
        logger.warning(f"数据不足，需要至少 {window + days_threshold} 天数据，当前只有 {len(df)} 天")
        return None
    if '收盘价' not in df.columns:
        df['收盘价'] = df['收盘']
        df.drop('收盘', axis=1, inplace=True)
        # print(df.columns)
    # 计算均线
    df['MA'] = df['收盘价'].rolling(window=window).mean()

    # 检查是否成功计算出均线
    if df['MA'].isna().all():
        logger.warning(f"无法计算 {window} 日均线")
        return None

    # 计算价格与均线的关系
    df['信号'] = df['收盘价'] > df['MA']

    # 检查最近的数据点
    if df['MA'].iloc[-1] != df['MA'].iloc[-1]:  # 检查NaN
        logger.warning(f"最近一天的 {window} 日均线为NaN")
        return None

    # 分析最近连续满足条件的天数
    last_signal = df.iloc[-1]['信号']
    count = 0

    # 从最近一天开始向前检查
    for i in range(1, min(days_threshold + 1, len(df) + 1)):
        if pd.isna(df.iloc[-i]['信号']):
            break
        if df.iloc[-i]['信号'] == last_signal:
            count += 1
        else:
            break

    # 只有当连续天数达到阈值时才发出信号
    if count >= days_threshold:
        # 额外检查：确保信号变化是显著的（避免在均线附近震荡）
        current_price = df.iloc[-1]['收盘价']
        ma_value = df.iloc[-1]['MA']
        price_ma_diff = abs(current_price - ma_value) / ma_value

        # 如果价格与均线差异过小（小于0.5%），认为信号不够强烈
        if price_ma_diff < 0.005:
            logger.info(f"价格与均线差异过小 ({price_ma_diff:.4f})，不发出信号")
            return None

        return "up" if last_signal else "down"

    return None

def daily_check(monitor_type, monitor_ids=None, ma_window=20):
    """
    统一的每日检查函数，支持股票和ETF检查
    :param monitor_type: 检查类型，"stock" 或 "etf"
    :param monitor_ids: 要监控的ID字典，格式为 {code: name}
    :param ma_window: 均线窗口大小，默认20日
    """
    today = datetime.date.today()
    if not is_trading_day(today):
        logger.info(f"{today} 是非交易日，跳过本次监控")
        return

    logger.info(f"开始执行每日{monitor_type.upper()}策略监控任务：{today}，使用{ma_window}日均线")

    for code, name in monitor_ids.items():
        logger.info(f"正在获取 {name}({code}) 的数据...")

        # 根据类型获取数据
        if monitor_type.lower() == "stock":
            df = fetch_stock_data(code, period=max(30, ma_window + 10))  # 确保有足够的数据
        elif monitor_type.lower() == "etf":
            df = fetch_etf_data(code, period=max(30, ma_window + 10))
        else:
            logger.error(f"不支持的监控类型: {monitor_type}")
            continue

        if df.empty:
            logger.warning(f"{name}({code}) 数据为空，跳过检查")
            continue

        # 根据类型选择不同的均线窗口
        if monitor_type.lower() == "stock":
            signal = check_strategy_ma(df, window=ma_window, days_threshold=3)  # 股票使用5日均线
        else:
            signal = check_strategy_ma(df, window=ma_window, days_threshold=3)  # ETF使用指定窗口均线

        if signal == "up":
            if monitor_type.lower() == "stock":
                msg = f"📈【{name}】({code}) 收盘价上穿{ma_window}日均线，建议关注买入机会！"
            else:
                msg = f"📈【{name}】({code}) 收盘价上穿{ma_window}日均线，建议关注买入机会！"
            send_notification(msg)
            logger.info(msg)
        elif signal == "down":
            if monitor_type.lower() == "stock":
                msg = f"📉【{name}】({code}) 收盘价下穿{ma_window}日均线，建议关注卖出机会！"
            else:
                msg = f"📉【{name}】({code}) 收盘价下穿{ma_window}日均线，建议关注卖出机会！"
            send_notification(msg)
            logger.info(msg)
        else:
            logger.info(f"{name}({code}) 当前未出现明显趋势信号")

# 定时执行器（每天15:00执行）
def schedule_daily_task(target_time="15:00"):
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time == target_time:
            try:
                # 执行ETF检查
                daily_check("etf", MONITORED_ETFS, ma_window=20)
            except Exception as e:
                logger.error(f"执行监控任务时发生异常: {e}")

            # 防止重复执行
            time.sleep(60)

        time.sleep(10)  # 每10秒检查一次时间
        logger.info(f"当前时间：{current_time}, 等待下一次执行...")

if __name__ == '__main__':
    # 要监控的 ETF
    MONITORED_ETFS = {
        "508011": "嘉实物美消费REIT",
        "508005": "华夏首创奥莱REIT",
        "511380": "可转债ETF",
        "511580": "国债证金债ETF",
        "518850": "黄金ETF华夏",
        # 可添加更多 ETF
    }

    # 定义要监控的股票
    MONITORED_STOCKS = {
        # "600570": "恒生电子",
        # "000573": "粤宏远A"
        "600858": "银座股份",
        "603978": "深圳新星",
        "603278": "大业股份",
        "603018": "华社集团",

        # 可添加更多股票
    }

    # 执行股票检查（使用5日均线）
    daily_check("stock", MONITORED_STOCKS, ma_window=20)

    # 执行ETF检查（使用20日均线）
    # daily_check("etf", MONITORED_ETFS, ma_window=20)

    # 启动定时任务
    # schedule_daily_task()
