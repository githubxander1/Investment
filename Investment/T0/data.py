# -*- coding: utf-8 -*-
# @Time    : 2022/6/1 23:10
# @Author  : Thresh
# 功能：循环抓取东方财富网分时数据（多页），解析jQuery包裹的JSON数据

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 关闭SSL证书验证警告（因接口可能存在证书问题，生产环境建议验证证书）
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_eastmoney_fenshi_by_requests(stock_code="688103", market="1", page_count=5):
    """
    抓取东方财富网分时数据（简易版）
    :param stock_code: 股票代码，如688103（默认）
    :param market: 市场标识，1=沪市，0=深市（默认沪市）
    :param page_count: 循环请求的页数（默认5页，每页144条数据）
    :return: 所有页的分时数据列表
    """
    all_fenshi_data = []  # 存储所有分时数据

    for page in range(page_count):
        # 1. 构造请求参数（关键参数需根据目标股票调整）
        params = (
            ('pagesize', '144'),  # 每页数据量
            ('ut', '7eea3edcaed734bea9cbfc24409ed989'),  # 固定标识（可能随网站更新变化）
            ('dpt', 'wzfscj'),  # 数据类型标识（分时数据）
            ('cb', 'jQuery1124029337350072397084_1631343037828'),  # jQuery回调函数名（需与接口返回匹配）
            ('pageindex', str(page)),  # 当前页码（从0开始）
            ('id', '6009051'),  # 可能为股票相关ID（需根据实际情况调整）
            ('sort', '1'),  # 排序方式（1=正序）
            ('ft', '1'),  # 过滤条件（默认1）
            ('code', stock_code),  # 目标股票代码
            ('market', market),  # 市场标识
            ('_', '1631343037827'),  # 时间戳（可替换为当前时间戳，避免缓存）
        )

        # 2. 发送GET请求（verify=False关闭SSL验证，生产环境需谨慎）
        try:
            response = requests.get(
                url='http://push2ex.eastmoney.com/getStockFenShi',
                params=params,
                verify=False,
                timeout=10  # 超时时间（避免请求挂起）
            )
            response.raise_for_status()  # 若状态码非200，抛出异常
        except requests.exceptions.RequestException as e:
            print(f"第{page}页请求失败：{e}")
            continue

        # 3. 解析响应（去除jQuery包裹的 "jQuery(...)" 格式）
        try:
            # 截取括号内的JSON字符串（如：jQuery123(...) → ...部分）
            json_str = response.text.split('(')[1].split(')')[0]
            data_dict = json.loads(json_str)  # 转为字典
        except (IndexError, json.JSONDecodeError) as e:
            print(f"第{page}页数据解析失败：{e}")
            continue

        # 4. 提取分时数据并存储
        fenshi_data = data_dict.get("data", {}).get("data", [])
        if fenshi_data:
            all_fenshi_data.extend(fenshi_data)
            print(f"成功获取第{page}页数据，共{len(fenshi_data)}条")
        else:
            print(f"第{page}页无数据")

    return all_fenshi_data


# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 抓取沪市股票688103的5页分时数据
    result = get_eastmoney_fenshi_by_requests(stock_code="600030", market="1", page_count=5)
    print(f"\n总获取数据条数：{len(result)}")
    # 打印前3条数据示例
    if result:
        print("前3条数据示例：")
        for i in range(min(3, len(result))):
            print(result[i])