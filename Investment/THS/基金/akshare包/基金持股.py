import akshare as ak
import pandas as pd
import os
import yaml

def fetch_fund_hold_detail(fund_code, date):
    """
    获取指定基金在特定财报发布日期的持股明细。

    :param fund_code: 基金代码，例如 '510310' 表示华泰柏瑞沪深300ETF
    :param date: 财报发布日期，格式为 "xxxx-03-31", "xxxx-06-30", "xxxx-09-30", "xxxx-12-31"
    :return: 包含基金持股明细的 DataFrame 或 None 如果未找到数据
    """
    try:
        # 调用 stock_report_fund_hold_detail 接口获取数据
        fund_portfolio_hold_em_df = ak.fund_portfolio_hold_em(symbol=fund_code, date=date)
        return fund_portfolio_hold_em_df
    except Exception as e:
        print(f"获取数据时出错: {e}")
        return None

def save_fund_holdings_to_excel(fund_data_dict, fund_name_dict, filename):
    """
    将多个基金的持股明细保存到同一个 Excel 文件的不同工作表中。

    :param fund_data_dict: 字典，键为基金代码，值为对应的持股明细 DataFrame
    :param fund_name_dict: 字典，键为基金代码，值为对应的基金名称
    :param filename: 保存的 Excel 文件名
    """
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for fund_code, df in fund_data_dict.items():
            if not df.empty:
                # sheet_name = next((name for name, code in fund_name_dict.items()), fund_code)
                sheet_name = next((name for name, code in fund_name_dict.items() if code == fund_code), fund_code)
                print(sheet_name)  # 输出 '纳指100'
                # sheet_name = fund_name_dict.get(fund_code, fund_code)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

def compare_fund_holdings(fund_data_dict, fund_name_dict, filename):
    """
    对比不同基金的股票持仓情况，并将结果保存到 Excel 文件中。

    :param fund_data_dict: 字典，键为基金代码，值为对应的持股明细 DataFrame
    :param fund_name_dict: 字典，键为基金代码，值为对应的基金名称
    :param filename: 保存的 Excel 文件名
    """
    # 获取所有基金的股票代码集合
    all_stock_codes = set()
    for df in fund_data_dict.values():
        all_stock_codes.update(df['股票代码'])

    # 创建对比结果的 DataFrame
    comparison_df = pd.DataFrame(index=all_stock_codes)

    # 填充对比结果的 DataFrame
    for fund_code, df in fund_data_dict.items():
        fund_name = fund_name_dict.get(fund_code, fund_code)
        comparison_df[fund_name] = df.set_index('股票代码')['股票名称']

    # 重置索引
    comparison_df.reset_index(inplace=True)
    comparison_df.rename(columns={'index': '股票代码'}, inplace=True)

    # 保存对比结果到 Excel 文件
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        comparison_df.to_excel(writer, sheet_name='Comparison', index=False)

if __name__ == "__main__":
    # 读取基金代码和名称映射
    with open('股票基金代码和名称对应.yaml', 'r', encoding='utf-8') as file:
        fund_name_dict = yaml.safe_load(file)
        print(fund_name_dict)

    # 指定要查询的基金代码和财报发布日期
    fund_codes_to_query = ['159696', '159655']  # 示例基金代码
    date = '2024'  # 财报发布日期

    # 存储基金持股明细的字典
    fund_data_dict = {}

    # 获取指定基金在特定日期的持股明细
    for fund_code in fund_codes_to_query:
        data = fetch_fund_hold_detail(fund_code=fund_code, date=date)
        if data is not None:
            fund_data_dict[fund_code] = data
        else:
            fund_data_dict[fund_code] = pd.DataFrame()

    # 保存基金持股明细到 Excel 文件
    holdings_filename = 'fund_holdings.xlsx'
    # print(fund_code)
    save_fund_holdings_to_excel(fund_data_dict, fund_name_dict, holdings_filename)

    # 对比不同基金的股票持仓情况
    # comparison_filename = 'fund_holdings_comparison.xlsx'
    # compare_fund_holdings(fund_data_dict, fund_name_dict, comparison_filename)
