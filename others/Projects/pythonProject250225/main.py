from data import readExcel
from web import *
import pytest
import allure
from sqlData import *
from jsonData import *


@allure.feature("新建代理商模块")
class Test_AgencyCreate():
    def setup_class(self):
        login()  # 打开游览器输入网址登录

    lst = readExcel("新建代理商", 2, 3)  # 读取模块数据添加为列表然后赋值给变量
    @allure.story("新建代理成功用例")
    @pytest.mark.parametrize("aName,con,Tel,address,uname,pd",lst)
    def test_01(self,aName,con,Tel,uname,address,pd):
        agency()
        agencyList()
        createAgency()
        agencyName(aName)
        concat(con)
        TelPhone(Tel)
        province(address)
        useName(uname)
        passWd(pd)
        submit()
        assert '新建代理商成功！' in alertTextSuccess()


    lst = readExcel("新建代理商", 4, 4)  # 读取模块数据添加为列表然后赋值给变量
    @allure.story("新建代理失败用例")
    @pytest.mark.parametrize("aName,con,Tel,address,uname,pd",lst)
    def test_02(self,aName,con,Tel,address,uname,pd):
        agency()
        agencyList()
        createAgency()
        agencyName(aName)
        concat(con)
        TelPhone(Tel)
        province(address)
        useName(uname)
        passWd(pd)
        submit()
        assert '您添加的用户已存在,请重新输入！' in alertTextError()


    @allure.story("新建代理必填测试")
    def test_03(self):
        agency()
        agencyList()
        createAgency()
        submit()
        assert ['必填字段', '必填字段', '必填字段',
                '必填字段', '必填字段', '必填字段',
                '必填字段', '必填字段', '必填字段',
                '必填字段'] == nullTest()


@allure.feature("查询代理商模块")
class Test_AgencySearch():
    def setup_class(self):
        login()  # 打开游览器输入网址登录

    lst = readExcel("查询代理商", 2, 3)  # 读取模块数据添加为列表然后赋值给变量
    @allure.story("查询代理成功用例")
    @pytest.mark.parametrize("text",lst)
    def test_01(self,text):
        agency()
        agencyList()
        time.sleep(15)
        agencySearch(text)
        agencySearchClick()
        assert text[0] in agencyTableResult()

    lst = readExcel("查询代理商", 4, 4)  # 读取模块数据添加为列表然后赋值给变量
    @allure.story("查询代理失败用例")
    @pytest.mark.parametrize("text", lst)
    def test_02(self,text):
        agency()
        agencyList()
        time.sleep(15)
        agencySearch(text)
        agencySearchClick()
        assert "没有数据" == agencyTableResultNull()



@allure.feature("代理商详情模块")
class Test_AgencyUpdata():
    def setup_class(self):
        login()  # 打开游览器输入网址登录
        conMySqlDB()

    @allure.story("代理详情页面用例")
    def test_01(self,):
        agency()
        agencyList()
        time.sleep(15)
        id=getAgencyId()
        pullLeft()
        result=getAgencyDetail(id)
        time.sleep(3)
        phone=result['data']["phone"]
        assert  phone == agencyTel(id)[0] #判断json返回值跟数据库值一致


    lst = readExcel("修改代理商", 2, 2)  # 读取模块数据添加为列表然后赋值给变量
    @allure.story("修改代理成功用例")
    @pytest.mark.parametrize("tel",lst)
    def test_02(self,tel):
        agency()
        agencyList()
        time.sleep(15)
        id=getAgencyId()
        pullLeft()
        upData_phone(tel[0])
        btnSubmit()
        time.sleep(3)
        conMySqlDB()
        result = agencyTel(id)[0]  # 获取数据库电话号码
        mysqlClose()
        time.sleep(1)
        assert  str(tel[0])==result


@allure.feature("删除代理商模块")
class Test_AgencydDelete():
    def setup_class(self):
        login()  # 打开游览器输入网址登录
        conMySqlDB()

    @allure.story("删除代理成功用例")
    def test_01(self):
        agency()
        agencyList()
        time.sleep(15)
        id=agencyChoose()
        btnDelete()
        alertSubmit()
        time.sleep(1)
        DelSuccess()
        assert  '删除成功' in DelSuccess() and (agencyTel(id) == None)
        mysqlClose()





