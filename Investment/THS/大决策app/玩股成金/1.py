import requests
import json
import certifi
import os

url = 'https://ai.api.traderwin.com/api/ai/robot/list.json'

headers = {
    'Content-Type': 'application/json',
    'from': 'Android',
    'token': '4d7d47d22810ab282cb38d2a28f2b8cd',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)',
    'Host': 'ai.api.traderwin.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
}

data = {
    'industryId': 'CN',
    'cmd': '9012',
    'userId': '0',
    'version': '2',
    'marketType': 'CN'
}

try:
    # 尝试使用certifi证书
    response = requests.post(url, headers=headers, json=data, verify=certifi.where())
    response.raise_for_status()

except requests.exceptions.SSLError as e:
    print(f"SSL验证错误: {e}")
    print("尝试禁用SSL验证（不推荐在生产环境使用）")

    # 禁用SSL验证
    response = requests.post(url, headers=headers, json=data, verify=False)
    print("警告: 已禁用SSL验证，此连接不安全")

except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")

else:
    try:
        json_response = response.json()
        print("JSON响应:")
        print(json.dumps(json_response, indent=2))
    except json.JSONDecodeError:
        print("非JSON响应:")
        print(response.text)