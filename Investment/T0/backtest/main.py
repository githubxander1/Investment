import pandas as pd
import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .config import DEFAULT_BACKTEST_STOCKS, DEFAULT_START_DATE, DEFAULT_END_DATE
from .engine import BacktestEngine
from .data_loader import load_stock_data
from config.settings import DEFAULT_STOCK_POOL

def run_backtest(stocks=None, indicators=None, start_date=None, end_date=None):
    """
    运行T0回测
    
    Args:
        stocks: 股票列表，默认使用配置中的股票池
        indicators: 指标列表，默认包含所有指标
        start_date: 开始日期，默认使用配置中的日期
        end_date: 结束日期，默认使用配置中的日期
    """
    # 设置默认参数
    if stocks is None:
        stocks = DEFAULT_STOCK_POOL  # 使用T0系统默认股票池
    
    if indicators is None:
        indicators = ['resistance_support', 'extended', 'volume_price']
    
    if start_date is None:
        start_date = DEFAULT_START_DATE
    
    if end_date is None:
        end_date = DEFAULT_END_DATE
    
    # 创建回测引擎
    engine = BacktestEngine()
    
    print(f"开始T0回测...")
    print(f"股票池: {stocks}")
    print(f"指标: {indicators}")
    print(f"回测期间: {start_date} 到 {end_date}")
    print("-" * 50)
    
    # 对每个股票和每个指标进行回测
    for stock in stocks:
        print(f"\n正在回测股票: {stock}")
        
        # 加载数据
        print(f"  加载数据...")
        data = load_stock_data(stock, start_date, end_date)
        
        if data.empty:
            print(f"  ❌ 无法加载{stock}的数据，跳过")
            continue
        
        print(f"  ✅ 成功加载{len(data)}条数据")
        
        # 对每个指标进行回测
        for indicator in indicators:
            print(f"  正在测试指标: {indicator}")
            try:
                result = engine.run_backtest(stock, indicator, data, start_date, end_date)
                print(f"    初始资金: {result.initial_capital:.2f}")
                print(f"    最终资金: {result.final_capital:.2f}")
                print(f"    收益: {result.profit:.2f} ({result.profit_rate:.2f}%)")
                print(f"    交易次数: {result.total_trades}")
                print(f"    胜率: {result.win_rate:.2f}")
            except Exception as e:
                print(f"    ❌ 回测{indicator}时出错: {e}")
                import traceback
                traceback.print_exc()
    
    # 保存结果
    print("\n" + "="*50)
    print("保存回测结果...")
    engine.save_results()
    
    # 绘制结果图表
    print("绘制分析图表...")
    engine.plot_results()
    
    print("回测完成!")

if __name__ == "__main__":
    # 指定股票和日期范围
    run_backtest(
        # stocks=['000333', '600036'],
        stocks=['000333'],
        # indicators=['resistance_support', 'extended'],
        start_date='20250901',
        end_date='20250930'
    )