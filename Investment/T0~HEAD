import matplotlib
matplotlib.use('TkAgg')  # 使用TkAgg后端，适用于大多数环境
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os
import sys
import akshare as ak

# 导入各个模块
from indicators.tdx_indicators import calculate_tdx_indicators
from data.data_handler import get_prev_close, get_cached_data, save_data_to_cache, fetch_intraday_data, preprocess_intraday_data
from visualization.plotting import setup_matplotlib, create_intraday_plot
from utils.tools import is_trading_time, notify_signal, wait_until_trading_time


class T0Strategy:
    """T0交易策略主类"""
    def __init__(self, stock_codes=None):
        """初始化T0策略"""
        # 默认股票池
        self.stock_codes = stock_codes or ["601398", "600900", "601728"]  # 工商银行、长江电力、中国电信
        setup_matplotlib()
    
    def analyze_stock(self, stock_code, trade_date=None):
        """分析单只股票"""
        try:
            # 1. 时间处理
            today = datetime.now().strftime('%Y%m%d')
            trade_date = trade_date or today
    
            # 2. 先尝试从缓存获取数据
            df = get_cached_data(stock_code, trade_date)
    
            # 3. 如果缓存没有数据，则从网络获取
            if df is None:
                print(f"缓存中无{stock_code}数据，从网络获取...")
                df = fetch_intraday_data(stock_code, trade_date)
                if df is None:
                    return None
    
                # 保存到缓存
                save_data_to_cache(df.copy(), stock_code, trade_date)
                data_from_cache = False
            else:
                print(f"使用{stock_code}缓存数据")
                data_from_cache = True
    
            # 4. 预处理数据
            df = preprocess_intraday_data(df, trade_date)
            if df is None:
                return None
    
            # 5. 校准时间索引
            # 分离上午和下午的数据
            morning_data = df[df['时间'].dt.hour < 12]
            afternoon_data = df[df['时间'].dt.hour >= 13]
    
            # 强制校准时间索引
            morning_index = pd.date_range(
                start=f"{trade_date} 09:30:00",
                end=f"{trade_date} 11:30:00",
                freq='1min'
            )
            afternoon_index = pd.date_range(
                start=f"{trade_date} 13:00:00",
                end=f"{trade_date} 15:00:00",
                freq='1min'
            )
    
            # 合并索引
            full_index = morning_index.union(afternoon_index)
            df = df.set_index('时间').reindex(full_index)
            df.index.name = '时间'
    
            # 6. 获取昨收（fallback到开盘价）
            prev_close = get_prev_close(stock_code, trade_date)
            if prev_close is None:
                prev_close = df['开盘'].dropna().iloc[0]
                print(f"⚠️ 使用{stock_code}分时开盘价替代昨收: {prev_close:.2f}")
    
            # 7. 计算指标
            df = df.ffill().bfill()  # 填充缺失值
            df = calculate_tdx_indicators(df, prev_close)
    
            # 8. 计算均价
            df['均价'] = df['收盘'].expanding().mean()
    
            # 9. 数据校验
            required_cols = ['开盘', '收盘', '最高', '最低', '支撑', '阻力']
            if not all(col in df.columns for col in required_cols):
                missing_cols = [col for col in required_cols if col not in df.columns]
                print(f"❌ {stock_code}数据缺失关键列：{missing_cols}")
                return None
    
            if df['收盘'].isna().all():
                print(f"❌ {stock_code}收盘价全为空")
                return None
    
            # 10. 调试信息
            print(f"✅ {stock_code}过滤后数据概览：")
            print(df[['开盘', '收盘', '最高', '最低']].head())
            print(f"数据时间范围：{df.index.min()} ~ {df.index.max()}")
            print(f"有效数据量：{len(df)} 条")
    
            # 11. 创建图表
            fig = create_intraday_plot(df, stock_code, trade_date, prev_close, notify_signal)
            if fig:
                # 强制显示（解决后端静默问题）
                plt.show(block=False)
                plt.pause(0.1)  # 给图表绘制留出时间
    
            # 12. 保存分析结果到CSV
            result_dir = "analysis_results"
            os.makedirs(result_dir, exist_ok=True)
            result_file = os.path.join(result_dir, f"{stock_code}_{trade_date}_analysis.csv")
            df.to_csv(result_file)
            print(f"分析结果已保存到：{result_file}")
    
            return df
        except Exception as e:
            print(f"❌ {stock_code}分析错误: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def run(self):
        """运行T0策略"""
        try:
            print("===== T0策略开始运行 =====")
            print(f"监控股票池: {self.stock_codes}")
            
            while True:
                # 检查是否在交易时间内
                if is_trading_time():
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 开始分析股票池...")
                    
                    # 分析所有股票
                    for stock_code in self.stock_codes:
                        print(f"\n----- 分析股票: {stock_code} -----")
                        self.analyze_stock(stock_code)
                    
                    # 交易时间内每分钟运行一次
                    print(f"\n等待1分钟后再次分析...")
                    time.sleep(60)
                else:
                    # 非交易时间，等待
                    wait_until_trading_time()
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        except Exception as e:
            print(f"程序运行错误: {e}")
        finally:
            print("\n===== T0策略结束运行 =====")

# 添加缺失的导入
try:
    import pandas as pd
except ImportError:
    pass

try:
    import numpy as np
except ImportError:
    pass

# 确保这个导入在pd和np之后
try:
    from datetime import timedelta
except ImportError:
    pass


if __name__ == "__main__":
    # 可以从命令行参数获取股票代码
    stock_codes = None
    if len(sys.argv) > 1:
        stock_codes = sys.argv[1:]
        
    # 初始化并运行策略
    strategy = T0Strategy(stock_codes)
    strategy.run()