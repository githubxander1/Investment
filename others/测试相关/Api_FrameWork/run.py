
import pytest
import time
import os
import requests
from common.com_yaml import c_yaml
if __name__ == '__main__':
    # 清除关联文件内容
    c_yaml('temp/refer.yaml')
    c_yaml('temp/failed_cases.yaml')
    # 启动测试
    pytest.main()
    # 等待报告结果生成
    time.sleep(2)
    # 生成报告
    os.system('allure generate temp/allure-results -o temp/allure-report --clean')
    # 读取测试结果
    with open('temp/statistics.txt', encoding='utf8') as fp:
        data = fp.read()
    print(data)
    # 推送企微信息
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xx'  # 杨翔学校测试群
    json = {
        "msgtype": "markdown",
        "markdown": {
            "content": f'''<font color="warning">xx（每周四8点20分执行）</font>\n{data}
            >测试报告：[点击查看测试报告](http://116.196.90.232:8001/job/security_auto_if/allure/) 账号test 密码123456
            >测试环境：http://xx/
            >用例说明：失败用例有红色和橙黄色标识，点击失败用例，点击右侧测试步骤下点击log查看失败日志，灰色为依赖用例执行失败而跳过的用例
            >维护人员：杨翔'''
        }
    }
    requests.post(url=url, json=json)