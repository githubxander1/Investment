import pytest
# from page_objects import Login
from Login_page import LoginPage

@pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
def test_login(page, username, password):  # 这里的page是pytest-playwright提供的fixture
    login_page = LoginPage(page)
    page.goto("https://www.saucedemo.com/")
    login_page.fill_username(username)
    login_page.fill_password(password)
    login_page.click_login_button()
    # 添加断言验证登录成功
    assert page.url == "https://www.saucedemo.com/inventory.html"

if __name__ == '__main__':
    pytest.main(["-v", "--headed"])  # 添加--headed参数用于调试时查看浏览器
