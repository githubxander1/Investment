import os

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("http://payok-test.com/merchant/payok-register-register.html")

# 定位文件上传输入框（根据实际HTML结构调整定位方式）
file_input = driver.find_element(By.ID, 'form1')

# 上传文件（替换为实际文件路径）

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)

# 文件路径配置
DATA_DIR = os.path.join(BASE_DIR, 'data')
# print(DATA_DIR)

# 日志文件路径
filepath = os.path.join(DATA_DIR, "合同.pdf")
print('文件存在' if os.path.exists(filepath) else '文件不存在')
file_input.send_keys(filepath)