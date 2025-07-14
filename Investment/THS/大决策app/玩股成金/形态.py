import requests
import json

def send_morphology_logs_request():
    url = "https://strategy.api.traderwin.com/api/strategy/morphology/logs/list.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "823d0c57978d4207d4053873560779ac",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "Host": "strategy.api.traderwin.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    data = {
        "morphologyId": "1-1",
        "cmd": "9090"
    }

    try:
        response = requests.post(url, json=data, headers=headers, verify=True)
        response.raise_for_status()  # 检查 HTTP 错误状态码

        try:
            return response.json()  # 返回 JSON 格式响应
        except json.JSONDecodeError:
            print("响应内容不是有效的 JSON")
            return response.text

    except requests.exceptions.SSLError as e:
        print(f"SSL 验证失败: {e}")
        print("尝试禁用 SSL 验证（仅限调试环境使用）")
        response = requests.post(url, json=data, headers=headers, verify=False)
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


if __name__ == "__main__":
    result = send_morphology_logs_request()
    print("响应结果：")
    print(json.dumps(result, indent=2, ensure_ascii=False) if isinstance(result, dict) else result)
