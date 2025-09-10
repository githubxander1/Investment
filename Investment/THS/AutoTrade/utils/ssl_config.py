import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# 获取证书文件路径
CERT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                         'reqable-ca.crt')

# 创建全局会话对象
def create_global_session():
    """
    创建一个全局的requests会话，配置自定义CA证书
    """
    session = requests.Session()
    
    # 配置重试策略
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    # 创建适配器
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # 配置证书验证
    if os.path.exists(CERT_PATH):
        session.verify = CERT_PATH
    else:
        # 如果找不到证书文件，使用默认验证
        session.verify = True
        
    return session


# 创建全局会话实例
GLOBAL_SESSION = create_global_session()


def get_global_session():
    """
    获取全局会话实例
    """
    return GLOBAL_SESSION


def patched_request(method, url, **kwargs):
    """
    修补的请求函数，使用全局会话发送请求
    
    Args:
        method: HTTP方法 ('GET', 'POST', 等)
        url: 请求URL
        **kwargs: 其他requests参数
    
    Returns:
        requests.Response对象
    """
    session = get_global_session()
    
    # 确保headers存在
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    
    # 添加默认User-Agent以避免一些常见问题
    if 'User-Agent' not in kwargs['headers']:
        kwargs['headers']['User-Agent'] = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
    response = session.request(method, url, **kwargs)
    return response


def request_with_global_session(method, url, **kwargs):
    """
    使用全局会话发送请求
    
    Args:
        method: HTTP方法 ('GET', 'POST', 等)
        url: 请求URL
        **kwargs: 其他requests参数
    
    Returns:
        requests.Response对象
    """
    return patched_request(method, url, **kwargs)