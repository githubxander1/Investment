from utils.retry_decorator import retry

@retry(3)
def test_login(driver):
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    login_page.input_username('default_user')
    login_page.input_password('default_password')
    login_page.click_login_button()