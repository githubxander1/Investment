# z_others.测试相关.ApiTest_mindmaster.api_mind.logic.rename.py
import os

from others.测试相关.api_mind.utils.requests_handler import RequestsHandler
from others.测试相关.api_mind.utils.yaml_handler import read_yaml

# rename_data = read_yaml(r'/z_others/测试相关/api_mind\config\Api.yaml')
test_data_path = os.path.join(os.path.dirname(__file__), "..", "config", "Api.yaml")
rename_data = read_yaml(test_data_path)["rename"]
def rename(body, token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        # "authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJFZHJhd1NvZnQiLCJzdWIiOiJ7XCJjb3JwVXNlcklkXCI6XCJcIixcIm9wZW5JZFwiOlwiXCIsXCJjb3JwSWRcIjpcIlwiLFwidW5pb25fa2V5XCI6XCIyMzkyODUxNi1CS2RVWlwiLFwicGxhdGZvcm1cIjpcIndlYlwifSIsImV4cCI6MTczNjkzNzkyOCwiaWF0IjoxNzM2OTMwNjY4LCJhdWQiOiIyMzkyODUxNiIsInNyYyI6InBhc3N3b3JkIn0.VLHr37Xybcou5LCKHzXY4T9_zLwbWhVtZXBCf8wuOrQ",
        "authorization": f"Bearer {token}",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    # body = {
    #     "name": name,
    #     "file_key": "Kg28ctsy8NEuQWc47AWLIh1ivSjrEEmG",
    #     "folder_id": 0
    # }

    url = rename_data["url"]
    method = rename_data["method"]

    response = RequestsHandler().visit(url=url, method=method, json=body, headers=headers)

    return response

# if __name__ == '__main__':
#     # response = rename('重命名文件2', login()[1])
#     print(response)
