# import pandas as pd
#
# # 创建两个 DataFrame
# old = pd.DataFrame({'股票名称': ['广信材料', '国防ETF'],
#                     '操作': ['买入', '卖出'],
#                     '新比例%': ['20.0', '10.0'],
#                     '时间': ['2025-03-26 13:51', '2025-03-26 10:36']})
# new = pd.DataFrame({'股票名称': ['广信材料', '国防ETF', '国防ETF', '优彩资源', '国防ETF'],
#                     '操作': ['买入', '卖出', '卖出', '卖出', '买入'],
#                     '新比例%': ['20.0', '10.0', '0.0', '0.0', '5.0'],
#                     '时间': ['2025-03-26 13:51', '2025-03-26 10:36', '2025-03-26 10:36', '2025-03-26 09:29', '2025-03-26 14:00']})
#
# print("测试merge:")
# print(old)
# print(new)
#
# new_data = new[~new.apply(tuple, axis=1).isin(old.apply(tuple, axis=1))]
# print("\n新增的记录:")
# print(new_data)
import os

from others.Investment.THS.AutoTrade.config.settings import ETF_Combination_TODAY_ADJUSTMENT_FILE
from others.Investment.THS.AutoTrade.utils.excel_handler import clear_sheet, read_excel

clear_sheet(ETF_Combination_TODAY_ADJUSTMENT_FILE, '所有今天调仓')
print(read_excel(ETF_Combination_TODAY_ADJUSTMENT_FILE, '所有今天调仓'))

# import sys
# print(f'当前路径：{sys.path[0]}')
# # 导入父目录的父目录模块
# others_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
# sys.path.append(others_dir)
# print(f'父目录的父目录路径：{others_dir}')
# print(f'包路径：{sys.path}')
