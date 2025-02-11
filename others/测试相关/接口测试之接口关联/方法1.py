import requests


def get_token():
    # 发送第一个接口请求# 获取 Cookie 或 Token，假设它在响应的头部
    response1 = requests.post("https://api.example.com/login", json={"username": "test", "password": "test"})
    token = response1.headers.get("Authorization")

    # 后续接口请求添加头部信息
    headers = {"Authorization": token}
    response2 = requests.get("https://api.example.com/protected", headers=headers)
    # 可以进行后续的断言操作
    assert response2.status_code == 200


def cookie_login():
    # 发送登录请求，获取 Cookie 或 Token
    response = requests.post("https://api.example.com/login", data={"username": "test", "password": "test"})
    cookie = response.cookies.get("session")

    # 发送受保护的资源请求，添加 Cookie 或 Token
    response = requests.get("https://api.example.com/protected", cookies={"session": cookie})
    assert response.status_code == 200
    # cookie_login()



if __name__ == "__main__":
    get_token()