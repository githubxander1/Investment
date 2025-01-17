from selenium import webdriver
from data import readExcel
from  element import *
import pytest
import allure

@allure.feature("登录模块")
class Test_Login():

    def setup_class(self):
        openUrl() #打开游览器输入网址

    lst = readExcel("login", 0, 3) #读取登录模块数据添加为列表然后赋值给变量
    @allure.story("登录成功用例")
    @pytest.mark.parametrize("name,pwd,text", lst)
    def test_01(self,name,pwd,text):
        login(name, pwd) #登录
        result = get_success_text()  #获取登录成功信息
        click_success_button()  #关闭登录成功提示框
        user_quit() #退出账号
        assert text in result

    lst=readExcel("login",3,7)

    @allure.story("登录失败用例")
    @pytest.mark.parametrize("name,pwd,text",lst)
    def test_02(self,name,pwd,text):
        login(name, pwd)         #登录
        result = get_fail_text() #获取登录失败信息
        click_fail_button() #关闭错误提示框
        close_login()  #关闭登录界面
        assert  text in result

    def teardown_class(self):
        brower_quit() #退出游览器

@allure.feature("贷款模块")
class Test_Borrow():
    def setup_class(self):
        openUrl()  # 打开游览器输入网址
        login("haizi", "123456")  # 登录
        click_success_button()  # 关闭登录成功提示框
        b_move_borrow()#鼠标悬浮在我要借款按钮
        b_click_applyBorrow()#点击申请借款
        b_click_apply()#点击立即申请

    lst = readExcel("borrow", 0, 2)
    @allure.story("验证标题输入框")
    @pytest.mark.parametrize('title,amount,apr,iframe,text',lst)
    def test_01(self,title,amount,apr,iframe,text):
        b_borrowtitle(title)#标题
        b_borrowAmount(amount)#金额
        b_borrowApr(apr)#利率
        b_iframe(iframe)#描述
        b_publishBnt()#提交审核
        result=b_errorText() #获取错误提示信息
        assert result==text
        b_errorBox()

    lst=readExcel("borrow", 2, 3)
    @allure.story("验证输入正确数据提交审核")
    @pytest.mark.parametrize('title,amount,apr,iframe,text', lst)
    def test_02(self, title, amount, apr, iframe, text):
        b_borrowtitle(title)  # 标题
        b_borrowAmount(amount)  # 金额
        b_borrowApr(apr)  # 利率
        b_iframe(iframe)  # 描述
        b_publishBnt()  # 提交审核
        b_alert()
        result = b_rightText()  # 获取错误提示信息
        assert result == text
        b_reback()

    lst = readExcel("borrow",3, 7)
    @allure.story("验证金额输入框")
    @pytest.mark.parametrize('title,amount,apr,iframe,text', lst)
    def test_03(self, title, amount, apr, iframe, text):
        b_borrowtitle(title)  # 标题
        b_borrowAmount(amount)  # 金额
        b_borrowApr(apr)  # 利率
        b_iframe(iframe)  # 描述
        b_publishBnt()  # 提交审核
        result = b_errorText()  # 获取错误提示信息
        assert result == text
        b_errorBox()

    def teardown_class(self):
        brower_quit() #退出游览器