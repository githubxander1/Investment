"""
反爬虫策略模块

该模块提供了一系列反爬虫策略，包括:
1. 随机User-Agent
2. 请求延迟
3. 重试机制
4. 会话保持
5. 代理支持
6. 请求头伪装
"""

import time
import random
from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import fake_useragent

class AntiCrawler:
    def __init__(self):
        self.session = requests.Session()
        self._setup_session()
        self.ua = fake_useragent.UserAgent()
        
    def _setup_session(self):
        """配置会话参数"""
        # 设置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
    def get_random_headers(self) -> Dict[str, str]:
        """获取随机请求头"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers
        
    def random_delay(self, min_delay: float = 1, max_delay: float = 3):
        """添加随机延迟"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def exponential_backoff(self, attempt: int, base_delay: float = 1):
        """指数退避延迟"""
        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
        time.sleep(delay)
        
    def make_request(self, 
                     method: str, 
                     url: str, 
                     headers: Optional[Dict[str, str]] = None,
                     **kwargs) -> requests.Response:
        """
        发送HTTP请求，包含反爬策略
        
        Args:
            method: HTTP方法
            url: 请求URL
            headers: 请求头
            **kwargs: 其他请求参数
            
        Returns:
            requests.Response对象
        """
        # 如果没有提供headers，则使用随机headers
        if headers is None:
            headers = self.get_random_headers()
        elif 'User-Agent' not in headers:
            headers['User-Agent'] = self.ua.random
            
        # 添加随机延迟
        self.random_delay(0.5, 2)
        
        # 设置默认超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
            
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise e
                # 指数退避
                self.exponential_backoff(attempt)
                
    def get(self, url: str, **kwargs) -> requests.Response:
        """发送GET请求"""
        return self.make_request('GET', url, **kwargs)
        
    def post(self, url: str, **kwargs) -> requests.Response:
        """发送POST请求"""
        return self.make_request('POST', url, **kwargs)

# 创建全局实例
anti_crawler = AntiCrawler()