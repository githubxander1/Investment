from pprint import pprint

import requests

from Investment.THS.策略.接口.策略相关推荐 import extracted_data


def get_strategy_detail(pool_id):
    # 请求URL（获取指定poolId的概览数据，含收益相关信息）
    url = "https://prod-lhw-strategy-data-center.ydtg.com.cn/lhwDataCenter/getOverViewByPoolId"

    params = {
        "poolId": pool_id
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

        # 处理响应内容（优先解析JSON格式，适用于收益等结构化数据）
        if response.headers.get("content-type") == "application/json":
            print("收益概览数据（JSON）:")
            response_json = response.json()
            # pprint(response.json())
        else:
            print("响应内容（文本）:")
            print(response.text)

        extracted_data = []
        for item in response_json:
            extracted_data.append({
                "策略名称": item.get("name"),
                "总市值": item.get("amount"),
                "余额": item.get("residue_amount"),
                "仓位%": round(item.get("cangwei") * 100, 2),
                "日收益%": round(item.get("riShouYi"), 2),
                "超额收益%": round(item.get("chaoeShouYi"), 2),
                "累计收益%": round(item.get("leiJiShouYi"), 2),
                "年化收益%": round(item.get("nianHuaShouYi"), 2),
                "胜率%": round(item.get("shengLv"), 2),
                "夏普比率%": round(item.get("xiaPuBiLv"), 2),
                "盈亏比%": round(item.get("yingKuiBi"), 2),
                "最大回测%": round(item.get("zuiDaHuiCe"), 2),
                "时间": item.get("calcDay"),
                "创建时间": item.get("createTime"),
            })
        return extracted_data

    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")

if __name__ == '__main__':
    print(get_strategy_detail(8007))