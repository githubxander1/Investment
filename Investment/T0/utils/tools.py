import os
import sys
import time
from datetime import datetime, timedelta
import pytz

# 添加项目根目录到路径，以便导入其他模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 股票代码和名称映射
STOCK_NAME_MAPPING = {
    '000333': '美的集团',
    '600036': '招商银行',
    '600900': '长江电力',
    '601088': '中国神华'
}

# 假设notification模块存在于项目中
try:
    from notification import send_notification
except ImportError:
    # 如果没有notification模块，定义一个占位函数
    def send_notification(title, content):
        """发送通知的占位函数"""
        print(f"通知: {title}\n{content}")


def get_stock_name(stock_code):
    """
    根据股票代码获取股票名称
    
    参数:
    stock_code: 股票代码
    
    返回:
    str: 股票名称
    """
    return STOCK_NAME_MAPPING.get(stock_code, stock_code)


def is_trading_time():
    """
    检查当前是否为A股交易时间
    
    返回:
    bool: 是否为交易时间
    """
    # 获取当前北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    
    # 获取当前日期和时间
    current_date = now.date()
    current_time = now.time()
    
    # 检查是否为周末
    if current_date.weekday() >= 5:  # 周六或周日
        return False
    
    # 定义交易时间段
    morning_start = datetime.strptime('09:30:00', '%H:%M:%S').time()
    morning_end = datetime.strptime('11:30:00', '%H:%M:%S').time()
    afternoon_start = datetime.strptime('13:00:00', '%H:%M:%S').time()
    afternoon_end = datetime.strptime('19:00:00', '%H:%M:%S').time()
    
    # 检查是否在交易时间内
    is_morning_trading = morning_start <= current_time <= morning_end
    is_afternoon_trading = afternoon_start <= current_time <= afternoon_end
    
    return is_morning_trading or is_afternoon_trading


def wait_until_trading_time():
    """
    等待直到交易时间开始
    """
    while not is_trading_time():
        # 获取当前北京时间
        beijing_tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(beijing_tz)
        
        # 计算下次交易时间
        next_trading_time = None
        
        # 检查是否为周末
        if now.weekday() >= 5:  # 周六或周日
            # 下周一早上9:30
            days_ahead = 7 - now.weekday() if now.weekday() < 6 else 1
            next_trading_date = now.date() + timedelta(days=days_ahead)
            next_trading_time = datetime.combine(next_trading_date, datetime.strptime('09:30:00', '%H:%M:%S').time())
            next_trading_time = beijing_tz.localize(next_trading_time)
        else:
            # 工作日，检查当前时间
            morning_start = datetime.combine(now.date(), datetime.strptime('09:30:00', '%H:%M:%S').time())
            morning_start = beijing_tz.localize(morning_start)
            morning_end = datetime.combine(now.date(), datetime.strptime('11:30:00', '%H:%M:%S').time())
            morning_end = beijing_tz.localize(morning_end)
            afternoon_start = datetime.combine(now.date(), datetime.strptime('13:00:00', '%H:%M:%S').time())
            afternoon_start = beijing_tz.localize(afternoon_start)
            afternoon_end = datetime.combine(now.date(), datetime.strptime('15:00:00', '%H:%M:%S').time())
            afternoon_end = beijing_tz.localize(afternoon_end)
            
            if now < morning_start:
                # 今天早上交易时间还没开始
                next_trading_time = morning_start
            elif now > morning_end and now < afternoon_start:
                # 午休时间
                next_trading_time = afternoon_start
            elif now > afternoon_end:
                # 今天交易时间已结束，等待下一个交易日
                days_ahead = 1
                if now.weekday() == 4:  # 周五
                    days_ahead = 3
                next_trading_date = now.date() + timedelta(days=days_ahead)
                next_trading_time = datetime.combine(next_trading_date, datetime.strptime('09:30:00', '%H:%M:%S').time())
                next_trading_time = beijing_tz.localize(next_trading_time)
        
        # 计算等待时间（秒）
        wait_seconds = (next_trading_time - now).total_seconds()
        
        # 显示等待信息
        print(f"当前非交易时间，将在 {next_trading_time.strftime('%Y-%m-%d %H:%M:%S')} 开始交易，等待 {wait_seconds:.0f} 秒...")
        
        # 等待，但每60秒检查一次是否需要提前结束等待（例如手动中断）
        wait_interval = 60  # 秒
        while wait_seconds > 0:
            sleep_time = min(wait_interval, wait_seconds)
            time.sleep(sleep_time)
            wait_seconds -= sleep_time
            
            # 检查是否需要提前结束等待（例如有新的输入）
            # 这里可以根据实际需求添加检查逻辑


