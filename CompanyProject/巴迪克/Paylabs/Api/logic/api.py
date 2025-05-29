import hashlib
import hmac

import requests
import json

def get_merchant_group_info():
    # 请求地址
    url = "https://sitch-admin.paylabs.co.id/api-platform/merchantInfo/queryAllMerchantGroupInfo.json"

    # 请求头
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="129", "Not=A?Brand";v="8"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "cookie": "JSESSIONID=C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0EB0C0E"
    }

    # 请求体
    data = {
        "randomStr": "-1253921925-553314872-2940910124-262261868121503-15418-156-16536-12313-9239485714597-8039-2436929607-25812-20635-130822381-31733-23510-31156-312-28524-299248042-14100",
        "hmac": "abfceb4605db56b8805701a9851c3c4dec78ac66b19be3d0953939ddb8a92de6"
    }

    # 发起 POST 请求
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=None,  # 可选：传入 session.cookies 或具体 cookie 字典
        verify=True  # 验证 SSL 证书（生产环境建议为 True）
    )

    # 输出响应内容
    print("状态码：", response.status_code)
    print("响应内容：", response.text)

def generate_hmac_sha256_sign(params, secret_key):
    sorted_params = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    sign_str = sorted_params + secret_key
    signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    return signature.upper()

if __name__ == '__main__':
    get_merchant_group_info()
#     session = requests.Session()
#
#     # 先登录获取 Cookie
#     login_data = {"username": "xxx", "password": "xxx"}
#     session.post("https://sitch-admin.paylabs.co.id/login", data=login_data)
#
#     # 再发起目标请求，会自动携带 Cookie
#     response = session.post(url, headers=headers, data=json.dumps(data))
