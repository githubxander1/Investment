import pandas as pd
import numpy as np

def calculate_main_force_accumulation(df):
    """
    计算主力建仓指标及相关信号
    
    参数:
    df (pd.DataFrame): 包含OHLC数据的DataFrame，必须包含'high', 'low', 'close'列
    
    返回:
    pd.DataFrame: 原始DataFrame添加了以下列：
        - slope: 收盘价34天线性回归斜率
        - H1: EMA(SLOPE(CLOSE,34)*20+CLOSE,75)
        - H2: EMA(CLOSE,8)
        - VAR1: H2-H1
        - 生命线: MA(CLOSE,26)
        - 买入信号: 买入信号标记
        - 卖出信号: 卖出信号标记
    """
    # 检查必要的列
    required_columns = ['high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"数据缺少必要的列: {col}")
    
    # 创建数据副本以避免修改原始数据
    result_df = df.copy()
    
    # H1:EMA(SLOPE(CLOSE,34)*20+CLOSE,75),COLORYELLOW;
    # 计算斜率SLOPE(CLOSE,34)，相当于线性回归的斜率
    slopes = []
    for i in range(len(result_df)):
        if i < 33:  # 前34天不足计算斜率
            slopes.append(0)
        else:
            # 计算最近34天的线性回归斜率
            x = np.arange(34)
            y = result_df['close'].iloc[i-33:i+1].values
            slope, _ = np.polyfit(x, y, 1)
            slopes.append(slope)
    result_df['slope'] = slopes
    
    # 计算H1
    H1_calc = result_df['slope'] * 20 + result_df['close']
    result_df['H1'] = pd.Series(H1_calc).ewm(span=75, adjust=False).mean()
    
    # H2:EMA(CLOSE,8),COLORWHITE;
    result_df['H2'] = result_df['close'].ewm(span=8, adjust=False).mean()
    
    # VAR1:=H2-H1;
    result_df['VAR1'] = result_df['H2'] - result_df['H1']
    
    # 生命线:MA(CLOSE,26),COLORRED,LINETHICK3;
    result_df['生命线'] = result_df['close'].rolling(window=26).mean()
    
    # 计算买入信号条件
    # 买入条件1：H2上穿H1 且 价格在生命线上方
    result_df['H2_cross_H1'] = ((result_df['H2'] > result_df['H1']) & 
                              (result_df['H2'].shift(1) <= result_df['H1'].shift(1))).astype(int)
    result_df['price_above_lifeline'] = (result_df['close'] > result_df['生命线']).astype(int)
    
    # 买入条件2：H2持续在H1上方且VAR1由负转正
    result_df['H2_above_H1'] = (result_df['H2'] > result_df['H1']).astype(int)
    result_df['VAR1_turn_positive'] = ((result_df['VAR1'] > 0) & 
                                    (result_df['VAR1'].shift(1) <= 0)).astype(int)
    
    # 综合买入信号：条件1 OR 条件2
    result_df['买入信号'] = ((result_df['H2_cross_H1'] & result_df['price_above_lifeline']) | 
                          (result_df['H2_above_H1'] & result_df['VAR1_turn_positive'])).astype(int)
    
    # 计算卖出信号条件
    # 卖出条件1：H2下穿H1
    result_df['H1_cross_H2'] = ((result_df['H1'] > result_df['H2']) & 
                              (result_df['H1'].shift(1) <= result_df['H2'].shift(1))).astype(int)
    
    # 卖出条件2：价格跌破生命线
    result_df['price_below_lifeline'] = (result_df['close'] < result_df['生命线']).astype(int)
    
    # 卖出条件3：VAR1由正转负
    result_df['VAR1_turn_negative'] = ((result_df['VAR1'] < 0) & 
                                    (result_df['VAR1'].shift(1) >= 0)).astype(int)
    
    # 综合卖出信号：条件1 OR 条件2 OR 条件3
    result_df['卖出信号'] = (result_df['H1_cross_H2'] | 
                          result_df['price_below_lifeline'] | 
                          result_df['VAR1_turn_negative']).astype(int)
    
    # 过滤重复信号，避免连续触发
    result_df['买入信号'] = result_df['买入信号'] & (result_df['买入信号'].shift(1) == 0)
    result_df['卖出信号'] = result_df['卖出信号'] & (result_df['卖出信号'].shift(1) == 0)
    
    return result_df

def get_indicator_info():
    """
    获取主力建仓指标的信息
    
    返回:
    dict: 包含指标名称、描述、参数等信息的字典
    """
    return {
        'name': '主力建仓指标',
        'description': '基于H1和H2两条线交叉以及生命线位置关系的交易信号指标',
        'parameters': {
            'slope_window': '计算斜率的窗口，默认34',
            'h1_span': 'H1线的EMA平滑参数，默认75',
            'h2_span': 'H2线的EMA平滑参数，默认8',
            'lifeline_window': '生命线的移动平均窗口，默认26'
        },
        'buy_conditions': [
            'H2上穿H1 且 价格在生命线上方',
            'H2持续在H1上方且VAR1由负转正'
        ],
        'sell_conditions': [
            'H2下穿H1',
            '价格跌破生命线',
            'VAR1由正转负'
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
    result = calculate_main_force_accumulation(sample_data)
    
    # 打印结果摘要
    print("主力建仓指标计算完成")
    print(f"买入信号数量: {result['买入信号'].sum()}")
    print(f"卖出信号数量: {result['卖出信号'].sum()}")
    print("\n生成的指标列:")
    for col in ['slope', 'H1', 'H2', 'VAR1', '生命线', '买入信号', '卖出信号']:
        print(f"  - {col}")