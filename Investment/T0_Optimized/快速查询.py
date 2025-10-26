#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速查询工具 - 便捷的数据库查询命令
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = 'db/t0_trading.db'

def quick_stats():
    """快速统计"""
    conn = sqlite3.connect(DB_PATH)
    
    print("\n" + "=" * 60)
    print("📊 数据库统计")
    print("=" * 60)
    
    # 分时数据统计
    query = """
        SELECT 
            COUNT(DISTINCT stock_code) as 股票数量,
            COUNT(*) as 总记录数,
            MIN(datetime) as 最早时间,
            MAX(datetime) as 最新时间
        FROM minute_data
    """
    df = pd.read_sql_query(query, conn)
    print("\n分时数据:")
    print(df.to_string(index=False))
    
    # 各股票统计
    query = """
        SELECT 
            stock_code as 股票代码,
            COUNT(*) as 记录数,
            MIN(datetime) as 开始时间,
            MAX(datetime) as 结束时间
        FROM minute_data
        GROUP BY stock_code
    """
    df = pd.read_sql_query(query, conn)
    print("\n各股票数据:")
    print(df.to_string(index=False))
    
    conn.close()


def today_data(stock_code='000333'):
    """查看今天的数据"""
    conn = sqlite3.connect(DB_PATH)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    query = f"""
        SELECT datetime as 时间, open as 开盘, close as 收盘, 
               high as 最高, low as 最低, volume as 成交量
        FROM minute_data
        WHERE stock_code = '{stock_code}' 
          AND datetime LIKE '{today}%'
        ORDER BY datetime
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        print(f"\n📈 {stock_code} 今天的数据 ({len(df)} 条):\n")
        print(df.to_string(index=False))
    else:
        print(f"\n❌ 今天还没有 {stock_code} 的数据")


def recent_data(stock_code='000333', days=1):
    """查看最近几天的数据"""
    conn = sqlite3.connect(DB_PATH)
    
    query = f"""
        SELECT datetime as 时间, open as 开盘, close as 收盘, 
               high as 最高, low as 最低, volume as 成交量
        FROM minute_data
        WHERE stock_code = '{stock_code}'
        ORDER BY datetime DESC
        LIMIT {days * 241}
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        print(f"\n📈 {stock_code} 最近的数据 ({len(df)} 条):\n")
        print(df.head(20).to_string(index=False))
        if len(df) > 20:
            print(f"\n... 还有 {len(df) - 20} 条记录")
    else:
        print(f"\n❌ 没有找到 {stock_code} 的数据")


def price_range(stock_code='000333', date='2025-10-24'):
    """查看价格区间"""
    conn = sqlite3.connect(DB_PATH)
    
    query = f"""
        SELECT 
            stock_code as 股票代码,
            DATE(datetime) as 日期,
            MIN(low) as 最低价,
            MAX(high) as 最高价,
            ROUND((MAX(high) - MIN(low)) / MIN(low) * 100, 2) as 振幅,
            SUM(volume) as 总成交量,
            ROUND(SUM(amount) / 100000000, 2) as 成交额亿
        FROM minute_data
        WHERE stock_code = '{stock_code}'
          AND datetime LIKE '{date}%'
        GROUP BY stock_code, DATE(datetime)
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        print(f"\n📊 {stock_code} 在 {date} 的价格统计:\n")
        print(df.to_string(index=False))
    else:
        print(f"\n❌ 没有找到数据")


def export_to_excel(stock_code='000333', output='数据导出.xlsx'):
    """导出数据到Excel"""
    conn = sqlite3.connect(DB_PATH)
    
    # 读取所有数据
    query = f"""
        SELECT datetime as 时间, stock_code as 股票代码,
               open as 开盘, close as 收盘, high as 最高, low as 最低,
               volume as 成交量, amount as 成交额, 
               avg_price as 均价, change_pct as 涨跌幅
        FROM minute_data
        WHERE stock_code = '{stock_code}'
        ORDER BY datetime
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        df.to_excel(output, index=False, engine='openpyxl')
        print(f"\n✅ 已导出 {len(df)} 条记录到: {output}")
    else:
        print(f"\n❌ 没有数据可导出")


def interactive_query():
    """交互式查询"""
    conn = sqlite3.connect(DB_PATH)
    
    print("\n" + "=" * 60)
    print("🔍 交互式SQL查询")
    print("=" * 60)
    print("\n输入 SQL 查询语句（输入 'exit' 退出）")
    print("示例: SELECT * FROM minute_data LIMIT 5")
    print()
    
    while True:
        try:
            query = input("SQL> ").strip()
            
            if query.lower() == 'exit':
                break
            
            if not query:
                continue
            
            df = pd.read_sql_query(query, conn)
            print()
            print(df.to_string(index=False))
            print(f"\n返回 {len(df)} 行")
            print()
            
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")
    
    conn.close()


if __name__ == '__main__':
    import sys
    
    print("\n" + "🔍 " * 20)
    print("快速查询工具")
    print("🔍 " * 20)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'stats':
            quick_stats()
        
        elif command == 'today':
            stock = sys.argv[2] if len(sys.argv) > 2 else '000333'
            today_data(stock)
        
        elif command == 'recent':
            stock = sys.argv[2] if len(sys.argv) > 2 else '000333'
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            recent_data(stock, days)
        
        elif command == 'range':
            stock = sys.argv[2] if len(sys.argv) > 2 else '000333'
            date = sys.argv[3] if len(sys.argv) > 3 else '2025-10-24'
            price_range(stock, date)
        
        elif command == 'export':
            stock = sys.argv[2] if len(sys.argv) > 2 else '000333'
            output = sys.argv[3] if len(sys.argv) > 3 else f'{stock}_数据.xlsx'
            export_to_excel(stock, output)
        
        elif command == 'sql':
            interactive_query()
        
        else:
            print(f"\n❌ 未知命令: {command}")
    
    else:
        # 默认显示统计
        quick_stats()
    
    print("\n💡 使用提示:")
    print("  查看统计:     python 快速查询.py stats")
    print("  今天数据:     python 快速查询.py today 000333")
    print("  最近数据:     python 快速查询.py recent 000333 3")
    print("  价格区间:     python 快速查询.py range 000333 2025-10-24")
    print("  导出Excel:    python 快速查询.py export 000333")
    print("  SQL查询:      python 快速查询.py sql")
    print()
