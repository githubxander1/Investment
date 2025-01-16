import requests


def login():
    url = "https://goapi.edrawsoft.cn/api/user/ws/account/login"
    headers = {
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
    referrer = "https://account.edrawsoft.cn/"
    referrer_policy = "strict-origin-when-cross-origin"
    body = {
        "email":"2695418206@qq.com",
        "pw":"f2d8ddfc169a0ee6f8b0ecd924b1d300",
        "product":"master-coop",
        "captcha_type":1,
        "from":"web",
        "pid":"13267",
        "version":"2.1",
        "device_id":"c61061b7-90a2-49a5-9523-b7403793853b"
    }
    method = "POST"
    mode = "cors"
    credentials = "omit"
    try:
        response = requests.post(url, json=body, headers=headers)

        if response.status_code == 200:
            data = response.json()['testdata']
            refresh_token = data['refresh_token']
            token = data['token']
            # pprint(response.json())
            return data, token
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"请求出错: {e}")


if __name__ == '__main__':
    token = login()
    print(token)
    # print(login())