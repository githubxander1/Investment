from string import Template

import jsonpath
import pytest
import requests


casedata = []
@pytest.mark.parametrize('case_info', casedata)
def test_case_execution(case_info):
    url = case_info['url']
    dict = g_var().set_dict(case_info)
    if '$' in url:
        #template的作用是如果url中遇到$，就替换成dict中的值
        url = Template(url).substitute(dict)


    req = requests.request(
        url=case_info['url'],
        method= case_info['method'],
        headers = case_info['headers'],
        data = case_info['data']
    )

    # 数据写入到对象中
    if case_info['提取参数'] is not None or case_info['提取参数'] != '':
        lst = jsonpath.jsonpath(req.json(), '$..'+case_info['提取参数'].split('='))
        g_var().set_dict(case_info['提取参数'].split('=')[0], lst[0])
    assert req.status_code == case_info['expected_code']

if __name__ == '__main__':
    pytest.main(['-vs', '--capture=sys', 'test_case_execution.py'])