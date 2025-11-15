import pandas as pd
import numpy as np
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.backtest_engine import BacktestEngine

class TopBottomStrategy(BacktestEngine):
    """顶底指标策略"""
    
    def __init__(self, stock_code, start_date, end_date, initial_capital=100000):
        super().__init__(stock_code, start_date, end_date, initial_capital)
    
    def calculate_indicators(self):
        """计算顶底指标"""
        if self.data is None:
            print("没有数据可计算指标")
            return False
        
        df = self.data.copy()
        
        # 计算A1, B1, C1
        df['A1'] = df[['high', 'open']].max(axis=1)
        df['B1'] = df[['low', 'open']].min(axis=1)
        df['C1'] = df['A1'] - df['B1']
        
        # 计算阻力、支撑、中线
        df['阻力'] = df['B1'] + df['C1'] * 7 / 8
        df['支撑'] = df['B1'] + df['C1'] * 0.5 / 8
        df['中线'] = (df['支撑'] + df['阻力']) / 2
        
        # 计算V11
        # 首先计算(C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100
        llv_55 = df['low'].rolling(window=55).min()
        hhv_55 = df['high'].rolling(window=55).max()
        rsv_55 = (df['close'] - llv_55) / (hhv_55 - llv_55) * 100
        
        # 计算SMA1 = SMA(RSV, 5, 1)
        sma1 = rsv_55.rolling(window=5).mean()
        
        # 计算SMA2 = SMA(SMA1, 3, 1)
        sma2 = sma1.rolling(window=3).mean()
        
        # 计算V11 = 3*SMA1 - 2*SMA2
        df['V11'] = 3 * sma1 - 2 * sma2
        
        # 计算趋势 = EMA(V11, 3)
        df['趋势'] = df['V11'].ewm(span=3, adjust=False).mean()
        
        # 计算V12 = (趋势-REF(趋势,1))/REF(趋势,1)*100
        df['V12'] = (df['趋势'] - df['趋势'].shift(1)) / df['趋势'].shift(1) * 100
        
        self.data = df
        print("指标计算完成")
        return True
    
    def calculate_signals(self):
        """计算买入和卖出信号"""
        if self.data is None:
            print("没有数据可计算信号")
            return False
        
        df = self.data.copy()
        
        # 买入信号计算
        # AA: 趋势<11 AND FILTER(趋势<=11,15) AND C<中线
        # 使用滚动窗口实现FILTER功能
        df['trend_below_11'] = (df['趋势'] <= 11).astype(int)
        df['filtered_trend'] = 0
        for i in range(len(df)):
            if i >= 15:
                # 检查前15天是否有True
                if not df['trend_below_11'].iloc[i-15:i].any() and df['trend_below_11'].iloc[i]:
                    df.loc[df.index[i], 'filtered_trend'] = 1
            else:
                # 对于前15天，只要trend_below_11为True就设置为1
                if df['trend_below_11'].iloc[i]:
                    df.loc[df.index[i], 'filtered_trend'] = 1
        
        df['AA'] = ((df['趋势'] < 11) & (df['filtered_trend'] == 1) & (df['close'] < df['中线'])).astype(int)
        
        # BB0: REF(趋势,1)<11 AND CROSS(趋势,11) AND C<中线
        df['BB0'] = ((df['趋势'].shift(1) < 11) & (df['趋势'] > 11) & (df['close'] < df['中线'])).astype(int)
        
        # BB1-BB5信号
        df['BB1'] = ((df['趋势'].shift(1) < 11) & (df['趋势'].shift(1) > 6) & (df['趋势'] > 11)).astype(int)
        df['BB2'] = ((df['趋势'].shift(1) < 6) & (df['趋势'].shift(1) > 3) & (df['趋势'] > 6)).astype(int)
        df['BB3'] = ((df['趋势'].shift(1) < 3) & (df['趋势'].shift(1) > 1) & (df['趋势'] > 3)).astype(int)
        df['BB4'] = ((df['趋势'].shift(1) < 1) & (df['趋势'].shift(1) > 0) & (df['趋势'] > 1)).astype(int)
        df['BB5'] = ((df['趋势'].shift(1) < 0) & (df['趋势'] > 0)).astype(int)
        
        # BB: 综合买入信号
        df['BB'] = (df['BB1'] | df['BB2'] | df['BB3'] | df['BB4'] | df['BB5']).astype(int)
        
        # 最终买入信号：BB=1 AND C<中线
        df['买入信号'] = ((df['BB'] == 1) & (df['close'] < df['中线'])).astype(int)
        
        # 卖出信号计算
        # CC: 趋势>89 AND FILTER(趋势>89,15) AND C>中线
        df['trend_above_89'] = (df['趋势'] > 89).astype(int)
        df['filtered_trend_sell'] = 0
        for i in range(len(df)):
            if i >= 15:
                # 检查前15天是否有True
                if not df['trend_above_89'].iloc[i-15:i].any() and df['trend_above_89'].iloc[i]:
                    df.loc[df.index[i], 'filtered_trend_sell'] = 1
            else:
                # 对于前15天，只要trend_above_89为True就设置为1
                if df['trend_above_89'].iloc[i]:
                    df.loc[df.index[i], 'filtered_trend_sell'] = 1
        
        df['CC'] = ((df['趋势'] > 89) & (df['filtered_trend_sell'] == 1) & (df['close'] > df['中线'])).astype(int)
        
        # DD0: REF(趋势,1)>89 AND CROSS(89,趋势) AND C>中线
        df['DD0'] = ((df['趋势'].shift(1) > 89) & (df['趋势'] < 89) & (df['close'] > df['中线'])).astype(int)
        
        # DD1-DD5信号
        df['DD1'] = ((df['趋势'].shift(1) > 89) & (df['趋势'].shift(1) < 94) & (df['趋势'] < 89)).astype(int)
        df['DD2'] = ((df['趋势'].shift(1) > 94) & (df['趋势'].shift(1) < 97) & (df['趋势'] < 94)).astype(int)
        df['DD3'] = ((df['趋势'].shift(1) > 97) & (df['趋势'].shift(1) < 99) & (df['趋势'] < 97)).astype(int)
        df['DD4'] = ((df['趋势'].shift(1) > 99) & (df['趋势'].shift(1) < 100) & (df['趋势'] < 99)).astype(int)
        df['DD5'] = ((df['趋势'].shift(1) > 100) & (df['趋势'] < 100)).astype(int)
        
        # DD: 综合卖出信号
        df['DD'] = (df['DD1'] | df['DD2'] | df['DD3'] | df['DD4'] | df['DD5']).astype(int)
        
        # 最终卖出信号：DD=1 AND C>中线
        df['卖出信号'] = ((df['DD'] == 1) & (df['close'] > df['中线'])).astype(int)
        
        self.data = df
        print(f"信号计算完成,统计买入和卖出信号：\n买入信号数量：{df['买入信号'].sum()}，卖出信号数量：{df['卖出信号'].sum()}")
        return True

def run_top_bottom_backtest(stock_code, stock_name):
    """运行顶底指标回测"""
    from datetime import datetime, timedelta
    
    print(f"\n=====================================")
    print(f"开始回测 {stock_name}({stock_code}) 的顶底指标策略")
    print(f"=====================================")
    
    # 计算近一年的日期范围
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    
    print(f"日期范围: {start_date} 到 {end_date}")
    
    # 使用通用回测引擎运行回测
    from utils.backtest_engine import run_backtest
    
    backtester = run_backtest(
        backtester_class=TopBottomStrategy,
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000
    )
    
    print(f"{stock_name} 回测完成！")
    return backtester

# 主函数
def main():
    try:
        # 回测中概互联ETF (513050)
        backtester1 = run_top_bottom_backtest('513050', '中概互联ETF')
    except Exception as e:
        print(f"中概互联ETF回测失败: {e}")
    
    try:
        # 回测恒生互联网ETF (513330)
        backtester2 = run_top_bottom_backtest('513330', '恒生互联网ETF')
    except Exception as e:
        print(f"恒生互联网ETF回测失败: {e}")
    
    print("\n所有回测完成！")

if __name__ == "__main__":
    main()