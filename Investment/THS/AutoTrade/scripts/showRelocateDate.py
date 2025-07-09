import requests
import pandas as pd
from datetime import datetime

from Investment.THS.AutoTrade.config.settings import Combination_headers


def fetch_and_parse_data():
    """发送GET请求到指定URL并解析返回的JSON数据"""
    # 目标URL
    url = "https://t.10jqka.com.cn/portfolio/base/showRelocateData?portfolioId=9800"

    # 请求头信息
    headers = Combination_headers

    try:
        # 发送GET请求
        response = requests.get(url, headers=headers, timeout=10)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析JSON数据
            data = response.json()

            # 提取重要数据
            result = data.get("result", {})
            error_code = data.get("errorCode", -1)
            error_msg = data.get("errorMsg", "未知错误")

            # 构建结果字典
            result_data = {
                "error_info": {
                    "error_code": error_code,
                    "error_msg": error_msg
                },
                "holding_count": result.get("holdingCount", 0),
                "holding_info": result.get("holdingInfo", {}),
                "relocate_info": result.get("relocateInfo", {})
            }

            return result_data

        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(response.text)
            return None

    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        print(response.text)
        return None


def extract_and_display_data(result_data):
    """提取重要数据并展示"""
    if not result_data:
        print("未获取到有效数据")
        return

    # 提取error_info
    error_info = result_data["error_info"]

    # 提取holding_info
    holding_info = result_data["holding_info"]
    holding_df = pd.DataFrame([{
        "股票代码": holding_info.get("code"),
        "成本价": holding_info.get("costPrice"),
        "市场代码": holding_info.get("marketCode"),
        "股票名称": holding_info.get("name"),
        "实际持仓比例": holding_info.get("positionRealRatio"),
        "当前价格": holding_info.get("presentPrice"),
        "盈亏率": holding_info.get("profitLossRate"),
        "类型": holding_info.get("type")
    }])

    # 提取relocate_info
    relocate_info = result_data["relocate_info"]
    relocate_df = pd.DataFrame([{
        "股票代码": relocate_info.get("code"),
        "当前比例": relocate_info.get("currentRatio"),
        "最终价格": relocate_info.get("finalPrice"),
        "市场代码": relocate_info.get("marketCode"),
        "股票名称": relocate_info.get("name"),
        "新比例": relocate_info.get("newRatio"),
        "盈亏率": relocate_info.get("profitLossRate"),
        "调仓时间": relocate_info.get("relocateTime"),
        "类型": relocate_info.get("type")
    }])

    # 展示DataFrame
    print("\n==== 持仓信息 ====")
    print(holding_df)
    print("\n==== 调仓信息 ====")
    print(relocate_df)

    # 保存数据到CSV文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    holding_filename = f"holding_info_{timestamp}.csv"
    relocate_filename = f"relocate_info_{timestamp}.csv"

    holding_df.to_csv(holding_filename, index=False, encoding="utf-8-sig")
    relocate_df.to_csv(relocate_filename, index=False, encoding="utf-8-sig")

    print(f"\n持仓信息已保存至 {holding_filename}")
    print(f"调仓信息已保存至 {relocate_filename}")


if __name__ == "__main__":
    result_data = fetch_and_parse_data()
    if result_data:
        extract_and_display_data(result_data)
