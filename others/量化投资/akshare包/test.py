import akshare as ak
import pandas as pd

# 获取指定类型的开放式基金规模数据
try:
    fund_scale_open_sina_df = ak.fund_scale_open_sina(symbol='股票型基金')
    print("\n开放式基金规模数据:")
    print(fund_scale_open_sina_df)

    # 将数据保存到 Excel 文件
    output_file = 'fund_scale_open_sina.xlsx'
    fund_scale_open_sina_df.to_excel(output_file, index=False)
    print(f"\n数据已成功保存到 {output_file}")
except Exception as e:
    print(f"获取开放式基金规模数据时出错: {e}")

try:
   fund_scale_open_sina_df = ak.fund_scale_open_sina(symbol='股票型基金')
   print("\n开放式基金规模数据:")
   print(fund_scale_open_sina_df)

   # 将数据保存到 Excel 文件
   output_file = 'fund_scale_open_sina.xlsx'
   fund_scale_open_sina_df.to_excel(output_file, index=False)
   print(f"\n数据已成功保存到 {output_file}")
except Exception as e:
   print(f"获取开放式基金规模数据时出错: {e}")
