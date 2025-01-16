# testcases/test_rename.py
import os
from pprint import pprint

import pytest

from others.测试相关.api_mind.logic.rename import rename
from others.测试相关.api_mind.utils.logger import logger
from others.测试相关.api_mind.utils.yaml_handler import read_yaml

# 读取测试数据
test_data_path = os.path.join(os.path.dirname(__file__), "..", "testdata", "test_data_rename.yaml")
test_data = read_yaml(test_data_path)["rename"]

@pytest.mark.parametrize('test_case', test_data,
                         ids=[case['case_name'] for case in test_data])
def test_rename(test_case, token):
    logger.info(f"开始 rename 测试: {test_case['case_name']}")
    response = rename(test_case["name"], token)
    pprint(response)
    logger.info(f"接口返回: {response}")

    assert response.get("code") == 200, f"请求失败，状态码: {response.get('code')}"
    logger.info(f"重命名测试结果: {test_case['case_name']}")

# if __name__ == '__main__':
#     pytest.main(['-vs', 'test_rename.py'])
