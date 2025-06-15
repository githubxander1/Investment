import os

import akshare as ak
import pandas as pd

def download_stock_data(stock_codes, save_path='stock_data'):
    """下载股票 K 线数据并保存为 CSV 文件"""
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for code in stock_codes:
        # 下载日 K 线数据
        stock_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="2022-06-15", end_date="2023-06-15")

        # 保存为 CSV 文件
        file_path = os.path.join(save_path, f"{code}.csv")
        stock_df.to_csv(file_path, index=False)
        print(f"数据已保存至 {file_path}")

# 示例：下载特定股票代码的数据
stock_codes = ['601800', '002601', '002028']  # 根据国家队持股数据挑选的股票代码
download_stock_data(stock_codes)
