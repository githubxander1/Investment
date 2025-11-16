import pandas as pd
import numpy as np

def calculate_top_bottom_indicator(df):
    """
    计算顶底指标及相关信号
    
    参数:
    df (pd.DataFrame): 包含OHLC数据的DataFrame，必须包含'high', 'low', 'open', 'close'列
    
    返回:
    pd.DataFrame: 原始DataFrame添加了以下列：
        - A1, B1, C1: 中间计算变量
        - 阻力, 支撑, 中线: 价格区域指标
        - V11, 趋势, V12: 趋势指标
        - 买入信号: 买入信号标记
        - 卖出信号: 卖出信号标记
    """
    # 检查必要的列
    required_columns = ['high', 'low', 'open', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"数据缺少必要的列: {col}")
    
    # 创建数据副本以避免修改原始数据
    result_df = df.copy()
    
    # 计算A1, B1, C1
    result_df['A1'] = result_df[['high', 'open']].max(axis=1)
    result_df['B1'] = result_df[['low', 'open']].min(axis=1)
    result_df['C1'] = result_df['A1'] - result_df['B1']
    
    # 计算阻力、支撑、中线
    result_df['阻力'] = result_df['B1'] + result_df['C1'] * 7 / 8
    result_df['支撑'] = result_df['B1'] + result_df['C1'] * 0.5 / 8
    result_df['中线'] = (result_df['支撑'] + result_df['阻力']) / 2
    
    # 计算V11
    # 首先计算(C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100
    llv_55 = result_df['low'].rolling(window=55).min()
    hhv_55 = result_df['high'].rolling(window=55).max()
    rsv_55 = (result_df['close'] - llv_55) / (hhv_55 - llv_55) * 100
    
    # 计算SMA1 = SMA(RSV, 5, 1)
    sma1 = rsv_55.rolling(window=5).mean()
    
    # 计算SMA2 = SMA(SMA1, 3, 1)
    sma2 = sma1.rolling(window=3).mean()
    
    # 计算V11 = 3*SMA1 - 2*SMA2
    result_df['V11'] = 3 * sma1 - 2 * sma2
    
    # 计算趋势 = EMA(V11, 3)
    result_df['趋势'] = result_df['V11'].ewm(span=3, adjust=False).mean()
    
    # 计算V12 = (趋势-REF(趋势,1))/REF(趋势,1)*100
    result_df['V12'] = (result_df['趋势'] - result_df['趋势'].shift(1)) / result_df['趋势'].shift(1) * 100
    
    # 买入信号计算
    # AA: 趋势<11 AND FILTER(趋势<=11,15) AND C<中线
    # 使用滚动窗口实现FILTER功能
    result_df['trend_below_11'] = (result_df['趋势'] <= 11).astype(int)
    result_df['filtered_trend'] = 0
    for i in range(len(result_df)):
        if i >= 15:
            # 检查前15天是否有True
            if not result_df['trend_below_11'].iloc[i-15:i].any() and result_df['trend_below_11'].iloc[i]:
                result_df.loc[result_df.index[i], 'filtered_trend'] = 1
        else:
            # 对于前15天，只要trend_below_11为True就设置为1
            if result_df['trend_below_11'].iloc[i]:
                result_df.loc[result_df.index[i], 'filtered_trend'] = 1
    
    result_df['AA'] = ((result_df['趋势'] < 11) & (result_df['filtered_trend'] == 1) & (result_df['close'] < result_df['中线'])).astype(int)
    
    # BB0: REF(趋势,1)<11 AND CROSS(趋势,11) AND C<中线
    result_df['BB0'] = ((result_df['趋势'].shift(1) < 11) & (result_df['趋势'] > 11) & (result_df['close'] < result_df['中线'])).astype(int)
    
    # BB1-BB5信号
    result_df['BB1'] = ((result_df['趋势'].shift(1) < 11) & (result_df['趋势'].shift(1) > 6) & (result_df['趋势'] > 11)).astype(int)
    result_df['BB2'] = ((result_df['趋势'].shift(1) < 6) & (result_df['趋势'].shift(1) > 3) & (result_df['趋势'] > 6)).astype(int)
    result_df['BB3'] = ((result_df['趋势'].shift(1) < 3) & (result_df['趋势'].shift(1) > 1) & (result_df['趋势'] > 3)).astype(int)
    result_df['BB4'] = ((result_df['趋势'].shift(1) < 1) & (result_df['趋势'].shift(1) > 0) & (result_df['趋势'] > 1)).astype(int)
    result_df['BB5'] = ((result_df['趋势'].shift(1) < 0) & (result_df['趋势'] > 0)).astype(int)
    
    # BB: 综合买入信号
    result_df['BB'] = (result_df['BB1'] | result_df['BB2'] | result_df['BB3'] | result_df['BB4'] | result_df['BB5']).astype(int)
    
    # 最终买入信号：BB=1 AND C<中线
    result_df['买入信号'] = ((result_df['BB'] == 1) & (result_df['close'] < result_df['中线'])).astype(int)
    
    # 卖出信号计算
    # CC: 趋势>89 AND FILTER(趋势>89,15) AND C>中线
    result_df['trend_above_89'] = (result_df['趋势'] > 89).astype(int)
    result_df['filtered_trend_sell'] = 0
    for i in range(len(result_df)):
        if i >= 15:
            # 检查前15天是否有True
            if not result_df['trend_above_89'].iloc[i-15:i].any() and result_df['trend_above_89'].iloc[i]:
                result_df.loc[result_df.index[i], 'filtered_trend_sell'] = 1
        else:
            # 对于前15天，只要trend_above_89为True就设置为1
            if result_df['trend_above_89'].iloc[i]:
                result_df.loc[result_df.index[i], 'filtered_trend_sell'] = 1
    
    result_df['CC'] = ((result_df['趋势'] > 89) & (result_df['filtered_trend_sell'] == 1) & (result_df['close'] > result_df['中线'])).astype(int)
    
    # DD0: REF(趋势,1)>89 AND CROSS(89,趋势) AND C>中线
    result_df['DD0'] = ((result_df['趋势'].shift(1) > 89) & (result_df['趋势'] < 89) & (result_df['close'] > result_df['中线'])).astype(int)
    
    # DD1-DD5信号
    result_df['DD1'] = ((result_df['趋势'].shift(1) > 89) & (result_df['趋势'].shift(1) < 94) & (result_df['趋势'] < 89)).astype(int)
    result_df['DD2'] = ((result_df['趋势'].shift(1) > 94) & (result_df['趋势'].shift(1) < 97) & (result_df['趋势'] < 94)).astype(int)
    result_df['DD3'] = ((result_df['趋势'].shift(1) > 97) & (result_df['趋势'].shift(1) < 99) & (result_df['趋势'] < 97)).astype(int)
    result_df['DD4'] = ((result_df['趋势'].shift(1) > 99) & (result_df['趋势'].shift(1) < 100) & (result_df['趋势'] < 99)).astype(int)
    result_df['DD5'] = ((result_df['趋势'].shift(1) > 100) & (result_df['趋势'] < 100)).astype(int)
    
    # DD: 综合卖出信号
    result_df['DD'] = (result_df['DD1'] | result_df['DD2'] | result_df['DD3'] | result_df['DD4'] | result_df['DD5']).astype(int)
    
    # 最终卖出信号：DD=1 AND C>中线
    result_df['卖出信号'] = ((result_df['DD'] == 1) & (result_df['close'] > result_df['中线'])).astype(int)
    
    return result_df

