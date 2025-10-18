# Core strategy implementation for T0 trading system
import os
import sys
import pandas as pd
from datetime import datetime
import time

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from indicators.tdx_indicators import calculate_tdx_indicators, generate_trading_signals
from visualization.plotting import set_chinese_font, plot_indicators
from utils.helpers import create_directory, get_current_date_str
from data.data_processor import validate_data, preprocess_data, get_previous_close


class T0Strategy:
    """
    T0交易策略主类
    负责协调各个模块完成股票分析和信号生成
    """
    
    def __init__(self, stock_pool=None, refresh_interval=60, save_charts=True, notification_enabled=True):
        """
        初始化T0策略
        
        参数:
        stock_pool: 股票池列表，如果为None则使用默认股票池
        refresh_interval: 数据刷新间隔（秒）
        save_charts: 是否保存图表
        notification_enabled: 是否启用通知
        """
        # 导入配置
        from config.settings import DEFAULT_STOCK_POOL
        
        # 设置股票池
        self.stock_pool = stock_pool if stock_pool else DEFAULT_STOCK_POOL
        # 设置参数
        self.refresh_interval = refresh_interval
        self.save_charts = save_charts
        self.notification_enabled = notification_enabled
        
        # 初始化结果记录
        self.results = {}
        
        # 设置中文字体
        set_chinese_font()
        
        # 创建输出目录
        self.output_dir = os.path.join(project_root, 'output')
        create_directory(self.output_dir)
        
        print(f"T0策略初始化成功，股票池: {self.stock_pool}")
    
    def analyze_stock(self, stock_code):
        """
        分析单只股票
        
        参数:
        stock_code: 股票代码
        
        返回:
        dict: 分析结果
        """
        try:
            print(f"分析股票: {stock_code}")
            
            # 获取当前日期
            current_date = get_current_date_str()
            
            # 获取股票分时数据
            df = self._get_stock_data(stock_code)
            
            # 验证数据
            if not validate_data(df):
                print(f"股票{stock_code}数据无效")
                return None
            
            # 数据预处理
            df = preprocess_data(df)
            
            # 检查是否有NaN值
            if df.isnull().values.any():
                print("数据包含NaN值，进行填充处理")
                df = df.fillna(method='ffill').fillna(method='bfill')
            
            # 计算前一日收盘价
            prev_close = get_previous_close(stock_code, current_date)
            
            # 计算技术指标
            df = calculate_tdx_indicators(df, prev_close)
            
            # 生成交易信号
            signals = generate_trading_signals(df)
            
            # 保存结果
            result = {
                'stock_code': stock_code,
                'data': df,
                'prev_close': float(prev_close),
                'signals': signals
            }
            
            # 保存到结果字典
            self.results[stock_code] = result
            
            # 如果需要保存图表
            if self.save_charts:
                self._save_chart(stock_code, df, signals)
            
            return result
            
        except Exception as e:
            print(f"分析股票{stock_code}时出错: {e}")
            return None
    
    def _get_stock_data(self, stock_code):
        """
        获取股票数据
        
        参数:
        stock_code: 股票代码
        
        返回:
        DataFrame: 股票数据
        """
        from data.data_fetcher import get_stock_intraday_data
        return get_stock_intraday_data(stock_code)
    
    def _save_chart(self, stock_code, df, signals):
        """
        保存图表
        
        参数:
        stock_code: 股票代码
        df: 股票数据
        signals: 交易信号
        """
        try:
            # 生成图表文件路径
            from config.settings import CHARTS_DIR
            chart_filename = f"{stock_code}_{get_current_date_str()}.png"
            chart_path = os.path.join(CHARTS_DIR, chart_filename)
            
            # 绘制图表
            plot_indicators(df, signals, chart_path)
            
            print(f"图表已保存: {chart_path}")
            
        except Exception as e:
            print(f"保存图表时出错: {e}")
    
    def run(self):
        """
        运行策略，分析股票池中所有股票
        
        返回:
        dict: 所有股票的分析结果
        """
        print("开始运行T0策略...")
        
        for stock_code in self.stock_pool:
            self.analyze_stock(stock_code)
        
        print("策略运行完成")
        return self.results


if __name__ == "__main__":
    # 测试策略
    strategy = T0Strategy()
    results = strategy.run()
    print(f"分析了 {len(results)} 只股票")