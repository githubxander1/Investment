import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class CCI_Backtester:
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
        
    def fetch_data(self):
        """使用akshare获取股票数据"""
        print(f"正在获取{self.stock_code}从{self.start_date}到{self.end_date}的数据...")
        
        # 尝试使用akshare获取数据
        try:
            # 使用akshare的股票历史行情接口
            df = ak.stock_zh_a_hist(symbol=self.stock_code, period="daily", 
                                   start_date=self.start_date, end_date=self.end_date, 
                                   adjust="qfq")
            
            # 重新组织数据
            df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low',
                '收盘': 'close',
                '成交量': 'volume'
            }, inplace=True)
            
            # 将日期转换为datetime类型并设置为索引
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # 按照日期排序
            df.sort_index(inplace=True)
            
            self.data = df
            print(f"数据获取成功，共{len(df)}条记录")
            return True
        except Exception as e:
            print(f"使用akshare获取数据失败: {e}")
            
            # 生成模拟数据作为演示
            print("生成模拟数据用于演示...")
            date_range = pd.date_range(start=self.start_date, end=self.end_date, freq='B')
            np.random.seed(42)
            base_price = 25
            prices = [base_price]
            for _ in range(1, len(date_range)):
                # 生成随机价格变动
                change = np.random.normal(0, 0.5)
                new_price = max(1, prices[-1] + change)
                prices.append(new_price)
            
            df = pd.DataFrame({
                'open': [p * (1 + np.random.normal(0, 0.01)) for p in prices],
                'high': [p * (1 + np.random.normal(0.01, 0.01)) for p in prices],
                'low': [p * (1 - np.random.normal(0.01, 0.01)) for p in prices],
                'close': prices,
                'volume': np.random.randint(100000, 10000000, size=len(date_range))
            }, index=date_range)
            
            self.data = df
            print(f"模拟数据生成成功，共{len(df)}条记录")
            return True
        
        return False
    
    def calculate_indicators(self):
        """计算优化后的CCI指标"""
        if self.data is None:
            print("没有数据，无法计算指标")
            return False
        
        df = self.data.copy()
        
        # 计算VAR1, VAR2, VAR3
        df['VAR1'] = (2 * df['close'] + df['high'] + df['low']) / 4
        df['VAR2'] = df['low'].rolling(window=34).min()
        df['VAR3'] = df['high'].rolling(window=34).max()
        
        # 计算AA指标线 - 简化计算方法
        df['CCI_raw'] = ((df['VAR1'] - df['VAR2']) / (df['VAR3'] - df['VAR2'])) * 100
        # 使用EMA计算AA（平滑后的CCI）
        df['AA'] = df['CCI_raw'].ewm(span=13, adjust=False).mean()
        
        # 计算BB指标线
        df['BB'] = df['AA'].ewm(span=2, adjust=False).mean()
        
        # 计算买入信号1: AA上穿BB且AA<20
        df['买入信号1'] = ((df['AA'] > df['BB']) & (df['AA'].shift(1) <= df['BB'].shift(1)) & 
                          (df['AA'] < 20)).astype(int)
        
        # 计算买入信号2: AA上穿22且BB<AA
        df['买入信号2'] = ((df['AA'] > 22) & (df['AA'].shift(1) <= 22) & 
                          (df['BB'] < df['AA'])).astype(int)
        
        # 综合买入信号
        df['买入信号'] = (df['买入信号1'] | df['买入信号2']).astype(int)
        
        # 计算卖出信号: BB上穿AA且AA>80.3，使用FILTER过滤重复信号
        df['卖出信号_raw'] = ((df['BB'] > df['AA']) & (df['BB'].shift(1) <= df['AA'].shift(1)) & 
                             (df['AA'] > 80.3)).astype(int)
        
        # 模拟FILTER函数，3天内只取第一个信号
        df['卖出信号'] = 0
        last_signal = -10  # 初始化为足够小的值
        for i in range(len(df)):
            if df['卖出信号_raw'].iloc[i] == 1 and (i - last_signal) >= 3:
                df.loc[df.index[i], '卖出信号'] = 1
                last_signal = i
        
        self.data = df
        print("指标计算完成")
        return True
    
    def backtest(self):
        """执行回测"""
        if self.data is None:
            print("没有数据，无法进行回测")
            return False
        
        df = self.data.copy()
        self.capital = self.initial_capital
        self.position = 0
        self.trades = []
        
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
        print("日期		类型	价格	数量	金额	持仓	资金")
        
        for i in range(len(df)):
            date = df.index[i]
            close_price = df['close'].iloc[i]
            
            # 买入信号
            if df['买入信号'].iloc[i] == 1 and self.position == 0:
                # 计算可以买入的数量（整手）
                quantity = int(self.capital // (close_price * 100)) * 100
                if quantity > 0:
                    cost = quantity * close_price
                    self.position = quantity
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
                    self.backtest_log.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'type': '买入',
                        'price': close_price,
                        'quantity': quantity,
                        'amount': cost,
                        'position': self.position,
                        'capital': self.capital,
                        'signal_type': '买入信号1' if df['买入信号1'].iloc[i] == 1 else '买入信号2'
                    })
                    
                    print(f"{date.strftime('%Y-%m-%d')}	买入	{close_price:.2f}	{quantity}	{cost:.2f}	{self.position}	{self.capital:.2f}")
            
            # 卖出信号
            elif df['卖出信号'].iloc[i] == 1 and self.position > 0:
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
                self.backtest_log.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'type': '卖出',
                    'price': close_price,
                    'quantity': self.position,
                    'amount': revenue,
                    'position': 0,
                    'capital': self.capital,
                    'signal_type': '卖出信号'
                })
                
                print(f"{date.strftime('%Y-%m-%d')}	卖出	{close_price:.2f}	{self.position}	{revenue:.2f}	0	{self.capital:.2f}")
                self.position = 0
        
        # 回测结束时如果还有持仓，强制卖出
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
            
            print(f"{df.index[-1].strftime('%Y-%m-%d')}	强制卖出	{last_price:.2f}	{self.position}	{revenue:.2f}	0	{self.capital:.2f}")
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
        for i in range(1, len(self.trades), 2):
            if i < len(self.trades) and self.trades[i]['type'] in ['卖出', '强制卖出']:
                buy_trade = self.trades[i-1]
                sell_trade = self.trades[i]
                if sell_trade['amount'] > buy_trade['amount']:
                    winning_trades += 1
        
        if len(self.trades) >= 2:
            win_rate = winning_trades / (len(self.trades) / 2) * 100
            print(f"胜率: {win_rate:.2f}%")
            # 更新胜率到回测日志
            self.backtest_log[-1]['win_rate'] = win_rate
        
        # 保存详细回测记录到CSV文件
        self.save_backtest_log()
        
        return True
    
    def plot_results(self):
        """绘制回测结果图表"""
        if self.data is None:
            print("没有数据，无法绘制图表")
            return False
        
        df = self.data.copy()
        
        # 创建一个图形，包含多个子图
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
        fig.subplots_adjust(hspace=0.3)
        
        # 绘制价格图和买卖信号
        ax1.plot(df.index, df['close'], 'b-', label='收盘价')
        # 如果有OHLC数据，绘制蜡烛图
        if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
            # 绘制蜡烛图的主体部分
            for i in range(len(df)):
                date = df.index[i]
                open_price = df['open'].iloc[i]
                close_price = df['close'].iloc[i]
                high_price = df['high'].iloc[i]
                low_price = df['low'].iloc[i]
                
                # 根据涨跌设置颜色
                color = 'red' if close_price >= open_price else 'green'
                
                # 绘制实体
                ax1.bar(date, abs(close_price - open_price), bottom=min(open_price, close_price), 
                        width=0.6, color=color, alpha=0.7)
                # 绘制影线
                ax1.plot([date, date], [low_price, high_price], color=color, linewidth=1)
        
        # 标记买入信号
        buy_signals = df[df['买入信号'] == 1]
        ax1.scatter(buy_signals.index, buy_signals['close'], color='red', marker='^', s=100, label='买入信号')
        
        # 标记卖出信号
        sell_signals = df[df['卖出信号'] == 1]
        ax1.scatter(sell_signals.index, sell_signals['close'], color='green', marker='v', s=100, label='卖出信号')
        
        # 绘制交易点
        for trade in self.trades:
            if trade['type'] == '买入':
                ax1.scatter(trade['date'], trade['price'], color='red', marker='^', s=150)
            elif trade['type'] in ['卖出', '强制卖出']:
                ax1.scatter(trade['date'], trade['price'], color='green', marker='v', s=150)
        
        ax1.set_title(f'优化CCI指标回测 - {self.stock_code}')
        ax1.set_ylabel('价格')
        ax1.grid(True)
        ax1.legend()
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # 绘制AA和BB指标线
        ax2.plot(df.index, df['AA'], 'blue', label='AA')
        ax2.plot(df.index, df['BB'], 'red', label='BB')
        ax2.axhline(y=20, color='gray', linestyle='--', alpha=0.5, label='20线')
        ax2.axhline(y=80.3, color='gray', linestyle='--', alpha=0.5, label='80.3线')
        ax2.set_ylabel('AA/BB值')
        ax2.grid(True)
        ax2.legend()
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax2.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # 绘制资金曲线
        capital_history = [self.initial_capital]
        current_capital = self.initial_capital
        current_position = 0
        
        for i in range(len(df)):
            date = df.index[i]
            
            # 检查是否有交易发生在这一天
            for trade in self.trades:
                if trade['date'] == date:
                    current_capital = trade['capital']
                    current_position = trade['position']
                    break
            
            # 如果有持仓，计算总资产
            if current_position > 0:
                asset_value = current_capital + current_position * df['close'].iloc[i]
            else:
                asset_value = current_capital
            
            capital_history.append(asset_value)
        
        # 绘制总资产曲线
        ax3.plot(df.index, capital_history[1:], 'purple', label='总资产')
        ax3.axhline(y=self.initial_capital, color='gray', linestyle='--', alpha=0.5, label='初始资金')
        ax3.set_xlabel('日期')
        ax3.set_ylabel('资金')
        ax3.grid(True)
        ax3.legend()
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax3.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig('优化CCI回测结果.png', dpi=300)
        plt.show()
        
        print("图表已生成并保存为'优化CCI回测结果.png'")
        plt.close(fig)  # 关闭图表以释放内存
        return True
    
    def save_backtest_log(self):
        """保存详细回测记录到CSV文件"""
        if not self.backtest_log:
            print("没有回测记录可保存")
            return
        
        # 创建日志DataFrame
        log_df = pd.DataFrame(self.backtest_log)
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"优化CCI回测记录_{self.stock_code}_{timestamp}.csv"
        filepath = f"e:\git_documents\Investment\回测\{filename}"
        
        # 保存到CSV文件
        log_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"详细回测记录已保存到: {filepath}")

# 主函数
def main():
    # 计算最近一年的日期范围
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    
    # 创建回测实例 - 海康威视(002415)
    backtester = CCI_Backtester(
        stock_code='002415',  # 海康威视
        start_date=start_date,
        end_date=end_date,
        initial_capital=10000
    )
    
    # 执行回测流程
    if backtester.fetch_data():
        if backtester.calculate_indicators():
            if backtester.backtest():
                backtester.plot_results()
                print("\n回测完成！")

if __name__ == "__main__":
    main()