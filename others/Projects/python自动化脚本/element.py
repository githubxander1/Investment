import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标操作导入 ActionChains 类
from selenium.webdriver.common.keys import Keys  # 在使用键盘按键方法前需要先导入 Keys 类


def openUrl():
    global driver
    driver = webdriver.Chrome()
    driver.get("http://120.76.119.135/syunke/fw")
    driver.maximize_window()  # 窗口最大化

def login(name,pwd):
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="user_head_tip"]/a[1]').click()
    driver.implicitly_wait(10)
    driver.find_element_by_name("email").send_keys(name)
    driver.find_element_by_name("user_pwd").send_keys(pwd)
    driver.find_element_by_name("commit").click()


def get_success_text(): #获取成功提示文本信息
    time.sleep(3)
    result = driver.find_element_by_xpath('//*[@id="fanwe_success_box"]/table/tbody/tr/td[2]/div[2]').text

    return result

def click_success_button(): #关闭登录成功提示框
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="fanwe_success_box"]/table/tbody/tr/td[2]/div[3]/input[1]').click()

def get_fail_text(): #获取错误提示文本信息
    time.sleep(3)
    result=driver.find_element_by_xpath('//*[@id="fanwe_error_box"]/table/tbody/tr/td[2]/div[2]').text
    print("值",result)
    return result

def click_fail_button(): #关闭错误提示框
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="fanwe_error_box"]/table/tbody/tr/td[2]/div[3]/input[1]').click()

def close_login():#关闭登录界面
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="pop_user_login"]/table/tbody/tr/td[2]/div[1]/div[2]').click()

def user_quit():
    time.sleep(3)
    driver.find_element_by_link_text('退出').click()


def brower_quit():
    time.sleep(3)
    driver.quit()

#==================申请借款场景元素===========================

def b_move_borrow():
    time.sleep(2)
    #定位到鼠标移动到我要借款上面的元素
    above = driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/ul/li[3]/a')
    #对定位到的元素执行鼠标移动到上面的操作
    ActionChains(driver).move_to_element(above).perform()
def b_click_applyBorrow():#申请贷款
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/ul/li[3]/div/a[3]').click()#申请贷款
def b_click_apply():#点击立即申请
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="borrowlb"]/div/ul/li[1]/div[3]/a/img').click()#立即申请
def b_borrowtitle(title):
    time.sleep(1)
    m=driver.find_element_by_name('borrowtitle')
    m.clear()#清除标题
    m.send_keys(title)#标题
def b_borrowAmount(amount):
    m=driver.find_element_by_name('borrowamount')
    m.clear()#清除金额
    m.send_keys(amount)#金额
def b_repaytime_type():
    driver.find_element_by_xpath('//*[@name="repaytime_type"]/dt').click()#点击还款周期下拉框
def b_repaytime_type_month():
    time.sleep(1)
    driver.find_element_by_xpath('//*[@name="repaytime_type"]/dd/a[2]').click()#选择按月
def b_repaytime_type_day():
    time.sleep(1)
    driver.find_element_by_xpath('//*[@name="repaytime_type"]/dd/a[1]').click()#选择按天
def b_repaytime_days(days):
    time.sleep(1)
    d=driver.find_element_by_xpath('//*[@id="repaytime"]')
    d.clear()
    d.send_keys(days)
def b_repaytime():#点击借款期限下拉框
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/form/div/div[12]/div/dl/dt').click()#借款期限
    #driver.find_element_by_xpath("//*[@name='repaytime']/dl/dt").click()
def b_repaytime_month(month):#选择借款期限月份
    time.sleep(3)
    driver.find_element_by_link_text(month).click()
def b_borrowApr(apr):
    time.sleep(1)
    m=driver.find_element_by_name('apr')
    m.clear()#清除利率
    m.send_keys(apr)#利率
def b_iframe(description):#借款描述
    d=driver.find_element_by_xpath('//*[@id="J_save_deal_form"]/div[1]/div[35]/div/div/div[2]/iframe')
    d.send_keys(Keys.CONTROL,'a')
    d.send_keys(Keys.BACK_SPACE)

    d.send_keys(description)
def b_publishBnt():
    driver.find_element_by_id('publishBnt').click()#提交审核
def b_alert():
    driver.switch_to.alert.accept()#弹出窗确定
def b_rightText():#正确的检查点

    t=driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[3]/div/div[5]/div[2]').text
    return t
def b_reback():#撤销审核
    driver.find_element_by_id('J_reback').click()
def b_errorText():#错误的检查点
    time.sleep(1)
    t=driver.find_element_by_xpath('//*[@id="fanwe_error_box"]/table/tbody/tr/td[2]/div[2]').text
    return t
def b_errorBox():#z错误确定
    driver.find_element_by_xpath('//*[@id="fanwe_error_box"]/table/tbody/tr/td[2]/div[3]/input[1]').click()



