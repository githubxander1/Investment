# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class PayokGet(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.blazedemo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_payok_get(self):
        driver = self.driver
        # Label: Test
        # ERROR: Caught exception [ERROR: Unsupported command [resizeWindow | 1920,953 | ]]
        driver.get("http://payok-test.com/merchant/payok-workorder-record.html")
        driver.find_element(By.CSS_SELECTOR,"ul.side-nav-second-level.mm-collapse.mm-show > li > a > span").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(2) li:nth-of-type(2) span").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(3) > .side-nav-link > span:nth-of-type(1)").click()
        driver.find_element(By.CSS_SELECTOR,"ul.side-nav-second-level.mm-collapse.mm-show > li > a > span").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(3) li:nth-of-type(2) span").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(4) > .side-nav-link > span:nth-of-type(1)").click()
        driver.find_element(By.CSS_SELECTOR,"ul.side-nav-second-level.mm-collapse.mm-show > li > a > span").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(4) li:nth-of-type(2) span").click()
        # ERROR: Caught exception [Error: unknown strategy [linkText] for locator [linkText=银行单笔转账]]
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(4) li:nth-of-type(4) span").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(5) > a > span:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(6) > a > span:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(7) > a > span:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(5) > .side-nav-link > span:nth-of-type(1)").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(6) > .side-nav-link > span:nth-of-type(1)").click()
        driver.find_element(By.CSS_SELECTOR,"ul.side-nav-second-level.mm-collapse.mm-show > li > a > span").click()
        driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(7) > .side-nav-link > span:nth-of-type(1)").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
