import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List
import akshare as ak
import matplotlib.font_manager as fm

from Investment.T0.utils.logger import setup_logger

logger = setup_logger('momentum_reversal')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def calculate_momentum_reversal(df: pd.DataFrame, momentum_window: int = 10, reversal_threshold: float = 0.5) -> pd.DataFrame:
    """
    计算动量反转策略指标
    
    策略逻辑：
    1. 计算短期动量（价格变化率）
    2. 当动量过大时，预期会发生反转
    3. 正动量过大时卖出，负动量过大时买入
    
    Args:
        df: 包含价格数据的DataFrame
        momentum_window: 动量计算窗口
        reversal_threshold: 反转阈值（百分比）
    
    Returns:
        添加了策略指标的DataFrame
    """
    df = df.copy()
    
    # 计算价格变化率（动量指标）
    df['Price_Change'] = df['收盘'].pct_change(periods=momentum_window) * 100
    
    # 计算动量的平均值和标准差，用于动态阈值
    df['Momentum_Mean'] = df['Price_Change'].rolling(window=momentum_window*3, min_periods=1).mean()
    df['Momentum_Std'] = df['Price_Change'].rolling(window=momentum_window*3, min_periods=1).std()
    
    # 动态阈值
    df['Upper_Threshold'] = df['Momentum_Mean'] + reversal_threshold
    df['Lower_Threshold'] = df['Momentum_Mean'] - reversal_threshold
    
    # 生成买卖信号
    # 买入信号：当价格变化率低于下阈值时（超卖）
    df['Buy_Signal'] = (df['Price_Change'] <= df['Lower_Threshold']) & (df['Price_Change'].shift(1) > df['Lower_Threshold'].shift(1))
    
    # 卖出信号：当价格变化率高于上阈值时（超买）
    df['Sell_Signal'] = (df['Price_Change'] >= df['Upper_Threshold']) & (df['Price_Change'].shift(1) < df['Upper_Threshold'].shift(1))
    
    # 记录所有信号
    buy_signals = df[df['Buy_Signal']]
    sell_signals = df[df['Sell_Signal']]
    
    print(f"动量反转策略：共检测到 {len(buy_signals)} 个买入信号和 {len(sell_signals)} 个卖出信号")
    
    for idx, row in buy_signals.iterrows():
        buy_time = row['时间'] if '时间' in df.columns else idx
        buy_price = row['收盘']
        buy_change = row['Price_Change']
        print(f"动量反转策略：买入信号时间点: {buy_time}, 价格: {buy_price:.2f}, 价格变化率: {buy_change:.2f}%")
    
    for idx, row in sell_signals.iterrows():
        sell_time = row['时间'] if '时间' in df.columns else idx
        sell_price = row['收盘']
        sell_change = row['Price_Change']
        print(f"动量反转策略：卖出信号时间点: {sell_time}, 价格: {sell_price:.2f}, 价格变化率: {sell_change:.2f}%")
    
    if len(buy_signals) == 0 and len(sell_signals) == 0:
        print("未检测到任何信号")
    
    return df

