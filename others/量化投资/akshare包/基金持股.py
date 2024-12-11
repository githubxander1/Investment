import akshare as ak

def fetch_fund_hold_detail(fund_code, report_date):
    """
    获取指定基金在特定财报发布日期的持股明细。

    :param fund_code: 基金代码，例如 '510310' 表示华泰柏瑞沪深300ETF
    :param report_date: 财报发布日期，格式为 "xxxx-03-31", "xxxx-06-30", "xxxx-09-30", "xxxx-12-31"
    :return: 包含基金持股明细的 DataFrame 或 None 如果未找到数据
    """
    try:
        # 调用 stock_report_fund_hold_detail 接口获取数据
        df = ak.stock_report_fund_hold_detail(symbol=fund_code, date=report_date)
        return df
    except Exception as e:
        print(f"获取数据时出错: {e}")
        return None

if __name__ == "__main__":
    # 指定要查询的基金代码和财报发布日期
    fund_code_to_query = '510310'  # 华泰柏瑞沪深300ETF为例
    report_date = '2020-12-31'  # 财报发布日期

    # 获取指定基金在特定日期的持股明细
    data = fetch_fund_hold_detail(fund_code=fund_code_to_query, report_date=report_date)

    if data is not None and not data.empty:
        print("查询到的持股明细如下：")
        print(data.head())
    else:
        print("未查询到数据或发生错误。")