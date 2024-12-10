# basePage.py
import time
from datetime import datetime
import uiautomator2 as u2

class BasePage:
    def __init__(self):
        self.d = u2.connect()
        self.d.implicitly_wait(10)

    def startApp(self):
        self.d.app_start('com.bv.fastbull')

    def closeApp(self):
        self.d.app_stop('com.bv.fastbull')

    def take_screenshot(self, text):
        now = datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f'result_screenshots/group_nickname/{text}_{now}.png'
        self.d.screenshot(filename)
