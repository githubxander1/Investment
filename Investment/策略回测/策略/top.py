from pprint import pprint

import requests

# 请求URL
url = "https://prod-lianghuawang-api.yd.com.cn/liangHuaEntrance/l/classicTopNList"

# 请求头
headers = {
    "accept": "application/json",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTY4MjQ1OTIsImlhdCI6MTc1NDE0NjE5Mn0.6MALkNP9CoK70OU3E3udHnR2rkcFF0BEuREPzOZVeiQ",
    "Content-Type": "application/json",
    "Host": "prod-lianghuawang-api.yd.com.cn",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.12.0"
}

# 请求体（空JSON对象）
data = {}

try:
    # 发送POST请求（使用json参数自动处理JSON格式）
    response = requests.post(url, headers=headers, json=data)

    # 打印响应状态码
    print(f"响应状态码: {response.status_code}")

    # 打印响应内容
    if response.headers.get("content-type") == "application/json":
        print("响应内容（JSON）:")
        pprint(response.json())  # 解析JSON响应
    else:
        print("响应内容（文本）:")
        print(response.text)  # 直接打印文本响应

except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")