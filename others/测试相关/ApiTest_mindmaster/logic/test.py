import os

import requests

# 使用环境变量管理敏感信息
EMAIL = os.getenv('LOGIN_EMAIL')
PASSWORD = os.getenv('LOGIN_PASSWORD')

# 提取硬编码的 URL 和其他参数
BASE_URL = "https://goapi.edrawsoft.cn/api/user/ws/account/login"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
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
BODY = {
    "email": EMAIL,
    "pw": PASSWORD,
    "product": "master-coop",
    "captcha_type": 1,
    "from": "web",
    "pid": "13267",
    "version": "2.1",
    "device_id": "c61061b7-90a2-49a5-9523-b7403793853b"
}


def login():
    try:
        response = requests.post(BASE_URL, json=BODY, headers=HEADERS)
        response.raise_for_status()  # 检查请求是否成功

        data = response.json()
        if 'testdata' not in data or 'refresh_token' not in data['testdata'] or 'token' not in data['testdata']:
            raise ValueError("API 返回的数据结构不符合预期")

        refresh_token = data['testdata']['refresh_token']
        token = data['testdata']['token']

        return data, refresh_token, token

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None, None, None
    except ValueError as e:
        print(f"数据解析失败: {e}")
        return None, None, None


if __name__ == '__main__':
    result = login()
    if result[0] is not None:
        print(result)
    else:
        print("登录失败")
