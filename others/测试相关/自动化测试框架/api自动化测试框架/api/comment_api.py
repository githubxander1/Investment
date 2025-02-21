import logging

import requests

logger = logging.getLogger(__name__)

class CommentAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def post_comment(self, content):
        url = f'{self.base_url}/comments'
        data = {
            "content": content
        }
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Post comment request failed: {e}")
            raise