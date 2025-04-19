from selenium import webdriver
import time

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
def province():
    driver.find_element_by_xpath('//*[@id="province"]').click()#点击所在区域选择
    driver.find_element_by_xpath('//*[@id="province"]/option[2]').click()#点击第一项
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="city"]').click()#选择城市
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="city"]/option[2]').click()#选择区第一项
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[6]/div/div/div/textarea').send_keys("一楼101")#地址输入必填
    time.sleep(1)
def useName(useName):
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[8]/div/div/div/input').send_keys(useName)#输入账号
def passWd(pd):
    #输入密码，
    driver.find_element_by_xpath('//*[@id="loginPwd"]').send_keys("123456")
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="formAgency"]/div[10]/div/div/div/input').send_keys(pd)#确认密码
def submit():
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()#点击提交
def alertText():
    time.sleep(1)
    #定位会消失的提示框
    result=driver.find_element_by_css_selector("[class*=alert]").text
    print(result)

def brower_quit():
    time.sleep(3)
    driver.quit()
