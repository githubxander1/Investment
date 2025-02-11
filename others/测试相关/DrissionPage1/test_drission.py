# import time
# from DrissionPage1 import ChromiumPage
#
# # from DrissionPage1.easy_set import set_paths
#
# # set_paths(browser_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
#
# pom = ChromiumPage()
# pom.get('https://designer.vivo.com.cn/#/login')
# ele = pom.ele("@placeholder=支持邮箱/用户名登录").input('yourname')
# pom.ele('@placeholder=请输入密码').input("yourpassword")
# pom.ele("登录").click()
# time.sleep(1000)
from DrissionPage._pages.web_page import WebPage

# from others.测试相关.DrissionPage1 import WebPage

# d: 操作浏览器模式
page = WebPage('d')
page.get('http://www.baidu.com')
page.ele('#kw').input('DrissionPage1')
page.ele('@value=百度一下').click(wait_loading=True)

# 切换到s模式: 收发包模式
page.change_mode()
results = page.eles('tag:h3')
for result in results:
    print(result.text)