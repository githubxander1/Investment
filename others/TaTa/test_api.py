import pytest
import requests
import json
from pprint import pprint

# 登录函数
def login_h5_get_token():
    url = "https://admin.hv68.cn/prod-api/api/wx/code2Token"

    payload = json.dumps({
        "openid": "otm7z6Cz6G70yB6t2EPQAbCc3i8w",
        "platformType": "1",
        "brandType": 3
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'admin.hv68.cn',
        'Connection': 'keep-alive'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

# 数据驱动测试用例
@pytest.mark.parametrize("api_info", [
    {
        "name": "获取所有会员类型",
        "url": "https://admin.hv68.cn/prod-api/api/vip/getVipList",
        "method": "GET",
        "headers": {},
        "payload": {}
    },
    {
        "name": "获取会员管理详细信息",
        "url": "https://admin.hv68.cn/prod-api/tata/customVip/{id}",
        "method": "GET",
        "headers": {},
        "payload": {"id": 24}  # 假设 id 为 1
    },
    # 补充新的 API 测试用例示例
    {
        "name": "添加新会员",
        "url": "https://admin.hv68.cn/prod-api/api/vip/addVip",
        "method": "POST",
        "headers": {},
        "payload": {
            "name": "John Doe",
            "phone": "1534567890",
            "email": "johndoe@example.com"
        }
    },
    {
        "name": "更新会员信息",
        "url": "https://admin.hv68.cn/prod-api/api/vip/updateVip/{id}",
        "method": "PUT",
        "headers": {},
        "payload": {
            "id": 24,
            "name": "Jane Doe",
            "phone": "0987654321",
            "email": "janedoe@example.com"
        }
    }
])
def test_api_endpoints(api_info):
    # 先进行登录获取 token
    login_response = login_h5_get_token()
    token = login_response.get('data', {}).get('token')

    # 添加 token 到请求头
    api_info["headers"]["Authorization"] = f"Bearer {token}"

    # 处理 URL 中的参数
    url = api_info["url"].format(**api_info["payload"])

    # 发送请求
    response = requests.request(api_info["method"], url, headers=api_info["headers"], data=json.dumps(api_info["payload"]))

    # 打印响应信息
    pprint(response.json())

    # 断言响应状态码
    assert response.status_code == 200

# 运行测试
if __name__ == "__main__":
    pytest.main('vs')