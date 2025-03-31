import requests

class BaseAPI:
    def __init__(self, token):
        self.base_url = "https://admin.hv68.cn/prod-api/api"
        self.headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'admin.hv68.cn',
            'Connection': 'keep-alive',
            'Authorization': f'Bearer {token}'
        }

    def send_request(self, method, url, **kwargs):
        full_url = f"{self.base_url}{url}"
        response = requests.request(method, full_url, headers=self.headers, **kwargs)
        return response.json()