# others.测试相关.ApiTest_mindmaster.api_mind.logic.login.py
import json
import os

import jsonpath
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
    response = RequestsHandler().visit(url=url, method=method, headers=headers, json=data)
    if response.status_code == 200:
        try:
            data = response.json()
            token_list = jsonpath.jsonpath(data, '$..token')
            if token_list and len(token_list) > 0:
                token = token_list[0]
                return response, token
            else:
                raise ValueError("Token not found in response")
        except (ValueError, json.JSONDecodeError) as e:
            # 处理 JSON 解析错误
            print(f"Failed to parse JSON: {e}")
            token = None


if __name__ == '__main__':
    email = "2695418206@qq.com"
    pw = "f2d8ddfc169a0ee6f8b0ecd924b1d300"
    # pass
    response, token = login(email, pw)
    print(token)
    # print(login()[1])