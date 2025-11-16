import pandas as pd
import numpy as np

def calculate_optimized_cci(df):
    """
    计算优化的CCI指标及相关信号
    
    参数:
    df (pd.DataFrame): 包含OHLC数据的DataFrame，必须包含'high', 'low', 'close'列
    
    返回:
    pd.DataFrame: 原始DataFrame添加了以下列：
        - VAR1, VAR2, VAR3: 中间计算变量
        - CCI_raw: 原始CCI值
        - AA: 平滑后的CCI指标线
        - BB: AA的快速平滑线
        - 买入信号1, 买入信号2, 买入信号: 买入信号标记
        - 卖出信号_raw, 卖出信号: 卖出信号标记
    """
    # 检查必要的列
    required_columns = ['high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"数据缺少必要的列: {col}")
    
    # 创建数据副本以避免修改原始数据
    result_df = df.copy()
    
    # 计算VAR1, VAR2, VAR3
    result_df['VAR1'] = (2 * result_df['close'] + result_df['high'] + result_df['low']) / 4
    result_df['VAR2'] = result_df['low'].rolling(window=34).min()
    result_df['VAR3'] = result_df['high'].rolling(window=34).max()
    
    # 计算原始CCI值
    result_df['CCI_raw'] = ((result_df['VAR1'] - result_df['VAR2']) / 
                           (result_df['VAR3'] - result_df['VAR2'])) * 100
    
    # 计算AA指标线 (EMA平滑)
    result_df['AA'] = result_df['CCI_raw'].ewm(span=13, adjust=False).mean()
    
    # 计算BB指标线 (AA的快速EMA)
    result_df['BB'] = result_df['AA'].ewm(span=2, adjust=False).mean()
    
    # 计算买入信号1: AA上穿BB且AA<20
    result_df['买入信号1'] = ((result_df['AA'] > result_df['BB']) & 
                           (result_df['AA'].shift(1) <= result_df['BB'].shift(1)) & 
                           (result_df['AA'] < 20)).astype(int)
    
    # 计算买入信号2: AA上穿22且BB<AA
    result_df['买入信号2'] = ((result_df['AA'] > 22) & 
                           (result_df['AA'].shift(1) <= 22) & 
                           (result_df['BB'] < result_df['AA'])).astype(int)
    
    # 综合买入信号
    result_df['买入信号'] = (result_df['买入信号1'] | result_df['买入信号2']).astype(int)
    
    # 计算卖出信号原始值: BB上穿AA且AA>80.3
    result_df['卖出信号_raw'] = ((result_df['BB'] > result_df['AA']) & 
                              (result_df['BB'].shift(1) <= result_df['AA'].shift(1)) & 
                              (result_df['AA'] > 80.3)).astype(int)
    
    # 模拟FILTER函数，3天内只取第一个信号
    result_df['卖出信号'] = 0
    last_signal = -10  # 初始化为足够小的值
    for i in range(len(result_df)):
        if result_df['卖出信号_raw'].iloc[i] == 1 and (i - last_signal) >= 3:
            result_df.loc[result_df.index[i], '卖出信号'] = 1
            last_signal = i
    
    return result_df

def get_indicator_info():
    """
    获取优化CCI指标的信息
    
    返回:
    dict: 包含指标名称、描述、参数等信息的字典
    """
    return {
        'name': '优化CCI',
        'description': '基于传统CCI指标的改进版本，使用AA和BB两条线产生交易信号',
        'parameters': {
            'window_var': 'VAR2和VAR3的计算窗口，默认34',
            'span_aa': 'AA线的EMA平滑参数，默认13',
            'span_bb': 'BB线的EMA平滑参数，默认2',
            'filter_days': '卖出信号过滤天数，默认3'
        },
        'buy_conditions': [
            'AA上穿BB且AA<20',
            'AA上穿22且BB<AA'
        ],
        'sell_conditions': [
            'BB上穿AA且AA>80.3，3天内只取第一个信号'
        ]
    }

# 示例用法
if __name__ == "__main__":
    # 创建示例数据
    dates = pd.date_range(start='2024-01-01', periods=100, freq='B')
    np.random.seed(42)
    prices = np.cumsum(np.random.normal(0, 0.5, 100)) + 25
    
    sample_data = pd.DataFrame({
        'open': prices * (1 + np.random.normal(0, 0.01, 100)),
        'high': prices * (1 + np.random.normal(0.01, 0.01, 100)),
        'low': prices * (1 - np.random.normal(0.01, 0.01, 100)),
        'close': prices,
        'volume': np.random.randint(100000, 10000000, size=100)
    }, index=dates)
    
    # 计算指标
    result = calculate_optimized_cci(sample_data)
    
    # 打印结果摘要
    print("优化CCI指标计算完成")
    print(f"买入信号数量: {result['买入信号'].sum()}")
    print(f"卖出信号数量: {result['卖出信号'].sum()}")
    print("\n生成的指标列:")
    for col in ['VAR1', 'VAR2', 'VAR3', 'CCI_raw', 'AA', 'BB', '买入信号', '卖出信号']:
        print(f"  - {col}")