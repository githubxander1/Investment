from ..base_page import BasePage

class PhoneLoginSection(BasePage):
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
    def sign_in_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_sign")

    def enter_phone_number(self, phone):
        self.phone_input.set_text(phone)

    def enter_password(self, password):
        self.password_input.set_text(password)

    def sign_in(self):
        self.sign_in_button.click()
