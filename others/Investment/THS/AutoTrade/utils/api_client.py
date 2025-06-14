# utils/api_client.py
import requests

# from config.settings import API_URL, HEADERS
from THS.AutoTrade.config.settings import API_URL, Combination_headers


class APIClient:
    def __init__(self):
        self.base_url = API_URL
        self.headers = Combination_headers

    def get(self, endpoint, params=None):
        try:
            response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # logger.error(f"请求失败: {e}")
            return None
