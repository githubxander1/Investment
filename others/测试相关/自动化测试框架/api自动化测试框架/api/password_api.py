import logging

import requests

logger = logging.getLogger(__name__)

class PasswordAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def change_password(self, old_password, new_password):
        url = f'{self.base_url}/users/change_password'
        data = {
            "old_password": old_password,
            "new_password": new_password
        }
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Change password request failed: {e}")
            raise