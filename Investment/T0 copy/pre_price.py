import akshare as ak
from datetime import datetime, timedelta
import pandas as pd


def get_previous_trading_date(date_obj):
    """
    获取前一个交易日，如果是周末或节假日，自动向前调整
    """
    # 如果是周六(5)或周日(6)，调整到周五
    while date_obj.weekday() >= 5:  # 5=Saturday, 6=Sunday
        date_obj = date_obj - timedelta(days=1)
    return date_obj


def get_previous_close_price(symbol, date_str):
    """
    获取指定日期的前一个交易日收盘价
    """
    # 尝试直接获取指定日期的数据
    try:
        stock_data = ak.stock_zh_a_daily(symbol=symbol, start_date=date_str, end_date=date_str)
        if not stock_data.empty:
            return stock_data['close'].iloc[0]
    except Exception as e:
        print(f"直接获取数据失败: {e}")
    
    # 如果直接获取失败，则尝试获取前几天的数据
    target_date = datetime.strptime(date_str, '%Y%m%d')
    # 调整到最近的交易日
    target_date = get_previous_trading_date(target_date)
    
    # 向前查找最多10个交易日的数据
    start_date = (target_date - timedelta(days=15)).strftime('%Y%m%d')
    
    try:
        stock_data = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, end_date=date_str)
        if not stock_data.empty:
            # 获取最后一个交易日的收盘价
            return stock_data['close'].iloc[-1]
        else:
            return None
    except Exception as e:
        print(f"获取历史数据失败: {e}")
        return None


def main():
    # 获取当前日期的前一天
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y%m%d')
    
    # 股票代码示例（正平股份）
    symbol = "sh603843"
    
    print(f"正在获取{symbol}在{yesterday_str}的收盘价...")
    
    close_price = get_previous_close_price(symbol, yesterday_str)
    
    if close_price is not None:
        print(f"{symbol}的前一个交易日收盘价为：{close_price}")
    else:
        print(f"未能获取到{symbol}的前一个交易日收盘价")


if __name__ == "__main__":
    main()
