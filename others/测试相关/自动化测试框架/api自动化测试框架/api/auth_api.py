import logging

import requests

logger = logging.getLogger(__name__)

class AuthAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username, password):
        url = f'{self.base_url}/login'
        data = {
            "username": username,
            "password": password
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Login request failed: {e}")
            raise