# -*- coding: utf-8 -*-
# 功能：抓取东方财富网分时数据，用pandas转为DataFrame（便于数据分析）

import urllib.request
import pandas as pd
import json
from datetime import datetime
from urllib.error import URLError, HTTPError
from typing import Optional


def get_eastmoney_fenshi_with_pandas(secid="1.600030") -> Optional[pd.DataFrame]:
    """
    抓取东方财富网分时数据并转为DataFrame
    
    Args:
        secid: 股票标识（格式：市场.股票代码，1=沪市，0=深市，如1.600030、0.300059）
        
    Returns:
        分时数据DataFrame，包含以下列：
        - 时间: datetime格式的时间
        - 开盘: 开盘价（与收盘价相同，为了与其他接口保持一致）
        - 收盘: 收盘价
        - 最高: 最高价（与收盘价相同，为了与其他接口保持一致）
        - 最低: 最低价（与收盘价相同，为了与其他接口保持一致）
        - 成交量: 成交量
        - 成交额: 成交额（根据价格和成交量计算）
        - 均价: 均价（与收盘价相同，为了与其他接口保持一致）
    """
    # 1. 构造请求URL（参数含义：fields1=基础字段，fields2=分时字段，mpi=最大数据量）
    url = (
        f'http://16.push2.eastmoney.com/api/qt/stock/details/sse'
        f'?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55'  # f51=时间，f52=价格等
        f'&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281'  # mpi=最大返回2000条数据
        f'&fltt=2&pos=-0&secid={secid}'  # secid=目标股票标识
    )

    # 2. 发送请求并读取响应
    try:
        with urllib.request.urlopen(url=url, timeout=10) as response:
            # 响应格式为 "data:{...}"，需去除前缀"data:"
            data_str = response.readline().decode('utf-8').lstrip('data:')
            
            if not data_str or data_str.strip() == '{}':
                print("响应为空，未获取到数据")
                return pd.DataFrame()
                
            # 解析JSON数据
            data_dict = json.loads(data_str)
            details_list = data_dict.get('data', {}).get('details', [])
            
            if not details_list:
                print("未获取到分时数据")
                return pd.DataFrame()
                
    except HTTPError as e:
        print(f"请求错误（状态码：{e.code}）：{e.reason}")
        return pd.DataFrame()
    except URLError as e:
        print(f"URL错误或网络问题：{e.reason}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        print(f"JSON解析错误：{e}")
        return pd.DataFrame()

    # 3. 解析details数据并转为DataFrame
    try:
        # 创建存储解析后数据的列表
        parsed_data = []
        
        # 解析每条记录
        for detail in details_list:
            # 每条记录格式: "时间,价格,成交量,未知,未知"
            parts = detail.split(',')
            if len(parts) >= 3:
                time_str = parts[0]  # 时间
                price = float(parts[1])  # 价格
                volume = int(parts[2])  # 成交量
                
                # 构造完整的时间字符串（假设是当天数据）
                # 获取当前日期
                current_date = datetime.now().strftime('%Y-%m-%d')
                full_time_str = f"{current_date} {time_str}"
                
                # 计算成交额
                amount = price * volume * 100  # 成交量单位是手，需要转换为股
                
                parsed_data.append({
                    '时间': full_time_str,
                    '开盘': price,
                    '收盘': price,
                    '最高': price,
                    '最低': price,
                    '成交量': volume,
                    '成交额': amount,
                    '均价': price
                })
        
        if not parsed_data:
            print("解析后的数据为空")
            return pd.DataFrame()
            
        # 转为DataFrame
        df = pd.DataFrame(parsed_data)
        
        # 转换时间列为datetime格式
        df['时间'] = pd.to_datetime(df['时间'])
        
        return df
        
    except Exception as e:
        print(f"数据解析失败：{e}")
        return pd.DataFrame()


def test_eastmoney_fenshi_data(stock_code="600030"):
    """
    测试东方财富分时数据获取功能
    
    Args:
        stock_code: 股票代码
    """
    # 根据股票代码确定市场标识
    if stock_code.startswith('6'):
        secid = f"1.{stock_code}"  # 沪市
    else:
        secid = f"0.{stock_code}"  # 深市
        
    df_fenshi = get_eastmoney_fenshi_with_pandas(secid=secid)
    print(f"DataFrame形状：{df_fenshi.shape}")  # 打印数据行数和列数
    if not df_fenshi.empty:
        print("\nDataFrame前5行：")
        print(df_fenshi.head())
        print("\nDataFrame后5行：")
        print(df_fenshi.tail())
        # 可选：导出为Excel或CSV
        # df_fenshi.to_excel(f"{stock_code}分时数据.xlsx", index=False)
        # df_fenshi.to_csv(f"{stock_code}分时数据.csv", index=False, encoding="utf-8-sig")
    else:
        print("未获取到数据")


# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 抓取沪市600030的分时数据
    test_eastmoney_fenshi_data("600030")