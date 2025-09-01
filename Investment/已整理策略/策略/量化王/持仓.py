from pprint import pprint

import pandas as pd
import requests


def get_top5_stock_selection(pool_id):
    # 请求URL
    url = "https://prod-lhw-strategy-data-center.ydtg.com.cn/lhwDataCenter/getQSCurrentCCGPById"

    # 请求参数（URL查询参数）
    params = {
        "poolId": pool_id  # 持仓查询的池ID
    }

    # 请求头信息
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTY4MjQ2MDEsImlhdCI6MTc1NDE0NjIwMX0.TbqTdscc1UyS6E3XYJgu9zGEbIgDBb8X4B_HR0Jwte0",
        "Host": "prod-lhw-strategy-data-center.ydtg.com.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.12.0",
        "If-Modified-Since": "Sun, 03 Aug 2025 13:56:57 GMT"
    }

    try:
        # 发送GET请求
        response = requests.get(url, params=params, headers=headers)

        # 打印响应状态码
        print(f"响应状态码: {response.status_code}")

        # 处理响应内容
        if response.headers.get("content-type") == "application/json":
            response_json = response.json()
            print("持仓数据（JSON）:")
            pprint(response.json())  # 解析JSON格式的持仓数据


        else:
            print("响应内容（文本）:")
            print(response.text)

        data =  response_json["data"]
        datas = []
        for item in data:
            datas.append({
                "股票名称": item["sec_name"],
                "股票代码": item["sec_code"],
                "价格": item["find_price"],
                "持仓数量": item["floating_pl"],
                "持仓l": round(item["position_pl"] * 100, 2),
                "持仓天数": item["position_day"],
                "股票池": item["stockpool_id"],
            })

        datas_df = pd.DataFrame(datas)
        return datas_df


    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")

if __name__ == '__main__':
    print(get_top5_stock_selection(pool_id=8007))