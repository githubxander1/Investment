import requests
import json


def get_portfolio_income_info():
    """获取组合收益信息（指定组合ID及时间范围）"""
    # 请求URL
    url = "https://t.10jqka.com.cn/portfolio/base/getPortfolioIncomeInfo"

    # URL参数
    params = {
        "id": "20811",  # 组合ID
        "startDate": "2024-08-12",  # 开始日期
        "endDate": "2025-08-12"  # 结束日期
    }

    # 请求头
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referrer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=20811",
        "referrerPolicy": "strict-origin-when-cross-origin"
    }

    try:
        # 发送GET请求，credentials: include 表示携带Cookie
        response = requests.get(
            url,
            params=params,
            headers=headers,
            cookies=None,  # 若需携带本地Cookie，可改为requests.utils.dict_from_cookiejar(session.cookies)
            verify=True,
            allow_redirects=True
        )
        response.raise_for_status()  # 检查响应状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求组合收益信息失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    income_data = get_portfolio_income_info()
    if income_data:
        print("组合收益信息:")
        print(json.dumps(income_data, indent=2, ensure_ascii=False))  # 格式化显示内容