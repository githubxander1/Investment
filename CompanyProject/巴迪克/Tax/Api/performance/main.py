import os

import allure
import locust

if __name__ == '__main__':
    # mkdir -p reports/allure-results reports/html


    # Step 1: 启动 Locust 压测
    os.system(locust -f locustfile.py)
    
    # Step 2: 运行 pytest 性能测试
    pytest --alluredir=./reports/allure-results tests/test_api_performance.py
    
    # Step 3: 查看 Allure 报告
    allure open ./reports/allure-results
    
    pytest --alluredir=./reports/allure-results tests/test_api_performance.py
    allure serve ./reports/allure-results
