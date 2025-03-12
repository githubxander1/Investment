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
        "Referer": "http://payok-test.com/id-payer/en-success-v2.html?p=bGYyaXFvcWx5ZHg0TVJvU01TQ1k4Wi9KUkFNUDJqWW0zOW1HU0ZSYlBzMFZ0L3FtU0QxMXdSYTc5VE5GZ2NkbQ==&channel=SHOPEEPAY-APP",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    data = {
        "queryType": "simple",
        "k": "bGYyaXFvcWx5ZHg0TVJvU01TQ1k4Wi9KUkFNUDJqWW0zOW1HU0ZSYlBzMFZ0L3FtU0QxMXdSYTc5VE5GZ2NkbQ==",
        "ramdonKey": "0e4e5803-32ab-4702-ad06-6eb2431744a4",
        "requestSign": "94145381A9CCA65EE266042AB1A8BCA6"
    }
    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
    except ValueError as e:
        print(f"解析响应数据时发生错误: {e}")
    return None

# 调用方法
result = send_request()
if result:
    pprint(result)