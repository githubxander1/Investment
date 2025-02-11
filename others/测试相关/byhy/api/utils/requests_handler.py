import requests


class RequestsHandler:
    def __init__(self):
        self.session = requests.session()
    def requests(self, url,method,params=None,data=None, json=None,headers=None):
        try:
            response = self.session.request(url=url, method=method, params=params, data=data, json=json,
                                            headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求发生错误: {e}")
            return None

    def close_session(self):
        self.session.close()

