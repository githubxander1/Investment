"""
账户信息接口
包含持仓、资金等账户信息查询
"""

from applications.trade.server.THS_Trader_Server import THSTraderServer
import pandas as pd


def get_position():
    """
    获取持仓信息
    
    Returns:
        pandas.DataFrame: 持仓数据，包含以下字段：
            - 证券代码: 股票代码
            - 证券名称: 股票名称
            - 数量: 持仓数量
            - 可用: 可用数量
            - 成本价: 成本价格
            - 当前价: 当前价格
            - 市值: 市场价值
            - 盈亏: 盈亏金额
    """
    # 初始化交易服务器
    trader = THSTraderServer()
    
    # 获取持仓信息
    position_data = trader.get_position()
    
    return position_data


def get_balance():
    """
    获取资金情况
    
    Returns:
        pandas.DataFrame: 资金数据
    """
    # 初始化交易服务器
    trader = THSTraderServer()
    
    # 获取资金情况
    balance_data = trader.get_balance()
    
    return balance_data


def get_account_info():
    """
    获取账户完整信息（包括持仓和资金）
    
    Returns:
        dict: 账户信息
            - position (pandas.DataFrame): 持仓信息
            - balance (pandas.DataFrame): 资金信息
    """
    # 初始化交易服务器
    trader = THSTraderServer()
    
    # 获取持仓和资金信息
    position_data = trader.get_position()
    balance_data = trader.get_balance()
    
    return {
        "position": position_data,
        "balance": balance_data
    }