# testcases/test_login.py
import os
from pprint import pprint

import pytest

from others.测试相关.api_mind.logic.login import login
from others.测试相关.api_mind.utils.logger import logger
from others.测试相关.api_mind.utils.yaml_handler import read_yaml

# @pytest.fixture(scope="session")
# def api_client():
#     return APIClient("https://goapi.edrawsoft.cn")

test_data_path = os.path.join(os.path.dirname(__file__), "..", "testdata", "test_data_login.yaml")
test_data = read_yaml(test_data_path)["login"]

@pytest.mark.parametrize('test_case', test_data,
                         ids=[case["name"] for case in test_data])
def test_login(test_case):
    logger.info(f"Starting test case: {test_case['name']}")
    try:
        response = login(test_case["email"], test_case["password"])
        pprint(response)
        # logger.info(f"Login response: {response}")

        if test_case["name"] == 'success':
            assert "user_name" in response[0], f"Expected 'token' in response, got {response}"
        elif test_case["name"] == 'false':
            assert "user_name" not in response[0], f"Unexpected 'token' in response, got {response}"
        else:
            pytest.fail(f"Invalid test case name: {test_case['name']}")
    except Exception as e:
        logger.error(f"Test case {test_case['name']} failed with exception: {e}")
        pytest.fail(f"Test case {test_case['name']} failed with exception: {e}")

# if __name__ == '__main__':
#     pytest.main(["-s", "test_login.py"])
    # allure_report_filepath = os.path.join(os.path.dirname(__file__), "../reports", "allure-report")
    # pytest.main(["-s", "--alluredir=reports/allure-results", "test_login.py"])
