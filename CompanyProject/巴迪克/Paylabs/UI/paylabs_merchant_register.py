import logging
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

from CompanyProject.巴迪克.common.config.settings import ENV_CONFIG
from CompanyProject.巴迪克.utils.logger import get_logger

# from utils.logger import get_logger
# from config.settings import ENV_CONFIG

logger = get_logger(__name__)

def paylabs_merchant_register(page, env="test", email=None):
    base_url = ENV_CONFIG[env]["base_url"]
    page.goto(f"{base_url}/merchant/paylabs-register-register.html")

    logger.info("开始注册商户流程")
    try:
        #切换到英文环境
        page.locator("span").filter(has_text="id").first.click()
        page.get_by_role("link", name="EN", exact=True).click()

        # 缓存常用定位器
        email_input = page.get_by_role("textbox", name="E-mail *", exact=True)
        code_input = page.get_by_role("textbox", name="Email Verification Code *")
        phone_input = page.locator("#phone")
        phone_code_input = page.locator("#phoneCode")
        secure_email_input = page.get_by_role("textbox", name="Secure Email for fund account")
        pic_name_input = page.get_by_role("textbox", name="Please enter contact")
        password_input = page.get_by_role("textbox", name="Password *", exact=True)
        confirm_password_input = page.get_by_role("textbox", name="Confirm password *", exact=True)
        invite_code_input = page.locator("#invitation_code")
        register_button = page.get_by_role("button", name="Register")
        agree_button = page.get_by_role("button", name="I have read and agree to the")
        gologin_button = page.locator("#gologin")

        # page.get_by_role("textbox", name="Email Verification Code *").click()

        # 表单填写
        page.pause()
        email_input.fill(email)
        # code_input.fill(verification_code)
        code_input.fill("652266")
        phone_input.fill('15318544154')
        phone_code_input.fill('652266')
        secure_email_input.fill(email)
        pic_name_input.fill(email)  # PIC 名字（联系人）
        password_input.fill("A123456@test")
        confirm_password_input.fill("A123456@test")
        invite_code_input.fill('123456')
        register_button.click()

        agree_button.click()  # 同意协议

        try:
            # 检查邮箱是否已注册
            expect(page.locator("#inputEmail")).to_contain_text("The E-mail has been registered")
            logging.info("邮箱已注册！")
        except AssertionError:
            try:
                gologin_button.wait_for(state='visible', timeout=10000)
                if gologin_button.is_visible():
                    logging.info("注册成功")
                else:
                    logging.warning("未找到 'gologin' 元素或其不可见")
            except PlaywrightTimeoutError:
                logging.error("'gologin' 元素未在预期时间内显示")
        except PlaywrightTimeoutError as e:
            logging.error(f"页面操作超时: {e}")
        except Exception as e:
            logging.error(f"发生未知错误: {e}")
    except Exception as e:
        logger.error(f"注册失败: {e}")
        raise
        # # 清理资源
        # context.close()
        # browser.close()


# if __name__ == '__main__':
#     config = {
#         "ui": {
#             "headless": False,
#             "slow_mo": 0
#         },
#         "env": "sitch",
#         "sitch_base_url": "https://sitch-merchant.paylabs.co.id",
#         "test_base_url": "http://test.paylabs.id"
#     }
#     email = "paylabsmerchant@sitch.com"
#     google_secret_key = "igz4obkiqirr16pudug7qkfbjj544yy2"
#
#     with sync_playwright() as playwright:
#         paylabs_merchant_register(playwright, "sitch", email)
