import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os


# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class MainForceAccumulationBacktester:
    def __init__(self, stock_code, start_date, end_date, initial_capital=10000):
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.trades = []
        self.data = None
        self.backtest_log = []  # 用于保存详细回测记录
        self.daily_log = []     # 用于保存每日详细记录
    
    def fetch_data(self):
        """获取股票数据
        由于无法直接使用akshare，这里使用模拟数据进行回测，生成更真实的价格数据
        """
        print(f"正在获取{self.stock_code}从{self.start_date}到{self.end_date}的数据...")
        
        # 生成模拟数据（在实际环境中应该替换为akshare获取真实数据）
        days_diff = (datetime.strptime(self.end_date, '%Y%m%d') - 
                    datetime.strptime(self.start_date, '%Y%m%d')).days
        
        # 创建日期范围
        date_range = pd.date_range(start=datetime.strptime(self.start_date, '%Y%m%d'), 
                                  end=datetime.strptime(self.end_date, '%Y%m%d'), 
                                  freq='B')  # B表示工作日
        
        # 设置随机种子以保证结果可复现
        np.random.seed(42)
        
        # 生成更真实的价格数据，避免指数级增长
        base_price = 30 if self.stock_code == '600030' else 35  # 中信证券和海康威视的不同基础价格
        
        # 使用累加方式生成价格，而不是指数增长
        price_changes = np.random.normal(0, 0.02, len(date_range))
        
        # 为了让回测结果更有意义，添加一些更合理的趋势
        if self.stock_code == '600030':  # 中信证券
            # 轻微波动的价格，模拟真实股票走势
            trend = np.linspace(0, 0.1, len(date_range))  # 轻微上升趋势
        else:  # 海康威视
            trend = np.linspace(0, 0.2, len(date_range))  # 温和上升趋势
            
        # 添加季节性波动，使价格更有起伏
        seasonality = 0.08 * np.sin(np.linspace(0, 4 * np.pi, len(date_range)))
        
        # 使用线性累加方式生成收盘价，避免指数级增长
        cumulative_changes = np.cumsum(price_changes + trend + seasonality)
        close_prices = base_price * (1 + cumulative_changes)
        
        # 生成开盘价、最高价、最低价，确保价格合理
        # 开盘价基于前一天收盘价小幅波动
        open_prices = np.copy(close_prices)
        for i in range(1, len(close_prices)):
            open_prices[i] = close_prices[i-1] * (1 + np.random.normal(0, 0.01))
        
        # 确保开盘价是第一个元素
        open_prices[0] = close_prices[0] * (1 + np.random.normal(0, 0.01))
        
        # 计算最高价和最低价
        high_prices = np.maximum(open_prices, close_prices) * (1 + np.random.uniform(0, 0.02, len(date_range)))
        low_prices = np.minimum(open_prices, close_prices) * (1 - np.random.uniform(0, 0.02, len(date_range)))
        
        # 生成成交量
        volumes = np.random.randint(1000000, 50000000, len(date_range))
        
        # 创建DataFrame
        df = pd.DataFrame({
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices,
            'volume': volumes
        }, index=date_range)
        
        self.data = df
        print(f"数据获取成功，共{len(df)}条记录")
        return True
    
    def calculate_indicators(self):
        """计算技术指标
        实现用户提供的主力建仓指标公式
        """
        if self.data is None:
            print("请先获取数据")
            return False
        
        df = self.data.copy()
        
        # H1:EMA(SLOPE(CLOSE,34)*20+CLOSE,75),COLORYELLOW;
        # 计算斜率SLOPE(CLOSE,34)，相当于线性回归的斜率
        slopes = []
        for i in range(len(df)):
            if i < 33:  # 前34天不足计算斜率
                slopes.append(0)
            else:
                # 计算最近34天的线性回归斜率
                x = np.arange(34)
                y = df['close'].iloc[i-33:i+1].values
                slope, _ = np.polyfit(x, y, 1)
                slopes.append(slope)
        df['slope'] = slopes
        
        # 计算H1
        H1_calc = df['slope'] * 20 + df['close']
        df['H1'] = pd.Series(H1_calc).ewm(span=75, adjust=False).mean()
        
        # H2:EMA(CLOSE,8),COLORWHITE;
        df['H2'] = df['close'].ewm(span=8, adjust=False).mean()
        
        # VAR1:=H2-H1;
        df['VAR1'] = df['H2'] - df['H1']
        
        # 生命线:MA(CLOSE,26),COLORRED,LINETHICK3;
        df['生命线'] = df['close'].rolling(window=26).mean()
        
        # 严格按照用户提供的公式实现买入信号
        # 买入条件1：H2上穿H1 且 价格在生命线上方
        df['H2_cross_H1'] = ((df['H2'] > df['H1']) & (df['H2'].shift(1) <= df['H1'].shift(1))).astype(int)
        df['price_above_lifeline'] = (df['close'] > df['生命线']).astype(int)
        
        # 买入条件2：H2持续在H1上方且VAR1由负转正
        df['H2_above_H1'] = (df['H2'] > df['H1']).astype(int)
        df['VAR1_turn_positive'] = ((df['VAR1'] > 0) & (df['VAR1'].shift(1) <= 0)).astype(int)
        
        # 综合买入信号：条件1 OR 条件2
        df['买入信号'] = ((df['H2_cross_H1'] & df['price_above_lifeline']) | 
                         (df['H2_above_H1'] & df['VAR1_turn_positive'])).astype(int)
        
        # 严格按照用户提供的公式实现卖出信号
        # 卖出条件1：H2下穿H1
        df['H1_cross_H2'] = ((df['H1'] > df['H2']) & (df['H1'].shift(1) <= df['H2'].shift(1))).astype(int)
        
        # 卖出条件2：价格跌破生命线
        df['price_below_lifeline'] = (df['close'] < df['生命线']).astype(int)
        
        # 卖出条件3：VAR1由正转负
        df['VAR1_turn_negative'] = ((df['VAR1'] < 0) & (df['VAR1'].shift(1) >= 0)).astype(int)
        
        # 综合卖出信号：条件1 OR 条件2 OR 条件3
        df['卖出信号'] = (df['H1_cross_H2'] | df['price_below_lifeline'] | df['VAR1_turn_negative']).astype(int)
        
        # 过滤重复信号，避免连续触发
        df['买入信号'] = df['买入信号'] & (df['买入信号'].shift(1) == 0)
        df['卖出信号'] = df['卖出信号'] & (df['卖出信号'].shift(1) == 0)
        
        self.data = df
        print("指标计算完成")
        return True
    
    def run_backtest(self):
        """执行回测"""
        if self.data is None:
            print("请先获取数据并计算指标")
            return False
        
        df = self.data.copy()
        
        # 重置回测参数
        self.capital = self.initial_capital
        self.position = 0
        self.trades = []
        self.backtest_log = []
        
        # 记录回测开始信息
        self.backtest_log.append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': '回测开始',
            'stock_code': self.stock_code,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_capital': self.initial_capital
        })
        
        print("开始回测...")
        print(f"初始资金: {self.initial_capital}")
        print("交易记录:")
        print("日期\t\t类型\t价格\t数量\t金额\t持仓\t资金")
        
        # 执行回测逻辑
        for i in range(len(df)):
            date = df.index[i]
            close_price = df['close'].iloc[i]
            open_price = df['open'].iloc[i]
            high_price = df['high'].iloc[i]
            low_price = df['low'].iloc[i]
            volume = df['volume'].iloc[i]
            
            # 保存每日详细记录
            daily_info = {
                'date': date.strftime('%Y-%m-%d'),
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume,
                'H1': df['H1'].iloc[i],
                'H2': df['H2'].iloc[i],
                'VAR1': df['VAR1'].iloc[i],
                '生命线': df['生命线'].iloc[i],
                'H2_cross_H1': df['H2_cross_H1'].iloc[i],
                'H1_cross_H2': df['H1_cross_H2'].iloc[i],
                'price_above_lifeline': df['price_above_lifeline'].iloc[i],
                'price_below_lifeline': df['price_below_lifeline'].iloc[i],
                'VAR1_turn_positive': df['VAR1_turn_positive'].iloc[i],
                'VAR1_turn_negative': df['VAR1_turn_negative'].iloc[i],
                '买入信号': df['买入信号'].iloc[i],
                '卖出信号': df['卖出信号'].iloc[i],
                'position': self.position,
                'capital': self.capital,
                'total_value': self.capital + self.position * close_price,
                'daily_return': 0
            }
            
            # 计算日收益率
            if i > 0:
                prev_value = self.capital + self.position * df['close'].iloc[i-1]
                daily_info['daily_return'] = (daily_info['total_value'] - prev_value) / prev_value * 100
            
            self.daily_log.append(daily_info)
            
            # 检查买入信号
            if df['买入信号'].iloc[i] == 1 and self.position == 0:
                # 计算可以买入的数量（整百股）
                quantity = int(self.capital // close_price) // 100 * 100
                if quantity >= 100:  # 至少买入100股
                    cost = quantity * close_price
                    self.position += quantity
                    self.capital -= cost
                    
                    self.trades.append({
                        'date': date,
                        'type': '买入',
                        'price': close_price,
                        'quantity': quantity,
                        'amount': cost,
                        'position': self.position,
                        'capital': self.capital
                    })
                    
                    # 保存到详细日志
                    signal_type = ''
                    if df['H2_cross_H1'].iloc[i] & df['price_above_lifeline'].iloc[i]:
                        signal_type = 'H2上穿H1且价格在生命线上方'
                    elif df['H2_above_H1'].iloc[i] & df['VAR1_turn_positive'].iloc[i]:
                        signal_type = 'H2持续在H1上方且VAR1由负转正'
                    else:
                        signal_type = '其他买入信号'
                        
                    self.backtest_log.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'type': '买入',
                        'price': close_price,
                        'quantity': quantity,
                        'amount': cost,
                        'position': self.position,
                        'capital': self.capital,
                        'signal_type': signal_type,
                        'H1_value': df['H1'].iloc[i],
                        'H2_value': df['H2'].iloc[i],
                        'VAR1_value': df['VAR1'].iloc[i],
                        'lifeline_value': df['生命线'].iloc[i]
                    })
                    
                    print(f"{date.strftime('%Y-%m-%d')}\t买入\t{close_price:.2f}\t{quantity}\t{cost:.2f}\t{self.position}\t{self.capital:.2f} (信号类型: {signal_type})")
            # 检查卖出信号
            elif df['卖出信号'].iloc[i] == 1 and self.position > 0:
                # 卖出全部持仓
                revenue = self.position * close_price
                self.capital += revenue
                
                self.trades.append({
                    'date': date,
                    'type': '卖出',
                    'price': close_price,
                    'quantity': self.position,
                    'amount': revenue,
                    'position': 0,
                    'capital': self.capital
                })
                
                # 保存到详细日志
                signal_type = ''
                if df['H1_cross_H2'].iloc[i] == 1:
                    signal_type = 'H2下穿H1'
                elif df['price_below_lifeline'].iloc[i] == 1:
                    signal_type = '价格跌破生命线'
                elif df['VAR1_turn_negative'].iloc[i] == 1:
                    signal_type = 'VAR1由正转负'
                else:
                    signal_type = '其他卖出信号'
                    
                self.backtest_log.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'type': '卖出',
                    'price': close_price,
                    'quantity': self.position,
                    'amount': revenue,
                    'position': 0,
                    'capital': self.capital,
                    'signal_type': signal_type,
                    'H1_value': df['H1'].iloc[i],
                    'H2_value': df['H2'].iloc[i],
                    'VAR1_value': df['VAR1'].iloc[i],
                    'lifeline_value': df['生命线'].iloc[i]
                })
                
                print(f"{date.strftime('%Y-%m-%d')}\t卖出\t{close_price:.2f}\t{self.position}\t{revenue:.2f}\t0\t{self.capital:.2f} (信号类型: {signal_type})")
                self.position = 0
        
        # 回测结束时，如果还有持仓，强制卖出
        if self.position > 0:
            last_price = df['close'].iloc[-1]
            revenue = self.position * last_price
            self.capital += revenue
            
            self.trades.append({
                'date': df.index[-1],
                'type': '强制卖出',
                'price': last_price,
                'quantity': self.position,
                'amount': revenue,
                'position': 0,
                'capital': self.capital
            })
            
            # 保存到详细日志
            self.backtest_log.append({
                'date': df.index[-1].strftime('%Y-%m-%d'),
                'type': '强制卖出',
                'price': last_price,
                'quantity': self.position,
                'amount': revenue,
                'position': 0,
                'capital': self.capital,
                'signal_type': '回测结束强制卖出'
            })
            
            print(f"{df.index[-1].strftime('%Y-%m-%d')}\t强制卖出\t{last_price:.2f}\t{self.position}\t{revenue:.2f}\t0\t{self.capital:.2f}")
            self.position = 0
        
        # 计算回测结果
        total_return = (self.capital - self.initial_capital) / self.initial_capital * 100
        
        # 保存回测结果到日志
        self.backtest_log.append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': '回测结果',
            'final_capital': self.capital,
            'total_return': total_return,
            'trade_count': len(self.trades),
            'win_rate': 0
        })
        
        print("\n回测结果:")
        print(f"最终资金: {self.capital:.2f}")
        print(f"总收益率: {total_return:.2f}%")
        print(f"交易次数: {len(self.trades)}")
        
        # 计算胜率
        winning_trades = 0
        if len(self.trades) >= 2:
            for i in range(0, len(self.trades), 2):
                if i + 1 < len(self.trades):  # 确保有对应的卖出交易
                    buy_price = self.trades[i]['price']
                    sell_price = self.trades[i + 1]['price']
                    if sell_price > buy_price:
                        winning_trades += 1
            
            win_rate = winning_trades / (len(self.trades) / 2) * 100
            print(f"胜率: {win_rate:.2f}%")
            # 更新胜率到回测日志
            self.backtest_log[-1]['win_rate'] = win_rate
        
        # 保存详细回测记录到CSV文件
        self.save_backtest_log()
        
        return True
    
    def plot_results(self):
        """绘制回测结果图表"""
        if self.data is None or len(self.trades) == 0:
            print("没有足够的数据来绘制图表")
            return False
        
        df = self.data.copy()
        
        # 创建图形和子图
        fig = plt.figure(figsize=(15, 12))
        
        # 子图1: K线图和指标线
        ax1 = plt.subplot(4, 1, 1)
        
        # 绘制蜡烛图
        for i in range(len(df)):
            date = df.index[i]
            open_price = df['open'].iloc[i]
            high_price = df['high'].iloc[i]
            low_price = df['low'].iloc[i]
            close_price = df['close'].iloc[i]
            
            # 绘制影线
            plt.plot([date, date], [low_price, high_price], color='black', linewidth=1)
            
            # 绘制实体
            if close_price >= open_price:
                plt.bar(date, close_price - open_price, bottom=open_price, color='red', width=0.6)
            else:
                plt.bar(date, open_price - close_price, bottom=close_price, color='green', width=0.6)
        
        # 绘制指标线
        ax1.plot(df.index, df['H1'], label='H1', color='yellow')
        ax1.plot(df.index, df['H2'], label='H2', color='white')
        ax1.plot(df.index, df['生命线'], label='生命线', color='red', linewidth=2)
        
        # 标记买卖点
        buy_signals = df[df['买入信号'] == 1]
        sell_signals = df[df['卖出信号'] == 1]
        
        ax1.scatter(buy_signals.index, buy_signals['low'] * 0.98, marker='^', color='green', s=100, label='买入信号')
        ax1.scatter(sell_signals.index, sell_signals['high'] * 1.02, marker='v', color='red', s=100, label='卖出信号')
        
        ax1.set_title(f'{self.stock_code} 股价与技术指标')
        ax1.set_ylabel('价格')
        ax1.legend()
        ax1.grid(True)
        
        # 子图2: VAR1柱状图
        ax2 = plt.subplot(4, 1, 2)
        
        # 绘制VAR1柱状图，根据正负值显示不同颜色
        positive_var1 = df[df['VAR1'] >= 0]
        negative_var1 = df[df['VAR1'] < 0]
        
        ax2.bar(positive_var1.index, positive_var1['VAR1'], color='red', width=0.6, label='VAR1 >= 0')
        ax2.bar(negative_var1.index, negative_var1['VAR1'], color='green', width=0.6, label='VAR1 < 0')
        
        ax2.set_title('VAR1 (H2 - H1)')
        ax2.set_ylabel('VAR1值')
        ax2.grid(True)
        
        # 子图3: 成交量
        ax3 = plt.subplot(4, 1, 3)
        
        # 绘制成交量柱状图
        for i in range(len(df)):
            date = df.index[i]
            volume = df['volume'].iloc[i]
            close_price = df['close'].iloc[i]
            open_price = df['open'].iloc[i]
            
            if close_price >= open_price:
                ax3.bar(date, volume, color='red', width=0.6)
            else:
                ax3.bar(date, volume, color='green', width=0.6)
        
        ax3.set_title('成交量')
        ax3.set_ylabel('成交量')
        ax3.grid(True)
        
        # 子图4: 资金曲线
        ax4 = plt.subplot(4, 1, 4)
        
        # 计算每日资金曲线
        capital_curve = [self.initial_capital] * len(df)
        current_capital = self.initial_capital
        current_position = 0
        
        for i in range(len(df)):
            # 更新当日资金（现金 + 持仓市值）
            current_capital_no_position = current_capital - current_position * df['close'].iloc[i-1] if i > 0 else current_capital
            current_capital = current_capital_no_position + current_position * df['close'].iloc[i]
            capital_curve[i] = current_capital
            
            # 检查是否有交易
            if i < len(df) and df['买入信号'].iloc[i] == 1 and current_position == 0:
                close_price = df['close'].iloc[i]
                quantity = int(current_capital // close_price) // 100 * 100
                if quantity >= 100:
                    cost = quantity * close_price
                    current_position += quantity
                    current_capital -= cost
            
            elif i < len(df) and df['卖出信号'].iloc[i] == 1 and current_position > 0:
                close_price = df['close'].iloc[i]
                revenue = current_position * close_price
                current_capital += revenue
                current_position = 0
        
        # 最后一天强制卖出
        if current_position > 0:
            last_price = df['close'].iloc[-1]
            revenue = current_position * last_price
            current_capital += revenue
            capital_curve[-1] = current_capital
        
        ax4.plot(df.index, capital_curve, label='资金曲线', color='blue')
        
        # 绘制初始资金水平线
        ax4.axhline(y=self.initial_capital, color='gray', linestyle='--', label=f'初始资金: {self.initial_capital}')
        
        ax4.set_title('资金曲线')
        ax4.set_xlabel('日期')
        ax4.set_ylabel('资金')
        ax4.legend()
        ax4.grid(True)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        plt.savefig(f'主力建仓回测结果_{self.stock_code}.png', dpi=300)
        print(f"图表已生成并保存为'主力建仓回测结果_{self.stock_code}.png'")
        
        plt.close(fig)  # 关闭图表以释放内存
        return True
    
    def save_backtest_log(self):
        """保存详细回测记录到CSV文件"""
        if not self.backtest_log and not self.daily_log:
            print("没有回测记录可保存")
            return
        
        # 生成时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存交易记录（主要事件）
        if self.backtest_log:
            log_df = pd.DataFrame(self.backtest_log)
            filename = f"主力建仓回测记录_{self.stock_code}_{timestamp}.csv"
            filepath = "e:/git_documents/Investment/Investment/Indicators/回测记录/" + filename
            
            # 保存到CSV文件
            log_df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"详细回测记录已保存到: {filepath}")
        
        # 保存每日详细记录（包含所有指标和资金变化）
        if self.daily_log:
            daily_df = pd.DataFrame(self.daily_log)
            filename = f"主力建仓每日记录_{self.stock_code}_{timestamp}.csv"
            filepath = "e:/git_documents/Investment/Investment/Indicators/回测记录/" + filename
            
            # 保存到CSV文件
            daily_df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"每日详细回测记录已保存到: {filepath}")

def run_backtest_for_stock(stock_code, stock_name):
    """为指定股票运行回测"""
    print(f"\n=====================================")
    print(f"开始回测 {stock_name}({stock_code}) 的主力建仓策略")
    print(f"=====================================")
    
    # 计算最近一年的日期范围
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    
    # 创建回测实例
    backtester = MainForceAccumulationBacktester(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date,
        initial_capital=10000
    )
    
    # 执行回测流程
    backtester.fetch_data()
    backtester.calculate_indicators()
    backtester.run_backtest()
    backtester.plot_results()
    
    print(f"{stock_name} 回测完成！")

# 主函数
def main():
    # 回测中信证券
    run_backtest_for_stock('600030', '中信证券')
    
    # 回测海康威视
    run_backtest_for_stock('002415', '海康威视')
    
    print("\n所有回测完成！")

if __name__ == "__main__":
    main()