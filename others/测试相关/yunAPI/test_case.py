from data import  *
from  API import  *
import pytest
import allure
from sqlData import *


@allure.feature("消息统计模块")
class Test_getMsg():
    lst=readExcel("通知消息数统计",2,4)
    @allure.story("通知消息数统计用例")
    @pytest.mark.parametrize("id,col,result",lst)
    def test_getMsgSum1(self,id,col,result):
        req=getMsgSum(id,col)
        assert  req.status_code ==200
        assert   req.text == result



@allure.feature("代理模块")
class Test_agency():
    lst=readExcel("新建代理",2,3)
    @allure.story("新建代理用例")
    @pytest.mark.parametrize("name,phone",lst)
    def test_createAgency(self,name,phone):
        req=createAgency(name,phone)
        conMySqlDB()
        resultId=agencyTel(phone)[0]
        mysqlClose()
        assert req.status_code == 200
        assert req.text == '{"msg": "Success", "code": 0, "id": %s}'%resultId

'''
    lst = readExcel("修改代理",2,3)
    @allure.story("修改代理用例")
    @pytest.mark.parametrize("id,contact",lst)
    def test_modifyAgency(self,id,contact):
        req=modifyAgency(id,contact)
        assert req.status_code == 200
        assert eval(req.text)["msg"] == "Success"
'''