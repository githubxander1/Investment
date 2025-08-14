import re
import os
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class SingleHoldingPeriodStrategy(bt.Strategy):
    """单个持有期策略"""
    params = (
        ('holding_period', None),
        ('print_log', True),
        ('stock_name', ''),
        ('buy_date', None)  # 接收字符串格式日期
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.sell_executed = False
        self.result = None
        self.buy_bar_index = 0  # 初始化买入bar索引
        self.buy_date = None    # 记录实际买入日期

        # ✅ 统一日期解析
        # print(f"🔍 DEBUG: 策略初始化 | 接收buy_date={self.params.buy_date}")

        if isinstance(self.params.buy_date, str):
            # print("🔄 转换字符串日期为Timestamp")
            self.target_date = pd.to_datetime(self.params.buy_date).date()
        elif isinstance(self.params.buy_date, pd.Timestamp):
            # print("🔄 转换Timestamp为date")
            self.target_date = self.params.buy_date.date()
        else:
            # print("🔄 直接使用date类型")
            self.target_date = self.params.buy_date

        # print(f"✅ 最终目标日期={self.target_date}({type(self.target_date)})")

    def next(self):
        current_date = self.datas[0].datetime.date(0)  # 获取date类型进行比较

        # 增强日期调试信息
        # debug_msg = (
        #     # f"[{self.p.stock_name}] 当前日期={current_date}({type(current_date)}) | "
        #     f"目标日期={self.target_date}({type(self.target_date)}) | "
        #     f"日期相等={current_date == self.target_date} | "
        #     f"持仓={bool(self.position)}"
        # )
        # print(debug_msg)

        # 买入逻辑
        if current_date == self.target_date and not self.position:
            if not self.order:
                self.log(f'✅ 建仓 @ {self.data_close[0]:.2f}')
                self.order = self.buy()
                self.buy_price = self.data_close[0]
                self.buy_bar_index = len(self)  # 记录买入时的bar索引
                self.buy_date = current_date    # 记录实际买入日期

        # 卖出逻辑：持有期满
        elif self.position and (len(self) - self.buy_bar_index) >= self.params.holding_period:
            self.log(f'💸 卖出 @ {self.data_close[0]:.2f}')
            self.order = self.close()
            self.sell_price = self.data_close[0]
            self.sell_executed = True
            self.sell_date = current_date  # 记录卖出日期

            # 计算并记录结果
            profit_pct = (self.sell_price / self.buy_price - 1) * 100
            self.result = {
                '股票': self.params.stock_name,
                '买入日期': self.buy_date.strftime("%Y-%m-%d"),  # 记录买入日期
                '卖出日期': current_date.strftime("%Y-%m-%d"),   # 记录卖出日期
                '买入价': self.buy_price,
                '卖出价': self.sell_price,
                '持有期(天)': self.params.holding_period,
                '收益率(%)': round(profit_pct, 2)
            }
            print(f"📊 交易结果: {self.result}")

    def log(self, txt, dt=None):
        if self.p.print_log:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt} [策略] {txt}')

def prepare_data(data_path, buy_date, filename):
    """准备股票数据，保持pandas时间戳格式"""
    try:
        # print(f"🔍 DEBUG: 准备数据 | 文件={filename} | 买入日={buy_date}")
        df = pd.read_csv(data_path, encoding='utf-8-sig', parse_dates=['日期'])

        # ✅ 保持原始pandas时间戳
        # print(f"🔍 DEBUG: 原始日期列类型={type(df['日期'].iloc[0])}")
        df['日期'] = pd.to_datetime(df['日期'])  # 保留datetime64类型，变成pandas标准时间格式
        df.set_index('日期', inplace=True)      # 使用pandas.Timestamp索引
        # print(f"🔍 DEBUG: 转换后索引类型={type(df.index[0])}")

        # 🔍 调试增强
        # print(f"[DEBUG] {filename} 首行日期类型: {type(df.index[0])}")
        # print(f"[DEBUG] 示例日期值: {df.index[0]}")
        # print(f"[DEBUG] 时间范围: {df.index[0]} ~ {df.index[-1]}")

        # ✅ 窗口筛选优化
        window_start = buy_date - pd.Timedelta(days=2)  # 使用原始Timestamp
        # print(f"🔍 DEBUG: 窗口开始={window_start}({type(window_start)})")
        df = df[df.index >= window_start]
        # print(f"🔍 DEBUG: 筛选后数据范围: {df.index[0]} ~ {df.index[-1]}")

        # 验证买入日
        days_diff = (df.index - buy_date).days
        # print(f"🔍 DEBUG: 买入日{buy_date}附近数据存在性检查")
        if not (pd.Series(days_diff).abs() <= 2).any():
            print(f"⏰ 数据延迟预警: 缺少目标日期±2天范围数据")
            return None, None

        # 列名映射
        df.rename(columns={
            '开盘': 'open',
            '最高': 'high',
            '最低': 'low',
            '收盘': 'close',
            '成交量': 'volume'
        }, inplace=True)

        stock_name = extract_stock_name(filename)
        return df, stock_name

    except Exception as e:
        print(f"❌ 数据处理失败: {str(e)}")
        if 'df' in locals() and not df.empty:
            print(f"📄 文件结构示例:\n{df.head().to_string()}")
        return None, None

