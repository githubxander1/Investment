#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库查看工具 - 快速预览SQLite数据库内容
"""

import sqlite3
import pandas as pd
from pathlib import Path

def view_database(db_path='db/t0_trading.db'):
    """查看数据库内容"""
    
    db_file = Path(db_path)
    if not db_file.exists():
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    print(f"📊 数据库路径: {db_file.absolute()}")
    print(f"📦 文件大小: {db_file.stat().st_size / 1024:.2f} KB\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. 查看所有表
    print("=" * 60)
    print("📋 数据库表列表")
    print("=" * 60)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table_name}: {count} 条记录")
    
    print()
    
    # 2. 查看分时数据详情
    print("=" * 60)
    print("📈 分时数据表 (每个股票每个日期一个表)")
    print("=" * 60)
    
    # 获取所有以stock_开头的表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name")
    stock_tables = cursor.fetchall()
    
    if stock_tables:
        print(f"\n找到 {len(stock_tables)} 个分时数据表:\n")
        for table in stock_tables:
            table_name = table[0]
            # 从表名解析信息 (stock_000333_date_20251024)
            parts = table_name.split('_')
            if len(parts) >= 4:
                stock_code = parts[1]
                date_str = parts[3]
                
                # 查询表中的数据统计
                cursor.execute(f"SELECT COUNT(*), MIN(datetime), MAX(datetime) FROM {table_name}")
                count, start_time, end_time = cursor.fetchone()
                
                print(f"  ✓ {stock_code} - {date_str}: {count} 条记录")
                print(f"    时间范围: {start_time} 至 {end_time}")
        
        # 显示最新的一个表的数据样例
        latest_table = stock_tables[-1][0]
        print("\n" + "-" * 60)
        print(f"数据样例 (表: {latest_table})")
        print("-" * 60)
        query_sample = f'''
            SELECT datetime, open, close, high, low, volume
            FROM {latest_table}
            ORDER BY datetime
            LIMIT 5
        '''
        df_sample = pd.read_sql_query(query_sample, conn)
        print(df_sample.to_string(index=False))
    else:
        print("  暂无分时数据")
    
    # 3. 查看交易信号
    print("\n" + "=" * 60)
    print("🔔 交易信号 (trading_signals)")
    print("=" * 60)
    
    cursor.execute("SELECT COUNT(*) FROM trading_signals")
    signal_count = cursor.fetchone()[0]
    
    if signal_count > 0:
        query_signals = """
            SELECT stock_code, datetime, indicator_name, signal_type, price, score
            FROM trading_signals
            ORDER BY datetime DESC
            LIMIT 10
        """
        df_signals = pd.read_sql_query(query_signals, conn)
        print(f"\n共 {signal_count} 个信号，最新10个:")
        print(df_signals.to_string(index=False))
    else:
        print("  暂无信号")
    
    # 4. 查看系统配置
    print("\n" + "=" * 60)
    print("⚙️ 系统配置 (system_config)")
    print("=" * 60)
    
    cursor.execute("SELECT COUNT(*) FROM system_config")
    config_count = cursor.fetchone()[0]
    
    if config_count > 0:
        query_config = "SELECT key, value, description FROM system_config"
        df_config = pd.read_sql_query(query_config, conn)
        print(df_config.to_string(index=False))
    else:
        print("  暂无配置")
    
    conn.close()
    print("\n" + "=" * 60)
    print("✅ 查看完成")
    print("=" * 60)


def query_stock_data(stock_code, date=None, db_path='db/t0_trading.db'):
    """查询特定股票的数据"""
    
    conn = sqlite3.connect(db_path)
    
    if date:
        query = f"""
            SELECT datetime, open, close, high, low, volume, amount, avg_price, change_pct
            FROM minute_data
            WHERE stock_code = '{stock_code}' 
              AND datetime LIKE '{date}%'
            ORDER BY datetime
        """
    else:
        query = f"""
            SELECT datetime, open, close, high, low, volume, amount, avg_price, change_pct
            FROM minute_data
            WHERE stock_code = '{stock_code}'
            ORDER BY datetime DESC
            LIMIT 50
        """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        print(f"\n📊 {stock_code} 的数据 (共 {len(df)} 条):\n")
        print(df.to_string(index=False))
    else:
        print(f"\n❌ 未找到 {stock_code} 的数据")


if __name__ == '__main__':
    import sys
    
    # 查看整个数据库
    print("\n" + "🔍 " * 20)
    print("SQLite 数据库查看工具")
    print("🔍 " * 20 + "\n")
    
    view_database()
    
    # 如果提供了股票代码，查询该股票的详细数据
    if len(sys.argv) > 1:
        stock_code = sys.argv[1]
        date = sys.argv[2] if len(sys.argv) > 2 else None
        print("\n" + "=" * 60)
        query_stock_data(stock_code, date)
        print("=" * 60)
    
    print("\n💡 使用提示:")
    print("  查看所有数据: python 查看数据库.py")
    print("  查看特定股票: python 查看数据库.py 000333")
    print("  查看特定日期: python 查看数据库.py 000333 2025-10-24")
    print()
