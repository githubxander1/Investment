import requests
import json
import pprint

from Investment.THS.AutoTrade.config.settings import Combination_headers


def fetch_package_feature_info():
    """获取投资组合产品特性信息并解析关键数据"""
    # 目标API地址（包含产品ID和类型参数）
    url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_feature_info"
    params = {
        "product_id": "9800",
        "product_type": "portfolio"
    }

    # 构建请求头（包含浏览器指纹和来源信息）
    headers = Combination_headers

    try:
        # 发送带参数的GET请求（设置10秒超时）
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(response.json())

        # 状态码校验
        if response.status_code == 200:
            # 解析JSON响应
            response_data = response.json()

            # 提取核心数据（根据API返回结构动态调整）
            result = response_data.get("result", {})
            error_code = response_data.get("errorCode", -1)
            error_msg = response_data.get("errorMsg", "请求处理异常")

            # 结构化封装关键信息
            parsed_data = {
                "request_info": {
                    "url": response.url,
                    "method": "GET"
                },
                "error_info": {
                    "code": error_code,
                    "message": error_msg
                },
                "product_basic": {
                    "id": result.get("product_id", ""),
                    "type": result.get("product_type", ""),
                    "name": result.get("product_name", ""),
                    "status": result.get("product_status", 0)
                },
                "feature_info": {
                    "description": result.get("feature_description", ""),
                    "highlight": result.get("feature_highlight", []),
                    "service_content": result.get("service_content", [])
                },
                "price_info": {
                    "original_price": result.get("original_price", 0),
                    "current_price": result.get("current_price", 0),
                    "discount": result.get("discount", 100)
                }
            }

            # 格式化输出（保留4级缩进）
            print("【投资组合产品特性解析】")
            pprint.pprint(parsed_data, indent=4)

        else:
            print(f"请求失败 | 状态码: {response.status_code} | 响应内容: {response.text[:100]}...")

    except requests.RequestException as e:
        print(f"网络请求异常 | 详情: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"JSON解析失败 | 响应内容: {response.text[:200]}... | 详情: {str(e)}")


if __name__ == "__main__":
    fetch_package_feature_info()