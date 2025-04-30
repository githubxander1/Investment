from pprint import pprint

import requests

def send_request():
    url = "http://payok-test.com/payer-api/query/bGYyaXFvcWx5ZHg0TVJvU01TQ1k4Wi9KUkFNUDJqWW0zOW1HU0ZSYlBzMFZ0L3FtU0QxMXdSYTc5VE5GZ2NkbQ=="
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://payok-test.com",
        "Referer": "http://payok-test.com/id-payer/en-pending-v2.html?p=bGYyaXFvcWx5ZHg0TVJvU01TQ1k4Wi9KUkFNUDJqWW0zOW1HU0ZSYlBzMFZ0L3FtU0QxMXdSYTc5VE5GZ2NkbQ==&channel=SHOPEEPAY-APP",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    data = {
        "queryType": "simple",
        "k": "bGYyaXFvcWx5ZHg0TVJvU01TQ1k4Wi9KUkFNUDJqWW0zOW1HU0ZSYlBzMFZ0L3FtU0QxMXdSYTc5VE5GZ2NkbQ==",
        "ramdonKey": "82e61cd0-dcb6-4710-9a0a-ab7c86f89e80",
        "requestSign": "FCC6E172E04C6F053E519B979C2FB7D6"
    }
    try:
        # 发送 POST 请求，verify=False 对应 --insecure 选项
        response = requests.post(url, headers=headers, json=data, verify=False)
        # 检查响应状态码
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
    except ValueError as e:
        print(f"解析响应 JSON 数据时出错: {e}")

# 调用函数
result = send_request()
if result:
    pprint(result)