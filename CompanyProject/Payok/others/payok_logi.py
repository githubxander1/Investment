import pytest
import allure
from playwright.sync_api import sync_playwright

@allure.feature("Paylabs 登录测试")
class TestPaylabsLogin:
    @pytest.fixture(scope="function")
    def browser_setup(self):
        """
        初始化浏览器实例，并在测试结束后关闭浏览器
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            yield page
            browser.close()

    @allure.story("完整登录流程测试")
    def test_paylabs_login(self, browser_setup):
        """
        测试 Paylabs 登录流程
        """
        page = browser_setup
        # 打开登录页面
        with allure.step("打开 Paylabs 登录页面"):
            page.goto("http://paylabs-test.com/merchant/paylabs-user-login.html")
        # 点击验证码区域
        with allure.step("点击验证码区域"):
            page.click("div.verify-move-block")
        # 点击登录按钮
        with allure.step("点击登录按钮"):
            page.click("#btnLogin")
        # 点击谷歌验证码输入框
        with allure.step("点击谷歌验证码输入框"):
            page.click("#googleCode")
        # 点击谷歌登录按钮
        with allure.step("点击谷歌登录按钮"):
            page.click("#btnGoogleLogin > span")
