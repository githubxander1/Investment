from collector import fetch_data
# from analyzer import generate_trading_signals
# main.py
from collector import generate_trading_signals

from strategy import run_backtest
from risk_manager import RiskManager
from simulator import Simulator
from visualizer import plot_equity_curve, plot_positions

if __name__ == '__main__':
    # Step 1: 获取数据
    df_lhb = fetch_data('lhb')       # 获取龙虎榜
    df_zt = fetch_data('zt_pool')   # 获取涨停池
    df_lb = fetch_data('lb_pool')   # 获取连板池

    # Step 2: 生成交易信号
    candidates = generate_trading_signals(df_lhb, df_zt, df_lb)
    print("今日精选股池:")
    print(candidates)

    # Step 3: 回测
    print("\n开始回测...")
    results = run_backtest(strategy=LHBStrategy, data=candidates)
    print(results.summary())

    # Step 4: 模拟交易
    sim = Simulator(initial_capital=100000)
    for _, row in candidates.iterrows():
        sim.buy(row['stock_code'], price=row['price'], size=sim.get_position_size(sim.capital, row['price']))

    # Step 5: 可视化
    plot_equity_curve(sim.history)
    plot_positions(sim)
