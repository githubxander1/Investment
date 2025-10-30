"""
增强版请求模块，整合所有反爬策略
"""

import time
import random
import requests
from typing import Dict, Any, Optional
from Investment.THS.AutoTrade.utils.ssl_config import request_with_global_session
from Investment.THS.AutoTrade.utils.anti_crawler import anti_crawler

def make_enhanced_request(method: str, 
                         url: str, 
                         headers: Optional[Dict[str, str]] = None,
                         use_global_session: bool = True,
                         add_random_delay: bool = True,
                         min_delay: float = 0.5,
                         max_delay: float = 3.0,
                         **kwargs) -> requests.Response:
    """
    发送增强版HTTP请求，包含多种反爬策略
    
    Args:
        method: HTTP方法 ('GET', 'POST', 等)
        url: 请求URL
        headers: 请求头
        use_global_session: 是否使用全局会话
        add_random_delay: 是否添加随机延迟
        min_delay: 最小延迟时间（秒）
        max_delay: 最大延迟时间（秒）
        **kwargs: 其他requests参数
        
    Returns:
        requests.Response对象
    """
    # 添加随机延迟
    if add_random_delay:
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    # 使用反爬策略
    if use_global_session:
        # 使用全局会话（包含SSL配置和重试机制）
        if headers is None:
            headers = anti_crawler.get_random_headers()
        elif 'User-Agent' not in headers:
            headers['User-Agent'] = anti_crawler.ua.random
            
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
            
        return request_with_global_session(method, url, headers=headers, **kwargs)
    else:
        # 使用anti_crawler模块的请求方法
        return anti_crawler.make_request(method, url, headers=headers, **kwargs)

def get(url: str, **kwargs) -> requests.Response:
    """发送GET请求"""
    return make_enhanced_request('GET', url, **kwargs)

def post(url: str, **kwargs) -> requests.Response:
    """发送POST请求"""
    return make_enhanced_request('POST', url, **kwargs)