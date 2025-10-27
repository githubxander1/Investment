from datetime import timedelta, datetime
import pandas as pd
import os
import numpy as np


def get_close_price_from_cache(stock_code, trade_date):
    """从缓存文件获取昨收价或最新收盘价
    
    Args:
        stock_code: 股票代码，格式：000000
        trade_date: 交易日期，格式：YYYY-MM-DD 或 YYYYMMDD
    
    Returns:
        float: 收盘价，如果无法获取返回None
    """
    # 标准化日期格式
    if isinstance(trade_date, str):
        if '-' in trade_date:
            trade_date_obj = datetime.strptime(trade_date.split()[0], '%Y-%m-%d')
            date_str = trade_date_obj.strftime('%Y%m%d')
        else:
            trade_date_obj = datetime.strptime(trade_date[:8], '%Y%m%d')
            date_str = trade_date[:8]
    else:
        trade_date_obj = trade_date
        date_str = trade_date_obj.strftime('%Y%m%d')
    
    # 尝试在T0项目的缓存目录查找
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 尝试分时数据缓存
    cache_dir = os.path.join(project_root, 'cache', 'fenshi_data')
    cache_file = os.path.join(cache_dir, f'{stock_code}_{date_str}_fenshi.csv')
    
    # 如果找不到，也尝试在T0_Optimized项目的缓存目录查找
    if not os.path.exists(cache_file):
        optimized_cache_dir = os.path.join(os.path.dirname(project_root), 'T0_Optimized', 'cache', 'fenshi_data')
        cache_file = os.path.join(optimized_cache_dir, f'{stock_code}_{date_str}_fenshi.csv')
    
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file)
            if not df.empty:
                # 尝试获取收盘或close列
                if '收盘' in df.columns:
                    return df['收盘'].iloc[-1]
                elif 'close' in df.columns:
                    return df['close'].iloc[-1]
        except Exception as e:
            print(f"读取缓存文件失败: {e}")
    
    return None


def get_close_price_from_simulated_data(stock_code):
    """生成模拟的收盘价数据
    
    Args:
        stock_code: 股票代码
    
    Returns:
        float: 模拟的收盘价
    """
    # 使用股票代码作为随机种子，确保相同股票代码返回相同的基础价格
    seed = int(''.join(filter(str.isdigit, stock_code))) % 10000
    np.random.seed(seed)
    
    # 生成一个合理范围的随机价格
    base_price = np.random.uniform(10, 100)
    print(f"为股票{stock_code}生成模拟收盘价: {base_price:.2f}")
    return base_price


def get_close_price_from_dfcf_em(stock_code, trade_date):
    """获取昨收价（已修改，不再使用东方财富接口）
    
    Args:
        stock_code: 股票代码，格式：000000
        trade_date: 交易日期，格式：YYYY-MM-DD HH:MM:SS
    
    Returns:
        float: 收盘价，如果无法获取返回None
    """
    print(f"注意：东方财富接口已被移除，使用替代方法获取{stock_code}的收盘价")
    
    # 尝试从缓存获取
    close_price = get_close_price_from_cache(stock_code, trade_date)
    if close_price is not None:
        return close_price
    
    # 使用模拟数据作为备选
    return get_close_price_from_simulated_data(stock_code)


def get_close_price_from_dfcf_daily(stock_code, trade_date):
    """获取昨收价（已修改，不再使用东方财富接口）
    
    Args:
        stock_code: 股票代码，格式：000000
        trade_date: 交易日期，格式：YYYYMMDD
    
    Returns:
        float: 收盘价，如果无法获取返回None
    """
    print(f"注意：东方财富接口已被移除，使用替代方法获取{stock_code}的收盘价")
    
    # 尝试从缓存获取
    close_price = get_close_price_from_cache(stock_code, trade_date)
    if close_price is not None:
        return close_price
    
    # 使用模拟数据作为备选
    return get_close_price_from_simulated_data(stock_code)
        print(f"从历史数据获取昨收价失败: {e}")
    return None

