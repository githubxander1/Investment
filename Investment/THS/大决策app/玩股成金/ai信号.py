from pprint import pprint

import requests
import json


def get_ai_signal_rank():
    """获取AI信号排名数据（POST请求）"""
    # 请求URL
    url = "https://ai.api.traderwin.com/api/ai/signal/rank.json"

    # 请求头
    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "94886a78b10e654f41c796fcd7d82db4",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Host": "ai.api.traderwin.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    # 请求体（JSON数据）
    payload = {
        "flag": 1,
        "pageSize": 10,
        "index": "1",
        "cmd": "9021",
        "marketType": ""
    }

    try:
        # 发送POST请求（JSON数据用json参数传递）
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            verify=False
        )
        response.raise_for_status()  # 检查响应状态码
        response_json = response.json()
        pprint(response_json)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求AI信号排名数据失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    ai_rank_data = get_ai_signal_rank()
    if ai_rank_data:
        print("AI信号排名数据:")
        pprint(json.dumps(ai_rank_data, indent=2, ensure_ascii=False))  # 格式化显示内容