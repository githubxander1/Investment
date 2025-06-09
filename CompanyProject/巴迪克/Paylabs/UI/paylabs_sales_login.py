import logging
from playwright.sync_api import Page

from CompanyProject.巴迪克.utils.GoogleSecure import GoogleAuth
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification

logger = get_logger(__name__)
ENV_URLS = {
    "test": "http://test.paylabs.id/sales/paylabs-user-login.html",
    "sitch": "https://sitch-sales.paylabs.co.id/paylabs-user-login.html"
}

@default_retry
def sales_login(page: Page, env="test", login_name="15318544153"):
    url = ENV_URLS.get(env, ENV_URLS["test"])
    page.goto(url)

    try:
        page.locator("span").filter(has_text="Bahasa").first.click()
        page.get_by_role("link", name="English").click()

        page.get_by_role("textbox", name="Phone Number").fill(login_name)
        page.get_by_role("textbox", name="Password").fill("A123456@test")
        perform_block_slider_verification(page)
        page.get_by_role("button", name="Login").click()

        # 获取谷歌验证码并登录
        if env == 'sitch':
            code = GoogleAuth._calculate("4cavnkhcy3x46g46jwhe45ajulmsouwe")
        else:
            code = GoogleAuth.generate(environment='test', project='paylabs',
                                      table='sales_operator', login_name=login_name)

        page.locator("#googleCode").fill(code)
        page.get_by_role("button", name="Login").click()

        #等待1秒
        page.wait_for_timeout(2000)
        assert_url ='http://test.paylabs.id/sales/paylabs-board-board.html'
        # assert page.url.startswith(ENV_URLS[env].split("//")[1]), f"URL 不匹配：{page.url}"
        assert assert_url  == page.url, f"URL 不匹配,实际值为：{page.url}"
        logger.info(f"Sales 登录成功：{login_name}")
    except Exception as e:
        logger.error(f"Sales 登录失败：{e}")
        raise
