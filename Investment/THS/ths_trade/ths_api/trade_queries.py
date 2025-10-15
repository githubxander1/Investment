"""
交易查询接口
包含当日成交、当日委托等查询操作
"""

from applications.trade.server.THS_Trader_Server import THSTraderServer
import pandas as pd


def get_today_trades():
    """
    获取当日成交记录
    
    Returns:
        pandas.DataFrame: 当日成交数据
    """
    # 初始化交易服务器
    trader = THSTraderServer()
    
    # 获取当日成交
    trades_data = trader.get_today_trades()
    
    return trades_data


def get_today_entrusts():
    """
    获取当日委托记录
    
    Returns:
        pandas.DataFrame: 当日委托数据
    """
    # 初始化交易服务器
    trader = THSTraderServer()
    
    # 获取当日委托
    entrusts_data = trader.get_today_entrusts()
    
    return entrusts_data


def get_trade_history(start_date=None, end_date=None):
    """
    获取历史交易记录（该接口基于当日成交实现，如需历史数据需扩展）
    
    Args:
        start_date (str, optional): 开始日期，格式'YYYY-MM-DD'
        end_date (str, optional): 结束日期，格式'YYYY-MM-DD'
        
    Returns:
        pandas.DataFrame: 历史交易数据
    """
    # 当前仅实现获取当日成交
    return get_today_trades()


def get_entrust_history(start_date=None, end_date=None):
    """
    获取历史委托记录（该接口基于当日委托实现，如需历史数据需扩展）
    
    Args:
        start_date (str, optional): 开始日期，格式'YYYY-MM-DD'
        end_date (str, optional): 结束日期，格式'YYYY-MM-DD'
        
    Returns:
        pandas.DataFrame: 历史委托数据
    """
    # 当前仅实现获取当日委托
    return get_today_entrusts()