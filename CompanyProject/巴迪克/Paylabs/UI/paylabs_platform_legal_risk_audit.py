import logging
from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


def platform_legal_risk_audit(page, merchant_id, pdf_file_path):
    # 法律风控
    link_risk_control = page.get_by_role("link", name=" Risk Control ")
    if link_risk_control.get_attribute("class") != "active":
        page.get_by_role("link", name=" Risk Control ").click()
        page.get_by_role("link", name="Risk Control", exact=True).click()

    # 移动滑块
    # scroll_div = page.wait_for_selector('#scrollDiv')  # 等待目标 div 加载
    # scroll_div_table = page.query_selector('#scrollDivTable')  # 获取 scrollDivTable 的宽度
    # scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    # scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')  # 滚动到最右侧
    #
    # row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    #
    # # 查找该行中的 Setting Sales 按钮
    # setting_sales_button = row.locator("button[name='btnSetSales']")
    # legal_audit_button = row.get_by_role("button", name="Legal Audit")
    # try:
    #     # 等待按钮可点击
    #     # page.pause()
    #     # 尝试直接使用 JavaScript 点击按钮
    #     page.evaluate('(button) => button.click()', legal_audit_button.element_handle())
    # except Exception as e:
    #     print(f"点击设置sales按钮失败：{e}")
    # page.get_by_text("Legal Audit", exact=True).nth(1).click()
    row = page.locator("tbody tr").filter(has_text=merchant_id)
    merchant_status = row.locator("td").nth(6)
    merchant_status_content = merchant_status.text_content()
    left_wrapper = page.locator(".dataTables_scrollBody")
    left_row = left_wrapper.locator("tbody tr").filter(has_text=merchant_id)
    left_row.wait_for(state="visible", timeout=3000)
    row_index = left_row.evaluate('(row) => Array.from(row.parentNode.children).indexOf(row)')
    right_wrapper = page.locator(".DTFC_RightBodyLiner")
    corresponding_right_row = right_wrapper.locator("tbody tr").nth(row_index)
    risk_control_audit_button = corresponding_right_row.get_by_text("Legal Audit")
    if merchant_status_content == "Pending Risk Control Audit":
        risk_control_audit_button.click()

    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm2").click()
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm3").click()

    # page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：商户列表-法律审核通过")
    # page.get_by_role("button", name="Comment").click()

    page.get_by_role("button", name="Approve").click()
    # page.pause()
    page.wait_for_timeout(1000)
    # page.locator("#btnCancel2").click()
    page.locator("#btnSurePass").click()

    if merchant_status_content == "Pending Risk Control Audit":
        print("法律风控审核通过")
    else:
        print("法律风控审核失败")
    # page.locator("#btnSubmitSure").click()
