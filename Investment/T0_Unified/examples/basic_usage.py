"""
T0统一交易策略系统的基本使用示例
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import T0Strategy


def example1_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建T0策略实例
    strategy = T0Strategy()
    
    # 运行策略
    # strategy.run()  # 取消注释以实际运行


def example2_custom_stock_pool():
    """自定义股票池示例"""
    print("\n=== 自定义股票池示例 ===")
    
    # 创建自定义股票池的策略实例
    strategy = T0Strategy(
        stock_pool=['600036', '600519', '000002'],  # 招商银行、贵州茅台、万科A
        refresh_interval=30,  # 30秒刷新一次
        save_charts=True,     # 保存图表
        notification_enabled=True  # 启用通知
    )
    
    print(f"自定义股票池: {strategy.stock_pool}")
    print(f"刷新间隔: {strategy.refresh_interval}秒")


def example3_single_stock_analysis():
    """单只股票分析示例"""
    print("\n=== 单只股票分析示例 ===")
    
    # 创建策略实例
    strategy = T0Strategy(save_charts=True)
    
    # 分析单只股票
    result = strategy.analyze_stock('600519')  # 贵州茅台
    
    # 查看分析结果
    if result:
        print(f"股票代码: {result['stock_code']}")
        print(f"最新价格: {result['data'].iloc[-1]['收盘']}")
        print(f"买入信号数量: {len(result['signals']['buy_signals'])}")
        print(f"卖出信号数量: {len(result['signals']['sell_signals'])}")


def example4_manual_analysis():
    """手动分析示例"""
    print("\n=== 手动分析示例 ===")
    
    # 使用兼容接口进行手动分析
    from src.main import plot_tdx_intraday
    
    # 分析指定股票和日期
    # result_df = plot_tdx_intraday('600519', '20250926')  # 贵州茅台，2025年9月26日
    print("手动分析完成")


if __name__ == '__main__':
    # 运行所有示例
    example1_basic_usage()
    example2_custom_stock_pool()
    example3_single_stock_analysis()
    example4_manual_analysis()
    
    print("\n所有示例运行完成！")