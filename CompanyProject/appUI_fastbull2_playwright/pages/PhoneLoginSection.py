class PhoneLoginSection:
    def __init__(self, page):
        self.page = page
        self.phone_input = page.locator('android=resourceId("com.bv.fastbull:id/et_mine_edit_phone_number")')
        self.password_input = page.locator('android=resourceId("com.bv.fastbull:id/et_password")')
        self.sign_in_button = page.locator('android=resourceId("com.bv.fastbull:id/tv_sign")')

    def enter_phone_number(self, phone):
        self.phone_input.fill(phone)

    def enter_password(self, password):
        self.password_input.fill(password)

    def sign_in(self):
        self.sign_in_button.click()
