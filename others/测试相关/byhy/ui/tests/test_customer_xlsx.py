import pandas as pd
import pytest

from others.测试相关.byhy.ui.pom.customer_page import CustomerPage
from others.测试相关.byhy.ui.pom.login_page import LoginPage
from others.测试相关.byhy.ui.utils.test_case_utils import read_test_cases, write_test_results, update_test_case

# 读取测试用例
test_cases_df = read_test_cases(r'D:\1document\1test\PycharmProject_gitee\others\测试相关\byhy\ui\data\byhy测试用例.xlsx')

@pytest.mark.parametrize("test_case", test_cases_df.to_dict('records'))
def test_add_customer(page, test_case):
    login_page = LoginPage(page)
    customer_page = CustomerPage(page)

    login_page.navigate()
    login_page.login("byhy", "88888888")

    test_data = eval(test_case['测试数据'])
    try:
        customer_page.add_customer(test_data['name'], test_data['phone'], test_data['address'])
        customer_page.delete_customer()
        actual_result = "成功添加"
        test_result = "Pass"
    except Exception as e:
        actual_result = str(e)
        test_result = "Fail"

    # 更新测试结果
    update_test_case(test_cases_df, test_case['序号'], actual_result, test_result)

    # 写入测试结果
    write_test_results(r'D:\1document\1test\PycharmProject_gitee\others\测试相关\byhy\ui\data\byhy测试用例.xlsx', test_cases_df)

if __name__ == '__main__':
    pytest.main(['-vs', 'test_customer_xlsx.py'])