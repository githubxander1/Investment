import requests

# 请求URL
url = "https://prod-lhw-strategy-data-center.ydtg.com.cn/lhwDataCenter/getQSChangeByIdAndDateNew"

# 请求参数
params = {
    "poolId": "8001",
    "startDate": "2024-08-08",
    "endDate": "2025-08-03",
    "by": "date",
    "ascOrDesc": "DESC",
    "startIndex": "0",
    "pageSize": "11"
}

# 请求头
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTY4MjA1NzgsImlhdCI6MTc1NDE0MjE3OH0.yKBdHg0gGPzkbEbX2_stiSXAY5uQxgQueL4rI7IlnOU",
    "Host": "prod-lhw-strategy-data-center.ydtg.com.cn",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.12.0",
    "If-Modified-Since": "Sun, 03 Aug 2025 13:45:54 GMT"
}

try:
    # 发送GET请求
    response = requests.get(url, params=params, headers=headers)
    
    # 打印响应状态码
    print(f"响应状态码: {response.status_code}")
    
    # 打印响应内容（如果是JSON格式）
    if response.headers.get("content-type") == "application/json":
        print("响应内容:")
        print(response.json())
    else:
        print("响应内容:")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")