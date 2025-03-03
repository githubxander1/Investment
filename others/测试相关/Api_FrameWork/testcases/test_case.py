import pytest
from pathlib import Path
from common.com_caseflow import caseflow
from common.com_yaml import r_yaml
import logging
# 第1步：定义测试类
class TestCase:
    ...
# 第2步：定义一个创建测试用例的函数
def create_case(path):
    # 处理用例文件为空
    case_info_collection = r_yaml(path)
    if case_info_collection is None:
        logging.info(f'\n此用例文件{path}读取用例集结果为空')
    else:
        @pytest.mark.parametrize('case_info', case_info_collection)
        def foo(self, case_info):
            # 处理用例之间依赖用例执行失败后，跳过某些用例
            depend_cases = case_info.get('depend', False)
            failed_cases = r_yaml('temp/failed_cases.yaml')
            if depend_cases and failed_cases:
                for depend_case in depend_cases:
                    if depend_case in failed_cases:
                        pytest.skip()
            # 设置allure报告的分类
            allure.dynamic.epic(case_info.get('epic', None))
            allure.dynamic.feature(case_info.get('feature', None))
            allure.dynamic.story(case_info.get('story', None))
            allure.dynamic.title(case_info.get('title', None))
            # 执行用例流程
            caseflow(case_info)
        return foo
# 第3步：获取testcases下所有测试用例的yaml文件
case_yaml_paths = Path(__file__).parent.glob(f"testcases/*/*.yaml")
for case_yaml_path in case_yaml_paths:
    # 获取yaml文件的名称（不要扩展名），用于自动创建测试函数
    case_yaml_name = case_yaml_path.stem
    # 使用反射setattr每次循环都向测试类中创建一个测试用例
    setattr(TestCase, "test_" + case_yaml_name, create_case(case_yaml_path))