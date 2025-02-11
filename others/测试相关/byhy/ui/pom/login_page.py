from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("用户名")
        self.password_input = page.get_by_placeholder("密码")
        self.login_button = page.get_by_role("button", name="登录")

    def navigate(self):
        self.page.goto("http://127.0.0.1:8047/mgr/sign.html")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
