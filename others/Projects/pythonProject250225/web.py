from selenium import webdriver
import time
import re

def login():
    global driver
    driver = webdriver.Chrome()
    driver.get("http://192.168.5.27:8080/100msh/")
    driver.maximize_window()  # 窗口最大化
    driver.find_element_by_name("username").send_keys("system")
    driver.find_element_by_id("password").send_keys("123456")
    driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
    driver.implicitly_wait(10)
#代理商模块
def agency():
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/ul/li[5]/a/span[1]').click()#点击代理商管理
#代理商列表
def agencyList():
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/ul/li[5]/ul/li[1]/a').click()#点击代理商列表


#============================================================================================================
#新建代理场景
#============================================================================================================


#点击新建代理
def createAgency():
    driver.find_element_by_xpath('//*[@id="btnCreateWrap"]/div/div/a').click()#点击新建
#输入代理商名称
def agencyName(name):
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[1]/div/div/div/input').send_keys(name)
#联系人
def concat(concat):
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[2]/div/div/div/input').send_keys(concat)
#手机
def TelPhone(phone):
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[3]/div/div/div/input').send_keys(phone)
#区域
def province(address):
    driver.find_element_by_xpath('//*[@id="province"]').click()#点击所在区域选择
    driver.find_element_by_xpath('//*[@id="province"]/option[2]').click()#点击第一项
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="city"]').click()#选择城市
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="city"]/option[2]').click()#选择区第一项
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[6]/div/div/div/textarea').send_keys(address)#地址输入必填
    time.sleep(1)
def useName(useName):
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[8]/div/div/div/input').send_keys(useName)#输入账号
def passWd(pd):
    #输入密码，
    driver.find_element_by_xpath('//*[@id="loginPwd"]').send_keys(pd)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[10]/div/div/div/input').send_keys(pd)#确认密码
def submit():
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()#点击提交
def alertTextSuccess():
    time.sleep(1)
    #定位会消失的提示框
    result=driver.find_element_by_css_selector("[class*=alert-success]").text
    return result

def alertTextError():
    time.sleep(1)
    #定位会消失的提示框
    result=driver.find_element_by_css_selector("[class*=alert-error]").text
    return result

def brower_quit():
    time.sleep(3)
    driver.quit()


def nullTest():
    lis = []
    for id in ["name-error","contact-error","phone-error",
               "province-error","city-error","address-error",
               "address-error","account-error","loginPwd-error",
               "rPassword-error"]:
        text=driver.find_element_by_id(id).text
        lis.append(text)
    return lis

#============================================================================================================
#查询代理场景
#============================================================================================================


#搜索框输入
def agencySearch(text):
    driver.implicitly_wait(30)
    driver.find_element_by_xpath('//*[@id="boxTop"]/div[2]/div[1]/input').send_keys(text)
#点击搜索按钮
def agencySearchClick():
    driver.find_element_by_xpath('//*[@id="boxTop"]/div[2]/div[1]/button').click()
#检查点
def agencyTableResult():
    driver.implicitly_wait(30)
    t=driver.find_element_by_xpath('//*[@id="table"]/tbody/tr[1]/td[3]/a').text
    return t
#查询无数据检查点
def agencyTableResultNull():
    time.sleep(15)
    driver.implicitly_wait(15)
    t=driver.find_element_by_xpath('//*[@id="table"]/tbody/tr/td').text
    return t

#============================================================================================================
#修改代理场景
#============================================================================================================

#获取详情页面信息,第一条的数据的Id号
def getAgencyId():
    driver.implicitly_wait(15)
    time.sleep(15)
    text=driver.find_element_by_xpath('//*[@id="table"]/tbody/tr[1]/td[3]/a').get_attribute("href")
    s = r"=(\d+)"
    n = re.search(s, text)
    return (n.group(1))

#点击列表详情页面信息,第一条
def pullLeft():
    driver.find_element_by_xpath('//*[@id="table"]/tbody/tr[1]/td[3]/a').click()

#修改联系人
def upData_contact(contact):
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[2]/div[1]/div/input').send_keys(contact)

#修改电话号码
def upData_phone(phone):
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[3]/div[1]/div/input').clear()#清除原来的号码
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[3]/div[1]/div/input').send_keys(phone)#输入新的号码


#点击提交
def btnSubmit():
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()


#============================================================================================================
#删除代理场景
#============================================================================================================


#勾选列表第一条,并且获取代理id
def agencyChoose():
    driver.implicitly_wait(15)
    d=driver.find_element_by_xpath('//*[@id="table"]/tbody/tr[1]/td[1]/input')
    d.click()
    t=d.text
    return t
#点击删除
def btnDelete():
    driver.find_element_by_xpath('//*[@id="btnDelete"]/span').click()
#弹框警告确定
def alertSubmit():
    time.sleep(2)
    driver.switch_to.alert.accept()

def DelSuccess():
    driver.implicitly_wait(3)
    t=driver.find_element_by_css_selector("[class*=alert]").text
    return t

