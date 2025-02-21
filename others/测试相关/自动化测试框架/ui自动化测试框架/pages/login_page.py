from base.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    username_input = (By.ID, 'username')
    password_input = (By.ID, 'password')
    login_button = (By.ID, 'login-button')

    def input_username(self, username):
        self.send_keys(*self.username_input, text=username)

    def input_password(self, password):
        self.send_keys(*self.password_input, text=password)

    def click_login_button(self):
        self.click(*self.login_button)