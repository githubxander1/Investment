# utils/api_client.py
import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
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

    def login(self, email, password):
        url = f"{self.base_url}/api/user/ws/account/login"
        body = {
            "email": email,
            "pw": password,
            "product": "master-coop",
            "captcha_type": 1,
            "from": "web",
            "pid": "13267",
            "version": "2.1",
            "device_id": "c61061b7-90a2-49a5-9523-b7403793853b"
        }
        response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def rename(self, token, name, file_key, folder_id):
        url = f"{self.base_url}/api/mm_web/file"
        self.headers["authorization"] = f"Bearer {token}"
        body = {
            "name": name,
            "file_key": file_key,
            "folder_id": folder_id
        }
        response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def logout(self, token):
        url = f"{self.base_url}/api/user/23928516/auth/logout"
        params = {"token": token}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