def notify_signal(signal_type, stock_code, price, time_str):
    """
    发送买卖信号通知
    
    参数:
    signal_type: 信号类型，'buy'或'sell'
    stock_code: 股票代码
    price: 价格
    time_str: 时间字符串
    """
    try:
        # 处理特殊情况：如果signal_type为"signal"，则time_str是完整的消息内容
        if signal_type == "signal":
            # 这种情况下，time_str包含完整的消息内容
            title = "T0交易信号"
            content = time_str
        else:
            if isinstance(price, str):
                # 尝试将价格转换为浮点数
                try:
                    price = float(price)
                except ValueError:
                    price = 0.0
            
            stock_name = get_stock_name(stock_code)
            if signal_type.lower() == 'buy':
                title = f"买入信号 - {stock_name}({stock_code})"
                content = f"股票 {stock_name}({stock_code}) 在 {time_str} 发出买入信号，价格: {price:.2f}"
            elif signal_type.lower() == 'sell':
                title = f"卖出信号 - {stock_name}({stock_code})"
                content = f"股票 {stock_name}({stock_code}) 在 {time_str} 发出卖出信号，价格: {price:.2f}"
            else:
                title = f"信号通知 - {stock_name}({stock_code})"
                content = f"股票 {stock_name}({stock_code}) 在 {time_str} 发出 {signal_type} 信号，价格: {price:.2f}"
        
        # 发送通知
        send_notification(title, content)
        
        # 同时打印到控制台
        print(f"{title}: {content}")
        
    except Exception as e:
        print(f"发送通知失败: {e}")


def create_directory(path):
    """
    创建目录，如果不存在
    
    参数:
    path: 目录路径
    
    返回:
    bool: 是否创建成功
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


def get_current_date_str(format_str='%Y%m%d'):
    """
    获取当前日期字符串
    
    参数:
    format_str: 日期格式
    
    返回:
    str: 日期字符串
    """
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    return now.strftime(format_str)


def get_current_time_str(format_str='%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间字符串
    
    参数:
    format_str: 时间格式
    
    返回:
    str: 时间字符串
    """
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    return now.strftime(format_str)


def calculate_percentage_change(current, previous):
    """
    计算百分比变化
    
    参数:
    current: 当前值
    previous: 之前的值
    
    返回:
    float: 百分比变化
    """
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def calculate_volatility(data, window=20):
    """
    计算波动率
    
    参数:
    data: 价格数据列表或Series
    window: 计算窗口
    
    返回:
    float: 波动率
    """
    import numpy as np
    
    if len(data) < window:
        return 0.0
    
    # 计算对数收益率
    log_returns = np.log(data / data.shift(1))
    
    # 计算滚动标准差作为波动率
    volatility = log_returns.rolling(window=window).std() * np.sqrt(252)  # 年化
    
    return volatility.iloc[-1] if not volatility.empty else 0.0


def is_market_closed():
    """
    检查市场是否已收盘
    
    返回:
    bool: 市场是否已收盘
    """
    # 获取当前北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    
    # 定义收盘时间
    close_time = datetime.strptime('15:00:00', '%H:%M:%S').time()
    
    # 检查是否为周末或已过收盘时间
    if now.weekday() >= 5 or now.time() > close_time:
        return True
    
    return False