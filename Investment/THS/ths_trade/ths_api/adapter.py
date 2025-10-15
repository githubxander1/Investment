"""
交易适配器接口
提供统一的交易接口封装
"""

from applications.adapter.ths_trade_adapter import THSTradeAdapter


def create_trade_adapter(exe_path=None, account_name=None):
    """
    创建交易适配器实例
    
    Args:
        exe_path (str, optional): 同花顺交易软件路径
        account_name (str, optional): 账户名称
        
    Returns:
        THSTradeAdapter: 交易适配器实例
    """
    adapter = THSTradeAdapter(exe_path=exe_path, account_name=account_name)
    return adapter


def buy_stock_via_adapter(adapter, stock_code, stock_name, amount, strategy_no="default"):
    """
    通过适配器买入股票
    
    Args:
        adapter (THSTradeAdapter): 交易适配器实例
        stock_code (str): 股票代码
        stock_name (str): 股票名称
        amount (int): 买入数量
        strategy_no (str): 策略编号
        
    Returns:
        dict: 交易结果
    """
    return adapter.buy_stock(stock_code, stock_name, amount, strategy_no)


def sell_stock_via_adapter(adapter, stock_code, stock_name, amount, strategy_no="default"):
    """
    通过适配器卖出股票
    
    Args:
        adapter (THSTradeAdapter): 交易适配器实例
        stock_code (str): 股票代码
        stock_name (str): 股票名称
        amount (int): 卖出数量
        strategy_no (str): 策略编号
        
    Returns:
        dict: 交易结果
    """
    return adapter.sell_stock(stock_code, stock_name, amount, strategy_no)


def get_position_via_adapter(adapter):
    """
    通过适配器获取持仓信息
    
    Args:
        adapter (THSTradeAdapter): 交易适配器实例
        
    Returns:
        pandas.DataFrame: 持仓数据
    """
    return adapter.get_position()


def get_balance_via_adapter(adapter):
    """
    通过适配器获取资金情况
    
    Args:
        adapter (THSTradeAdapter): 交易适配器实例
        
    Returns:
        pandas.DataFrame: 资金数据
    """
    return adapter.get_balance()