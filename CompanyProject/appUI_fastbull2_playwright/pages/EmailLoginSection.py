class EmailLoginSection:
    def __init__(self, page):
        self.page = page
        self.email_input = page.locator('android=resourceId("com.bv.fastbull:id/et_email")')
        self.password_input = page.locator('android=resourceId("com.bv.fastbull:id/et_password")')
        self.login_button = page.locator('android=resourceId("com.bv.fastbull:id/tv_login")')

    def enter_email(self, email):
        self.email_input.fill(email)

    def enter_password(self, password):
        self.password_input.fill(password)

    def login(self):
        self.login_button.click()
