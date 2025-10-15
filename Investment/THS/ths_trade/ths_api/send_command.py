"""
策略命令发送接口
封装applications.startegy.Send_Command中的功能
"""

import requests
import json


def send_command_to_queue(post_data):
    """
    发送命令到队列
    
    Args:
        post_data (dict or list): 要发送的数据
        
    Returns:
        dict: 响应结果
        
    Raises:
        Exception: 发送失败时抛出异常
    """
    session = requests.session()
    print("开始发送:", post_data)
    
    try:
        response = session.post("http://127.0.0.1:6003/api/queue", json=post_data)
    except Exception as e:
        raise e
    
    result = json.loads(response.text)
    
    if result["code"] != 200:
        print(result)
        raise Exception(result["msg"])
    else:
        print("成功处理")
        
    return result


def send_single_command(stock_code, stock_name, amount, operation, strategy_no):
    """
    发送单个命令
    
    Args:
        stock_code (str): 股票代码
        stock_name (str): 股票名称
        amount (int): 数量
        operation (str): 操作类型 ('buy' 或 'sell')
        strategy_no (str): 策略编号
        
    Returns:
        dict: 响应结果
    """
    post_data = [{
        "code": stock_code,
        "name": stock_name,
        "ct_amount": amount,
        "operate": operation,
        "strategy_no": strategy_no
    }]
    
    return send_command_to_queue(post_data)