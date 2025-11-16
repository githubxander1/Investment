import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import sys

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取Indicators目录
indicators_dir = os.path.dirname(current_dir)
# 添加Indicators目录到Python路径
sys.path.append(indicators_dir)

from utils.backtest_engine import BacktestEngine
from Technology.top_bottom_strategy import TopBottomStrategy

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class FixedTopBottomStrategy(TopBottomStrategy):
    """修复版的顶底策略类"""
    
    def calculate_indicators(self):
        """计算技术指标，修复除以0错误和指标计算"""
        try:
            df = self.data.copy()
            
            # 确保必要的列存在
            if not all(col in df.columns for col in ['high', 'low', 'close']):
                print("错误: 数据缺少必要的列")
                return False
            
            # 计算A1、B1、C1指标
            # 避免除以0的情况
            df['atr'] = df['high'] - df['low']
            df['atr_ma5'] = df['atr'].rolling(window=5).mean().fillna(1)  # 使用1替代NaN避免除以0
            df['atr_ma5'] = df['atr_ma5'].replace(0, 1)  # 确保不为0
            
            # 计算最高价和最低价的移动平均
            df['high_ma5'] = df['high'].rolling(window=5).mean()
            df['low_ma5'] = df['low'].rolling(window=5).mean()
            
            # 计算A1、B1、C1指标，添加安全检查
            df['A1'] = 100 * (df['close'] - df['low_ma5']) / df['atr_ma5']
            df['B1'] = 100 * (df['high_ma5'] - df['close']) / df['atr_ma5']
            df['C1'] = 100 * (df['high_ma5'] - df['low_ma5']) / df['atr_ma5']
            
            # 计算阻力、支撑、中线
            df['阻力'] = df['high_ma5']
            df['支撑'] = df['low_ma5']
            df['中线'] = (df['high_ma5'] + df['low_ma5']) / 2
            
            # 添加顶底中参考线
            df['顶参考线'] = 50  # 顶参考线固定值
            df['底参考线'] = -50  # 底参考线固定值
            df['中参考线'] = 0    # 中参考线固定值
            
            # 计算V11指标线
            # 先计算最高价和最低价的历史数据
            df['high_20'] = df['high'].rolling(window=20).max()
            df['low_20'] = df['low'].rolling(window=20).min()
            
            # 避免除以0的情况
            df['high_low_diff'] = df['high_20'] - df['low_20']
            df['high_low_diff'] = df['high_low_diff'].replace(0, 1)  # 确保不为0
            
            df['V11'] = 100 * (df['close'] - df['low_20']) / df['high_low_diff']
            
            # 计算趋势线
            df['趋势'] = df['V11'] - 50
            
            # 计算V12指标
            df['high_30'] = df['high'].rolling(window=30).max()
            df['low_30'] = df['low'].rolling(window=30).min()
            df['high_low_diff_30'] = df['high_30'] - df['low_30']
            df['high_low_diff_30'] = df['high_low_diff_30'].replace(0, 1)  # 确保不为0
            df['V12'] = 100 * (df['close'] - df['low_30']) / df['high_low_diff_30']
            
            # 保存计算结果
            self.data = df.copy()
            print("指标计算完成")
            return True
        except Exception as e:
            print(f"计算指标时出错: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def calculate_signals(self):
        """计算买卖信号，修复FILTER函数实现和DD3条件"""
        try:
            df = self.data.copy()
            
            # 确保必要的列存在
            if not all(col in df.columns for col in ['A1', 'B1', 'C1', 'V11', '趋势']):
                print("错误: 缺少计算信号所需的指标列")
                return False
            
            # 初始化信号列
            df['AA'] = 0  # 超卖见底信号
            df['BB0'] = 0  # 抄底信号
            df['BB1'] = 0
            df['BB2'] = 0
            df['BB3'] = 0
            df['BB4'] = 0
            df['BB5'] = 0
            df['CC'] = 0  # 超买见顶信号
            df['DD0'] = 0  # 逃顶信号
            df['DD1'] = 0
            df['DD2'] = 0
            df['DD3'] = 0
            df['DD4'] = 0
            df['DD5'] = 0
            
            # 计算AA超卖见底信号
            df['AA'] = ((df['A1'] < -50) & (df['A1'].shift(1) >= -50)).astype(int)
            
            # 计算CC超买见顶信号
            df['CC'] = ((df['B1'] < -50) & (df['B1'].shift(1) >= -50)).astype(int)
            
            # 计算BB0抄底信号（使用修复版FILTER函数）
            # 实现简化版的FILTER函数功能
            signal = np.zeros(len(df))
            state = 0  # 0: 无信号状态，1: 持有信号状态
            persistence = 5  # 保持信号的周期数
            counter = 0
            
            for i in range(len(df)):
                if df['AA'].iloc[i] == 1 and state == 0:
                    signal[i] = 1
                    state = 1
                    counter = persistence
                elif state == 1:
                    counter -= 1
                    if counter <= 0:
                        state = 0
            
            df['BB0'] = signal
            
            # 计算BB1-BB5信号
            df['BB1'] = ((df['V11'] < 20) & (df['V11'].shift(1) >= 20)).astype(int)
            df['BB2'] = ((df['趋势'] < -30) & (df['趋势'].shift(1) >= -30)).astype(int)
            
            # BB3-BB5使用简化逻辑
            df['BB3'] = ((df['V11'] < 10) & (df['V11'].shift(1) >= 10)).astype(int)
            df['BB4'] = ((df['A1'] < -60) & (df['A1'].shift(1) >= -60)).astype(int)
            df['BB5'] = ((df['V11'] < 5) & (df['V11'].shift(1) >= 5)).astype(int)
            
            # 计算DD0逃顶信号（使用修复版FILTER函数）
            signal = np.zeros(len(df))
            state = 0  # 0: 无信号状态，1: 持有信号状态
            counter = 0
            
            for i in range(len(df)):
                if df['CC'].iloc[i] == 1 and state == 0:
                    signal[i] = 1
                    state = 1
                    counter = persistence
                elif state == 1:
                    counter -= 1
                    if counter <= 0:
                        state = 0
            
            df['DD0'] = signal
            
            # 计算DD1-DD5信号
            df['DD1'] = ((df['V11'] > 80) & (df['V11'].shift(1) <= 80)).astype(int)
            df['DD2'] = ((df['趋势'] > 30) & (df['趋势'].shift(1) <= 30)).astype(int)
            
            # 修复DD3条件（根据通达信公式修正）
            df['DD3'] = ((df['V11'] > 90) & (df['V11'].shift(1) <= 90)).astype(int)
            
            df['DD4'] = ((df['B1'] < -60) & (df['B1'].shift(1) >= -60)).astype(int)
            df['DD5'] = ((df['V11'] > 95) & (df['V11'].shift(1) <= 95)).astype(int)
            
            # 计算最终买入信号
            df['买入信号'] = ((df['BB0'] == 1) | (df['BB1'] == 1) | (df['BB2'] == 1) | 
                           (df['BB3'] == 1) | (df['BB4'] == 1) | (df['BB5'] == 1)).astype(int)
            
            # 计算最终卖出信号
            df['卖出信号'] = ((df['DD0'] == 1) | (df['DD1'] == 1) | (df['DD2'] == 1) | 
                           (df['DD3'] == 1) | (df['DD4'] == 1) | (df['DD5'] == 1)).astype(int)
            
            # 保存信号计算结果
            self.data = df.copy()
            print("信号计算完成")
            return True
        except Exception as e:
            print(f"计算信号时出错: {e}")
            import traceback
            traceback.print_exc()
            return False

def load_etf_data(file_path):
    """
    从CSV文件加载ETF数据，增强了数据处理的鲁棒性
    
    Parameters:
    file_path (str): CSV文件路径
    
    Returns:
    pd.DataFrame: ETF数据
    """
    try:
        print(f"正在加载ETF数据: {file_path}")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在 '{file_path}'")
            return None
            
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 打印数据列信息以调试
        print(f"数据包含列: {list(df.columns)}")
        
        # 确保日期列是datetime类型
        date_column = None
        for col in ['date', 'Date', '日期']:
            if col in df.columns:
                date_column = col
                df[col] = pd.to_datetime(df[col])
                break
        
        if date_column is None:
            print("错误: 找不到日期列")
            return None
        
        # 重命名日期列为'date'
        if date_column != 'date':
            df.rename(columns={date_column: 'date'}, inplace=True)
        
        # 检查并映射必要的列名
        column_mapping = {
            'open': ['open', 'Open', '开盘价'],
            'high': ['high', 'High', '最高价'],
            'low': ['low', 'Low', '最低价'],
            'close': ['close', 'Close', '收盘价', '收盘'],
            'volume': ['volume', 'Volume', '成交量']
        }
        
        # 重命名列
        for standard_col, possible_names in column_mapping.items():
            for name in possible_names:
                if name in df.columns:
                    if name != standard_col:
                        df.rename(columns={name: standard_col}, inplace=True)
                    break
            else:
                print(f"警告: 找不到'{standard_col}'相关列，将使用NaN值")
                df[standard_col] = np.nan
        
        # 确保数据有必要的列
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                print(f"错误: 数据缺少必要的列 '{col}'")
                return None
        
        # 检查价格数据是否有效
        price_columns = ['open', 'high', 'low', 'close']
        for col in price_columns:
            if df[col].isnull().all():
                print(f"错误: 价格列 '{col}' 全部为NaN")
                return None
            
        # 按照日期排序
        df.sort_values('date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # 打印数据前几行以验证
        print("数据前5行预览：")
        print(df.head())
        
        print(f"成功加载ETF数据，共{len(df)}条记录")
        return df
    except Exception as e:
        print(f"加载ETF数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_etf_backtest(etf_code, etf_name, data_file):
    """
    运行ETF的顶底指标回测（使用完整修复版策略）
    
    Parameters:
    etf_code (str): ETF代码
    etf_name (str): ETF名称
    data_file (str): 数据文件路径
    
    Returns:
    BacktestEngine: 回测实例
    """
    print(f"\n{'='*50}")
    print(f"开始回测 {etf_name}({etf_code}) 的顶底指标策略（完整修复版）")
    print(f"{'='*50}")
    
    # 从文件加载数据
    data = load_etf_data(data_file)
    if data is None:
        print(f"无法加载{etf_name}的数据")
        return None
    
    # 获取日期范围
    start_date = data['date'].iloc[0].strftime('%Y%m%d')
    end_date = data['date'].iloc[-1].strftime('%Y%m%d')
    print(f"数据日期范围: {start_date} 到 {end_date}")
    
    # 创建回测实例（使用修复版策略）
    backtester = FixedTopBottomStrategy(
        stock_code=etf_code,
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000
    )
    
    # 加载数据（使用副本避免修改原始数据）
    backtester.load_data(data.copy())
    
    # 计算指标
    if not backtester.calculate_indicators():
        print("指标计算失败")
        return None
    
    # 计算信号
    if not backtester.calculate_signals():
        print("信号计算失败")
        return None
    
    # 输出信号统计
    df = backtester.data
    print(f"信号统计：")
    print(f"AA超卖见底信号：{df['AA'].sum()}个")
    print(f"BB0抄底信号：{df['BB0'].sum()}个")
    print(f"买入信号总数：{df['买入信号'].sum()}个")
    print(f"CC超买见顶信号：{df['CC'].sum()}个")
    print(f"DD0逃顶信号：{df['DD0'].sum()}个")
    print(f"卖出信号总数：{df['卖出信号'].sum()}个")
    
    # 运行回测
    if not backtester.run_backtest():
        print("回测执行失败")
        return None
    
    # 绘制结果图表（指定保存路径为Indicators目录下的回测文件夹）
    chart_dir = os.path.join(indicators_dir, '回测')
    if not backtester.plot_results(title_suffix=f"- {etf_name}（完整修复版）", save_dir=chart_dir):
        print("图表绘制失败")
    
    # 保存详细回测日志（指定保存路径为Indicators目录下的回测记录文件夹）
    log_dir = os.path.join(indicators_dir, '回测记录')
    backtester.save_backtest_log(prefix=f"回测记录_顶底指标_完整修复版_{etf_name}", log_dir=log_dir)
    
    print(f"\n{etf_name} 回测完成！")
    return backtester

def main():
    """主函数"""
    # 获取数据文件路径（使用相对路径）
    data_dir = os.path.join(indicators_dir, 'Data', '日线数据')
    
    # 检查数据目录是否存在
    if not os.path.exists(data_dir):
        print(f"错误: 数据目录不存在 '{data_dir}'")
        # 尝试使用绝对路径作为备选
        data_dir = 'e:/git_documents/Investment/Investment/Indicators/Data/日线数据'
        print(f"尝试使用备选路径: {data_dir}")
        if not os.path.exists(data_dir):
            print("错误: 备选数据目录也不存在")
            return
    
    etf_files = [
        {
            'code': '513050',
            'name': '中概互联网ETF',
            'file_path': os.path.join(data_dir, '513050中概互联网ETF_20241115_20251115.csv')
        },
        {
            'code': '513330',
            'name': '恒生互联网ETF',
            'file_path': os.path.join(data_dir, '513330恒生互联网ETF_20241115_20251115.csv')
        }
    ]
    
    # 确保回测记录目录存在（在Indicators目录下）
    log_dir = os.path.join(indicators_dir, '回测记录')
    os.makedirs(log_dir, exist_ok=True)
    
    # 确保图表保存目录存在（在Indicators目录下）
    chart_dir = os.path.join(indicators_dir, '回测')
    os.makedirs(chart_dir, exist_ok=True)
    
    print("开始ETF顶底指标回测（完整修复版）...")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"回测图表将保存到: {chart_dir}")
    print(f"回测记录将保存到: {log_dir}")
    
    backtesters = []
    
    # 逐个回测ETF
    for etf in etf_files:
        try:
            # 检查文件是否存在
            if not os.path.exists(etf['file_path']):
                print(f"错误: ETF文件不存在 '{etf['file_path']}'")
                continue
            
            backtester = run_etf_backtest(
                etf_code=etf['code'],
                etf_name=etf['name'],
                data_file=etf['file_path']
            )
            if backtester:
                backtesters.append(backtester)
        except Exception as e:
            print(f"{etf['name']}回测失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 汇总回测结果
    if backtesters:
        print(f"\n{'='*60}")
        print(f"所有ETF回测完成！")
        print(f"{'='*60}")
        print("回测结果汇总:")
        print("-" * 60)
        print(f"{'ETF名称':<12} {'ETF代码':<8} {'初始资金':>10} {'最终资金':>10} {'总收益率':>10} {'交易次数':>8}")
        print("-" * 60)
        
        for i, backtester in enumerate(backtesters):
            etf = etf_files[i]
            total_return = (backtester.capital - backtester.initial_capital) / backtester.initial_capital * 100
            print(f"{etf['name']:<12} {etf['code']:<8} {backtester.initial_capital:>10.0f} {backtester.capital:>10.2f} {total_return:>10.2f}% {len(backtester.trades):>8}")
        
        print("-" * 60)
    
    print(f"图表已保存到: {chart_dir}")
    print(f"详细日志已保存到: {log_dir}")

if __name__ == "__main__":
    main()