def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    获取分时数据
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        分时数据DataFrame
    """
    try:
        # 确保 trade_date 是正确的格式
        if isinstance(trade_date, str):
            if '-' in trade_date:
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
            else:
                trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
        else:
            trade_date_obj = trade_date
            
        # 格式化为 akshare 接口需要的日期格式
        trade_date_str = trade_date_obj.strftime('%Y%m%d')
        
        # 构造 akshare 需要的时间格式 (YYYY-MM-DD HH:MM:SS)
        start_time = f'{trade_date_obj.strftime("%Y-%m-%d")} 09:30:00'
        end_time = f'{trade_date_obj.strftime("%Y-%m-%d")} 15:00:00'

        # 如果缓存没有数据，则从网络获取
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=start_time,
            end_date=end_time,
            adjust=''
        )

        if df.empty:
            print(f"❌ {stock_code} 在 {trade_date} 无分时数据")
            return None
            
        return df
    except Exception as e:
        print(f"❌ 获取分时数据失败: {e}")
        return None

def detect_trading_signals(df: pd.DataFrame) -> Dict[str, List[Tuple[datetime, float]]]:
    """
    检测交易信号
    
    Args:
        df: 包含指标的DataFrame
    
    Returns:
        信号字典
    """
    signals = {
        'buy_signals': [],
        'sell_signals': []
    }
    
    # 检测买入信号
    buy_signals = df[df['Buy_Signal']]
    for idx, row in buy_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['buy_signals'].append((signal_time, row['收盘']))
    
    # 检测卖出信号
    sell_signals = df[df['Sell_Signal']]
    for idx, row in sell_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['sell_signals'].append((signal_time, row['收盘']))
    
    return signals

def plot_momentum_reversal(stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
    """
    绘制动量反转策略图表
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        图表保存路径
    """
    try:
        # 时间处理
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date)
        if df is None or df.empty:
            return None
        
        # 计算指标
        df_with_indicators = calculate_momentum_reversal(df)
        
        # 创建图形和子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
        fig.suptitle(f'{stock_code} 动量反转策略图 ({trade_date})', fontsize=16)
        
        # 过滤掉无效数据
        df_filtered = df_with_indicators.dropna(subset=['收盘'])
        
        # 绘制价格
        ax1.plot(df_filtered.index, df_filtered['收盘'], label='收盘价', color='black', linewidth=1)
        
        # 绘制买入信号
        buy_signals = df_filtered[df_filtered['Buy_Signal']].dropna()
        for idx, row in buy_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax1.scatter(x_pos, row['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
            ax1.text(x_pos, row['收盘'] * 0.99, '买',
                     color='red', fontsize=12, ha='center', va='top', fontweight='bold')
        
        # 绘制卖出信号
        sell_signals = df_filtered[df_filtered['Sell_Signal']].dropna()
        for idx, row in sell_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax1.scatter(x_pos, row['收盘'] * 1.005, marker='v', color='green', s=100, zorder=5)
            ax1.text(x_pos, row['收盘'] * 1.01, '卖',
                     color='green', fontsize=12, ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 绘制价格变化率和阈值
        ax2.plot(df_filtered.index, df_filtered['Price_Change'], label='价格变化率(%)', color='blue', linewidth=1)
        ax2.plot(df_filtered.index, df_filtered['Upper_Threshold'], label='卖出阈值', color='green', linewidth=1, linestyle='--')
        ax2.plot(df_filtered.index, df_filtered['Lower_Threshold'], label='买入阈值', color='red', linewidth=1, linestyle='--')
        ax2.plot(df_filtered.index, df_filtered['Momentum_Mean'], label='平均动量', color='purple', linewidth=1)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.set_ylabel('价格变化率(%)', fontsize=12)
        ax2.set_xlabel('时间', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 自动旋转时间标签
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        import os
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, f'{stock_code}_momentum_reversal_{trade_date}.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 图表已保存至: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ 绘图失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_momentum_reversal(stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
    """
    动量反转策略分析主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        (数据框, 信号字典) 或 None
    """
    try:
        # 时间处理
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date)
        if df is None or df.empty:
            return None
        
        # 计算指标
        df_with_indicators = calculate_momentum_reversal(df)
        
        # 检测信号
        signals = detect_trading_signals(df_with_indicators)
        
        return df_with_indicators, signals
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # 测试代码
    stock_code = "000333"  # 美的集团
    trade_date = datetime.now().strftime('%Y-%m-%d')
    
    result = analyze_momentum_reversal(stock_code, trade_date)
    if result:
        df_with_indicators, signals = result
        print(f"📊 检测到 {len(signals['buy_signals'])} 个买入信号和 {len(signals['sell_signals'])} 个卖出信号")
        
        # 绘制图表
        plot_momentum_reversal(stock_code, trade_date)