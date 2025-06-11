import logging
from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification

def sales_setting_sales(page, merchant_id):
    link_merchant = page.get_by_role("link", name="ﱖ Merchant ")
    if link_merchant.get_attribute("class") != "active":
        page.get_by_role("link", name="ﱖ Merchant ").click()
        page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()

    page.wait_for_timeout(1000)
    row = page.locator("tbody tr").filter(has_text=merchant_id)
    merchant_status = row.locator("td").nth(2)
    merchant_status_content = merchant_status.text_content()
    left_wrapper = page.locator(".dataTables_scrollBody")
    left_row = left_wrapper.locator("tbody tr").filter(has_text=merchant_id)
    left_row.wait_for(state="visible", timeout=3000)
    row_index = left_row.evaluate('(row) => Array.from(row.parentNode.children).indexOf(row)')
    right_wrapper = page.locator(".DTFC_RightBodyLiner")
    corresponding_right_row = right_wrapper.locator("tbody tr").nth(row_index)
    submit_button = corresponding_right_row.get_by_text("Setting Sales")

    if merchant_status_content == "New Merchant":
        submit_button.click()

        page.locator('#select2-newSalesManModal-container').click()
        page.locator(".select2-results__option").nth(1).click()
        page.get_by_role("textbox", name="Remarks").fill("1设置sales")
        page.locator("#btnSureSaleModal").click()

        page.reload(wait_until="networkidle")
        merchant_status_content = merchant_status.text_content()
        if merchant_status_content != "New Merchant" and merchant_status_content == "Pending complete the information":
            print("✅销售设置成功，下一步：Pending complete the information提交资料")
        else:
            print("⚠️提示：销售设置失败")
    else:
        print("⚠️提示：商户状态不是New Merchant，不需要再设置销售")