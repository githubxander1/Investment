import os
import pytest


# 生成测试报告
pytest.main(["./main.py","-sv", "--alluredir", "./report/temp"])#执行 testcase.py 也可以执行某个文件夹下的所有文件
os.system("allure generate ./report/temp -o ./report/html --clean")#生成报告