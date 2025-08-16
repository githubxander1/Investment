# 益萌强势.py
from pprint import pprint

import requests
import json
import pandas as pd
from datetime import datetime
import os

def get_strategy_detail():
    # 请求URL
    url = "https://emapp.emoney.cn/SmartInvestment/Strategy/Detail"
    
    # 请求头信息
    headers = {
        "X-Protocol-Id": "SmartInvestment%2FStrategy%2FDetail",
        "X-Request-Id": "null",
        "EM-Sign": "23082404151001:a0443b49b1c0c9a5d3182cd67b074ae5:bwqKUviNHF:1754225006705",
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCJ9.eyJ1dWQiOjEwMTUwNDYxMDEsInVpZCI6MjkwMTg0NjIsImRpZCI6IjExY2ZlMmQzZmZlOTkzMDMzMTY2NmNiZmIwZWNkMmJjIiwidHlwIjo0LCJhY2MiOiIxMWNmZTJkM2ZmZTk5MzAzMzE2NjZjYmZiMGVjZDJiYyIsInN3dCI6MSwibGd0IjoxNzU0MjIyMjg1MjEyLCJuYmYiOjE3NTQyMjIyODUsImV4cCI6MTc1NTk1MDI4NSwiaWF0IjoxNzU0MjIyMjg1fQ.91dKxwW5Z9rh9PjHHUhfnOFnnCHzoU_ToZGq6HuTdhg",
        "X-Android-Agent": "EMAPP/5.12.0(Android;29)",
        "Emapp-ViewMode": "1",
        "Content-Type": "application/json",
        "Host": "emapp.emoney.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.13"
    }
    
    # 请求体数据
    data = {
        "stockPoolSize": -1,
        "id": 70008
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析响应为JSON
        result = response.json()
        
        # 修改返回结果中的auth字段为true（若存在）
        if "auth" in result:
            result["auth"] = True
        else:
            # 若原结果中无auth字段，主动添加
            result["auth"] = True
        
        # 打印处理后的结果（可根据需求改为返回结果）
        print("处理后的详情结果：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
    except json.JSONDecodeError:
        print("响应内容不是有效的JSON格式")
    return None

def extract_important_data(strategy_data):
    """
    提取策略重要数据
    """
    if not strategy_data or 'data' not in strategy_data:
        print("无效的策略数据")
        return None

    data = strategy_data['data']

    # 1. 提取策略基本信息
    basic_info = {
        '策略名称': data.get('name', ''),
        '策略ID': data.get('id', ''),
        '收益率': data.get('yieldRate', ''),
        '年化收益率': data.get('annualYieldRate', ''),
        '最大回撤': data.get('maxDrawdown', ''),
        '夏普比率': data.get('sharpRate', ''),
        '更新时间': data.get('updateTime', ''),
        '股票池数量': data.get('stockPoolSize', ''),
        '策略描述': data.get('description', ''),
    }

    # 2. 提取持仓股票信息
    positions = []
    if 'positions' in data:
        for pos in data['positions']:
            position_info = {
                '股票代码': pos.get('stockCode', ''),
                '股票名称': pos.get('stockName', ''),
                '持仓比例': pos.get('positionRatio', ''),
                '最新价格': pos.get('newPrice', ''),
                '涨跌幅': pos.get('changeRatio', ''),
                '市值': pos.get('marketValue', ''),
            }
            positions.append(position_info)

    # 3. 提取历史表现数据
    history_performance = []
    if 'historyYieldRates' in data:
        for hist in data['historyYieldRates']:
            history_info = {
                '日期': hist.get('date', ''),
                '收益率': hist.get('yieldRate', ''),
                '沪深300对比': hist.get('hs300YieldRate', ''),
            }
            history_performance.append(history_info)

    # 4. 提取调仓记录
    rebalance_records = []
    if 'rebalanceRecords' in data:
        for record in data['rebalanceRecords']:
            record_info = {
                '调仓日期': record.get('rebalanceDate', ''),
                '调仓类型': record.get('rebalanceType', ''),
                '调仓描述': record.get('description', ''),
            }
            rebalance_records.append(record_info)

    return {
        'basic_info': basic_info,
        'positions': positions,
        'history_performance': history_performance,
        'rebalance_records': rebalance_records
    }

def save_to_excel(extracted_data, filename="益萌强势策略数据.xlsx"):
    """
    将提取的数据保存到Excel文件的不同工作表中
    """
    if not extracted_data:
        print("没有数据可保存")
        return

    # 创建Excel写入器
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 1. 保存基本信息到"策略概况"工作表
        basic_info_df = pd.DataFrame([extracted_data['basic_info']])
        basic_info_df.to_excel(writer, sheet_name='策略概况', index=False)
        print(f"已保存策略概况到 {filename} 的 策略概况 工作表")

        # 2. 保存持仓信息到"持仓股票"工作表
        if extracted_data['positions']:
            positions_df = pd.DataFrame(extracted_data['positions'])
            positions_df.to_excel(writer, sheet_name='持仓股票', index=False)
            print(f"已保存持仓股票到 {filename} 的 持仓股票 工作表")
        else:
            pd.DataFrame([{'提示': '无持仓数据'}]).to_excel(writer, sheet_name='持仓股票', index=False)

        # 3. 保存历史表现到"历史表现"工作表
        if extracted_data['history_performance']:
            history_df = pd.DataFrame(extracted_data['history_performance'])
            history_df.to_excel(writer, sheet_name='历史表现', index=False)
            print(f"已保存历史表现到 {filename} 的 历史表现 工作表")
        else:
            pd.DataFrame([{'提示': '无历史表现数据'}]).to_excel(writer, sheet_name='历史表现', index=False)

        # 4. 保存调仓记录到"调仓记录"工作表
        if extracted_data['rebalance_records']:
            rebalance_df = pd.DataFrame(extracted_data['rebalance_records'])
            rebalance_df.to_excel(writer, sheet_name='调仓记录', index=False)
            print(f"已保存调仓记录到 {filename} 的 调仓记录 工作表")
        else:
            pd.DataFrame([{'提示': '无调仓记录数据'}]).to_excel(writer, sheet_name='调仓记录', index=False)

    print(f"所有数据已保存到 {filename}")

def main():
    """
    主函数：获取策略数据，提取重要信息并保存到Excel
    """
    # 获取策略详情数据
    strategy_data = get_strategy_detail()

    if strategy_data:
        # 提取重要数据
        extracted_data = extract_important_data(strategy_data)

        if extracted_data:
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"益萌强势策略数据_{timestamp}.xlsx"

            # 保存到Excel
            # save_to_excel(extracted_data, filename)
        else:
            print("数据提取失败")
    else:
        print("获取策略数据失败")

if __name__ == "__main__":
    # 执行函数获取详情
    main()
    # 股票对比:'https://appstatic.emoney.cn/ymstock/compare/?goodsAid=600017&goodsBid=1000528&goodsCid=1002001&emoneyScaleType=0&emoneyLandMode=0&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCJ9.eyJ1dWQiOjEwMTUwNDYxMDEsInVpZCI6MjkwMTg0NjIsImRpZCI6IjExY2ZlMmQzZmZlOTkzMDMzMTY2NmNiZmIwZWNkMmJjIiwidHlwIjo0LCJhY2MiOiIxMWNmZTJkM2ZmZTk5MzAzMzE2NjZjYmZiMGVjZDJiYyIsInN3dCI6MSwibGd0IjoxNzU0MjIyMjg1MjEyLCJuYmYiOjE3NTQyMjIyODUsImV4cCI6MTc1NTk1MDI4NSwiaWF0IjoxNzU0MjIyMjg1fQ.91dKxwW5Z9rh9PjHHUhfnOFnnCHzoU_ToZGq6HuTdhg'
