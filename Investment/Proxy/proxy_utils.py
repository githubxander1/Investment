import re
import requests
import logging
from py_mini_racer import py_mini_racer

def decode_js_ip(js_code):
    """
    解码JavaScript混淆的IP地址
    
    Args:
        js_code: 包含document.write的JavaScript代码
        
    Returns:
        str: 解码后的IP地址，如果解码失败则返回None
    """
    try:
        # 创建JavaScript运行环境
        ctx = py_mini_racer.MiniRacer()
        
        # 定义document对象，以便JavaScript可以执行
        ctx.eval("""
            var document = {
                written_content: "",
                write: function(content) {
                    this.written_content = content;
                },
                get_content: function() {
                    return this.written_content;
                }
            };
        """)
        
        # 执行JavaScript代码
        ctx.eval(js_code)
        
        # 获取结果
        ip = ctx.eval("document.get_content()")
        return ip
    except Exception as e:
        logging.warning(f"JavaScript IP解码失败: {e}")
        return None

def is_valid_ip(ip):
    """
    检查IP地址是否有效
    
    Args:
        ip: IP地址字符串
        
    Returns:
        bool: 如果IP地址有效返回True，否则返回False
    """
    if not ip:
        return False
        
    # 检查是否是标准IPv4地址格式
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def verify_proxy_curl_style(ip, port, timeout=5):
    """
    使用类似curl的方式验证代理
    
    Args:
        ip: 代理IP地址
        port: 代理端口
        timeout: 超时时间（秒）
        
    Returns:
        bool: 代理是否有效
    """
    try:
        # 使用http://azenv.net/验证代理
        response = requests.get(
            "http://azenv.net/",
            proxies={
                "http": f"http://{ip}:{port}",
                "https": f"http://{ip}:{port}"
            },
            timeout=timeout,
            verify=False
        )
        
        # 检查响应内容中是否包含代理信息
        if response.status_code == 200:
            content = response.text
            # 检查响应中是否包含IP地址，确认代理工作正常
            if ip in content:
                logging.debug(f"✅ 代理可用（CURL方式）：{ip}:{port}")
                return True
            else:
                logging.debug(f"❌ 代理无效（响应异常）：{ip}:{port}，响应内容：{content[:100]}")
                return False
        else:
            logging.debug(f"❌ 代理无效（状态码）：{ip}:{port}，状态码：{response.status_code}")
            return False
    except requests.exceptions.ConnectTimeout:
        logging.debug(f"❌ 代理超时（连接超时）：{ip}:{port}")
        return False
    except requests.exceptions.ProxyError:
        logging.debug(f"❌ 代理错误（无法连接代理）：{ip}:{port}")
        return False
    except Exception as e:
        logging.warning(f"❌ 代理验证异常：{ip}:{port}，异常信息：{str(e)[:100]}")
        return False