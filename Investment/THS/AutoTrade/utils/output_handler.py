# output_handler.py
def format_output(dataframe, exclude_columns=None):
    """格式化输出，排除指定列"""
    exclude_columns = exclude_columns or []
    return dataframe.drop(columns=exclude_columns, errors='ignore')

def print_results(dataframe, exclude_columns=None):
    """打印结果"""
    if dataframe.empty:
        print("⚠️ 当前无数据")
        return

    formatted_df = format_output(dataframe, exclude_columns)
    print(formatted_df.to_string(index=False))
