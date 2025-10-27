# -*- coding: utf-8 -*-
# 功能：抓取东方财富网分时数据，用pandas转为DataFrame（便于数据分析）

import urllib.request
import pandas as pd
from urllib.error import URLError, HTTPError


def get_eastmoney_fenshi_with_pandas(secid="1.688103"):
    """
    抓取分时数据并转为DataFrame
    :param secid: 股票标识（格式：市场.股票代码，1=沪市，0=深市，如1.688103、0.300059）
    :return: 分时数据DataFrame（无数据则返回空DataFrame）
    """
    # 1. 构造请求URL（参数含义：fields1=基础字段，fields2=分时字段，mpi=最大数据量）
    url = (
        f'http://16.push2.eastmoney.com/api/qt/stock/details/sse'
        f'?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55'  # f51=时间，f52=价格等（需参考接口文档）
        f'&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281'  # mpi=最大返回2000条数据
        f'&fltt=2&pos=-0&secid={secid}'  # secid=目标股票标识
    )

    # 2. 发送请求并读取响应
    try:
        with urllib.request.urlopen(url=url, timeout=10) as response:
            # 响应格式为 "data:{...}"，需去除前缀"data:"
            data_str = response.readline().decode('utf-8').lstrip('data:')
            df = pd.read_json(data_str)
            details = df.get('details', [])
            #details:09:15:02,32.86,1901,0,4

            time = details[0][0]
            price = details[0][1]
            volume = details[0][2]



            if not data_str:
                print("响应为空，未获取到数据")
                return pd.DataFrame()
    except HTTPError as e:
        print(f"请求错误（状态码：{e.code}）：{e.reason}")
        return pd.DataFrame()
    except URLError as e:
        print(f"URL错误或网络问题：{e.reason}")
        return pd.DataFrame()

    # 3. 解析数据并转为DataFrame
    try:
        # eval() 将字符串转为字典（注意：仅信任已知来源数据，避免安全风险）
        data_dict = eval(data_str)
        fenshi_data = data_dict.get('data', {})
        if not fenshi_data:
            print("数据字典中无分时数据")
            return pd.DataFrame()
        # 转为DataFrame（列名对应fields2的字段，如f51、f52等）
        df = pd.DataFrame(fenshi_data)
    except (SyntaxError, KeyError) as e:
        print(f"数据解析失败：{e}")
        return pd.DataFrame()

    return df


# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 抓取沪市688103的分时数据（secid=1.688103）
    stock_code = "600030"
    df_fenshi = get_eastmoney_fenshi_with_pandas(secid=f"1.{stock_code}")#1为沪市，0为深市
    print(f"DataFrame形状：{df_fenshi.shape}")  # 打印数据行数和列数
    if not df_fenshi.empty:
        print("\nDataFrame前5行：")
        print(df_fenshi.head())
        # 可选：导出为Excel或CSV
        df_fenshi.to_excel(f"{stock_code}分时数据.xlsx", index=False)
        df_fenshi.to_csv(f"{stock_code}分时数据.csv", index=False, encoding="utf-8-sig")