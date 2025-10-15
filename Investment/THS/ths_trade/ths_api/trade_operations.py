"""
交易操作接口
包含买入、卖出等交易操作
"""

from applications.trade.server.THS_Trader_Server import THSTraderServer


def buy_stock(stock_code, stock_name, amount, strategy_no="default"):
    """
    买入股票
    
    Args:
        stock_code (str): 股票代码
        stock_name (str): 股票名称
        amount (int): 买入数量
        strategy_no (str): 策略编号，默认为"default"
        
    Returns:
        dict: 交易结果
            - success (bool): 是否成功
            - msg (str): 结果信息
            - entrust_no (str, optional): 委托编号（仅在成功时返回）
    """
    # 创建交易请求项
    request_item = {
        "operate": "buy",
        "stock_no": stock_code,
        "stock_name": stock_name,
        "amount": amount,
        "strategy_no": strategy_no
    }
    
    # 初始化交易服务器
    trader = THSTraderServer()
    
    # 执行买入操作
    result = trader.buy(request_item)
    
    return result


def sell_stock(stock_code, stock_name, amount, strategy_no="default"):
    """
    卖出股票
    
    Args:
        stock_code (str): 股票代码
        stock_name (str): 股票名称
        amount (int): 卖出数量
        strategy_no (str): 策略编号，默认为"default"
        
    Returns:
        dict: 交易结果
            - success (bool): 是否成功
            - msg (str): 结果信息
            - entrust_no (str, optional): 委托编号（仅在成功时返回）
    """
    # 创建交易请求项
    request_item = {
        "operate": "sell",
        "stock_no": stock_code,
        "stock_name": stock_name,
        "amount": amount,
        "strategy_no": strategy_no
    }
    
    # 初始化交易服务器
    trader = THSTraderServer()
    
    # 执行卖出操作
    result = trader.sell(request_item)
    
    return result