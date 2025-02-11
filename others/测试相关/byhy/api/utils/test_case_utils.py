import pandas as pd

def read_test_cases(file_path, sheet_name):
    """读取测试用例"""
    return pd.read_excel(file_path, sheet_name=sheet_name)

def write_test_results(file_path, sheet_name, test_cases_df):
    """写入测试结果"""
    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
        test_cases_df.to_excel(writer, sheet_name=sheet_name, index=False)

def update_test_case(test_cases_df, test_id, actual_result, test_result):
    """更新单个测试用例的结果"""
    test_cases_df.loc[test_cases_df['编号'] == test_id, '实际结果'] = actual_result
    test_cases_df.loc[test_cases_df['编号'] == test_id, '测试结果'] = test_result
