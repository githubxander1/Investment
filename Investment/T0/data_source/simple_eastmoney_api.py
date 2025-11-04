# -*- coding: utf-8 -*-
"""
简化版东方财富分时数据接口
只包含基本的请求和数据提取功能
"""
from pprint import pprint

import requests
import pandas as pd
import json
import random
from datetime import datetime


def get_user_agent():
    """返回随机User-Agent"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    return random.choice(user_agents)


def get_eastmoney_fenshi_simple(stock_code, market_type=1):
    """
    简化版东方财富分时数据获取
    
    Args:
        stock_code (str): 股票代码，如 "600030"
        market_type (int): 市场类型，1=沪市，0=深市，默认为1
    
    Returns:
        pandas.DataFrame: 分时数据DataFrame
    """
    # 构造secid
    secid = f"{market_type}.{stock_code}"
    
    # 构造请求URL
    url = (
        f'http://16.push2.eastmoney.com/api/qt/stock/details/sse'
        f'?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55'
        f'&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281'
        f'&fltt=2&pos=-0&secid={secid}'
    )
    
    # 设置请求头
    headers = {
        'User-Agent': get_user_agent(),
        'Referer': f'http://quote.eastmoney.com/sh{stock_code}.html',
        'Host': '16.push2.eastmoney.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    try:
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        pprint(response.json())
        
        if response.status_code == 200:
            # 处理响应数据
            data_str = response.text.lstrip('data:')
            if not data_str:
                print(f"响应为空，未获取到数据 (secid: {secid})")
                return pd.DataFrame()
            
            # 确保是完整JSON
            if not data_str.startswith('{'):
                data_str = data_str[data_str.find('{'):]
            
            data_dict = json.loads(data_str)
            
            # 检查接口返回状态
            if data_dict.get('rc') != 0:
                print(f"接口返回错误: rc={data_dict.get('rc')}, rt={data_dict.get('rt')}")
                return pd.DataFrame()
            
            # 获取分时数据
            if 'data' not in data_dict or data_dict['data'] is None:
                print(f"响应中缺少data字段或data为null (secid: {secid})")
                return pd.DataFrame()
            
            data_content = data_dict['data']
            preprice = data_content.get('prePrice', 0)
            details = data_content.get('details', [])
            
            if not details:
                print("分时数据为空")
                return pd.DataFrame()
            
            # 解析所有分时数据
            data = []
            for detail in details:
                try:
                    items = detail.split(',')
                    if len(items) >= 5:
                        time_str = items[0]
                        price = float(items[1])
                        volume = int(items[2])
                        operation = items[3]
                        trade_type = items[4]
                        
                        # 转换时间格式
                        try:
                            time_obj = datetime.strptime(time_str, "%H:%M")
                            time_str = time_obj.strftime("%H:%M:%S")
                        except:
                            pass
                        
                        data.append({
                            "昨收价": preprice,
                            "时间": time_str,
                            "最新价": price,
                            "涨跌幅(%)": (price - preprice) / preprice * 100 if preprice else 0,
                            "成交量(手)": volume,
                            "操作": operation,
                            "交易类型": trade_type
                        })
                except Exception as e:
                    print(f"解析分时数据行出错: {e}, 行内容: {detail}")
                    continue
            
            print(f"成功解析 {len(data)} 条分时数据")
            df = pd.DataFrame(data)
            return df
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return pd.DataFrame()


# 使用示例
if __name__ == "__main__":
    # 获取中信证券(600030)的分时数据
    stock_code = "600030"
    df = get_eastmoney_fenshi_simple(stock_code)
    
    if not df.empty:
        print(f"获取到 {len(df)} 条数据")
        print(df.head())
        
        # 保存到CSV文件
        df.to_csv(f"{stock_code}_分时数据_simple.csv", index=False, encoding="utf-8-sig")
        print(f"数据已保存到 {stock_code}_分时数据_simple.csv")
    else:
        print("未能获取到数据")