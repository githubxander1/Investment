import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt
from HoldingPeriodStrategy import SingleHoldingPeriodStrategy

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def extract_stock_name(filename):
    """从文件名中提取股票名称"""
    match = re.search(r'[\u4e00-\u9fff]+', filename)
    return match.group(0) if match else filename.split('.')[0]

def plot_results(results, stock_name, output_path):
    """绘制持有期收益图表"""
    periods = [r['持有期(天)'] for r in results]
    profits = [r['收益率(%)'] for r in results]

    plt.figure(figsize=(12, 6))
    plt.plot(periods, profits, 'o-', markersize=8)
    plt.title(f'{stock_name} - 不同持有期收益')
    plt.xlabel('持有期(天)')
    plt.ylabel('收益率(%)')
    plt.grid(True)
    plt.axhline(0, color='red', linestyle='--')

    # 标记最高点和最低点
    if profits:
        max_idx = profits.index(max(profits))
        min_idx = profits.index(min(profits))
        plt.annotate(f'{profits[max_idx]:.2f}%',
                     (periods[max_idx], profits[max_idx]),
                     xytext=(periods[max_idx], profits[max_idx] + 5))
        plt.annotate(f'{profits[min_idx]:.2f}%',
                     (periods[min_idx], profits[min_idx]),
                     xytext=(periods[min_idx], profits[min_idx] - 5))

    # 保存图表
    chart_path = os.path.join(output_path, f"{stock_name}_holding_period_chart.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def prepare_data(data_path, buy_date, filename):
    """准备股票数据，保持pandas时间戳格式"""
    try:
        # print(f"🔍 DEBUG: 准备数据 | 文件={filename} | 买入日={buy_date}")
        df = pd.read_csv(data_path, encoding='utf-8-sig', parse_dates=['日期'])

        # ✅ 保持原始pandas时间戳
        # print(f"🔍 DEBUG: 原始日期列类型={type(df['日期'].iloc[0])}")
        df['日期'] = pd.to_datetime(df['日期'])  # 保留datetime64类型
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
