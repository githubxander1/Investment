import pandas as pd
import numpy as np
import akshare as ak
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class TopBottomBacktester:
    def __init__(self, stock_code, start_date, end_date, initial_capital=100000):
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.data = None
        self.backtest_log = []
        
    def fetch_data(self):
        """使用akshare获取股票数据"""
        print(f"正在获取{self.stock_code}从{self.start_date}到{self.end_date}的数据...")
        try:
            # 首先尝试使用带市场前缀的代码
            try:
                stock_zh_a_daily_df = ak.stock_zh_a_daily(symbol=self.stock_code, start_date=self.start_date, end_date=self.end_date)
            except Exception as e1:
                # 如果失败，尝试不带市场前缀的代码
                code_without_market = self.stock_code.lstrip('sh').lstrip('sz')
                print(f"尝试不带市场前缀的代码: {code_without_market}")
                stock_zh_a_daily_df = ak.stock_zh_a_daily(symbol=code_without_market, start_date=self.start_date, end_date=self.end_date)
            
            # 打印数据结构以便调试
            print(f"原始数据列名: {stock_zh_a_daily_df.columns.tolist()}")
            print(f"数据前5行:\n{stock_zh_a_daily_df.head()}")
            
            # 创建结果DataFrame，确保包含所有需要的列
            df = pd.DataFrame()
            
            # 处理日期列
            if 'date' in stock_zh_a_daily_df.columns:
                df['date'] = pd.to_datetime(stock_zh_a_daily_df['date'])
            elif stock_zh_a_daily_df.index.name == 'date':
                df['date'] = pd.to_datetime(stock_zh_a_daily_df.index)
                df = df.reset_index(drop=True)
            else:
                # 如果没有日期列，尝试查找类似的列名
                date_columns = [col for col in stock_zh_a_daily_df.columns if 'date' in col.lower()]
                if date_columns:
                    df['date'] = pd.to_datetime(stock_zh_a_daily_df[date_columns[0]])
                else:
                    print("警告: 未找到日期列，使用索引作为日期")
                    df['date'] = pd.date_range(start=self.start_date, periods=len(stock_zh_a_daily_df))
            
            # 处理价格和成交量列
            for col in ['open', 'high', 'low', 'close', 'volume']:
                if col in stock_zh_a_daily_df.columns:
                    df[col] = stock_zh_a_daily_df[col]
                else:
                    # 尝试查找类似的列名
                    similar_cols = [c for c in stock_zh_a_daily_df.columns if col.lower() in c.lower()]
                    if similar_cols:
                        df[col] = stock_zh_a_daily_df[similar_cols[0]]
                    else:
                        print(f"警告: 未找到{col}列")
                        # 如果是收盘价，使用其他价格的平均值
                        if col == 'close' and all(x in df.columns for x in ['open', 'high', 'low']):
                            df['close'] = (df['open'] + df['high'] + df['low']) / 3
                        # 对于其他缺失的列，使用默认值
                        elif col == 'volume':
                            df['volume'] = 0
                        else:
                            # 对于开盘价、最高价、最低价，如果收盘价存在，使用收盘价的变体
                            if 'close' in df.columns:
                                if col == 'open':
                                    df['open'] = df['close'] * 0.99
                                elif col == 'high':
                                    df['high'] = df['close'] * 1.02
                                elif col == 'low':
                                    df['low'] = df['close'] * 0.98
            
            self.data = df
            print(f"数据处理成功，共{len(self.data)}条记录")
            print(f"处理后的数据列名: {self.data.columns.tolist()}")
            print(f"处理后的数据前5行:\n{self.data.head()}")
            return True
        except Exception as e:
            print(f"数据获取失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
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
        print("信号计算完成")
        return True
    
    def run_backtest(self):
        """运行回测"""
        if self.data is None:
            print("没有数据可进行回测")
            return False
        
        df = self.data.copy()
        self.capital = self.initial_capital
        self.position = 0
        self.backtest_log = []
        
        print("开始回测...")
        print(f"初始资金: {self.initial_capital}")
        print("交易记录:")
        print("日期\t\t类型\t价格\t数量\t金额\t持仓\t资金")
        
        # 遍历每一天
        for i in range(len(df)):
            date = df['date'].iloc[i]
            close_price = df['close'].iloc[i]
            
            # 检查买入信号
            if df['买入信号'].iloc[i] == 1 and self.position == 0:
                # 计算可以买入的数量（整数股）
                quantity = int(self.capital / close_price)
                if quantity > 0:
                    cost = quantity * close_price
                    self.position = quantity
                    self.capital -= cost
                    
                    # 记录交易
                    trade_record = {
                        'date': date,
                        'type': '买入',
                        'price': close_price,
                        'quantity': quantity,
                        'amount': cost,
                        'position': self.position,
                        'capital': self.capital
                    }
                    self.backtest_log.append(trade_record)
                    print(f"{date.strftime('%Y-%m-%d')}\t买入\t{close_price:.2f}\t{quantity}\t{cost:.2f}\t{self.position}\t{self.capital:.2f}")
            
            # 检查卖出信号
            elif df['卖出信号'].iloc[i] == 1 and self.position > 0:
                # 卖出所有持仓
                revenue = self.position * close_price
                self.capital += revenue
                quantity = self.position
                self.position = 0
                
                # 记录交易
                trade_record = {
                    'date': date,
                    'type': '卖出',
                    'price': close_price,
                    'quantity': quantity,
                    'amount': revenue,
                    'position': self.position,
                    'capital': self.capital
                }
                self.backtest_log.append(trade_record)
                print(f"{date.strftime('%Y-%m-%d')}\t卖出\t{close_price:.2f}\t{quantity}\t{revenue:.2f}\t{self.position}\t{self.capital:.2f}")
        
        # 最后一天如果还有持仓，强制卖出
        if self.position > 0:
            last_date = df['date'].iloc[-1]
            last_close = df['close'].iloc[-1]
            revenue = self.position * last_close
            self.capital += revenue
            quantity = self.position
            self.position = 0
            
            trade_record = {
                'date': last_date,
                'type': '强制卖出',
                'price': last_close,
                'quantity': quantity,
                'amount': revenue,
                'position': self.position,
                'capital': self.capital
            }
            self.backtest_log.append(trade_record)
            print(f"{last_date.strftime('%Y-%m-%d')}\t强制卖出\t{last_close:.2f}\t{quantity}\t{revenue:.2f}\t{self.position}\t{self.capital:.2f}")
        
        # 计算回测结果
        self.calculate_results()
        return True
    
    def calculate_results(self):
        """计算回测结果"""
        # 计算最终资金
        final_capital = self.capital
        
        # 计算总收益率
        total_return = (final_capital - self.initial_capital) / self.initial_capital * 100
        
        # 计算交易次数和胜率
        trade_count = len(self.backtest_log)
        winning_trades = 0
        
        # 分析交易对
        for i in range(0, len(self.backtest_log)-1, 2):
            if i+1 < len(self.backtest_log):
                buy_price = self.backtest_log[i]['price']
                sell_price = self.backtest_log[i+1]['price']
                if sell_price > buy_price:
                    winning_trades += 1
        
        win_rate = (winning_trades / (trade_count / 2)) * 100 if trade_count > 0 else 0
        
        # 打印回测结果
        print("\n回测结果:")
        print(f"最终资金: {final_capital:.2f}")
        print(f"总收益率: {total_return:.2f}%")
        print(f"交易次数: {trade_count}")
        print(f"胜率: {win_rate:.2f}%")
        
        # 保存回测结果
        self.save_backtest_log()
        
        # 绘制回测图表
        self.plot_backtest_results()
    
    def save_backtest_log(self):
        """保存回测日志"""
        if not self.backtest_log:
            print("没有交易记录可保存")
            return
        
        # 创建DataFrame
        log_df = pd.DataFrame(self.backtest_log)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"顶底指标回测记录_{self.stock_code}_{timestamp}.csv"
        filepath = "e:/git_documents/Investment/回测/" + filename
        
        # 保存到CSV文件
        log_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"详细回测记录已保存到: {filepath}")
        
        # 保存每日数据
        daily_df = self.data.copy()
        filename = f"顶底指标每日记录_{self.stock_code}_{timestamp}.csv"
        filepath = "e:/git_documents/Investment/回测/" + filename
        daily_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"每日详细回测记录已保存到: {filepath}")
    
    def plot_backtest_results(self):
        """绘制回测结果图表"""
        if self.data is None:
            print("没有数据可绘制图表")
            return
        
        df = self.data.copy()
        
        # 创建两个子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [3, 1]})
        
        # 第一个子图：K线图和指标
        ax1.plot(df['date'], df['close'], 'b-', label='收盘价')
        ax1.plot(df['date'], df['阻力'], 'g--', label='阻力')
        ax1.plot(df['date'], df['支撑'], 'r--', label='支撑')
        ax1.plot(df['date'], df['中线'], 'k:', label='中线')
        
        # 标记买入信号
        buy_signals = df[df['买入信号'] == 1]
        ax1.scatter(buy_signals['date'], buy_signals['close'], marker='^', color='red', s=100, label='买入信号')
        
        # 标记卖出信号
        sell_signals = df[df['卖出信号'] == 1]
        ax1.scatter(sell_signals['date'], sell_signals['close'], marker='v', color='green', s=100, label='卖出信号')
        
        # 设置标题和标签
        ax1.set_title(f'{self.stock_code} 顶底指标回测结果')
        ax1.set_ylabel('价格')
        ax1.grid(True)
        ax1.legend()
        
        # 第二个子图：趋势指标
        ax2.plot(df['date'], df['趋势'], 'y-', label='趋势')
        ax2.axhline(y=89, color='g', linestyle='--', label='顶(89)')
        ax2.axhline(y=50, color='k', linestyle=':', label='中(50)')
        ax2.axhline(y=11, color='r', linestyle='--', label='底(11)')
        
        # 标记超买超卖区域
        ax2.fill_between(df['date'], df['趋势'], 89, where=(df['趋势'] > 89), color='green', alpha=0.2)
        ax2.fill_between(df['date'], 11, df['趋势'], where=(df['趋势'] < 11), color='red', alpha=0.2)
        
        # 设置标签
        ax2.set_xlabel('日期')
        ax2.set_ylabel('趋势指标')
        ax2.grid(True)
        ax2.legend()
        
        # 设置日期格式
        locator = mdates.AutoDateLocator()
        formatter = mdates.ConciseDateFormatter(locator)
        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(formatter)
        ax2.xaxis.set_major_locator(locator)
        ax2.xaxis.set_major_formatter(formatter)
        
        plt.tight_layout()
        
        # 保存图表
        filename = f'顶底指标回测结果_{self.stock_code}.png'
        filepath = "e:/git_documents/Investment/回测/" + filename
        plt.savefig(filepath)
        print(f"图表已生成并保存为'{filename}'")
        
        # 显示图表
        plt.close()

def run_backtest_for_china_telecom():
    """运行中国电信的顶底指标回测"""
    # 计算近一年的日期范围
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    
    print(f"日期范围: {start_date} 到 {end_date}")
    
    # 中国电信的股票代码
    stock_code = "sh601728"  # 使用带市场前缀的代码
    stock_name = "中国电信"
    
    print(f"=====================================")
    print(f"开始回测 {stock_name}({stock_code}) 的顶底指标策略")
    print(f"=====================================")
    
    # 创建回测实例
    backtester = TopBottomBacktester(stock_code, start_date, end_date)
    
    # 执行回测流程
    if backtester.fetch_data() and backtester.calculate_indicators() and backtester.calculate_signals() and backtester.run_backtest():
        print(f"{stock_name} 回测完成！")
    else:
        print(f"{stock_name} 回测失败！")

if __name__ == "__main__":
    run_backtest_for_china_telecom()
    print("\n所有回测完成！")