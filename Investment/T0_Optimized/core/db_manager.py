#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库管理器 - 优化的分层存储结构

目录结构：
db/
├── stocks/{stock_code}/{year}/{YYYYMM}.db  # 按月分库
├── signals/signals.db                       # 交易信号
├── config/system_config.db                  # 系统配置
└── archive/{year}/                          # 归档数据
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import logging
import json

logger = logging.getLogger(__name__)


class DBManager:
    """优化的数据库管理器 - 分层存储"""
    
    def __init__(self, base_dir: str = None):
        """
        初始化数据库管理器
        
        Args:
            base_dir: 数据库根目录，默认为项目根目录下的db
        """
        if base_dir is None:
            project_root = Path(__file__).parent.parent
            base_dir = str(project_root / 'db')
        
        self.base_dir = Path(base_dir)
        self._init_directory_structure()
        self.connections = {}  # 连接池
        
        logger.info(f"数据库管理器初始化完成，根目录: {self.base_dir}")
    
    def _init_directory_structure(self):
        """初始化目录结构"""
        # 创建主要目录
        (self.base_dir / 'stocks').mkdir(parents=True, exist_ok=True)
        (self.base_dir / 'signals').mkdir(parents=True, exist_ok=True)
        (self.base_dir / 'config').mkdir(parents=True, exist_ok=True)
        (self.base_dir / 'archive').mkdir(parents=True, exist_ok=True)
        
        logger.info("数据库目录结构初始化完成")
    
    def _get_stock_db_path(self, stock_code: str, trade_date: str) -> Path:
        """
        获取股票数据库文件路径
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期 (YYYY-MM-DD 或 YYYYMMDD)
        
        Returns:
            数据库文件路径
        """
        # 解析日期
        date_str = trade_date.replace('-', '').replace('/', '')
        year = date_str[:4]
        month = date_str[:6]  # YYYYMM
        
        # 构建路径: db/stocks/000333/2025/202510.db
        db_path = self.base_dir / 'stocks' / stock_code / year / f"{month}.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        return db_path
    
    def _get_table_name(self, trade_date: str) -> str:
        """
        生成表名（按日期）
        
        Args:
            trade_date: 交易日期
        
        Returns:
            表名，格式: day_YYYYMMDD
        """
        date_str = trade_date.replace('-', '').replace('/', '')
        return f"day_{date_str}"
    
    def _get_connection(self, db_path: Path) -> sqlite3.Connection:
        """
        获取数据库连接（连接池）
        
        Args:
            db_path: 数据库文件路径
        
        Returns:
            数据库连接
        """
        db_key = str(db_path)
        
        if db_key not in self.connections or self.connections[db_key] is None:
            self.connections[db_key] = sqlite3.connect(
                db_path, 
                check_same_thread=False
            )
            self.connections[db_key].row_factory = sqlite3.Row
        
        return self.connections[db_key]
    
    def _create_minute_table(self, conn: sqlite3.Connection, table_name: str):
        """
        创建分时数据表
        
        Args:
            conn: 数据库连接
            table_name: 表名
        """
        cursor = conn.cursor()
        
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL UNIQUE,
                open REAL NOT NULL,
                close REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                volume INTEGER NOT NULL,
                amount REAL NOT NULL,
                avg_price REAL,
                change_pct REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        cursor.execute(f'''
            CREATE INDEX IF NOT EXISTS idx_{table_name}_datetime 
            ON {table_name}(datetime)
        ''')
        
        conn.commit()
    
    # ==================== 分时数据操作 ====================
    
    def save_minute_data(self, df: pd.DataFrame, stock_code: str, trade_date: str = None) -> int:
        """
        保存分时数据
        
        Args:
            df: 分时数据DataFrame
            stock_code: 股票代码
            trade_date: 交易日期
        
        Returns:
            插入的记录数
        """
        if df.empty:
            logger.warning(f"尝试保存空数据: {stock_code}")
            return 0
        
        # 如果没有指定交易日期，从数据中提取
        if trade_date is None:
            if '时间' in df.columns:
                first_time = df['时间'].iloc[0]
                if isinstance(first_time, str):
                    trade_date = pd.to_datetime(first_time).strftime('%Y%m%d')
                else:
                    trade_date = first_time.strftime('%Y%m%d')
            else:
                logger.error("无法确定交易日期")
                return 0
        
        # 获取数据库路径和表名
        db_path = self._get_stock_db_path(stock_code, trade_date)
        table_name = self._get_table_name(trade_date)
        
        # 获取连接并创建表
        conn = self._get_connection(db_path)
        self._create_minute_table(conn, table_name)
        
        cursor = conn.cursor()
        
        # 准备数据
        records = []
        for _, row in df.iterrows():
            # 处理时间格式
            if '时间' in row:
                dt = row['时间']
                if isinstance(dt, str):
                    dt = pd.to_datetime(dt)
                datetime_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                continue
            
            # 计算均价（如果没有）
            avg_price = row.get('均价', None)
            if avg_price is None or pd.isna(avg_price):
                volume = row.get('成交量', 0)
                amount = row.get('成交额', 0)
                avg_price = amount / volume if volume > 0 else row.get('收盘', 0)
            
            # 计算涨跌幅（如果没有）
            change_pct = row.get('涨跌幅', 0)
            if pd.isna(change_pct):
                change_pct = 0
            
            record = (
                datetime_str,
                float(row.get('开盘', 0)),
                float(row.get('收盘', 0)),
                float(row.get('最高', 0)),
                float(row.get('最低', 0)),
                int(row.get('成交量', 0)),
                float(row.get('成交额', 0)),
                float(avg_price),
                float(change_pct)
            )
            records.append(record)
        
        if not records:
            logger.warning(f"没有有效的数据记录: {stock_code}")
            return 0
        
        # 批量插入
        try:
            cursor.executemany(f'''
                INSERT OR REPLACE INTO {table_name} 
                (datetime, open, close, high, low, volume, amount, avg_price, change_pct)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', records)
            conn.commit()
            logger.info(f"成功保存 {len(records)} 条数据: {stock_code} {trade_date} -> {db_path.name}/{table_name}")
            return len(records)
        except sqlite3.Error as e:
            logger.error(f"保存数据失败: {e}")
            conn.rollback()
            return 0
    
    def get_minute_data(self, stock_code: str, trade_date: str) -> pd.DataFrame:
        """
        查询分时数据
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期
        
        Returns:
            分时数据DataFrame
        """
        db_path = self._get_stock_db_path(stock_code, trade_date)
        table_name = self._get_table_name(trade_date)
        
        # 检查数据库文件是否存在
        if not db_path.exists():
            logger.warning(f"数据库文件不存在: {db_path}")
            return pd.DataFrame()
        
        try:
            conn = self._get_connection(db_path)
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if not cursor.fetchone():
                logger.warning(f"表不存在: {table_name} in {db_path.name}")
                return pd.DataFrame()
            
            # 查询数据
            query = f'''
                SELECT datetime, open, close, high, low, volume, amount, avg_price, change_pct
                FROM {table_name}
                ORDER BY datetime
            '''
            
            df = pd.read_sql_query(query, conn)
            
            if not df.empty:
                # 转换时间列并重命名
                df['datetime'] = pd.to_datetime(df['datetime'])
                df = df.rename(columns={
                    'datetime': '时间',
                    'open': '开盘',
                    'close': '收盘',
                    'high': '最高',
                    'low': '最低',
                    'volume': '成交量',
                    'amount': '成交额',
                    'avg_price': '均价',
                    'change_pct': '涨跌幅'
                })
                logger.info(f"查询到 {len(df)} 条数据: {stock_code} {trade_date}")
            
            return df
        except Exception as e:
            logger.error(f"查询数据失败: {e}")
            return pd.DataFrame()
    
    def get_month_data(self, stock_code: str, year_month: str) -> pd.DataFrame:
        """
        查询整月数据
        
        Args:
            stock_code: 股票代码
            year_month: 年月 (YYYYMM 或 YYYY-MM)
        
        Returns:
            合并后的DataFrame
        """
        year_month = year_month.replace('-', '')
        year = year_month[:4]
        
        db_path = self.base_dir / 'stocks' / stock_code / year / f"{year_month}.db"
        
        if not db_path.exists():
            logger.warning(f"月度数据库不存在: {db_path}")
            return pd.DataFrame()
        
        try:
            conn = self._get_connection(db_path)
            cursor = conn.cursor()
            
            # 获取该月所有表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'day_%'")
            tables = cursor.fetchall()
            
            if not tables:
                return pd.DataFrame()
            
            # 合并所有表的数据
            all_data = []
            for table in tables:
                table_name = table[0]
                query = f"SELECT * FROM {table_name} ORDER BY datetime"
                df = pd.read_sql_query(query, conn)
                if not df.empty:
                    all_data.append(df)
            
            if all_data:
                combined_df = pd.concat(all_data, ignore_index=True)
                logger.info(f"查询到 {len(combined_df)} 条月度数据: {stock_code} {year_month}")
                return combined_df
            else:
                return pd.DataFrame()
        
        except Exception as e:
            logger.error(f"查询月度数据失败: {e}")
            return pd.DataFrame()
    
    # ==================== 信号数据操作 ====================
    
    def save_signals(self, signals: List[Dict]) -> int:
        """保存交易信号到signals数据库"""
        if not signals:
            return 0
        
        signals_db = self.base_dir / 'signals' / 'signals.db'
        conn = self._get_connection(signals_db)
        cursor = conn.cursor()
        
        # 创建信号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                datetime TEXT NOT NULL,
                indicator_name TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                price REAL NOT NULL,
                score REAL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 插入信号
        records = []
        for signal in signals:
            metadata_json = json.dumps(signal.get('metadata', {}), ensure_ascii=False)
            record = (
                signal['stock_code'],
                signal['datetime'],
                signal['indicator_name'],
                signal['signal_type'].upper(),
                float(signal['price']),
                float(signal.get('score', 0)),
                metadata_json
            )
            records.append(record)
        
        try:
            cursor.executemany('''
                INSERT INTO trading_signals 
                (stock_code, datetime, indicator_name, signal_type, price, score, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', records)
            conn.commit()
            logger.info(f"成功保存 {len(records)} 个交易信号")
            return len(records)
        except sqlite3.Error as e:
            logger.error(f"保存信号失败: {e}")
            conn.rollback()
            return 0
    
    # ==================== 工具方法 ====================
    
    def get_database_stats(self) -> Dict:
        """获取数据库统计信息"""
        stats = {
            'stocks': {},
            'total_files': 0,
            'total_size_mb': 0
        }
        
        stocks_dir = self.base_dir / 'stocks'
        if stocks_dir.exists():
            for stock_dir in stocks_dir.iterdir():
                if stock_dir.is_dir():
                    stock_code = stock_dir.name
                    stock_stats = {
                        'files': 0,
                        'size_mb': 0,
                        'months': []
                    }
                    
                    for db_file in stock_dir.rglob('*.db'):
                        stock_stats['files'] += 1
                        size = db_file.stat().st_size / (1024 * 1024)
                        stock_stats['size_mb'] += size
                        stats['total_size_mb'] += size
                        stock_stats['months'].append(db_file.stem)
                    
                    stats['total_files'] += stock_stats['files']
                    stats['stocks'][stock_code] = stock_stats
        
        return stats
    
    def close_all(self):
        """关闭所有数据库连接"""
        for db_key, conn in self.connections.items():
            if conn:
                conn.close()
                logger.debug(f"关闭连接: {db_key}")
        
        self.connections.clear()
        logger.info("所有数据库连接已关闭")


# ==================== 使用示例 ====================

if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 创建数据库管理器
    db_mgr = DBManager()
    
    # 测试保存和查询
    print("\n测试分层数据库结构...\n")
    
    # 从本地缓存导入数据
    from pathlib import Path
    import pandas as pd
    
    project_root = Path(__file__).parent.parent
    cache_dir = project_root / 'cache' / 'fenshi_data'
    
    if not cache_dir.exists():
        print(f"❗ 缓存目录不存在: {cache_dir}")
        print("请将CSV数据文件放在 cache/fenshi_data/ 目录下")
        db_mgr.close_all()
        sys.exit(1)
    
    # 读取并导入CSV文件
    for csv_file in cache_dir.glob('*.csv'):
        # 解析文件名: 000333_20251024_fenshi.csv
        parts = csv_file.stem.split('_')
        if len(parts) >= 2:
            stock_code = parts[0]
            trade_date = parts[1]  # 20251024
            
            # 读取CSV
            df = pd.read_csv(csv_file)
            
            # 保存到新的分层结构
            count = db_mgr.save_minute_data(df, stock_code, trade_date)
            print(f"✅ {stock_code}: 保存 {count} 条记录")
    
    # 查询数据
    print("\n查询测试:")
    df = db_mgr.get_minute_data('000333', '2025-10-24')
    print(f"查询到 {len(df)} 条记录")
    print(df.head())
    
    # 获取统计信息
    print("\n数据库统计:")
    stats = db_mgr.get_database_stats()
    print(f"总文件数: {stats['total_files']}")
    print(f"总大小: {stats['total_size_mb']:.2f} MB")
    for stock_code, stock_stats in stats['stocks'].items():
        print(f"\n{stock_code}:")
        print(f"  文件数: {stock_stats['files']}")
        print(f"  大小: {stock_stats['size_mb']:.2f} MB")
        print(f"  月份: {', '.join(stock_stats['months'])}")
    
    # 关闭所有连接
    db_mgr.close_all()
