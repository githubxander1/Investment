# data_loader.py
import os

import pandas as pd


def load_data(filename):
    file_path = os.path.abspath(os.path.dirname(__file__)) + '/股票数据/' + filename
    table = pd.read_csv(file_path, encoding='gbk', parse_dates=['交易日期'])
    # 打印数据的前几行，检查数据是否正确加载
    # print(table.head())
    table['股票代码'] = filename.split('.')[0]  # 假设文件名是股票代码.csv
    # 将数值列转换为Decimal类型
    # for col in ['收盘价_复权', '5日均线']:
    #     table[col] = table[col].apply(Decimal)
    return table