def extract_stock_name(filename):
    """从文件名中提取股票名称"""
    match = re.search(r'[\u4e00-\u9fff]+', filename)
    return match.group(0) if match else filename.split('.')[0]

def get_stock_price_data(stock_name):
    """获取股票价格数据"""
    file_path = os.path.join(data_dir, f"{stock_name}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path, index_col=0, parse_dates=True)
    else:
        print(f"⚠️ 文件不存在: {file_path}")
        return None
# HoldingPeriodStrategy.py

def plot_results(results, stock_name, output_path, price_data=None):
    """绘制持有期收益与价格对比图表（双Y轴）"""
    # 准备数据
    periods = [r['持有期(天)'] for r in results]
    profits = [r['收益率(%)'] for r in results]
    buy_date = pd.to_datetime(results[0]['买入日期'])

    # 计算每个周期对应的日期
    profit_dates = [buy_date + pd.Timedelta(days=p) for p in periods]

    # 创建图表
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # 绘制收益曲线（左侧Y轴）
    line1 = ax1.plot(profit_dates, profits, 'o-', markersize=8, color='blue', label='收益率')
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('收益率(%)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True)
    ax1.axhline(0, color='red', linestyle='--', alpha=0.3)

    # 格式化日期轴
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, ha='right')  # 日期倾斜45度

    # 标注最高点和最低点
    if profits:
        max_idx = profits.index(max(profits))
        min_idx = profits.index(min(profits))
        # 添加标注（包含周期天数）
        ax1.annotate(f"{periods[max_idx]}天\n{profits[max_idx]:.2f}%",
                     (profit_dates[max_idx], profits[max_idx]),
                     xytext=(5, 5), textcoords='offset points',
                     bbox=dict(boxstyle='round,pad=0.3', fc='blue', alpha=0.1))
        ax1.annotate(f"{periods[min_idx]}天\n{profits[min_idx]:.2f}%",
                     (profit_dates[min_idx], profits[min_idx]),
                     xytext=(5, -15), textcoords='offset points',
                     bbox=dict(boxstyle='round,pad=0.3', fc='blue', alpha=0.1))

    # 绘制价格曲线（右侧Y轴）
    if price_data is not None and not price_data.empty:
        # 截取与最长周期匹配的时间段
        max_period = max(periods)
        end_date = buy_date + pd.Timedelta(days=max_period)

        # 截取价格数据（包含买入日前20天用于显示买入前走势）
        price_start_date = buy_date - pd.Timedelta(days=20)
        price_data_sub = price_data[(price_data.index >= price_start_date) &
                                   (price_data.index <= end_date)]

        # 绘制价格曲线
        ax2 = ax1.twinx()
        line2 = ax2.plot(price_data_sub.index, price_data_sub['close'],
                        color='green', linewidth=1, label='收盘价')
        ax2.set_ylabel('价格', color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        # 标记买入点
        if results:
            try:
                buy_price = price_data.loc[buy_date, 'close']
                ax2.scatter(buy_date, buy_price, color='red', s=100,
                           marker='^', label='买入点')
            except KeyError:
                print(f"⚠️ 价格数据缺失: {buy_date} 不存在于价格数据中")

        # 合并图例
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.1, 0.9))
    else:
        ax1.text(0.5, 0.5, '无价格数据', ha='center', va='center',
                transform=ax1.transAxes, fontsize=14, alpha=0.5)

    # 设置标题
    plt.title(f'{stock_name} 收益率与价格走势对比\n（显示周期：{max(periods)}天）',
             fontsize=14, pad=20)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    chart_path = os.path.join(output_path, f"{stock_name}_combined_chart.png")
    plt.savefig(chart_path)
    plt.close()

    return chart_path




def run_backtest(df, stock_name, buy_date, period):
    # print(f"🔍 DEBUG: 开始回测 | 股票={stock_name} | 持有期={period}天 | 买入日={buy_date}")
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.broker.setcash(10000.0)

    # 添加数据
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    # ✅ 统一时间格式传递
    buy_date_str = buy_date.strftime('%Y-%m-%d')
    # print(f"🔍 DEBUG: 策略参数 | buy_date={buy_date_str}(str) | 原类型={type(buy_date)}")
    cerebro.addstrategy(
        SingleHoldingPeriodStrategy,
        stock_name=stock_name,
        holding_period=period,
        buy_date=buy_date_str,  # 统一使用字符串格式
        print_log=True
    )

    # 运行回测
    print("🔄 执行回测引擎...")
    results = cerebro.run()
    strat = results[0]
    return strat

