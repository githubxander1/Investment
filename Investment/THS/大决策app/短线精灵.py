import requests
import json


def get_short_term_elves():
    """获取短线精灵数据（GET请求）"""
    # 请求URL
    url = "https://dfgs.upoem1.com/elves/query"

    # URL参数
    params = {
        "page": "1",
        "size": "10",
        "market": "2"
    }

    # 请求头
    headers = {
        "Host": "dfgs.upoem1.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 UPHybridSDK/3.0 (stock; 1.0.5) SN=ADR_com.sztg.ceniu&VN=25062680_1.0.5_25062680_GA&RV=_&CHID=2000_2000&MN=stock",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://dfgs.upoem1.com/elves/ListforApp",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        # 发送GET请求
        response = requests.get(
            url,
            params=params,
            headers=headers,
            verify=True
        )
        response.raise_for_status()  # 检查响应状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求短线精灵数据失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    elves_data = get_short_term_elves()
    if elves_data:
        print("短线精灵数据:")
        print(json.dumps(elves_data, indent=2, ensure_ascii=False))  # 格式化显示JSON数据