
class LoginPage:
    def __init__(self, page):
        self.page = page

    def get_login_button(self):
        return self.page.locator("#login-button")
    def click_login_button(self):
        self.page.locator("#login-button").click()

    def get_username(self):
        return self.page.locator("#username")

    def get_password(self):
        return self.page.locator("#password")

    def fill_password(self, text):
        self.page.locator("#password").fill(text)

    def fill_username(self, text):
        self.page.locator("#username").fill(text)
