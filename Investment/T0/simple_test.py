import urllib.request
import json
import gzip
import io
import random
import time

# 反爬措施 - User-Agent池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
]

def get_timestamp():
    return int(time.time() * 1000)

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def test_simple_request():
    # 构造请求URL
    timestamp = get_timestamp()
    secid = "1.600030"
    url = (
        f'http://push2.eastmoney.com/api/qt/stock/details/sse'
        f'?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55'
        f'&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281'
        f'&fltt=2&pos=-0&secid={secid}'
        f'&_={timestamp}'
    )
    
    print(f"请求URL: {url}")
    
    # 创建请求
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }
    
    request = urllib.request.Request(url, headers=headers)
    
    print("发送请求...")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            print(f"收到响应，状态码: {response.getcode()}")
            print(f"响应头信息: {dict(response.headers)}")
            
            print("正在读取内容...")
            content = response.read()
            print(f"响应内容大小: {len(content)} 字节")
            
            # 检查是否是gzip压缩数据
            if content.startswith(b'\x1f\x8b'):
                print("检测到gzip压缩数据，正在解压...")
                buffer = io.BytesIO(content)
                with gzip.GzipFile(fileobj=buffer, mode='rb') as f:
                    content = f.read()
                print(f"gzip解压后内容大小: {len(content)} 字节")
            
            # 显示前1000字节的内容
            print(f"内容前1000字节: {content[:1000]}")
            
            # 尝试解码
            try:
                data_str = content.decode('utf-8')
                print(f"UTF-8解码成功，长度: {len(data_str)}")
                print(f"数据预览: {repr(data_str[:300])}")
                
                # 去除"data:"前缀
                if data_str.startswith('data:'):
                    data_str = data_str[5:]
                    print("已去除'data:'前缀")
                
                # 尝试解析JSON
                try:
                    data_dict = json.loads(data_str)
                    print(f"JSON解析成功: {list(data_dict.keys())}")
                    if 'data' in data_dict:
                        print(f"data字段类型: {type(data_dict['data'])}")
                        if isinstance(data_dict['data'], dict) and 'details' in data_dict['data']:
                            print(f"details字段长度: {len(data_dict['data']['details']) if data_dict['data']['details'] else 0}")
                            print(f"details内容预览: {repr(data_dict['data']['details'][:300] if data_dict['data']['details'] else '')}")
                        elif isinstance(data_dict['data'], str):
                            print(f"data字符串长度: {len(data_dict['data'])}")
                            print(f"data内容预览: {repr(data_dict['data'][:300])}")
                        else:
                            print(f"data内容预览: {repr(str(data_dict['data'])[:300])}")
                except json.JSONDecodeError as e:
                    print(f"JSON解析失败: {e}")
                    
            except UnicodeDecodeError:
                print("UTF-8解码失败，尝试其他编码...")
                
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_request()