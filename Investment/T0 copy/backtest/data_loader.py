import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import akshare as ak
from typing import Dict, List
from .config import BACKTEST_DATA_DIR

def load_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    加载股票历史分时数据用于回测
    
    Args:
        symbol: 股票代码
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)
        
    Returns:
        DataFrame: 包含历史分时数据的DataFrame
    """
    # 尝试从缓存加载数据
    cache_file = os.path.join(BACKTEST_DATA_DIR, f"{symbol}_{start_date}_{end_date}.csv")
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file)
            df['时间'] = pd.to_datetime(df['时间'])
            df.set_index('时间', inplace=True)
            return df
        except Exception as e:
            print(f"读取缓存文件失败: {e}")

    # 如果缓存不存在，则从网络获取数据
    try:
        # 将日期字符串转换为datetime对象
        start_dt = datetime.strptime(start_date, '%Y%m%d')
        end_dt = datetime.strptime(end_date, '%Y%m%d')
        
        # 生成日期范围
        date_range = pd.date_range(start=start_dt, end=end_dt, freq='D')
        
        all_data = []
        for date in date_range:
            # 跳过周末
            if date.weekday() >= 5:
                continue
                
            date_str = date.strftime('%Y%m%d')
            try:
                # 获取指定日期的分时数据
                daily_data = ak.stock_zh_a_hist_min_em(
                    symbol=symbol,
                    period="1",
                    start_date=date_str,
                    end_date=date_str,
                    adjust=''
                )
                
                if not daily_data.empty:
                    # 重命名列
                    daily_data = daily_data.rename(columns={
                        '时间': '时间',
                        '开盘': '开盘',
                        '收盘': '收盘',
                        '最高': '最高',
                        '最低': '最低',
                        '成交量': '成交量',
                        '成交额': '成交额'
                    })
                    
                    # 转换时间列为datetime类型
                    daily_data['时间'] = pd.to_datetime(daily_data['时间'])
                    daily_data.set_index('时间', inplace=True)
                    
                    # 过滤掉午休时间
                    daily_data = daily_data[
                        ~((daily_data.index.hour == 11) & (daily_data.index.minute >= 30)) & 
                        ~(daily_data.index.hour == 12)
                    ]
                    
                    all_data.append(daily_data)
                    
            except Exception as e:
                print(f"获取{symbol}在{date_str}的数据时出错: {e}")
                continue
        
        if all_data:
            # 合并所有日期的数据
            df = pd.concat(all_data)
            
            # 保存到缓存
            df_reset = df.reset_index()
            df_reset.to_csv(cache_file, index=False, encoding='utf-8-sig')
            
            return df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        print(f"加载{symbol}数据时出错: {e}")
        return pd.DataFrame()

def get_prev_close(symbol: str, date: str) -> float:
    """
    获取指定日期的前收盘价
    
    Args:
        symbol: 股票代码
        date: 日期 (YYYYMMDD)
        
    Returns:
        float: 前收盘价
    """
    try:
        date_dt = datetime.strptime(date, '%Y%m%d')
        
        # 获取日线数据
        daily_df = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            adjust=""
        )
        
        if daily_df.empty:
            return None
            
        # 转换日期列
        daily_df['日期'] = pd.to_datetime(daily_df['日期'])
        
        # 找到指定日期前的最后一个交易日
        prev_data = daily_df[daily_df['日期'] < date_dt]
        
        if prev_data.empty:
            return None
            
        return prev_data.iloc[-1]['收盘']
        
    except Exception as e:
        print(f"获取{symbol}前收盘价时出错: {e}")
        return None