import requests

def send_post_request():
    url = "http://ai.api.traderwin.com/api/ai/signal/rank.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "94886a78b10e654f41c796fcd7d82db4",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    data = {
        "flag": 3,
        "pageSize": 3,
        "index": "1",
        "cmd": "9023",
        "marketType": ""
    }

    # 添加 verify=False 参数跳过 SSL 证书验证
    response = requests.post(url, json=data, headers=headers, verify=False)

    return response

# def test_url(url):
#     response = requests.get(url, verify=False)
#     print("Test URL:", url)
#     print("Status Code:", response.status_code)
#     print("Response Text:", response.text[:500])  # 打印前500字符用于分析

if __name__ == '__main__':
    # test_url("https://ai.api.traderwin.com/api/ai/signal/rank.json")

    res = send_post_request()
    print("Status Code:", res.status_code)

    if res.status_code == 200:
        try:
            print(res.json())
        except requests.exceptions.JSONDecodeError:
            print("响应内容不是 JSON 格式")
            print("原始响应内容：", res.text)
    else:
        print(f"请求失败，状态码：{res.status_code}")
        print("响应内容：", res.text)

