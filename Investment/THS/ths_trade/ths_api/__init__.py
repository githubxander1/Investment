"""
同花顺交易接口模块
基于ths_trade项目实际接口封装
"""

# 交易操作接口
from .trade_operations import buy_stock, sell_stock

# 账户信息接口
from .account_info import get_position, get_balance, get_account_info

# 交易查询接口
from .trade_queries import get_today_trades, get_today_entrusts, get_trade_history, get_entrust_history

# 适配器接口
from .adapter import create_trade_adapter, buy_stock_via_adapter, sell_stock_via_adapter
from .adapter import get_position_via_adapter, get_balance_via_adapter

# 自动化交易执行接口
from .exec_auto_trade import execute_buy_order, execute_sell_order, execute_trade_operation

# 同花顺交易适配器接口
from .ths_trade_adapter import create_ths_adapter, is_adapter_initialized, get_adapter_account_name

# CSV工具接口
from .csv_helper import get_csv_data, save_csv_data, clear_csv_data, add_csv_data

# 活动工作队列接口
from .active_work import create_active_work, get_next_work_item, update_work_item_status

# 策略命令发送接口
from .send_command import send_command_to_queue, send_single_command

# 错误码定义
from .error_codes import *

__all__ = [
    # 交易操作接口
    'buy_stock', 'sell_stock',
    
    # 账户信息接口
    'get_position', 'get_balance', 'get_account_info',
    
    # 交易查询接口
    'get_today_trades', 'get_today_entrusts', 'get_trade_history', 'get_entrust_history',
    
    # 适配器接口
    'create_trade_adapter', 'buy_stock_via_adapter', 'sell_stock_via_adapter',
    'get_position_via_adapter', 'get_balance_via_adapter',
    
    # 自动化交易执行接口
    'execute_buy_order', 'execute_sell_order', 'execute_trade_operation',
    
    # 同花顺交易适配器接口
    'create_ths_adapter', 'is_adapter_initialized', 'get_adapter_account_name',
    
    # CSV工具接口
    'get_csv_data', 'save_csv_data', 'clear_csv_data', 'add_csv_data',
    
    # 活动工作队列接口
    'create_active_work', 'get_next_work_item', 'update_work_item_status',
    
    # 策略命令发送接口
    'send_command_to_queue', 'send_single_command',
    
    # 错误码
    'SUCCESS', 'TRADE_FAILED', 'INSUFFICIENT_FUNDS', 'INSUFFICIENT_POSITION',
    'INVALID_AMOUNT', 'SYSTEM_ERROR', 'CLIENT_NOT_INITIALIZED', 'NETWORK_ERROR',
    'TIMEOUT_ERROR', 'get_error_message'
]