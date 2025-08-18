import requests
import os

def qianwen_parse_trade(trade_info):
    prompt = f"""
    我需要在同花顺APP中执行以下交易：{trade_info}。
    请告诉我具体操作步骤（按顺序），例如：
    1. 点击底部"交易"按钮
    2. 点击"买入"按钮
    3. 在股票代码输入框输入{trade_info['code']}
    ...
    只返回步骤，不解释。
    """
    # 调用通义千问API（参考之前的requests调用方式）
    response = call_qianwen(prompt)  # 复用之前的API调用函数
    return response.split("\n")  # 拆分步骤为列表

# 示例：解析交易指令
trade_info = {"code":"600000","price":10.5,"action":"买入","amount":1000}
steps = qianwen_parse_trade(trade_info)  # 得到["1. 点击交易...", "2. 点击买入..."]