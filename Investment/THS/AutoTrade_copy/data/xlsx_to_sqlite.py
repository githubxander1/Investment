# xlsx_to_sqlite.py
import os
import sqlite3
import pandas as pd
from datetime import datetime

def clean_column_name(column_name):
    """清理列名，移除特殊字符"""
    if isinstance(column_name, str):
        # 替换特殊字符为空格，然后替换空格为下划线
        cleaned = ''.join(c if c.isalnum() or c in ['_', ' '] else ' ' for c in str(column_name))
        # 将多个空格替换为单个下划线
        cleaned = '_'.join(cleaned.split())
        # 如果以数字开头，加上前缀
        if cleaned and cleaned[0].isdigit():
            cleaned = 'col_' + cleaned
        # 如果为空，使用默认名称
        if not cleaned:
            cleaned = 'unnamed_column'
        return cleaned.lower()
    return str(column_name)

def clean_table_name(table_name):
    """清理表名"""
    # 移除特殊字符
    cleaned = ''.join(c if c.isalnum() or c == '_' else '_' for c in table_name)
    # 确保不以数字开头
    if cleaned and cleaned[0].isdigit():
        cleaned = 'table_' + cleaned
    # 如果为空，使用默认名称
    if not cleaned:
        cleaned = 'unnamed_table'
    return cleaned.lower()

def process_data_types(df):
    """处理DataFrame中的数据类型"""
    df_copy = df.copy()

    for column in df_copy.columns:
        # 尝试转换数值类型
        if df_copy[column].dtype == 'object':
            # 尝试转换为数值
            numeric_series = pd.to_numeric(df_copy[column], errors='coerce')
            if not numeric_series.isna().all():
                df_copy[column] = numeric_series

            # 处理日期
            if df_copy[column].dtype == 'object':
                try:
                    # 尝试转换为日期
                    df_copy[column] = pd.to_datetime(df_copy[column], errors='coerce')
                except:
                    pass

        # 填充NaN值
        if df_copy[column].dtype in ['int64', 'float64']:
            df_copy[column] = df_copy[column].fillna(0)
        else:
            df_copy[column] = df_copy[column].fillna('')

    return df_copy

def convert_xlsx_to_sqlite(xlsx_path, db_path):
    """
    将Excel文件中的所有工作表转换为SQLite数据库中的表

    参数:
    xlsx_path: Excel文件路径
    db_path: SQLite数据库文件路径
    """
    print(f"处理文件: {xlsx_path}")

    try:
        # 使用openpyxl引擎读取Excel文件
        with pd.ExcelFile(xlsx_path, engine='openpyxl') as xls:
            sheet_names = xls.sheet_names
            print(f"  工作表数量: {len(sheet_names)}")

            # 遍历所有工作表
            for sheet_name in sheet_names:
                print(f"    处理工作表: {sheet_name}")

                try:
                    # 读取工作表数据
                    df = pd.read_excel(xls, sheet_name=sheet_name, engine='openpyxl')

                    # 清理列名（移除特殊字符，替换空格为下划线）
                    df.columns = [clean_column_name(col) for col in df.columns]

                    # 处理数据类型
                    df = process_data_types(df)

                    # 添加导入时间列
                    df['imported_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # 将DataFrame保存到SQLite数据库
                    # 表名使用文件名+工作表名的方式
                    file_name = os.path.splitext(os.path.basename(xlsx_path))[0]
                    table_name = f"{file_name}_{sheet_name}" if sheet_name != file_name else sheet_name

                    # 清理表名
                    table_name = clean_table_name(table_name)

                    # 连接SQLite数据库
                    conn = sqlite3.connect(db_path)

                    # 保存到数据库
                    df.to_sql(table_name, conn, if_exists='replace', index=False)
                    print(f"      ✓ 成功导入 {len(df)} 行数据到表 {table_name}")

                    # 关闭数据库连接
                    conn.close()

                except Exception as e:
                    print(f"      ❌ 处理工作表 {sheet_name} 时出错: {str(e)}")
                    continue

    except Exception as e:
        print(f"  ❌ 处理文件 {xlsx_path} 时出错: {str(e)}")

def find_xlsx_files(data_dir):
    """查找data目录下的所有xlsx文件"""
    xlsx_files = []

    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.xlsx') and not file.startswith('~$'):  # 排除临时文件
                xlsx_files.append(os.path.join(root, file))

    return xlsx_files

def main():
    """主函数"""
    # 项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))

    # data目录路径
    data_dir = os.path.join(project_root)

    # SQLite数据库路径
    db_path = os.path.join(project_root, 'data_storage.db')

    # 检查data目录是否存在
    if not os.path.exists(data_dir):
        print(f"目录 {data_dir} 不存在")
        return

    # 查找所有xlsx文件
    xlsx_files = find_xlsx_files(data_dir)

    if not xlsx_files:
        print("未找到任何xlsx文件")
        return

    print(f"找到 {len(xlsx_files)} 个xlsx文件:")
    for file in xlsx_files:
        print(f"  - {file}")

    # 转换每个xlsx文件
    for xlsx_file in xlsx_files:
        convert_xlsx_to_sqlite(xlsx_file, db_path)

    print(f"\n所有数据已导入到 {db_path}")

if __name__ == "__main__":
    main()
