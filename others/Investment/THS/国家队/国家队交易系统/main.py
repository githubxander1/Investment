from national_team_analyzer import national_team_scoring
from backtest_engine import run_backtest
from simulator import Simulator  # 修复：从正确模块导入
from wechat_notifier import send_wechat_message
from plot_analyse import plot_equity_curve, plot_positions
from trading_strategy import NationalTeamStrategy  # 导入策略类

import akshare as ak

def get_real_time_price(stock_code):
    try:
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        if 'code' not in stock_zh_a_spot_df.columns or 'price' not in stock_zh_a_spot_df.columns:
            raise ValueError("数据结构异常，缺少必要字段")
        price = stock_zh_a_spot_df[stock_zh_a_spot_df['code'] == stock_code]['price'].values[0]
        return float(price)
    except Exception as e:
        print(f"获取 {stock_code} 实时价格失败: {e}")
        return 10.0  # 默认价格

if __name__ == '__main__':
    print("【1/5】获取国家队数据并评分选股...")
    candidates = national_team_scoring(filename="国家队持股.xlsx")
    print("今日精选股池:")
    print(candidates)

    # print("\n【2/5】发送微信通知...")
    # send_wechat_message(candidates)

    print("\n【3/5】开始回测...")
    # 使用正确的策略类名称
    results = run_backtest(strategy_class=NationalTeamStrategy, data=candidates)

    print(results.summary())

    print("\n【4/5】模拟交易...")
    sim = Simulator(initial_capital=100000)

    # 简化风险控制（因缺少risk_control模块）
    max_position = 0.05
    for i, row in candidates.iterrows():
        price = get_real_time_price(row['股票代码'])
        size = int(sim.capital * max_position / price)
        sim.buy(row['股票代码'], price=price, size=size)

    print("\n【5/5】可视化展示...")
    plot_equity_curve(sim.history)
    plot_positions(sim)
