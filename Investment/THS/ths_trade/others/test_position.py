#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本：获取川财证券的持仓数据
"""
import os
import sys
import time
import json
import requests
import subprocess
import psutil

def check_ths_running():
    """检查同花顺交易软件是否正在运行"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'xiadan.exe':
            print("同花顺交易软件正在运行")
            return True
    print("警告：同花顺交易软件(xiadan.exe)未运行，请先手动启动并登录川财证券账户")
    return False

def check_server_running(port=6003):
    """检查ths_trade服务是否正在运行"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] in ['python.exe', 'pythonw.exe']:
                cmdline = ' '.join(proc.info['cmdline'])
                if 'app.py' in cmdline:
                    for conn in psutil.Process(proc.info['pid']).connections():
                        if conn.laddr.port == port:
                            print(f"ths_trade服务正在端口{port}运行")
                            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"ths_trade服务未在端口{port}运行")
    return False

def start_server():
    """启动ths_trade服务"""
    print("正在启动ths_trade服务...")
    # 创建一个新的进程来运行app.py
    process = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    # 等待服务启动
    print("等待服务启动中...")
    for i in range(10):
        time.sleep(1)
        if check_server_running():
            print("服务启动成功！")
            return True
    print("警告：服务可能未成功启动，请检查是否有错误")
    # 尝试获取错误输出
    try:
        stderr = process.stderr.read().decode('utf-8')
        if stderr:
            print(f"错误输出: {stderr}")
    except:
        pass
    return False

def get_position_data(strategy_no="test001"):
    """获取持仓数据"""
    url = "http://127.0.0.1:6003/api/search"
    payload = {
        "strategy_no": strategy_no,
        "operate": "get_position"
    }
    
    print(f"正在请求持仓数据，URL: {url}")
    print(f"请求参数: {payload}")
    
    try:
        response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        response.raise_for_status()  # 如果状态码不是200，抛出异常
        
        data = response.json()
        print(f"\n请求成功！状态码: {response.status_code}")
        print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务，请检查服务是否正在运行")
    except requests.exceptions.Timeout:
        print("错误：请求超时")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except json.JSONDecodeError:
        print("错误：无法解析响应数据，请检查响应格式是否正确")
    
    return None

def main():
    print("===== ths_trade持仓数据测试工具 =====\n")
    
    # 1. 检查同花顺是否运行
    if not check_ths_running():
        input("请先启动同花顺交易软件并登录川财证券账户，然后按Enter键继续...")
    
    # 2. 检查服务是否运行，如果没有则启动
    if not check_server_running():
        if not start_server():
            print("无法启动服务，请手动启动app.py后再试")
            return
    
    # 3. 获取持仓数据
    print("\n开始获取川财证券持仓数据...")
    position_data = get_position_data()
    
    if position_data and isinstance(position_data, dict) and 'data' in position_data:
        # 分析持仓数据
        stocks = position_data['data']
        if isinstance(stocks, list):
            print(f"\n=== 持仓分析 ===")
            print(f"持仓股票数量: {len(stocks)}")
            
            total_value = 0
            for stock in stocks:
                # 打印每只股票的基本信息
                if isinstance(stock, dict):
                    print(f"股票名称: {stock.get('证券名称', '未知')}")
                    print(f"股票代码: {stock.get('证券代码', '未知')}")
                    print(f"持仓数量: {stock.get('持仓数量', '未知')}")
                    print(f"可用数量: {stock.get('可用数量', '未知')}")
                    print(f"最新价格: {stock.get('最新价格', '未知')}")
                    print(f"市值: {stock.get('市值', '未知')}")
                    print("---")
                    
                    # 计算总市值
                    try:
                        value = float(stock.get('市值', '0').replace(',', ''))
                        total_value += value
                    except:
                        pass
            
            print(f"总市值: {total_value:.2f}元")
    
    print("\n测试完成！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"发生未预期的错误: {e}")
    finally:
        input("按Enter键退出...")