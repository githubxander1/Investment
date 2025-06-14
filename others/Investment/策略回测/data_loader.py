# data_loader.py
import akshare as ak
import pandas as pd
import os
from datetime import datetime


DATA_DIR = "股票数据"  # 本地缓存目录

os.makedirs(DATA_DIR, exist_ok=True)


def get_stock_name(stock_code):
    """获取股票名称"""
    try:
        df = ak.stock_info_a_code_name()
        return df[df["code"] == stock_code]["name"].iloc[0]
    except Exception as e:
        return stock_code


def fetch_or_load_stock_data(stock_code, start_date="20240531", end_date=None):
    """
    如果本地存在对应股票CSV，则加载；
    否则通过 akshare 获取数据并保存到本地。
    """
    file_path = os.path.join(DATA_DIR, f"{stock_code}.csv")

    if os.path.exists(file_path):
        print(f"正在加载本地缓存数据: {file_path}")
        df = pd.read_csv(file_path, encoding="utf-8")
        df['交易日期'] = pd.to_datetime(df['交易日期'])
        return df

    print(f"未找到本地缓存数据，开始从 akshare 下载 {stock_code} ...")
    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")

    try:
        df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date)
        df.rename(columns={
            '日期': '交易日期',
            '开盘': '开盘价',
            '最高': '最高价',
            '最低': '最低价',
            '收盘': '收盘价',
            '成交量': '成交量'
        }, inplace=True)
        df['收盘价_复权'] = df['收盘价']
        df['股票代码'] = stock_code
        df['股票名称'] = get_stock_name(stock_code)

        df = df[['交易日期', '开盘价', '最高价', '最低价', '收盘价', '成交量', '收盘价_复权', '股票代码', '股票名称']]
        df.to_csv(file_path, index=False, encoding="utf-8")
        print(f"数据已保存至: {file_path}")
        return df

    except Exception as e:
        print(f"获取股票 {stock_code} 数据失败: {e}")
        return pd.DataFrame()
