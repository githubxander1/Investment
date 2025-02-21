import logging

import requests

logger = logging.getLogger(__name__)

class ChatAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def send_message(self, message):
        url = f'{self.base_url}/chat/messages'
        data = {
            "message": message
        }
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Send chat message request failed: {e}")
            raise

    def send_file(self, file_path):
        url = f'{self.base_url}/chat/files'
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, files=files, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            logger.error(f"Send chat file request failed: {e}")
            raise
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise