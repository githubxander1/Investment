"""
自动化交易执行接口
封装Exec_Auto_Trade.py中的功能
"""

from applications.trade.Exec_Auto_Trade import exec_run


def execute_buy_order(stock_code, stock_name, amount, strategy_no="default"):
    """
    执行买入指令
    
    Args:
        stock_code (str): 股票代码
        stock_name (str): 股票名称
        amount (int): 买入数量
        strategy_no (str): 策略编号
        
    Returns:
        dict: 交易结果
    """
    # 构建交易请求
    request_item = {
        "operate": "buy",
        "stock_no": stock_code,
        "stock_name": stock_name,
        "amount": amount,
        "strategy_no": strategy_no,
        "key": f"{stock_code}_{strategy_no}_buy"
    }
    
    # 执行交易
    result = exec_run(request_item)
    return result


def execute_sell_order(stock_code, stock_name, amount, strategy_no="default"):
    """
    执行卖出指令
    
    Args:
        stock_code (str): 股票代码
        stock_name (str): 股票名称
        amount (int): 卖出数量
        strategy_no (str): 策略编号
        
    Returns:
        dict: 交易结果
    """
    # 构建交易请求
    request_item = {
        "operate": "sell",
        "stock_no": stock_code,
        "stock_name": stock_name,
        "amount": amount,
        "strategy_no": strategy_no,
        "key": f"{stock_code}_{strategy_no}_sell"
    }
    
    # 执行交易
    result = exec_run(request_item)
    return result


def execute_trade_operation(operation, stock_code, stock_name, amount, strategy_no="default"):
    """
    执行交易操作
    
    Args:
        operation (str): 操作类型 ('buy' 或 'sell')
        stock_code (str): 股票代码
        stock_name (str): 股票名称
        amount (int): 交易数量
        strategy_no (str): 策略编号
        
    Returns:
        dict: 交易结果
    """
    # 构建交易请求
    request_item = {
        "operate": operation,
        "stock_no": stock_code,
        "stock_name": stock_name,
        "amount": amount,
        "strategy_no": strategy_no,
        "key": f"{stock_code}_{strategy_no}_{operation}"
    }
    
    # 执行交易
    result = exec_run(request_item)
    return result