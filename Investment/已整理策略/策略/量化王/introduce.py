# 九凤鸣岐策略数据提取.py
import json
import pandas as pd
from datetime import datetime
import os

import requests


def load_strategy_data(json_file_path):
    """
    从JSON文件加载策略数据
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"文件 {json_file_path} 未找到")
        return None
    except json.JSONDecodeError:
        print(f"文件 {json_file_path} 不是有效的JSON格式")
        return None

def get_introduction_data():
    # 接口配置
    url = "https://prod-lianghuawang-api.yd.com.cn/liangHuaEntrance/l/getLiangHuaCeLue"
    headers = {
        "accept": "application/json",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTY4MjQ2MDEsImlhdCI6MTc1NDE0NjIwMX0.TbqTdscc1UyS6E3XYJgu9zGEbIgDBb8X4B_HR0Jwte0",
        "Content-Type": "application/json",
        "Host": "prod-lianghuawang-api.yd.com.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.12.0"
    }

    # 请求体（查询id为8007的策略介绍）
    payload = {"id": "8007"}

    response = requests.post(
        url,
        headers=headers,
        json=payload,  # 自动处理JSON序列化
        timeout=10
    )
    response.raise_for_status()
    strategy_data = response.json()
    return strategy_data
def extract_important_data(strategy_data):
    """
    从策略JSON数据中提取重要信息
    """
    if not strategy_data or 'data' not in strategy_data:
        print("无效的策略数据")
        return {}

    data = strategy_data['data']
    extracted_data = {}

    # 1. 策略基本信息
    basic_info_data = {
        '字段': [
            '策略名称', '策略ID', '发布日期', '更新时间', '上架时间',
            '年化收益', '最大回撤', '夏普比率', '胜率', '盈亏比',
            '近1年收益', '近3年收益', '近5年收益', '历史累计收益'
        ],
        '值': [
            data.get('name', ''),
            data.get('lhid', ''),
            data.get('publishTime', ''),
            data.get('updateTime', ''),
            data.get('shelfTime', ''),
            data.get('nsy', ''),
            data.get('maxIncome', ''),
            data.get('jsy', ''),  # 夏普比率
            data.get('winRate', ''),
            data.get('winLoseRatio', ''),
            data.get('ysy', ''),  # 近1年收益
            data.get('zsy', ''),  # 近3年收益
            data.get('hnsy', ''), # 近5年收益
            data.get('backtestingIncome', '')  # 历史累计收益
        ]
    }
    extracted_data['策略基本信息'] = pd.DataFrame(basic_info_data)

    # 2. 策略参数条件
    if 'stockLabelJson' in data and 'tiaoJianTree' in data['stockLabelJson']:
        tiaoJianTree = data['stockLabelJson']['tiaoJianTree']
        if 'params' in tiaoJianTree:
            params_list = []
            for param in tiaoJianTree['params']:
                params_list.append({
                    '参数类别': param.get('selectTitle', ''),
                    '参数描述': param.get('selectDesc', ''),
                    '完整描述': param.get('selectFullDesc', ''),
                    '参数ID': param.get('selectId', ''),
                    '参数缩写': param.get('abbrs', '')
                })
            extracted_data['选股条件'] = pd.DataFrame(params_list)

    # 3. 回测参数设置
    if 'stockLabelJson' in data and 'huiceTree' in data['stockLabelJson']:
        huiceTree = data['stockLabelJson']['huiceTree']
        backtest_params = [
            {'参数': '回测开始时间', '值': datetime.fromtimestamp(huiceTree.get('startTime', 0)).strftime('%Y-%m-%d') if huiceTree.get('startTime') else ''},
            {'参数': '回测结束时间', '值': datetime.fromtimestamp(huiceTree.get('endTime', 0)).strftime('%Y-%m-%d') if huiceTree.get('endTime') else ''},
            {'参数': '买入时间', '值': huiceTree.get('buyTime', '')},
            {'参数': '持有天数', '值': huiceTree.get('holdingPeriod', '')},
            {'参数': '持仓上限', '值': huiceTree.get('holdingLimit', '')},
            {'参数': '单日买入上限', '值': huiceTree.get('singleDayBuyLimit', '')},
            {'参数': '初始资金', '值': huiceTree.get('initialCapital', '')},
            {'参数': '止盈点', '值': huiceTree.get('takeProfit', '')},
            {'参数': '止损点', '值': huiceTree.get('stopLoss', '')},
            {'参数': '最大仓位', '值': huiceTree.get('maximumPosition', '')}
        ]
        extracted_data['回测参数'] = pd.DataFrame(backtest_params)

    # 4. 交易模型
    if 'stockLabelJson' in data and 'tiao_jian_select_tree' in data['stockLabelJson']:
        tiao_jian_select_tree = data['stockLabelJson']['tiao_jian_select_tree']
        if 'transactionModel' in tiao_jian_select_tree:
            transaction_model = tiao_jian_select_tree['transactionModel']
            if 'child' in transaction_model:
                model_list = []
                for item in transaction_model['child']:
                    model_list.append({
                        '交易模型参数': item.get('key', ''),
                        '参数值': item.get('value', '')
                    })
                extracted_data['交易模型'] = pd.DataFrame(model_list)

    # 5. 策略介绍
    introduction_data = {
        '策略介绍': [data.get('introduction', '无介绍')]
    }
    extracted_data['策略介绍'] = pd.DataFrame(introduction_data)

    return extracted_data

def save_to_excel(data_dict, filename='九凤鸣岐策略数据.xlsx'):
    """
    将提取的数据保存到Excel文件的不同工作表中
    """
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                # 如果DataFrame为空，创建一个提示信息
                pd.DataFrame([f'无{sheet_name}数据']).to_excel(writer, sheet_name=sheet_name, index=False, header=False)

    print(f"数据已保存至: {filename}")

def main():
    """
    主函数：加载JSON数据、提取重要信息并保存到Excel
    """
    # JSON文件路径
    json_file_path = 'strategy_8007_intro.json'

    # 加载策略数据
    # strategy_data = load_strategy_data(json_file_path)
    strategy_data = get_introduction_data()

    if strategy_data:
        # 提取重要数据
        important_data = extract_important_data(strategy_data)

        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'九凤鸣岐策略数据_{timestamp}.xlsx'

        # 保存到Excel
        save_to_excel(important_data, filename)

        # 打印部分数据预览
        print("数据提取完成，部分数据预览:")
        for name, df in important_data.items():
            if not df.empty:
                print(f"\n=== {name} ===")
                print(df.head())
    else:
        print("加载策略数据失败")

if __name__ == "__main__":
    main()

    # 股票对比:'https://appstatic.emoney.cn/ymstock/compare/?goodsAid=600017&goodsBid=1000528&goodsCid=1002001&emoneyScaleType=0&emoneyLandMode=0&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCJ9.eyJ1dWQiOjEwMTUwNDYxMDEsInVpZCI6MjkwMTg0NjIsImRpZCI6IjExY2ZlMmQzZmZlOTkzMDMzMTY2NmNiZmIwZWNkMmJjIiwidHlwIjo0LCJhY2MiOiIxMWNmZTJkM2ZmZTk5MzAzMzE2NjZjYmZiMGVjZDJiYyIsInN3dCI6MSwibGd0IjoxNzU0MjIyMjg1MjEyLCJuYmYiOjE3NTQyMjIyODUsImV4cCI6MTc1NTk1MDI4NSwiaWF0IjoxNzU0MjIyMjg1fQ.91dKxwW5Z9rh9PjHHUhfnOFnnCHzoU_ToZGq6HuTdhg'