def get_indicator_info():
    """
    获取顶底指标的信息
    
    返回:
    dict: 包含指标名称、描述、参数等信息的字典
    """
    return {
        'name': '顶底指标',
        'description': '基于价格区域和趋势指标的顶底判断和交易信号指标',
        'parameters': {
            'rsv_window': 'RSV计算窗口，默认55',
            'sma1_window': 'SMA1计算窗口，默认5',
            'sma2_window': 'SMA2计算窗口，默认3',
            'trend_span': '趋势线EMA参数，默认3',
            'filter_days': '信号过滤天数，默认15'
        },
        'buy_conditions': [
            '趋势线突破不同级别阈值且价格在中线下',
            '包含BB1-BB5五种突破模式'
        ],
        'sell_conditions': [
            '趋势线跌破不同级别阈值且价格在中线上',
            '包含DD1-DD5五种突破模式'
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
    result = calculate_top_bottom_indicator(sample_data)
    
    # 打印结果摘要
    print("顶底指标计算完成")
    print(f"买入信号数量: {result['买入信号'].sum()}")
    print(f"卖出信号数量: {result['卖出信号'].sum()}")
    print("\n生成的指标列:")
    for col in ['A1', 'B1', 'C1', '阻力', '支撑', '中线', 'V11', '趋势', '买入信号', '卖出信号']:
        print(f"  - {col}")