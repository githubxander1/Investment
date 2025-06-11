import logging
from playwright.sync_api import Playwright, sync_playwright

from CompanyProject.巴迪克.utils.change_ui_language import change_ui_language
from CompanyProject.巴迪克.utils.retry import default_retry
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuthenticator
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification

logger = get_logger(__name__)

@default_retry
def platform_login(page, login_email):
    try:
        page.goto("http://paylabs-test.com/platform/paylabs-user-login.html")
        change_ui_language(page, "English")

        page.get_by_role("textbox", name="E-mail").fill(login_email)
        page.get_by_role("textbox", name="Password Verification Code").fill("Asd123456789.")
        perform_block_slider_verification(page)
        page.get_by_role("button", name=" Login").click()

        if page.locator("text=This user has logged in on another device").is_visible():
            page.get_by_role("button", name="Confirm").click()

        google_code = GoogleAuthenticator.generate(environment='test', project='paylabs',
                                                  table='platform_operator', login_name=login_email)
        page.get_by_role("textbox", name="Google Verification Code").fill(google_code)
        page.get_by_role("button", name="Login").click()

        logger.info("平台登录完成")
    except Exception as e:
        logger.error(f"平台登录失败：{e}")
        raise
