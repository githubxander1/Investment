import requests


def test_session_chaining():
    # 发送第一个接口请求
    response1 = requests.post("https://api.example.com/login", json={"username": "test", "password": "test"})
    # 获取 Cookie 或 Token，假设它在响应的头部
    token = response1.headers.get("Authorization")
    # 后续接口请求添加头部信息
    headers = {"Authorization": token}
    response2 = requests.get("https://api.example.com/protected", headers=headers)
    # 可以进行后续的断言操作
    assert response2.status_code == 200


if __name__ == "__main__":
    test_session_chaining()