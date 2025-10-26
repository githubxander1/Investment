#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据管理模块 - 基于SQLite的高效数据存储和查询

功能：
1. 分时数据的CRUD操作
2. 交易信号的存储和查询
3. CSV数据迁移
4. 数据验证和完整性检查
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import logging
import json

logger = logging.getLogger(__name__)


class DataManager:
    """数据管理器 - 封装SQLite操作"""
    
    def __init__(self, db_path: str = None):
        """
        初始化数据管理器
        
        Args:
            db_path: 数据库文件路径，默认为项目根目录下的db/t0_trading.db
        """
        if db_path is None:
            project_root = Path(__file__).parent.parent
            db_dir = project_root / 'db'
            db_dir.mkdir(exist_ok=True)
            db_path = str(db_dir / 't0_trading.db')
        
        self.db_path = db_path
        self.conn = None
        self._init_database()
        logger.info(f"数据管理器初始化完成，数据库路径: {self.db_path}")
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 注意：分时数据不再使用统一的表，而是为每个股票每个日期创建独立的表
        # 表名格式: {stock_code}_{date}，例如: 000333_20251024
        # 这样做的好处：
        # 1. 查询速度更快（不需要WHERE条件过滤）
        # 2. 数据隔离性好
        # 3. 便于按日期删除数据（直接DROP表）
        
        # 创建交易信号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                datetime TEXT NOT NULL,
                indicator_name TEXT NOT NULL,
                signal_type TEXT NOT NULL CHECK(signal_type IN ('BUY', 'SELL')),
                price REAL NOT NULL,
                score REAL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_signal_stock_datetime 
            ON trading_signals(stock_code, datetime)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_signal_indicator 
            ON trading_signals(indicator_name)
        ''')
        
        # 创建系统配置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        logger.info("数据库表结构初始化完成")
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接（单例模式）"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
        return self.conn
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("数据库连接已关闭")
    
    # ==================== 分时数据操作 ====================
    
    def _get_table_name(self, stock_code: str, trade_date: str) -> str:
        """
        生成表名
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期 (YYYY-MM-DD 或 YYYYMMDD)
            
        Returns:
            表名，格式: stock_code_date_YYYYMMDD
        """
        # 统一日期格式为YYYYMMDD
        date_str = trade_date.replace('-', '').replace('/', '')
        # 表名前缀加stock_避免数字开头
        return f"stock_{stock_code}_date_{date_str}"
    
    def _create_minute_table(self, table_name: str):
        """
        创建分时数据表
        
        Args:
            table_name: 表名
        """
        conn = self._get_connection()
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
        
        # 创建时间索引
        cursor.execute(f'''
            CREATE INDEX IF NOT EXISTS idx_{table_name}_datetime 
            ON {table_name}(datetime)
        ''')
        
        conn.commit()
        logger.info(f"创建表: {table_name}")
    
    def save_minute_data(self, df: pd.DataFrame, stock_code: str, trade_date: str = None) -> int:
        """
        保存分时数据到独立表
        
        Args:
            df: 分时数据DataFrame，必须包含列：时间, 开盘, 收盘, 最高, 最低, 成交量, 成交额
            stock_code: 股票代码
            trade_date: 交易日期，如果为None则从数据中提取
            
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
                logger.error("无法确定交易日期，且数据中缺少'时间'列")
                return 0
        
        # 生成表名并创建表
        table_name = self._get_table_name(stock_code, trade_date)
        self._create_minute_table(table_name)
        
        conn = self._get_connection()
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
                logger.error("数据中缺少'时间'列")
                continue
            
            # 计算均价（如果没有）
            avg_price = row.get('均价', None)
            if avg_price is None or pd.isna(avg_price):
                volume = row.get('成交量', 0)
                amount = row.get('成交额', 0)
                avg_price = amount / volume if volume > 0 else row.get('收盘', 0)
            
            # 计算涨跌幅（如果没有）
            change_pct = row.get('涨跌幅', None)
            if change_pct is None or pd.isna(change_pct):
                change_pct = 0  # 默认值，实际应该基于前一日收盘价计算
            
            record = (
                stock_code,
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
        
        # 批量插入（使用 INSERT OR REPLACE 避免重复）
        try:
            cursor.executemany(f'''
                INSERT OR REPLACE INTO {table_name} 
                (datetime, open, close, high, low, volume, amount, avg_price, change_pct)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', [(r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]) for r in records])
            conn.commit()
            logger.info(f"成功保存 {len(records)} 条分时数据到表: {table_name}")
            return len(records)
        except sqlite3.Error as e:
            logger.error(f"保存分时数据失败: {e}")
            conn.rollback()
            return 0
    
    def get_minute_data(self, stock_code: str, trade_date: str) -> pd.DataFrame:
        """
        查询指定日期的分时数据
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期（YYYY-MM-DD 或 YYYYMMDD）
            
        Returns:
            分时数据DataFrame
        """
        table_name = self._get_table_name(stock_code, trade_date)
        conn = self._get_connection()
        
        try:
            # 检查表是否存在
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if not cursor.fetchone():
                logger.warning(f"表不存在: {table_name}")
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
                logger.info(f"查询到 {len(df)} 条分时数据: {table_name}")
            else:
                logger.warning(f"表 {table_name} 中没有数据")
            
            return df
        except Exception as e:
            logger.error(f"查询分时数据失败: {e}")
            return pd.DataFrame()
    
    def delete_minute_data(self, stock_code: str, start_date: str = None, 
                          end_date: str = None) -> int:
        """
        删除分时数据
        
        Args:
            stock_code: 股票代码
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
            
        Returns:
            删除的记录数
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = 'DELETE FROM minute_data WHERE stock_code = ?'
        params = [stock_code]
        
        if start_date:
            query += ' AND datetime >= ?'
            params.append(f"{start_date} 00:00:00")
        
        if end_date:
            query += ' AND datetime <= ?'
            params.append(f"{end_date} 23:59:59")
        
        try:
            cursor.execute(query, params)
            deleted_count = cursor.rowcount
            conn.commit()
            logger.info(f"删除了 {deleted_count} 条分时数据: {stock_code}")
            return deleted_count
        except sqlite3.Error as e:
            logger.error(f"删除分时数据失败: {e}")
            conn.rollback()
            return 0
    
    # ==================== 交易信号操作 ====================
    
    def save_signals(self, signals: List[Dict]) -> int:
        """
        保存交易信号
        
        Args:
            signals: 信号列表，每个信号是字典：
                {
                    'stock_code': str,
                    'datetime': str,
                    'indicator_name': str,
                    'signal_type': str,  # 'BUY' or 'SELL'
                    'price': float,
                    'score': float,
                    'metadata': dict  # 可选
                }
                
        Returns:
            插入的记录数
        """
        if not signals:
            return 0
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
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
            logger.error(f"保存交易信号失败: {e}")
            conn.rollback()
            return 0
    
    def get_signals(self, stock_code: str = None, indicator_name: str = None,
                   start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        查询交易信号
        
        Args:
            stock_code: 股票代码
            indicator_name: 指标名称
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            信号DataFrame
        """
        conn = self._get_connection()
        
        query = 'SELECT * FROM trading_signals WHERE 1=1'
        params = []
        
        if stock_code:
            query += ' AND stock_code = ?'
            params.append(stock_code)
        
        if indicator_name:
            query += ' AND indicator_name = ?'
            params.append(indicator_name)
        
        if start_date:
            query += ' AND datetime >= ?'
            params.append(f"{start_date} 00:00:00")
        
        if end_date:
            query += ' AND datetime <= ?'
            params.append(f"{end_date} 23:59:59")
        
        query += ' ORDER BY datetime ASC'
        
        try:
            df = pd.read_sql_query(query, conn, params=params)
            
            if not df.empty:
                df['datetime'] = pd.to_datetime(df['datetime'])
                # 解析metadata JSON
                df['metadata'] = df['metadata'].apply(lambda x: json.loads(x) if x else {})
            
            return df
        except sqlite3.Error as e:
            logger.error(f"查询交易信号失败: {e}")
            return pd.DataFrame()
    
    # ==================== CSV数据迁移 ====================
    
    def import_from_csv(self, csv_path: str, stock_code: str, trade_date: str = None) -> bool:
        """
        从CSV文件导入分时数据
        
        Args:
            csv_path: CSV文件路径
            stock_code: 股票代码
            trade_date: 交易日期，如果为None则从文件名提取
            
        Returns:
            是否成功
        """
        try:
            # 检查文件是否存在
            csv_file = Path(csv_path)
            if not csv_file.exists():
                logger.error(f"CSV文件不存在: {csv_path}")
                return False
            
            df = pd.read_csv(csv_path)
            logger.info(f"从CSV读取 {len(df)} 条记录: {csv_path}")
            
            # 处理时间列
            if '时间' in df.columns:
                df['时间'] = pd.to_datetime(df['时间'])
                
                # 如果没有指定交易日期，从文件名提取 (000333_20251024_fenshi.csv)
                if trade_date is None:
                    filename = Path(csv_path).stem
                    parts = filename.split('_')
                    if len(parts) >= 2:
                        trade_date = parts[1]  # 20251024
                    else:
                        # 从数据中提取
                        trade_date = df['时间'].iloc[0].strftime('%Y%m%d')
            
            count = self.save_minute_data(df, stock_code, trade_date)
            logger.info(f"成功导入 {count} 条记录到数据库")
            return count > 0
        except FileNotFoundError as e:
            logger.error(f"文件未找到: {csv_path}，错误: {e}")
            return False
        except Exception as e:
            logger.error(f"从CSV导入失败: {csv_path}，错误: {e}")
            return False
    
    def export_to_csv(self, stock_code: str, output_path: str, 
                     start_date: str = None, end_date: str = None) -> bool:
        """
        导出分时数据到CSV
        
        Args:
            stock_code: 股票代码
            output_path: 输出文件路径
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            是否成功
        """
        try:
            df = self.get_minute_data(stock_code, start_date, end_date)
            if df.empty:
                logger.warning(f"没有数据可导出: {stock_code}")
                return False
            
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            logger.info(f"成功导出 {len(df)} 条记录到CSV: {output_path}")
            return True
        except Exception as e:
            logger.error(f"导出到CSV失败: {e}")
            return False
    
    def batch_import_from_cache(self, cache_dir: str, stock_codes: List[str] = None) -> Dict[str, int]:
        """
        批量从缓存目录导入CSV文件
        
        Args:
            cache_dir: 缓存目录路径（如: ../T0/cache/fenshi_data）
            stock_codes: 股票代码列表，None表示导入所有
            
        Returns:
            导入结果字典 {stock_code: count}
        """
        cache_path = Path(cache_dir)
        
        # 检查目录是否存在
        if not cache_path.exists():
            abs_path = cache_path.absolute()
            logger.error(f"缓存目录不存在: {cache_dir}")
            logger.error(f"绝对路径: {abs_path}")
            logger.info(f"提示：如果从T0_Optimized运行，应使用 '../T0/cache/fenshi_data'")
            return {}
        
        # 检查是否有CSV文件
        csv_files = list(cache_path.glob('*.csv'))
        if not csv_files:
            logger.warning(f"在目录 {cache_dir} 中未找到CSV文件")
            return {}
        
        logger.info(f"在 {cache_dir} 中找到 {len(csv_files)} 个CSV文件")
        
        results = {}
        
        for csv_file in csv_files:
            # 从文件名提取股票代码（格式: 000333_20251024_fenshi.csv）
            filename = csv_file.stem
            parts = filename.split('_')
            if len(parts) >= 1:
                stock_code = parts[0]
                
                # 过滤股票代码
                if stock_codes and stock_code not in stock_codes:
                    continue
                
                logger.info(f"正在导入: {csv_file.name}")
                success = self.import_from_csv(str(csv_file), stock_code)
                
                if success:
                    # 从文件名提取日期 (000333_20251024_fenshi.csv)
                    if len(parts) >= 2:
                        date_str = parts[1]
                    else:
                        date_str = datetime.now().strftime('%Y%m%d')
                    
                    # 统计导入数量
                    df = self.get_minute_data(stock_code, date_str)
                    results[f"{stock_code}_{date_str}"] = len(df)
        
        if results:
            logger.info(f"批量导入完成，共导入 {len(results)} 个股票的数据")
        else:
            logger.warning(f"未成功导入任何数据")
        
        return results
    
    # ==================== 配置操作 ====================
    
    def set_config(self, key: str, value: str, description: str = None):
        """设置配置项"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO system_config (key, value, description)
                VALUES (?, ?, ?)
            ''', (key, value, description))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"设置配置失败: {e}")
            conn.rollback()
    
    def get_config(self, key: str, default: str = None) -> Optional[str]:
        """获取配置项"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT value FROM system_config WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result['value'] if result else default
        except sqlite3.Error as e:
            logger.error(f"获取配置失败: {e}")
            return default


# ==================== 使用示例 ====================

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 创建数据管理器
    dm = DataManager()
    
    # 自动检测缓存目录（使用T0_Optimized本地缓存）
    from pathlib import Path
    
    # 使用本地缓存目录
    project_root = Path(__file__).parent.parent
    cache_dir = project_root / 'cache' / 'fenshi_data'
    
    if not cache_dir.exists():
        logger.error(f"缓存目录不存在: {cache_dir}")
        logger.error("请确保已将分时数据CSV文件放在 cache/fenshi_data/ 目录下")
        dm.close()
        sys.exit(1)
    
    logger.info(f"使用缓存目录: {cache_dir}")
    
    # 从缓存导入数据（使用T0_Optimized本地缓存）
    results = dm.batch_import_from_cache(str(cache_dir), stock_codes=['000333', '600030', '002415'])
    print(f"\n导入结果: {results}")
    
    # 查询数据 - 注意现在需要指定日期
    df = dm.get_minute_data('000333', '2025-10-24')
    print(f"\n查询到 {len(df)} 条数据")
    if not df.empty:
        print(df.head())
    
    # 关闭连接
    dm.close()
