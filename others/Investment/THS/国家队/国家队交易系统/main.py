from national_team_analyzer import national_team_scoring
from backtester import run_backtest, LHBStrategy
from simulate_trade import Simulator
from risk_control import RiskManager
from wechat_notifier import send_wechat_message
from plot_analyse import plot_equity_curve, plot_positions

import akshare as ak

def get_real_time_price(stock_code):
    try:
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        price = stock_zh_a_spot_df[stock_zh_a_spot_df['code'] == stock_code]['price'].values[0]
        return float(price)
    except Exception as e:
        print(f"获取 {stock_code} 实时价格失败: {e}")
        return 10.0  # 默认价格

# 在 main.py 中使用
for i, row in candidates.iterrows():
    candidates.at[i, 'price'] = get_real_time_price(row['股票代码'])

if __name__ == '__main__':
    print("【1/5】获取国家队数据并评分选股...")
    candidates = national_team_scoring(filename="国家队持股.xlsx")
    print("今日精选股池:")
    print(candidates)

    print("\n【2/5】发送微信通知...")
    send_wechat_message(candidates)

    print("\n【3/5】开始回测...")
    # 假设你有一个函数 run_backtest 可以接受 data 参数进行回测
    from backtester import run_backtest
    results = run_backtest(strategy=LHBStrategy, data=candidates)
    print(results.summary())

    print("\n【4/5】模拟交易...")
    sim = Simulator(initial_capital=100000)
    risk_manager = RiskManager(max_position=0.05)

    for _, row in candidates.iterrows():
        size = risk_manager.get_position_size(sim.capital, price=row['price'])
        sim.buy(row['股票代码'], price=row['price'], size=size)

    print("\n【5/5】可视化展示...")
    plot_equity_curve(sim.history)
    plot_positions(sim)
