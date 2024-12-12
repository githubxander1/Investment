import akshare as ak
import pandas as pd

# 下载北向资金数据
def download_northbound_data():
    stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="北向资金")
    stock_hsgt_hist_em_df = stock_hsgt_hist_em_df.head(10)
    return stock_hsgt_hist_em_df

# 计算阈值并执行策略
def execute_strategy(data):
    daily_returns = []
    position = 0  # 0表示空仓，1表示持有
    for i in range(len(data)):
        if i == 0:
            daily_returns.append(0)
            continue
        current_date = data.index[i]
        current_net_inflow = data['净流入额'].iloc[i]
        historical_data = data[:i]
        # 计算阈值
        upper_threshold, lower_threshold = calculate_thresholds(historical_data)
        if current_net_inflow > upper_threshold and position == 0:
            position = 1
            daily_returns.append((data['沪深300涨跌幅'].iloc[i] if i < len(data) else 0) * position)
        elif current_net_inflow < lower_threshold and position == 1:
            position = 0
            daily_returns.append((data['沪深300涨跌幅'].iloc[i] if i < len(data) else 0) * position)
        else:
            daily_returns.append((data['沪深300涨跌幅'].iloc[i] if i < len(data) else 0) * position)
    return daily_returns

# 计算阈值
def calculate_thresholds(historical_data):
    sorted_data = historical_data.sort_values(by='净流入额', ascending=False)
    third = len(sorted_data) // 3
    upper_threshold = sorted_data['净流入额'].iloc[third - 1]
    lower_threshold = sorted_data['净流入额'].iloc[2 * third - 1]
    return upper_threshold, lower_threshold

# 主函数
def main():
    # 下载数据
    northbound_data = download_northbound_data()
    # 合并沪股通和深股通数据（如果需要的话，根据实际数据结构进行合并操作）
    # 假设数据中已经包含了沪深300指数涨跌幅数据，如果没有，需要获取并合并
    # 这里简化处理，直接使用假设的数据
    data_with_returns = northbound_data.copy()
    # 执行策略
    daily_returns = execute_strategy(data_with_returns)
    # 计算策略净值
    strategy_net_value = [1]
    for ret in daily_returns:
        strategy_net_value.append(strategy_net_value[-1] * (1 + ret))
    # 输出策略净值
    print(pd.Series(strategy_net_value, index=data_with_returns.index))

if __name__ == "__main__":
    main()