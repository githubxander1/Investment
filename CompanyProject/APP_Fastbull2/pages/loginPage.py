import time
from datetime import datetime

from time import sleep

import uiautomator2 as u2

# d = u2.connect_usb('22addc6f0403')
# d = u2.connect_wifi('192.168.31.117')
# d = u2.connect_adb_wifi('192.168.5.220:5555')
d = u2.connect()
# print(d.info)
class Login:
    def __init__(self):
        self.d = u2.connect()

    avatar=d(resourceId="com.bv.fastbull:id/iv_avatar")
    tologin=d(resourceId="com.bv.fastbull:id/tv_mine_top_welcome")

    # phoneOremail=d.xpath('//*[@resource-id="com.bv.fastbull:id/ll_btn"]/android.widget.RelativeLayout[1]')
    phoneOremail=d.xpath('//*[@resource-id="com.bv.fastbull:id/ll_btn"]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]')
    # phoneOremail = d.xpath('//android.widget.RelativeLayout[@resource-id="com.bv.fastbull:id/ll_btn"]/android.widget.TextView[contains(@text, "手机号")]')
    get_code=d(resourceId="com.bv.fastbull:id/tv_get_code")
    et_password=d(resourceId="com.bv.fastbull:id/et_password")
    et_phone=d(resourceId="com.bv.fastbull:id/et_mine_edit_phone_number")
    identifyCode=d(resourceId="com.bv.fastbull:id/et_code")
    login=d(resourceId="com.bv.fastbull:id/tv_sign")

    sign_in=d(resourceId="com.bv.fastbull:id/tv_sign")
    def click_tologin(self):
        self.tologin.click()
    def click_get_code(self):
        self.get_code.click()

    def input_phone(self,text):
        self.et_phone.set_text(text)
    def click_sign_in(self):
        self.sign_in.click()
    def input_password(self,text):
        self.et_password.set_text(text)
    def click_phoneOremail(self):
        self.phoneOremail.click()
    def click_avatar(self):
        self.avatar.click()
    def click_login(self):
        self.login.click()

    # def __init__(self):
    # #     # self.d = u2.connect_adb_wifi('192.168.31.19')
    # #     # self.d = u2.connect_adb_wifi('192.168.31.19:5555')
    # #     self.d = u2.connect_adb_wifi('192.168.5.220:5555')
    #     self.d = u2.connect()
    #     self.d.implicitly_wait(10)
    # #     # self.d = u2.connect_usb('22addc6f0403')

    def startApp(self):
        self.d.app_start('com.bv.fastbull')
        # self.chat.click()


    def closeApp(self):
        self.d.app_stop('com.bv.fastbull')

    def login_phone_password(self):
        self.startApp()
        time.sleep(4)
        self.click_avatar()
        self.click_tologin()
        time.sleep(2)
        # self.click_phoneOremail()
        self.d.click(0.854, 0.347)
        self.input_phone('13111111113')
        self.input_password('a1234567')
        self.click_sign_in()


    def take_screenshot(self,text):
        now=datetime.now().strftime('%Y%m%d-%H%M%S')
        filename=f'result_screenshots/group_nickname/{text}_{now}.png'
        d.screenshot(filename)

login=Login()
login.login_phone_password()
# # screenshot_path = "./screenshot1.png"  # 截图保存的路径
# # d.screenshot(screenshot_path)# base.login_phone()
# base.startApp()