# others.测试相关.ApiTest_mindmaster.api_mind.logic.login.py
import os

import requests

from others.测试相关.api_mind.utils.requests_handler import RequestsHandler
from others.测试相关.api_mind.utils.yaml_handler import read_yaml

# api_data = read_yaml('config/Api.yaml')
# api_data = read_yaml(r'D:\1document\1test\PycharmProject_gitee\others\测试相关\api_mind\config\Api.yaml')["login"]
# pprint(api_data)
test_data_path = os.path.join(os.path.dirname(__file__), "..", "config", "Api.yaml")
api_data = read_yaml(test_data_path)["login"]


def login(email, pw):
    url = api_data["url"]
    method = api_data["method"]
    headers = api_data["headers"]
    # data = api_data["data"]
    data = {"email": email,
           "from": "web",
           "product": "master-online",
           "pw": pw}
    try:
        response = RequestsHandler().visit(url=url, method=method, headers=headers, json=data)

        # pprint(response)

        data = response.json()['data']
        # refresh_token = data['refresh_token']
        token = data['token']
        # pprint(response.json())
        return data, token
    #     else:
    #         print(f"请求失败，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"请求出错: {e}")


if __name__ == '__main__':
    pass
    # data, token = login()
    # print(token)
    # print(login()[1])