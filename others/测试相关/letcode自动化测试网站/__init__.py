from selenium import webdriver

d=webdriver.Edge()
d.get('https://www.baidu.com')
d.implicitly_wait(10)