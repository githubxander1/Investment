from pprint import pprint

from others.测试相关.api_mind.utils.requests_handler import RequestsHandler
# 使用环境变量管理敏感信息
from others.测试相关.api_mind.utils.yaml_handler import read_yaml

# TOKEN = login()[1]
# print(TOKEN)
logout_data = read_yaml(r"/z_others/测试相关/api_mind\config\Api.yaml")["logout"]
def logout(token):
    # headers = {
    #     "accept": "application/json, text/plain, */*",
    #     "accept-language": "zh-CN,zh;q=0.9",
    #     "cache-control": "no-cache",
    #     "pragma": "no-cache",
    #     "sec-ch-ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"",
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": "\"Windows\"",
    #     "sec-fetch-dest": "empty",
    #     "sec-fetch-mode": "cors",
    #     "sec-fetch-site": "same-site"
    # }
    params = {
        "token": token
    }
    url = logout_data["url"]
    method = logout_data["method"]
    headers = logout_data["headers"]

    response = RequestsHandler().visit(url=url, method=method,headers=headers, params=params)


    # if response.status_code == 200:
    pprint(response)
    #     return response.json()
    # else:
    #     print(f"请求失败，状态码: {response.status_code}")

# if __name__ == '__main__':
#     logout(TOKEN)