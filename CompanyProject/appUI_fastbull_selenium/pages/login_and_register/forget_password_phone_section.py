from ..base_page import BasePage

class ForgetPasswordPhoneSection(BasePage):
    def __init__(self, device_name='127.0.0.1:21503'):
        super().__init__(device_name)
        self.d = self.d  # 确保d对象在类内部可用

    @property
    def phone_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_mine_edit_phone_number")

    @property
    def new_password_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_password_new")

    @property
    def confirm_password_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_password_again")

    @property
    def get_verification_code_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_get_code")

    @property
    def verification_code_input(self):
        return self.d(resourceId="com.bv.fastbull:id/et_code")

    @property
    def reset_password_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_reset")

    def enter_phone_number(self, phone):
        self.phone_input.set_text(phone)

    def enter_new_password(self, password):
        self.new_password_input.set_text(password)

    def enter_confirm_password(self, password):
        self.confirm_password_input.set_text(password)

    def get_verification_code(self):
        self.get_verification_code_button.click()

    def enter_verification_code(self, code):
        self.verification_code_input.set_text(code)

    def reset_password(self):
        self.reset_password_button.click()
