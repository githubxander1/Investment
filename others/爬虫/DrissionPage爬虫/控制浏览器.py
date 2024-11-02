from DrissionPage import ChromiumPage
# from DrissionPage import WebPage
# 创建页面对象，并启动或接管浏览器
page = ChromiumPage()
# 跳转到登录页面
page.get('https://gitee.com/login')

# 定位到账号文本框，获取文本框元素
ele = page.ele('#user_login')
# 输入对文本框输入账号
ele.input('2695418206@qq.com')
# 定位到密码文本框并输入密码
page.ele('#user_password').input('gitee0520@xl')
# 点击登录按钮
page.ele('@value=登 录').click()