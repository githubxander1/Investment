import pytest
from CompanyProject.appUI_fastbull_selenium.pages.login_and_register.login_page import LoginPage
from CompanyProject.appUI_fastbull_selenium.pages.login_and_register.phone_login_section import PhoneLoginSection
from CompanyProject.appUI_fastbull_selenium.pages.login_and_register.email_login_section import EmailLoginSection
from CompanyProject.appUI_fastbull_selenium.pages.login_and_register.forget_password_phone_section import ForgetPasswordPhoneSection
from CompanyProject.appUI_fastbull_selenium.pages.login_and_register.forget_password_email_section import ForgetPasswordEmailSection
from CompanyProject.appUI_fastbull_selenium.pages.login_and_register.register_phone_section import RegisterPhoneSection
from CompanyProject.appUI_fastbull_selenium.pages.login_and_register.register_email_section import RegisterEmailSection

# login_page = LoginPage()
@pytest.fixture
def login_page(setup):
    return setup

@pytest.fixture
def phone_login_section(login_page):
    login_page.click_avatar()
    login_page.click_to_login_button()
    login_page.click_phone_and_email_login_button()
    login_page.click_phone_login_button()
    return PhoneLoginSection()

@pytest.fixture
def email_login_section(login_page):
    login_page.click_avatar()
    login_page.click_to_login_button()
    login_page.click_phone_and_email_login_button()
    login_page.click_email_login_button()
    return EmailLoginSection()

@pytest.fixture
def forget_password_phone_section(login_page):
    login_page.click_avatar()
    login_page.click_login_button()
    login_page.click_forget_password_button()
    return ForgetPasswordPhoneSection()

@pytest.fixture
def forget_password_email_section(login_page):
    login_page.click_avatar()
    login_page.click_login_button()
    login_page.click_forget_password_button()
    return ForgetPasswordEmailSection()

@pytest.fixture
def register_phone_section(login_page):
    login_page.click_avatar()
    login_page.click_login_button()
    login_page.click_register_button()
    return RegisterPhoneSection()

@pytest.fixture
def register_email_section(login_page):
    login_page.click_avatar()
    login_page.click_login_button()
    login_page.click_register_button()
    return RegisterEmailSection()

def test_phone_login(phone_login_section):
    phone_login_section.enter_phone_number("13111111126")
    phone_login_section.enter_password("a1234567")
    phone_login_section.sign_in()

    LoginPage().logout()
def test_email_login(email_login_section):
    email_login_section.enter_email("7@qq.com")
    email_login_section.enter_password("a1234567")
    email_login_section.login()

    LoginPage().logout()

def test_forget_password_phone(forget_password_phone_section):
    forget_password_phone_section.enter_phone_number("13111111126")
    forget_password_phone_section.enter_new_password("a1234567")
    forget_password_phone_section.enter_confirm_password("a1234567")
    forget_password_phone_section.get_verification_code()
    forget_password_phone_section.enter_verification_code("1234")
    forget_password_phone_section.reset_password()

def test_forget_password_email(forget_password_email_section):
    forget_password_email_section.enter_email("7@qq.com")
    forget_password_email_section.send()

def test_register_phone(register_phone_section):
    register_phone_section.enter_phone_number("13111111126")
    register_phone_section.enter_password("a1234567")
    register_phone_section.register()
    register_phone_section.enter_verification_code("1234")
    register_phone_section.verify()

def test_register_email(register_email_section):
    register_email_section.enter_email("7@qq.com")
    register_email_section.enter_password("a1234567")
    register_email_section.register()
    register_email_section.enter_verification_code("1234")
    register_email_section.verify()

if __name__ == '__main__':
    pytest.main()