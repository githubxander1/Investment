import requests
import json


def get_strategy_profit_analyse():
    """获取策略收益分析数据（对应strategyId=156275的全周期分析）"""
    # 请求URL
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/profit_analyse"

    # URL参数
    params = {
        "strategyId": "156275",  # 策略ID，指定目标策略
        "period": "all"  # 时间周期，all表示全周期
    }

    # 请求头
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "priority": "u=1, i",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "referrer": "https://bowerbird.10jqka.com.cn/",
        "referrerPolicy": "strict-origin-when-cross-origin"
    }

    try:
        # 发送GET请求，credentials: omit 对应不携带Cookie
        response = requests.get(
            url,
            params=params,
            headers=headers,
            cookies=None,  # 不发送Cookie
            verify=True
        )
        response.raise_for_status()  # 检查响应状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求策略收益分析数据失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    profit_data = get_strategy_profit_analyse()
    if profit_data:
        print("策略收益分析数据:")
        print(json.dumps(profit_data, indent=2, ensure_ascii=False))  # 格式化显示内容