import logging
from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


def platform_activation_audit(page,merchant_id):
    # 激活审核
    link_merchant = page.get_by_role("link", name="Merchant")
    if link_merchant.get_attribute("class") != "active":
        link_merchant.click()
        page.locator("#left-bar-menu").get_by_role("link", name="Merchant List", exact=True).click()

    row = page.locator("tbody tr").filter(has_text=merchant_id)
    merchant_status = row.locator("td").nth(16)
    merchant_status_content = merchant_status.text_content()
    left_wrapper = page.locator(".dataTables_scrollBody")
    left_row = left_wrapper.locator("tbody tr").filter(has_text=merchant_id)
    left_row.wait_for(state="visible", timeout=3000)
    row_index = left_row.evaluate('(row) => Array.from(row.parentNode.children).indexOf(row)')
    right_wrapper = page.locator(".DTFC_RightBodyLiner")
    corresponding_right_row = right_wrapper.locator("tbody tr").nth(row_index)
    activate_audit_button = corresponding_right_row.get_by_text("Activation Audit")
    if merchant_status_content == "Pending Activation Audit":
        activate_audit_button.click()

        page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：激活审核通过")
        page.get_by_role("button", name="Passed").click()

        page.reload(wait_until="networkidle")
        merchant_status2 = row.locator("td").nth(16)
        merchant_status_content = merchant_status2.text_content()
        print(merchant_status2)
        print("激活审核通过,商户入驻成功！") if merchant_status_content == "Active" else print(f"激活审核未通过,{merchant_status2}")

    else:
        print(f"商户状态不是Pending Activation Audit,不需要该流程, 商户状态为{merchant_status_content}")

    # 退出登录
    page.locator("#txtOperatorName").click()
    page.locator("a").filter(has_text="Log Out").click()
    page.get_by_role("button", name="Submit").click()
    print("退出登录成功")