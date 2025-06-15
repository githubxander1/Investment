import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from BacktestUtils import *
from HoldingPeriodStrategy import SingleHoldingPeriodStrategy

def main():
    # 设置路径
    data_dir = 'stock_data'
    output_path = 'backtest_results'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # ✅ 保持 datetime 类型
    selection_date = '2024-06-13'
    buy_date = pd.to_datetime(selection_date) + pd.Timedelta(days=1)
    print(f"📅 买入日期: {buy_date}")
    # print(f"🔄 DEBUG: 选股日={selection_date}(str) -> 买入日={buy_date}")

    periods = [2, 5, 10, 20, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300]

    summary_results = []
    print(f"📢 开始日期筛选: {buy_date}")

    for filename in os.listdir(data_dir):
        if not filename.endswith('.csv'):
            continue

        data_path = os.path.join(data_dir, filename)
        # print(f"\n🔍 DEBUG: 处理文件={filename} | 买入日期={buy_date}")
        df, stock_name = prepare_data(data_path, buy_date, filename)

        if df is None or not stock_name:
            print(f"🚫 跳过数据缺失股票: {filename}")
            continue

        print(f"\n{'=' * 60}")
        # ✅ 正确显示日期
        print(f"🔄 正式回测: {stock_name} | 数据周期: {df.index[0]} → {df.index[-1]}")
        # print(f"🔍 DEBUG: 数据首行类型={type(df.index[0])} | 末行类型={type(df.index[-1])}")

        # 存储所有持有期结果
        stock_results = []

        # 🧪 多周期回测
        for period in periods:
            # print(f"🔄 DEBUG: 开始回测 {stock_name} 持有期={period}天 | 买入日={buy_date}")
            strat = run_backtest(df, stock_name, buy_date, period)
            if strat.result:
                # 添加额外信息
                strat.result['买入日期'] = buy_date.strftime('%Y-%m-%d')
                stock_results.append(strat.result)
                summary_results.append({
                    **strat.result,
                    '测试持有期': period
                })

                # 打印每个周期的详细结果
                r = strat.result
                print(f"✅ {stock_name} {period}天结果: "
                      f"买入日={r['买入日期']} | 卖出日={r['卖出日期']} | "
                      f"收益率={r['收益率(%)']:.2f}% | "
                      f"买入价={r['买入价']:.2f} | 卖出价={r['卖出价']:.2f}")

        # 保存个股结果到Excel（使用默认引擎）
        if stock_results:
            result_df = pd.DataFrame(stock_results)
            excel_file = os.path.join(output_path, f"{stock_name}_周期回报.xlsx")
            try:
                # 尝试使用xlsxwriter，失败时使用默认引擎
                with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                    result_df.to_excel(writer, index=False)
            except ModuleNotFoundError:
                print("⚠️ xlsxwriter未安装，使用默认引擎")
                result_df.to_excel(excel_file, index=False)
            print(f"📖 个股历史记录: {excel_file}")

        # 绘制并保存收益图表
        if stock_results:
            chart_path = plot_results(stock_results, stock_name, output_path)
            print(f"📈 收益图表已保存至: {chart_path}")

        print(f"{'='*50}\n")

    # 保存所有股票的汇总结果
    if summary_results:
        # 移除重复字段
        summary_df = pd.DataFrame(summary_results).drop(columns=['测试持有期'])

        summary_file = os.path.join(output_path, "所有股票持有期收益汇总.xlsx")
        try:
            # 尝试使用xlsxwriter，失败时使用默认引擎
            with pd.ExcelWriter(summary_file, engine='xlsxwriter') as writer:
                summary_df.to_excel(writer, index=False)
        except ModuleNotFoundError:
            print("⚠️ xlsxwriter未安装，使用默认引擎")
            summary_df.to_excel(summary_file, index=False)

        # 打印汇总结果
        print("\n📋 所有股票持有期收益汇总:")
        # 价格也打印出来
        summary_df = summary_df[['股票', '买入日期', '买入价', '卖出日期', '卖出价', '持有期(天)', '收益率(%)']]
        print(summary_df)
        # print(summary_df[['股票', '买入日期', '', '卖出日期', '', '持有期(天)', '收益率(%)']].to_string(index=False))
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

if __name__ == '__main__':
    main()