if __name__ == '__main__':
    # 设置路径
    data_dir = '../国家队/龙虎榜联动分析交易系统/stock_data'
    output_path = '../国家队/龙虎榜联动分析交易系统/backtest_results_低位锁定'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 定义选股日（假设选股日是2024-06-13）
    selection_date = '2024-06-13'
    # 计算买入日（选股日+1）
    buy_date = pd.to_datetime(selection_date) + pd.Timedelta(days=1)
    print(f"买入日: {buy_date.date()}")

    # 定义持有期列表
    holding_periods = [5, 10, 20, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300]

    # 创建汇总结果DataFrame
    summary_results = []

    # 遍历所有CSV文件
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            print(f"\n{'='*50}")
            print(f"开始回测: {filename}")

            # 构建完整文件路径
            data_path = os.path.join(data_dir, filename)

            try:
                # 使用pandas读取CSV文件
                df = pd.read_csv(data_path, encoding='utf-8-sig', parse_dates=['日期'])
                df['日期'] = pd.to_datetime(df['日期']).dt.date  # 强制转换为date类型
                df.set_index('日期', inplace=True)

                print('前2条\n', df.head(2))

                # 确保数据包含买入日
                if buy_date.date() not in df.index:
                    print(f"警告: {filename} 数据不包含买入日 {buy_date.date()}")
                    print(f"数据日期范围: {df.index[0]} → {df.index[-1]}")
                    continue

                # 重命名列以符合Backtrader的PandasData格式
                df.rename(columns={
                    '开盘': 'open',
                    '最高': 'high',
                    '最低': 'low',
                    '收盘': 'close',
                    '成交量': 'volume'
                }, inplace=True)

                # 提取股票名称
                stock_name = extract_stock_name(filename)
                print(f"股票名称: {stock_name}")

                # 创建Excel写入器
                excel_file = os.path.join(output_path, f"{stock_name}_周期回报.xlsx")
                writer = pd.ExcelWriter(excel_file)

                # 存储所有持有期结果
                stock_results = []

                # 遍历每个持有期
                for period in holding_periods:
                    # print(f"\n--- 回测持有期: {period}天 ---")

                    # 创建新的cerebro实例
                    cerebro = bt.Cerebro()
                    cerebro.broker.setcash(10000.0)

                    # 添加数据
                    data = bt.feeds.PandasData(dataname=df)
                    cerebro.adddata(data)

                    # 添加策略
                    cerebro.addstrategy(
                        SingleHoldingPeriodStrategy,
                        stock_name=stock_name,
                        holding_period=period,
                        buy_date=buy_date.date(),  # 确保传递date类型
                        print_log=True
                    )

                    # 运行回测
                    # print(f"数据开始日期: {df.index[0].date()}")
                    # print(f"数据结束日期: {df.index[-1].date()}")
                    # print(f"买入日: {buy_date.date()}")
                    # print('初始资金: %.2f' % cerebro.broker.getvalue())

                    # 运行策略
                    strat = cerebro.run()[0]

                    # print('最终资金: %.2f' % cerebro.broker.getvalue())

                    # 收集结果
                    if strat.result:
                        result_df = pd.DataFrame([strat.result])
                        result_df.to_excel(writer, sheet_name=f'{period}天', index=False)
                        stock_results.append(strat.result)
                        # print(f"持有期 {period}天 收益: {strat.result['收益率(%)']:.2f}%")
                    else:
                        print(f"持有期 {period}天 未完成交易")
                #
                # 保存股票结果到Excel
                if stock_results:
                    writer.save()
                    # print(f"📊 {stock_name} 持有期收益结果已保存至: {excel_file}")

                # 绘制收益图表
                if stock_results:
                    chart_path = plot_results(stock_results, stock_name, output_path, df)
                    # print(f"📈 收益图表已保存至: {chart_path}")

                # 打印股票汇总结果
                if stock_results:
                    stock_summary = pd.DataFrame(stock_results)
                    # print(f"\n{stock_name} 汇总结果:")
                    # print(stock_summary[['持有期(天)', '收益率(%)']].to_string(index=False))

            except Exception as e:
                print(f"回测 {filename} 失败: {str(e)}")
                import traceback
                traceback.print_exc()

            print(f"{'='*50}\n")

    # 保存所有股票的汇总结果
    if summary_results:
        summary_df = pd.DataFrame(summary_results)
        summary_file = os.path.join(output_path, "所有股票持有期收益汇总.xlsx")
        summary_df.to_excel(summary_file, index=False)

        # 打印汇总结果
        print("\n所有股票持有期收益汇总:")
        print(summary_df.to_string(index=False))
        print(f"📋 汇总结果已保存至: {summary_file}")

        # 绘制汇总图表
        plt.figure(figsize=(14, 8))
        for stock in summary_df['股票'].unique():
            stock_data = summary_df[summary_df['股票'] == stock]
            plt.plot(stock_data['持有期(天)'], stock_data['收益率(%)'], 'o-', label=stock)

        plt.title('不同股票在不同持有期的收益对比')
        plt.xlabel('持有期(天)')
        plt.ylabel('收益率(%)')
        plt.legend()
        plt.grid(True)
        plt.axhline(0, color='red', linestyle='--')

        chart_path = os.path.join(output_path, "所有股票持有期收益对比.png")
        plt.savefig(chart_path)
        print(f"📊 所有股票收益对比图表已保存至: {chart_path}")
