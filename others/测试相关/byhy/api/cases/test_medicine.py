import pandas as pd
import pytest
from utils.test_case_utils import read_test_cases, write_test_results, update_test_case

from others.测试相关.byhy.api.lib.logic import login, add_medicine, del_medicine

# 读取测试用例
test_cases_df = read_test_cases('data/medicine_data.xlsx', sheet_name='药品管理')

@pytest.mark.parametrize("test_case", test_cases_df.to_dict('records'))
def test_add_medicine(test_case):
    login('byhy', '88888888')

    test_data = eval(test_case['测试数据'])
    try:
        response = add_medicine(test_data['name'], test_data['desc'], test_data['sn'])
        if response['ret'] == 0:
            actual_result = response['msg']
            test_result = "Pass"
        else:
            actual_result = response['msg']
            test_result = "Fail"
    except Exception as e:
        actual_result = str(e)
        test_result = "Fail"

    # 更新测试结果
    update_test_case(test_cases_df, test_case['编号'], actual_result, test_result)

    # 写入测试结果
    write_test_results('data/medicine_data.xlsx', sheet_name='药品管理', test_cases_df=test_cases_df)
