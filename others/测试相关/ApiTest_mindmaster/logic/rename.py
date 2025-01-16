import requests

from others.测试相关.api_mind.logic.login import login

token = login()[1]
def rename(name):
    url = "https://mindapi.edrawsoft.cn/api/mm_web/file"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        # "authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJFZHJhd1NvZnQiLCJzdWIiOiJ7XCJjb3JwVXNlcklkXCI6XCJcIixcIm9wZW5JZFwiOlwiXCIsXCJjb3JwSWRcIjpcIlwiLFwidW5pb25fa2V5XCI6XCIyMzkyODUxNi1CS2RVWlwiLFwicGxhdGZvcm1cIjpcIndlYlwifSIsImV4cCI6MTczNjkzNzkyOCwiaWF0IjoxNzM2OTMwNjY4LCJhdWQiOiIyMzkyODUxNiIsInNyYyI6InBhc3N3b3JkIn0.VLHr37Xybcou5LCKHzXY4T9_zLwbWhVtZXBCf8wuOrQ",
        "authorization": f"Bearer {token}",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    referrer = "https://mm.edrawsoft.cn/"
    referrer_policy = "strict-origin-when-cross-origin"
    body = {
        "name": name,
        "file_key":"Kg28ctsy8NEuQWc47AWLIh1ivSjrEEmG",
        "folder_id":0
    }
    method = "POST"
    mode = "cors"
    credentials = "include"


    response = requests.post(url, json=body, headers=headers)


    if response.status_code == 200:
        print(response.json())
    else:
        print(f"请求失败，状态码: {response.status_code}")

if __name__ == '__main__':
    rename('重命名文件1')