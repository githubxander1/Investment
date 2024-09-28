from CompanyProject.appUI_fastbull_selenium.pages.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, device_name='127.0.0.1:21503'):
        super().__init__(device_name)
        self.d = self.d  # 确保d对象在类内部可用

    @property
    def avatar(self):
        return self.d(resourceId="com.bv.fastbull:id/iv_avatar")

    # 点击登录按钮
    @property
    def to_login_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_mine_top_welcome")

    # 登录页-手机号 / 邮箱登录
    @property
    def phone_and_email_login_button(self):
        return self.d.xpath('//*[@resource-id="com.bv.fastbull:id/ll_btn"]/android.widget.RelativeLayout[1]')

    @property
    def input_phone_number(self):
        return self.d(resourceId="com.bv.fastbull:id/et_mine_edit_phone_number")
    @property
    def by_email_login(self):
        return self.d(text="邮箱/ID")

    def click_by_email_login(self):
        self.by_email_login.click()


    @property
    def email_login_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_email_login")

    # 忘记密码
    @property
    def forget_password_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tv_forget_password")

    @property
    def register_button(self):
        return self.d.xpath('//*[@resource-id="com.bv.fastbull:id/fl_view"]/android.widget.LinearLayout[1]/android.widget.TextView[3]')
        # return self.d(resourceId="com.bv.fastbull:id/tv_create_account")

    def click_avatar(self):
        self.avatar.click()

    def click_to_login_button(self):
        self.to_login_button.click()

    def click_phone_and_email_login_button(self):
        self.phone_and_email_login_button.click()

    def click_email_login_button(self):
        self.email_login_button.click()

    def click_forget_password_button(self):
        self.forget_password_button.click()

    def click_register_button(self):
        self.register_button.click()

    # 退出登录
    @property
    def settting_button(self):
        return self.d(resourceId="com.bv.fastbull:id/iv_setting")

    def click_settting_button(self):
        self.settting_button.click()

    @property
    def account_security(self):
        return self.d.xpath('//*[@resource-id="com.bv.fastbull:id/rv_mine_set_item"]/android.view.ViewGroup[1]')
    def click_account_security(self):
        self.account_security.click()

    @property
    def logout_button(self):
        return self.d(resourceId="com.bv.fastbull:id/tvLogOff")
    def click_logout_button(self):
        self.logout_button.click()

    @property
    def confirm_logout_button(self):
        return self.d(resourceId="com.bv.fastbull:id/bt_sure")

    def logout(self):
        self.click_settting_button()
        self.click_account_security()
        self.click_logout_button()
        self.confirm_logout_button.click()

    @property
    def register_by_phone_and_email(self):
        return self.d.xpath('//*[@resource-id="com.bv.fastbull:id/ll_btn"]/android.widget.RelativeLayout[1]')

    def click_register_by_phone_and_email(self):
        self.register_by_phone_and_email.click()

# if __name__ == '__main__':
#     login_page = LoginPage()
#     login_page.open_app()
#     login_page.click_avatar()
#     login_page.click_to_login_button()
#     login_page.click_phone_and_email_login_button()
#     login_page.click_input_phone_number.set_text("123456789")


    # login_page.close_app()


