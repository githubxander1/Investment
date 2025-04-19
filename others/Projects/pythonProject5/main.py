from data import readExcel
from web import *
import pytest
import allure
from sqlData import *
from jsonData import *
import time

@allure.feature("代理商模块")
class Test_Login():

    def setup_class(self):
        login()  # 打开游览器输入网址登录

    lst = readExcel("agency", 1, 2)  # 读取登录模块数据添加为列表然后赋值给变量
    @allure.story("新建代理成功用例")
    @pytest.mark.parametrize("aName,con,Tel,uname,pd",lst)
    def test_01(self,aName,con,Tel,uname,pd):
        agency()
        agencyList()
        createAgency()
        agencyName(aName)
        concat(con)
        TelPhone(Tel)
        province()
        useName(uname)
        passWd(pd)
        submit()
        time.sleep(5)
        brower_quit()#关闭浏览器
        time.sleep(5)
        conMySqlDB()#连接数据库
        time.sleep(5)
        agencyId=t_acc_account(aName)
        nameAndPhone=t_agency_list(agencyId)
        assert createAgencyJson(agencyId[0],nameAndPhone[0],nameAndPhone[1]) == send_createAgencyJson()
        mysqlClose()

    '''lst = readExcel("testid", 1, 2)  # 读取登录模块数据添加为列表然后赋值给变量
    @allure.story("新建代理成功用例")
    @pytest.mark.parametrize("Aid,name",lst)
    def test_02(self,Aid,name):
        #brower_quit()#关闭浏览器
        time.sleep(5)
        conMySqlDB()#连接数据库
        time.sleep(3)
        name = t_agency_list(Aid)[0]
        print(name)
        agenvyId = t_acc_account(name)[0]
        print(agenvyId)
        #assert createAgencyJson(agenvyId,name,phone) == send_createAgencyJson()
        mysqlClose()'''


