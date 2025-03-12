import akshare as ak
import pandas as pd

stock_report_fund_hold_df = ak.stock_report_fund_hold(symbol="基金持仓", date="20240930")
stock_report_fund_hold_df = stock_report_fund_hold_df.head(20)
stock_report_fund_hold_df.to_csv("stock_report_fund_hold.csv", encoding="gbk")
print(stock_report_fund_hold_df)
