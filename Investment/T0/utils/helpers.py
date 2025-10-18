# Helper functions for T0 trading system
import os
import sys
from datetime import datetime, timedelta
import pandas as pd

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


def create_directory(directory_path):
    """
    创建目录，如果不存在
    
    参数:
    directory_path: 目录路径
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"创建目录: {directory_path}")
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


def get_current_date_str(format='%Y%m%d'):
    """
    获取当前日期字符串
    
    参数:
    format: 日期格式
    
    返回:
    str: 当前日期字符串
    """
    return datetime.now().strftime(format)


def format_datetime(dt, format='%Y-%m-%d %H:%M:%S'):
    """
    格式化日期时间
    
    参数:
    dt: datetime对象
    format: 日期时间格式
    
    返回:
    str: 格式化后的日期时间字符串
    """
    if isinstance(dt, str):
        dt = pd.to_datetime(dt)
    return dt.strftime(format)


def calculate_time_difference(start_time, end_time):
    """
    计算时间差
    
    参数:
    start_time: 开始时间
    end_time: 结束时间
    
    返回:
    float: 时间差（秒）
    """
    if isinstance(start_time, str):
        start_time = pd.to_datetime(start_time)
    if isinstance(end_time, str):
        end_time = pd.to_datetime(end_time)
    
    return (end_time - start_time).total_seconds()


def is_trading_time():
    """
    判断当前是否为交易时间
    
    返回:
    bool: 是否为交易时间
    """
    now = datetime.now()
    weekday = now.weekday()
    current_time = now.time()
    
    # 检查是否为交易日（周一至周五）
    if weekday < 0 or weekday > 4:
        return False
    
    # 检查是否为交易时间
    morning_start = datetime.strptime('09:30', '%H:%M').time()
    morning_end = datetime.strptime('11:30', '%H:%M').time()
    afternoon_start = datetime.strptime('13:00', '%H:%M').time()
    afternoon_end = datetime.strptime('15:00', '%H:%M').time()
    
    morning_session = morning_start <= current_time <= morning_end
    afternoon_session = afternoon_start <= current_time <= afternoon_end
    
    return morning_session or afternoon_session


def get_trading_dates(start_date, end_date):
    """
    获取两个日期之间的所有交易日
    
    参数:
    start_date: 开始日期，格式'YYYYMMDD'
    end_date: 结束日期，格式'YYYYMMDD'
    
    返回:
    list: 交易日列表，格式'YYYYMMDD'
    """
    try:
        # 转换日期格式
        start = datetime.strptime(start_date, '%Y%m%d')
        end = datetime.strptime(end_date, '%Y%m%d')
        
        # 生成日期范围
        delta = timedelta(days=1)
        trading_dates = []
        
        current_date = start
        while current_date <= end:
            # 检查是否为交易日（周一至周五）
            if 0 <= current_date.weekday() <= 4:
                trading_dates.append(current_date.strftime('%Y%m%d'))
            current_date += delta
        
        return trading_dates
        
    except Exception as e:
        print(f"获取交易日列表失败: {e}")
        return []


def format_price(price, precision=2):
    """
    格式化价格
    
    参数:
    price: 价格
    precision: 小数位数
    
    返回:
    str: 格式化后的价格
    """
    try:
        return f"{float(price):.{precision}f}"
    except Exception:
        return str(price)


def format_volume(volume):
    """
    格式化成交量
    
    参数:
    volume: 成交量
    
    返回:
    str: 格式化后的成交量
    """
    try:
        volume = int(volume)
        if volume >= 100000000:
            return f"{volume/100000000:.2f}亿"
        elif volume >= 10000:
            return f"{volume/10000:.2f}万"
        else:
            return str(volume)
    except Exception:
        return str(volume)


def calculate_profit_loss(buy_price, sell_price, quantity):
    """
    计算盈亏
    
    参数:
    buy_price: 买入价格
    sell_price: 卖出价格
    quantity: 数量
    
    返回:
    tuple: (盈亏金额, 盈亏百分比)
    """
    try:
        profit_loss_amount = (sell_price - buy_price) * quantity
        profit_loss_pct = ((sell_price - buy_price) / buy_price) * 100 if buy_price > 0 else 0
        return profit_loss_amount, profit_loss_pct
    except Exception:
        return 0, 0


def safe_divide(numerator, denominator, default=0):
    """
    安全除法
    
    参数:
    numerator: 分子
    denominator: 分母
    default: 分母为0时的默认值
    
    返回:
    float: 结果
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except Exception:
        return default


def validate_stock_code(stock_code):
    """
    验证股票代码格式
    
    参数:
    stock_code: 股票代码
    
    返回:
    bool: 是否有效
    """
    try:
        # 检查是否为6位数字
        if len(stock_code) != 6:
            return False
        
        # 检查是否全为数字
        if not stock_code.isdigit():
            return False
        
        # 检查是否为有效的股票代码范围
        # 上海A股: 600000-609999
        # 深圳A股: 000001-009999, 300000-309999
        code_num = int(stock_code)
        if (600000 <= code_num <= 609999) or \
           (000001 <= code_num <= 009999) or \
           (300000 <= code_num <= 309999):
            return True
        
        return False
        
    except Exception:
        return False


def get_stock_exchange(stock_code):
    """
    根据股票代码获取交易所
    
    参数:
    stock_code: 股票代码
    
    返回:
    str: 'sh' 或 'sz'
    """
    if stock_code.startswith('6'):
        return 'sh'  # 上海证券交易所
    elif stock_code.startswith(('0', '3')):
        return 'sz'  # 深圳证券交易所
    else:
        return 'unknown'


def pause_execution(seconds=1):
    """
    暂停执行
    
    参数:
    seconds: 暂停时间（秒）
    """
    import time
    time.sleep(seconds)


def retry(func, max_attempts=3, delay=1, *args, **kwargs):
    """
    重试装饰器
    
    参数:
    func: 要执行的函数
    max_attempts: 最大尝试次数
    delay: 重试间隔（秒）
    *args, **kwargs: 传递给函数的参数
    
    返回:
    函数执行结果
    """
    import time
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 0
        while attempts < max_attempts:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                if attempts == max_attempts:
                    raise
                print(f"尝试 {attempts} 失败: {e}, 重试中...")
                time.sleep(delay * (2 ** (attempts - 1)))  # 指数退避
    
    return wrapper


if __name__ == "__main__":
    # 测试辅助函数
    print(f"当前日期: {get_current_date_str()}")
    print(f"是否为交易时间: {is_trading_time()}")
    print(f"格式化价格: {format_price(123.456)}")
    print(f"格式化成交量: {format_volume(1234567)}")
    print(f"验证股票代码: {validate_stock_code('000333')}")
    print(f"获取交易所: {get_stock_exchange('000333')}")