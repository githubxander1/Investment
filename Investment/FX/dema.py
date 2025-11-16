# 1. 导入依赖库
import MetaTrader5 as mt5
import backtrader as bt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 2. 从MT5获取EURUSD历史数据（适配Backtrader格式）
def get_mt5_eurusd_data(start_date, end_date, timeframe=mt5.TIMEFRAME_H1):
    """
    从MT5获取EURUSD历史数据
    :param start_date: 开始日期（格式：datetime）
    :param end_date: 结束日期（格式：datetime）
    :param timeframe: 数据周期（MT5_TIMEFRAME_H1=1小时，可改TIMEFRAME_M15=15分钟等）
    :return: Backtrader兼容的DataFrame
    """
    # 连接MT5（若已打开MT5，自动关联当前登录账户）
    if not mt5.initialize():
        print("MT5连接失败！请检查客户端是否已启动并登录")
        mt5.shutdown()
        return None
    
    # 获取EURUSD数据（MT5返回的是列表，需转换为DataFrame）
    rates = mt5.copy_rates_range(
        symbol="EURUSD",
        timeframe=timeframe,
        start_date=mt5.datetime_to_timestamp(start_date),
        end_date=mt5.datetime_to_timestamp(end_date)
    )
    
    # 断开MT5连接（避免占用资源）
    mt5.shutdown()
    
    # 转换为DataFrame并适配Backtrader格式
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # 时间戳转日期
    df.rename(columns={
        'time': 'datetime',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'tick_volume': 'volume'  # Backtrader默认用tick_volume作为成交量
    }, inplace=True)
    df.set_index('datetime', inplace=True)  # 日期设为索引
    df = df[['open', 'high', 'low', 'close', 'volume']]  # 保留必要列
    
    return df

# 3. 编写双EMA交叉策略（核心逻辑）
class EmaCrossStrategy(bt.Strategy):
    """
    双EMA交叉策略：
    - 短期EMA（fast_ema）上穿长期EMA（slow_ema）→ 金叉，做多
    - 短期EMA下穿长期EMA → 死叉，做空
    - 每次交易固定手数，默认不设止损（可自行添加）
    """
    # 策略参数（可在回测时调整）
    params = (
        ('fast_ema_period', 20),  # 短期EMA周期（默认20）
        ('slow_ema_period', 50),  # 长期EMA周期（默认50）
        ('trade_size', 0.1),      # 每次交易手数（外汇1手=10万单位，0.1手=1万单位）
    )

    def __init__(self):
        # 初始化EMA指标（使用Backtrader内置指标）
        self.fast_ema = bt.indicators.EMA(
            self.data.close, period=self.params.fast_ema_period, plotname='短期EMA'
        )
        self.slow_ema = bt.indicators.EMA(
            self.data.close, period=self.params.slow_ema_period, plotname='长期EMA'
        )
        
        # 金叉/死叉信号（内置交叉指标）
        self.crossover = bt.indicators.CrossOver(self.fast_ema, self.slow_ema)
        
        # 记录当前持仓（0=无持仓，1=多头，-1=空头）
        self.position_status = 0

    def next(self):
        """每根K线执行一次（策略核心逻辑）"""
        # 金叉：短期EMA上穿长期EMA，且无多头持仓 → 做多
        if self.crossover > 0 and self.position_status != 1:
            # 先平仓（若有空头持仓）
            if self.position_status == -1:
                self.close()  # 平掉空头
            # 开多头
            self.buy(size=self.params.trade_size)
            self.position_status = 1
            print(f"做多信号：{self.data.datetime.date()} | 价格：{self.data.close[0]}")
        
        # 死叉：短期EMA下穿长期EMA，且无空头持仓 → 做空
        elif self.crossover < 0 and self.position_status != -1:
            # 先平仓（若有多头持仓）
            if self.position_status == 1:
                self.close()  # 平掉多头
            # 开空头
            self.sell(size=self.params.trade_size)
            self.position_status = -1
            print(f"做空信号：{self.data.datetime.date()} | 价格：{self.data.close[0]}")

