from ..base_page import BasePage

class ForgetPasswordEmailSection(BasePage):
    def __init__(self, device_name='127.0.0.1:21503'):
        super().__init__(device_name)
        self.d = self.d  # 确保d对象在类内部可用

    @property
    def email_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_email")

    @property
    def send_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_send")

    @property
    def resend_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_re_send")

    def enter_email(self, email):
        self.email_input.set_text(email)

    def send(self):
        self.send_button.click()

    def resend(self):
        self.resend_button.click()
