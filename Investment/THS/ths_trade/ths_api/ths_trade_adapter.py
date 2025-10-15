"""
同花顺交易适配器接口
封装applications.adapter.ths_trade_adapter中的功能
"""

from applications.adapter.ths_trade_adapter import THSTradeAdapter


def create_ths_adapter(exe_path=None, account_name=None):
    """
    创建同花顺交易适配器实例
    
    Args:
        exe_path (str, optional): 同花顺交易软件路径
        account_name (str, optional): 账户名称
        
    Returns:
        THSTradeAdapter: 交易适配器实例
    """
    adapter = THSTradeAdapter(exe_path=exe_path, account_name=account_name)
    return adapter


def is_adapter_initialized(adapter):
    """
    检查适配器是否初始化成功
    
    Args:
        adapter (THSTradeAdapter): 交易适配器实例
        
    Returns:
        bool: 是否初始化成功
    """
    return adapter.initialized


def get_adapter_account_name(adapter):
    """
    获取适配器账户名称
    
    Args:
        adapter (THSTradeAdapter): 交易适配器实例
        
    Returns:
        str: 账户名称
    """
    return adapter.account_name