# 4. 回测配置与运行
if __name__ == "__main__":
    # ------------ 回测参数设置（可自定义修改）------------
    START_DATE = datetime(2023, 1, 1)  # 回测开始日期（2年前数据，足够验证）
    END_DATE = datetime(2025, 1, 1)    # 回测结束日期
    TIMEFRAME = mt5.TIMEFRAME_H1       # 数据周期（H1=1小时，推荐新手用；可改M15=15分钟）
    FAST_EMA = 20                      # 短期EMA周期
    SLOW_EMA = 50                      # 长期EMA周期
    TRADE_SIZE = 0.1                   # 每次交易手数（0.1手适合新手，风险低）
    INIT_CASH = 10000                  # 初始资金（1万美元，符合外汇账户常见规模）
    COMMISSION = 0.0002                # 交易手续费（0.02%，外汇经纪商常见费率）
    SLIPPAGE = 0.0001                  # 滑点（1个点，EURUSD 1点=0.0001，模拟真实交易）
    
    # ------------ 步骤1：获取MT5的EURUSD数据 ------------
    print("正在从MT5获取EURUSD数据...")
    data = get_mt5_eurusd_data(START_DATE, END_DATE, TIMEFRAME)
    if data is None or data.empty:
        print("数据获取失败！请检查MT5配置和EURUSD合约")
        exit()
    print(f"数据获取成功：共 {len(data)} 根K线")
    
    # ------------ 步骤2：配置Backtrader回测引擎 ------------
    cerebro = bt.Cerebro()  # 初始化回测引擎
    cerebro.broker.set_cash(INIT_CASH)  # 设置初始资金
    cerebro.broker.set_commission(commission=COMMISSION)  # 设置手续费
    cerebro.broker.set_slippage_fixed(slippage=SLIPPAGE)  # 设置固定滑点
    
    # 将数据导入回测引擎（name='EURUSD'，方便后续识别）
    bt_data = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(bt_data)
    
    # ------------ 步骤3：添加策略并设置参数 ------------
    cerebro.addstrategy(
        EmaCrossStrategy,
        fast_ema_period=FAST_EMA,
        slow_ema_period=SLOW_EMA,
        trade_size=TRADE_SIZE
    )
    
    # ------------ 步骤4：添加回测分析指标（评估策略用） ------------
    cerebro.addanalyzer(bt.analyzers.TotalReturn, _name='total_return')  # 总收益率
    cerebro.addanalyzer(bt.analyzers.MaxDrawDown, _name='max_drawdown')  # 最大回撤
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')  # 夏普比率（风险调整后收益）
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')  # 交易详情（胜率、盈亏比等）
    
    # ------------ 步骤5：运行回测 ------------
    print("开始回测...")
    results = cerebro.run()
    strategy = results[0]  # 获取策略结果
    
    # ------------ 步骤6：输出回测报告 ------------
    print("\n" + "="*50)
    print("                     回测报告（EURUSD 双EMA策略）")
    print("="*50)
    print(f"初始资金：{INIT_CASH} 美元")
    print(f"最终资金：{cerebro.broker.getvalue():.2f} 美元")
    print(f"总收益率：{strategy.analyzers.total_return.get_analysis()['rtot']*100:.2f}%")
    print(f"最大回撤：{strategy.analyzers.max_drawdown.get_analysis()['maxdrawdown']:.2f}%")
    print(f"夏普比率：{strategy.analyzers.sharpe_ratio.get_analysis()['sharperatio']:.2f}")  # ≥1.5较优
    
    # 交易详情分析
    trade_analysis = strategy.analyzers.trade_analyzer.get_analysis()
    total_trades = trade_analysis['total']['total']
    winning_trades = trade_analysis['won']['total']
    losing_trades = trade_analysis['lost']['total']
    print(f"\n总交易次数：{total_trades}")
    print(f"盈利交易次数：{winning_trades}")
    print(f"亏损交易次数：{losing_trades}")
    print(f"胜率：{winning_trades/total_trades*100:.2f}%")
    
    # 盈亏比（平均盈利/平均亏损）
    if losing_trades > 0:
        avg_win = trade_analysis['won']['pnl']['average']
        avg_lose = abs(trade_analysis['lost']['pnl']['average'])
        print(f"平均盈利：{avg_win:.2f} 美元")
        print(f"平均亏损：{avg_lose:.2f} 美元")
        print(f"盈亏比：{avg_win/avg_lose:.2f}")  # ≥1.5较优
    print("="*50)
    
    # ------------ 步骤7：可视化回测结果（K线+EMA+交易信号） ------------
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题
    cerebro.plot(
        style='candle',  # K线图样式
        iplot=False,     # 关闭交互式绘图（避免闪退）
        volume=False,    # 不显示成交量（外汇成交量参考意义小）
        figsize=(15, 10)
    )
    plt.title(f"EURUSD 双EMA策略回测结果（{FAST_EMA}EMA/{SLOW_EMA}EMA）", fontsize=14)
    plt.show()