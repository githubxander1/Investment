# te.py
import pandas as pd
import os
import sqlite3
from datetime import datetime

def test_read_excel_to_db():
    """测试读取Excel文件并转换为SQLite数据库"""
    # 测试文件路径
    # test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\trade_operation_history.xlsx'
    # test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Combination_portfolio_today.xlsx'
    # test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Strategy_portfolio_today.xlsx'
    # test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Robot_portfolio_today.xlsx'
    test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Lhw_portfolio_today.xlsx'

    # test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Combination_position.xlsx'
    # test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Strategy_position.xlsx'
    # test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Robots_position.xlsx'
    test_file = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\account_info.xlsx'

    if not os.path.exists(test_file):
        print(f"测试文件不存在: {test_file}")
        return

    try:
        print("=== 测试读取Excel文件并转换为数据库 ===")
        # 使用openpyxl引擎读取Excel文件
        with pd.ExcelFile(test_file, engine='openpyxl') as xls:
            print(f"文件中的工作表: {xls.sheet_names}")

            for sheet_name in xls.sheet_names:
            # 读取第一个工作表
            # if xls.sheet_names:
            #     sheet_name = xls.sheet_names[0]
                print(f"读取工作表: {sheet_name}")
                df = pd.read_excel(xls, sheet_name=sheet_name, engine='openpyxl')
                print(f"数据形状: {df.shape}")
                print("前5行数据:")
                print(df.head())
                print("\n数据列:")
                print(df.columns.tolist())

                # 将数据保存到SQLite数据库
                # db_file = "Combination_portfolio_today.db"
                # db_file = "Strategy_portfolio_today.db"
                # db_file = "Robot_portfolio_today.db"

                # db_file = "Combination_position.db"
                # db_file = "Strategy_position.db"
                # db_file = "Robots_position.db"
                db_file = "Lhw_data.db"
                conn = sqlite3.connect(db_file)

                # 清理表名，确保符合SQLite规范
                clean_table_name = "".join(c for c in sheet_name if c.isalnum() or c == '_')
                if clean_table_name[0].isdigit():
                    clean_table_name = "sheet_" + clean_table_name

                # 保存到数据库
                df.to_sql(clean_table_name, conn, if_exists='replace', index=False)
                print(f"\n✅ 数据已保存到数据库 {db_file} 中的表 {clean_table_name}")

                # 验证保存的数据
                saved_df = pd.read_sql_query(f"SELECT * FROM {clean_table_name}", conn)
                print(f"数据库中数据形状: {saved_df.shape}")
                print("数据库中前3行数据:")
                print(saved_df.head(3))

                conn.close()

            else:
                print("文件中没有工作表")

    except Exception as e:
        print(f"处理文件出错: {e}")

if __name__ == "__main__":
    # 运行测试
    # file_path = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\account_info.xlsx'
#     r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Combination_portfolio_today.xlsx',
#   r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Combination_position.xlsx',
#     r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\ETF组合对比.xlsx',
#   r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Lhw_portfolio_today.xlsx',
# r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Robots_position.xlsx',
#   r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Robot_portfolio_today.xlsx',
#     r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Strategy_portfolio_today.xlsx',
# r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\Strategy_position.xlsx',
# r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\trade_operation_history.xlsx',

    # db_file = 'account_info.db'
               # 'Combination_portfolio_today.db',
               # 'Combination_position.db',
               # 'ETF组合对比.db',
               # 'Lhw_portfolio_today.db',
               # 'Robots_position.db',
               # 'Robot_portfolio_today.db',
               # 'Strategy_portfolio_today.db',
               # 'Strategy_position.db',
               # 'trade_operation_history.db'

    # for file_path in file_paths:
    # read_excel_to_db(file_path,db_file)
    test_read_excel_to_db()

    print("\n=== 测试完成 ===")
