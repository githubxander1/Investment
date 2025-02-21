import requests

class UserAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_info(self, user_id):
        url = f'{self.base_url}/users/{user_id}'
        response = requests.get(url)
        return response