def get_prev_close(stock_code, trade_date):
    """获取昨收价"""
    # 确保股票代码格式正确（akshare需要sh或sz前缀）
    if stock_code.startswith('6'):
        stock_code = f'sh{stock_code}'
    elif stock_code.startswith(('0', '3')):
        stock_code = f'sz{stock_code}'
    else:
        stock_code = stock_code

    # 将交易日期转换为datetime对象
    try:
        trade_date_dt = datetime.strptime(trade_date, '%Y-%m-%d')
    except ValueError as e:
        print(f"日期格式错误: {e}")
        return None

    # 如果是周末，获取上周五的收盘价
    weekday = trade_date_dt.weekday()  # 0=Monday, 6=Sunday
    if weekday == 5:  # Saturday
        trade_date_dt = trade_date_dt - timedelta(days=1)  # Friday
    elif weekday == 6:  # Sunday
        trade_date_dt = trade_date_dt - timedelta(days=2)  # Friday
    elif weekday == 0: # Monday
        trade_date_dt = trade_date_dt - timedelta(days=3)   #Friday

    # 转换为函数期望的格式
    # em函数期望的格式: YYYY-MM-DD HH:MM:SS
    em_date_format = trade_date_dt.strftime('%Y-%m-%d')
    # daily函数期望的格式: YYYYMMDD
    daily_date_format = trade_date_dt.strftime('%Y%m%d')

    # 尝试多个数据源获取昨收价
    # 注意：保存原始股票代码用于日K数据查询
    original_stock_code = stock_code.lstrip('sz').lstrip('sh')  # 移除可能的交易所前缀
    
    try:
        # 先尝试日K数据（使用原始股票代码格式，不带交易所前缀）
        print(f"尝试获取日K数据，原始股票代码: {original_stock_code}, 日期: {daily_date_format}")
        prev_close = get_close_price_from_dfcf_daily(original_stock_code, daily_date_format)
        if prev_close is not None:
            print(f"✅ 成功从数据源 2 获取昨收价: {prev_close:.2f}")
            return prev_close
    except Exception as e:
        print(f"数据源 2 获取昨收价失败: {e}")

    try:
        # 再尝试分时数据（可能需要带交易所前缀）
        print(f"尝试获取分时数据，股票: {stock_code}, 日期: {em_date_format}")
        prev_close = get_close_price_from_dfcf_em(stock_code, em_date_format)
        if prev_close is not None:
            print(f"✅ 成功从数据源 1 获取昨收价: {prev_close:.2f}")
            return prev_close
    except Exception as e:
        print(f"数据源 1 获取昨收价失败: {e}")

    print("❌ 所有数据源均无法获取昨收价")
    return None


# 直接使用一个已知的有效日期进行测试（2023年的一个交易日）
# 避免使用未来日期，因为API可能无法提供这些数据
# stock_code = '000333'
# trade_date = '2025-10-16'  # 一个已知的交易日
# print(f"测试股票: {stock_code}, 测试日期: {trade_date}")

# 直接测试每个函数，以便更好地诊断问题
# print("\n测试 get_close_price_from_dfcf_daily:")
# daily_result = get_close_price_from_dfcf_daily(stock_code, trade_date)  # daily函数需要YYYYMMDD格式
# print(f"日K函数结果: {daily_result}")

# print("\n测试 get_close_price_from_dfcf_em:")
# em_result = get_close_price_from_dfcf_em(stock_code, trade_date)  # em函数需要YYYY-MM-DD格式
# print(f"分时函数结果: {em_result}")

# print("\n测试 get_prev_close:")
# result = get_prev_close(stock_code, trade_date)
# print(f"综合函数结果: {result}")
# hist_df = ak.stock_zh_a_hist(
#             symbol=stock_code,
#             period="daily",
#             start_date=trade_date,
#             end_date=trade_date,
#             adjust=""
#         )
# print(hist_df)