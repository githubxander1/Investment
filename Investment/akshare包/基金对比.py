import akshare as ak
import pandas as pd

# 定义要对比的两个 ETF 代码
etf_codes = ["562500", "159819"]

for code in etf_codes:
    print(f"\n对比 ETF 代码: {code}")

    try:
        # 获取 ETF 的持仓比例
        fund_portfolio_hold_em_df = ak.fund_portfolio_hold_em(symbol=code, date="2024")
        top_10_holdings = fund_portfolio_hold_em_df.head(10).reset_index(drop=True)
        print(f"\nETF {code} 前十大持仓股:")
        print(top_10_holdings)
    except Exception as e:
        print(f"获取 ETF {code} 持仓比例时出错: {e}")

    try:
        # 获取 ETF 的基本信息
        fund_individual_basic_info_xq_df = ak.fund_individual_basic_info_xq(symbol=code)
        print(f"\nETF {code} 基本信息:")
        print(fund_individual_basic_info_xq_df)
    except KeyError as ke:
        print(f"JSON 数据中缺少 'data' 键: {ke}")
    except Exception as e:
        print(f"获取 ETF {code} 基本信息时出错: {e}")

    try:
        # 获取 ETF 的历史表现分析数据
        fund_individual_analysis_xq_df = ak.fund_individual_analysis_xq(symbol=code)
        print(f"\nETF {code} 历史表现分析数据:")
        print(fund_individual_analysis_xq_df)
    except Exception as e:
        print(f"获取 ETF {code} 历史表现分析数据时出错: {e}")

    try:
        # 获取 ETF 的盈利概率及平均收益
        fund_individual_profit_probability_xq_df = ak.fund_individual_profit_probability_xq(symbol=code)
        print(f"\nETF {code} 盈利概率及平均收益:")
        print(fund_individual_profit_probability_xq_df)
    except Exception as e:
        print(f"获取 ETF {code} 盈利概率及平均收益时出错: {e}")
