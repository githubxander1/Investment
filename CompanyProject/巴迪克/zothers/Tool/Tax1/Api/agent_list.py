from pprint import pprint

import requests

def get_agent_list(page_num=1, page_size=10):
    """
    向指定 URL 发送 POST 请求，获取代理列表数据。

    :param page_num: 页码
    :param page_size: 每页数量
    :return: 返回 list 数据或 None
    """
    url = "http://balitax-test.com/tax-center/agent/agentPage"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "pragma": "no-cache",
        "x-requested-with": "XMLHttpRequest"
    }

    data = {
        "pageSize": page_size,
        "pageNum": page_num
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,  # 自动设置 Content-Type 为 application/json
            cookies=None,  # 使用默认 session cookie 管理
            timeout=10  # 设置超时时间
        )

        response.raise_for_status()  # 如果响应状态码不是 2xx 抛出异常

        # 假设返回的 JSON 结构包含 'data' 字段，其中包含 'list'
        result = response.json()

        if result.get("code") == 200:  # 根据实际接口判断是否成功
            return result.get("data", {}).get("list", [])
        else:
            print("请求失败:", result.get("message"))
            return []

    except requests.exceptions.RequestException as e:
        print("请求异常:", str(e))
        return []

pprint(get_agent_list())