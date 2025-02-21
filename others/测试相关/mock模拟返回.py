# 示例：使用requests-mock模拟登录接口返回Token
import requests
import requests_mock

def test_login():
    with requests_mock.Mocker() as m:
        # 模拟登录接口返回200和固定Token
        m.post("https://api.auth.com/login", json={"token": "mock_token"}, status_code=200)
        response = requests.post("https://api.auth.com/login", json={"username": "test", "password": "123"})
        assert response.json()["token"] == "mock_token"