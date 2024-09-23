from ..base_page import BasePage

class RegisterPhoneSection(BasePage):
    def __init__(self, device_name='127.0.0.1:21503'):
        super().__init__(device_name)
        self.d = self.d  # 确保d对象在类内部可用

    @property
    def phone_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_mine_edit_phone_number")

    @property
    def password_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_password")

    @property
    def register_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_sign")

    @property
    def verification_code_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_code")

    @property
    def verify_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_verify")

    def enter_phone_number(self, phone):
        self.phone_input.set_text(phone)

    def enter_password(self, password):
        self.password_input.set_text(password)

    def click_register(self):
        self.register_button.click()

    def enter_verification_code(self, code):
        self.verification_code_input.set_text(code)

    def click_verify(self):
        self.verify_button.click()

    @property
    def register_by_phone_and_email(self):
        return self.d.xpath('//*[@resource-id="com.bv.fastbull:id/ll_btn"]/android.widget.RelativeLayout[1]')

    def click_register_by_phone_and_email(self):
        self.register_by_phone_and_email.click()
