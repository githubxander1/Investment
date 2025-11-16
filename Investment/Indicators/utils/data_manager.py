import pandas as pd
import numpy as np
import os
import akshare as ak
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DataManager:
    """统一的数据管理类，用于获取、存储和加载股票数据"""
    
    def __init__(self, data_dir="e:/git_documents/Investment/Investment/Indicators/Data"):
        self.data_dir = data_dir
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_data_file_path(self, stock_code, start_date, end_date):
        """获取数据文件路径"""
        filename = f"{stock_code}_{start_date}_{end_date}.csv"
        return os.path.join(self.data_dir, filename)
    
    def fetch_stock_data(self, stock_code, start_date, end_date, force_update=False):
        """
        获取股票数据，优先从本地缓存加载，如果没有则从网络获取并保存
        
        Parameters:
        stock_code (str): 股票代码
        start_date (str): 开始日期，格式'YYYYMMDD'
        end_date (str): 结束日期，格式'YYYYMMDD'
        force_update (bool): 是否强制从网络更新数据
        
        Returns:
        pd.DataFrame: 股票数据
        """
        file_path = self.get_data_file_path(stock_code, start_date, end_date)
        
        # 如果不强制更新且文件存在，直接加载本地数据
        if not force_update and os.path.exists(file_path):
            print(f"从本地缓存加载数据: {file_path}")
            try:
                df = pd.read_csv(file_path)
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                return df
            except Exception as e:
                print(f"读取本地数据失败: {e}")
        
        # 从网络获取数据
        print(f"正在从网络获取{stock_code}从{start_date}到{end_date}的数据...")
        df = self._fetch_from_akshare(stock_code, start_date, end_date)
        
        if df is not None and not df.empty:
            # 保存到本地
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"数据已保存到: {file_path}")
            return df
        else:
            print(f"获取{stock_code}数据失败")
            return None
    
    def _fetch_from_akshare(self, stock_code, start_date, end_date):
        """
        使用akshare获取股票数据
        
        Parameters:
        stock_code (str): 股票代码
        start_date (str): 开始日期，格式'YYYYMMDD'
        end_date (str): 结束日期，格式'YYYYMMDD'
        
        Returns:
        pd.DataFrame: 股票数据
        """
        try:
            # 尝试使用stock_zh_a_hist接口
            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", 
                                   start_date=start_date, end_date=end_date, 
                                   adjust="qfq")
            
            if df is not None and not df.empty:
                # 重新组织数据
                df.rename(columns={
                    '日期': 'date',
                    '开盘': 'open',
                    '最高': 'high',
                    '最低': 'low',
                    '收盘': 'close',
                    '成交量': 'volume'
                }, inplace=True)
                
                # 将日期转换为datetime类型
                df['date'] = pd.to_datetime(df['date'])
                
                # 按照日期排序
                df.sort_values('date', inplace=True)
                df.reset_index(drop=True, inplace=True)
                
                print(f"成功获取{stock_code}数据，共{len(df)}条记录")
                return df
        except Exception as e1:
            print(f"使用stock_zh_a_hist获取数据失败: {e1}")
            
            try:
                # 尝试使用stock_zh_a_daily接口
                df = ak.stock_zh_a_daily(symbol=stock_code, start_date=start_date, end_date=end_date)
                
                if df is not None and not df.empty:
                    # 创建结果DataFrame
                    result_df = pd.DataFrame()
                    result_df['date'] = pd.to_datetime(df.index) if isinstance(df.index, pd.DatetimeIndex) else pd.to_datetime(df['date'])
                    result_df['open'] = df['open']
                    result_df['high'] = df['high']
                    result_df['low'] = df['low']
                    result_df['close'] = df['close']
                    result_df['volume'] = df['volume']
                    
                    # 按照日期排序
                    result_df.sort_values('date', inplace=True)
                    result_df.reset_index(drop=True, inplace=True)
                    
                    print(f"成功获取{stock_code}数据，共{len(result_df)}条记录")
                    return result_df
            except Exception as e2:
                print(f"使用stock_zh_a_daily获取数据失败: {e2}")
        
        # 如果akshare获取失败，生成模拟数据
        print("生成模拟数据用于演示...")
        return self._generate_mock_data(stock_code, start_date, end_date)
    
    def _generate_mock_data(self, stock_code, start_date, end_date):
        """
        生成模拟数据用于演示
        
        Parameters:
        stock_code (str): 股票代码
        start_date (str): 开始日期，格式'YYYYMMDD'
        end_date (str): 结束日期，格式'YYYYMMDD'
        
        Returns:
        pd.DataFrame: 模拟股票数据
        """
        # 创建日期范围
        start_dt = datetime.strptime(start_date, '%Y%m%d')
        end_dt = datetime.strptime(end_date, '%Y%m%d')
        date_range = pd.date_range(start=start_dt, end=end_dt, freq='B')  # B表示工作日
        
        if len(date_range) == 0:
            return None
        
        # 设置随机种子以保证结果可复现
        np.random.seed(abs(hash(stock_code)) % (2**32))
        
        # 生成更真实的价格数据
        base_price = np.random.uniform(20, 50)  # 随机基础价格
        
        # 使用累加方式生成价格，而不是指数增长
        price_changes = np.random.normal(0, 0.02, len(date_range))
        
        # 添加一些更合理的趋势
        trend = np.linspace(0, np.random.uniform(-0.2, 0.3), len(date_range))  # 随机趋势
        
        # 添加季节性波动，使价格更有起伏
        seasonality = 0.05 * np.sin(np.linspace(0, 4 * np.pi, len(date_range)))
        
        # 使用线性累加方式生成收盘价
        cumulative_changes = np.cumsum(price_changes + trend + seasonality)
        close_prices = base_price * (1 + cumulative_changes)
        
        # 确保价格为正数
        close_prices = np.maximum(close_prices, 0.01)
        
        # 生成开盘价、最高价、最低价，确保价格合理
        open_prices = np.copy(close_prices)
        for i in range(1, len(close_prices)):
            open_prices[i] = close_prices[i-1] * (1 + np.random.normal(0, 0.01))
        
        # 确保开盘价是第一个元素
        open_prices[0] = close_prices[0] * (1 + np.random.normal(0, 0.01))
        
        # 计算最高价和最低价
        high_prices = np.maximum(open_prices, close_prices) * (1 + np.abs(np.random.uniform(0, 0.03, len(date_range))))
        low_prices = np.minimum(open_prices, close_prices) * (1 - np.abs(np.random.uniform(0, 0.03, len(date_range))))
        
        # 确保最高价和最低价合理
        high_prices = np.maximum(high_prices, np.maximum(open_prices, close_prices))
        low_prices = np.minimum(low_prices, np.minimum(open_prices, close_prices))
        
        # 生成成交量
        volumes = np.random.randint(1000000, 50000000, len(date_range))
        
        # 创建DataFrame
        df = pd.DataFrame({
            'date': date_range,
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices,
            'volume': volumes
        })
        
        return df


if __name__ == "__main__":
    # 测试数据管理器
    test_code = "000001.SZ"
    test_start = "20230101"
    test_end = "20251114"
    
    
    # 全局数据管理器实例
    data_manager = DataManager()

    def get_stock_data(stock_code, start_date, end_date, force_update=False):
        """
        获取股票数据的便捷函数
        
        Parameters:
        stock_code (str): 股票代码
        start_date (str): 开始日期，格式'YYYYMMDD'
        end_date (str): 结束日期，格式'YYYYMMDD'
        force_update (bool): 是否强制从网络更新数据
        
        Returns:
        pd.DataFrame: 股票数据
        """
        return data_manager.fetch_stock_data(stock_code, start_date, end_date, force_update)