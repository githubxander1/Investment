from pprint import pprint

import requests

# 使用环境变量管理敏感信息
from others.测试相关.api_mind.logic.login import login

TOKEN = login()[1]
print(TOKEN)
def logout():
    # url = "https://userapi.edrawsoft.cn/api/user/23928516/auth/logout?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJFZHJhd1NvZnQiLCJzdWIiOiJ7XCJjb3JwVXNlcklkXCI6XCJcIixcIm9wZW5JZFwiOlwiXCIsXCJjb3JwSWRcIjpcIlwiLFwidW5pb25fa2V5XCI6XCIyMzkyODUxNi1zWEFpTFwiLFwicGxhdGZvcm1cIjpcIndlYlwifSIsImV4cCI6MTczNjkzNTkwNiwiaWF0IjoxNzM2OTI4NjQ2LCJhdWQiOiIyMzkyODUxNiIsInNyYyI6InBhc3N3b3JkIn0.VM9Odco7Ja5CR4tDPC4KsrwZLRyrHGFbZ7LejqsHCro"
    url = "https://userapi.edrawsoft.cn/api/user/23928516/auth/logout"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    params = {
        "token": TOKEN
    }
    referrer = "https://mm.edrawsoft.cn/"
    referrer_policy = "strict-origin-when-cross-origin"
    method = "GET"
    mode = "cors"
    credentials = "omit"


    response = requests.get(url, headers=headers, params=params)


    if response.status_code == 200:
        pprint(response.json())
        return response.json()
    else:
        print(f"请求失败，状态码: {response.status_code}")

if __name__ == '__main__':
    logout()