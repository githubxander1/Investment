from datetime import datetime
import time
import sys

# 添加项目根目录到路径，以便导入notification模块
sys.path.append('d:\\Xander\\Inverstment')
# from Investment.THS.AutoTrade_copy.utils.notification import send_notification


def is_trading_time():
    """检查当前是否为交易日的交易时间（9:30-11:30 和 13:00-15:00）"""
    now = datetime.now()
    
    # 检查是否为周末（周六、周日不交易）
    if now.weekday() >= 5:
        print(f"当前为非交易日（{now.strftime('%Y-%m-%d %H:%M:%S')}）")
        return False
    
    # 检查是否在交易时间内
    hour = now.hour
    minute = now.minute
    
    # 上午交易时间：9:30-11:30
    morning_trading = (hour == 9 and minute >= 30) or (10 <= hour < 11) or (hour == 11 and minute < 30)
    # 下午交易时间：13:00-15:00
    afternoon_trading = 13 <= hour < 15
    
    is_trading = morning_trading or afternoon_trading
    if not is_trading:
        print(f"当前不在交易时间内（{now.strftime('%Y-%m-%d %H:%M:%S')}）")
    
    return is_trading


def notify_signal(signal_type, stock_code, price, time_str):
    """当出现买卖信号时进行通知提醒"""
    if signal_type == 'buy':
        message = f"【买入信号】股票: {stock_code}, 价格: {price:.2f}, 时间: {time_str}"
        title = "买入信号提醒"
    elif signal_type == 'sell':
        message = f"【卖出信号】股票: {stock_code}, 价格: {price:.2f}, 时间: {time_str}"
        title = "卖出信号提醒"
    else:
        message = f"【未知信号】股票: {stock_code}, 价格: {price:.2f}, 时间: {time_str}"
        title = "交易信号提醒"
    
    try:
        # 调用通知函数发送通知
        send_notification(title, message)
        print(f"通知发送成功: {message}")
    except Exception as e:
        print(f"通知发送失败: {e}")


def wait_until_trading_time():
    """等待直到交易时间开始"""
    while True:
        now = datetime.now()
        if now.weekday() >= 5:
            # 周末，等待到周一早上
            wait_time = (7 - now.weekday()) * 24 * 3600 - now.hour * 3600 - now.minute * 60 - now.second
            print(f"当前是周末，等待 {wait_time//3600} 小时 {wait_time%3600//60} 分钟后重试")
            time.sleep(60)
        else:
            # 工作日
            hour = now.hour
            minute = now.minute
            
            # 检查是否在交易时间前
            if hour < 9 or (hour == 9 and minute < 30):
                # 上午交易时间前，等待到9:30
                wait_minutes = (9 - hour) * 60 + (30 - minute)
                print(f"等待到上午交易时间开始，还需 {wait_minutes} 分钟")
                time.sleep(60)
            elif hour == 11 and minute >= 30 and hour < 13:
                # 午休时间，等待到13:00
                wait_minutes = (13 - hour) * 60 - minute
                print(f"午休时间，等待到下午交易时间开始，还需 {wait_minutes} 分钟")
                time.sleep(60)
            elif hour >= 15:
                # 交易时间已结束，等待到下一个交易日
                next_day = now + timedelta(days=1)
                while next_day.weekday() >= 5:
                    next_day += timedelta(days=1)
                wait_time = ((next_day - now).days * 24 * 3600 + 
                             (9 - now.hour) * 3600 + 
                             (30 - now.minute) * 60 - 
                             now.second)
                print(f"今日交易时间已结束，等待到 {next_day.strftime('%Y-%m-%d')} 9:30开始")
                time.sleep(60)
            else:
                # 在交易时间内
                break

# 添加缺失的导入
try:
    from datetime import timedelta
except ImportError:
    pass