from ..base_page import BasePage

class RegisterEmailSection(BasePage):
    def __init__(self, device_name='127.0.0.1:21503'):
        super().__init__(device_name)
        self.d = self.d  # 确保d对象在类内部可用

    @property
    def email_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_email")

    @property
    def password_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_password")

    @property
    def register_button(self):
        # return self.d(resourceId="com.bv.fastbull:id/tv_register")
        return self.d(resourceId="com.bv.fastbull:id/tv_login")


    @property
    def verification_code_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_code")

    @property
    def verify_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_verify")

    def enter_email(self, email):
        self.email_input.set_text(email)

    def enter_password(self, password):
        self.password_input.set_text(password)

    def click_register_button(self):
        self.register_button.click()

    def enter_verification_code(self, code):
        self.verification_code_input.set_text(code)

    def click_verify(self):
        self.verify_button.click()

    @property
    def by_email_register(self):
        return self.d(text="邮箱")

    def click_by_email_register(self):
        self.by_email_register.click()
