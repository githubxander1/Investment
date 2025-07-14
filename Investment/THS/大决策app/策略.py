import requests
import json


def get_portfolio_industry_theme():
    """获取组合行业主题数据（GET请求）"""
    # 请求URL
    url = "https://nkmapiv3.aniu.tv/nkm-api/Rest2/api/INKBPortfolio/getPortfolioIndustryThemeV2"

    # URL参数
    params = {
        "aniu_uid": "3a51f1c06372435cbb79e41609285c1a",
        "get_type": "0",
        "pfId": "132008",
        "pfid": "132008",
        "user_level": "1",
        "channelid": "700015",
        "clienttype": "3",
        "clientid": "first_install_android_id",
        "devid": "800009",
        "time": "20250714130243",
        "version": "6.9.63",
        "platform": "app_anzt_anzt",
        "platForm": "app_anzt_anzt",
        "sign": "d27c8505dccf72ab39afe62effadefd3"
    }

    # 请求头
    headers = {
        "Host": "nkmapiv3.aniu.tv",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.2.0"
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
        print(f"请求组合行业主题数据失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    industry_theme_data = get_portfolio_industry_theme()
    if industry_theme_data:
        print("组合行业主题数据:")
        print(json.dumps(industry_theme_data, indent=2, ensure_ascii=False))  # 格式化显示内容