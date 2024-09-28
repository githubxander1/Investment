from ..base_page import BasePage

class EmailLoginSection(BasePage):
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
    def login_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_login")

    def enter_email(self, email):
        self.email_input.set_text(email)

    def enter_password(self, password):
        self.password_input.set_text(password)

    def login(self):
        self.login_button.click()
