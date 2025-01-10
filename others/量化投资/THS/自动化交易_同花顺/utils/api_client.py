# utils/api_client.py
import requests

from others.量化投资.THS.自动化交易_同花顺.config.settings import API_URL, HEADERS


class APIClient:
    def __init__(self):
        self.base_url = API_URL
        self.headers = HEADERS

    def get(self, endpoint, params=None):
        try:
            response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # logger.error(f"请求失败: {e}")
            return None
