# from CompanyProject.巴迪克 import ui_payok_merchant


def convert_to_pytest(recorded_script, page_objects):
    """
    将 Playwright 录制脚本转换为 pytest + PO 模式
    :param recorded_script: 录制的脚本代码
    :param page_objects: 页面对象类
    :return: pytest 测试代码
    """
    test_code = f"""
    import pytest
    from page_objects import {', '.join(page_objects.keys())}
    
    @pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
    def test_login(page, username, password):
        login_page = LoginPage(page)
        page.goto("https://www.saucedemo.com/")
        login_page.fill_username(username)
        login_page.fill_password(password)
        login_page.click_login()
        """
    return test_code

# 示例：转换为 pytest 测试代码
import recorded_script
pytest_code = convert_to_pytest(recorded_script, {"Login": "LoginPage"})
print(pytest_code)