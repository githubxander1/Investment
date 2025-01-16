# testcases/test_rename_excel.py
import os
from pprint import pprint

import pytest

from others.测试相关.api_mind.logic.rename import rename
from others.测试相关.api_mind.utils.excel_handler import read_excel, write_excel
from others.测试相关.api_mind.utils.logger import logger

# 读取测试数据
test_data_path = os.path.join(os.path.dirname(__file__), "..", "testdata", "rename.xlsx")
test_data = read_excel(test_data_path)
pprint(test_data)

@pytest.mark.parametrize('test_case', test_data,
                         ids=[case['用例标题'] for case in test_data])
def test_rename(test_case, token):
    logger.info(f"开始 rename 测试: {test_case['用例标题']}")
    response = rename(test_case["测试数据"], token)
    pprint(response)
    logger.info(f"接口返回: {response}")

    # 断言预期结果
    expected_result = test_case["预期结果"]
    actual_result = response.json()
    test_result = "fail"
    try:
        assert actual_result == expected_result, f"请求失败，预期结果: {expected_result}, 实际结果: {actual_result}"
        test_result = "pass"
        logger.info(f"重命名测试结果: {test_case['用例标题']} - 通过")
    except AssertionError as e:
        logger.error(f"重命名测试结果: {test_case['用例标题']} - 失败: {e}")

    # 写回实际结果到 Excel 文件
    row_index = test_data.index(test_case) + 7  # 计算行索引，从第七行开始
    column_index_actual = 7  # 假设实际结果在第七列
    column_index_test_result = 8  # 假设测试结果在第八列

    write_excel(test_data_path, row_index, column_index_actual, str(actual_result))  # 将实际结果转换为字符串
    write_excel(test_data_path, row_index, column_index_test_result, test_result)  # 将测试结果写入第八列
    logger.info(f"实际结果和测试结果已写入到 Excel 文件: {test_data_path}")

# if __name__ == '__main__':
#     pytest.main(['-vs', 'test_rename_excel.py'])
