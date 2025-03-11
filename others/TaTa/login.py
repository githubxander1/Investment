from pprint import pprint

import requests
import json

# 登录
def login_h5_get_token():
    url = "https://admin.hv68.cn/prod-api/api/wx/code2Token"

    payload = json.dumps({
       "openid": "otm7z6Cz6G70yB6t2EPQAbCc3i8w",
       "platformType": "1",
       "brandType": 3
    })
    headers = {
       'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
       'Content-Type': 'application/json',
       'Accept': '*/*',
       'Host': 'admin.hv68.cn',
       'Connection': 'keep-alive'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

pprint(login_h5_get_token())

customId = login_h5_get_token()["data"]["customId"]
print(customId)
openid = login_h5_get_token()["data"]["openid"]
print(openid)
phoneNumber = login_h5_get_token()["data"]["phoneNumber"]
print(phoneNumber)
token = login_h5_get_token()["data"]["token"]
print(token)