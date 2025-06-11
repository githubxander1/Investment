import logging
from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


def platform_risk_control_audit(page, merchant_id, pdf_file_path):
    # 开始风险审核
    link_risk_control = page.get_by_role("link", name=" Risk Control ")
    if link_risk_control.get_attribute("class") != "active":
        page.get_by_role("link", name=" Risk Control ").click()
        page.get_by_role("link", name="Risk Control", exact=True).click()
    page.pause()
    row = page.locator("tbody tr").filter(has_text=merchant_id)
    merchant_status = row.locator("td").nth(6)
    merchant_status_content = merchant_status.text_content()
    left_wrapper = page.locator(".dataTables_scrollBody")
    left_row = left_wrapper.locator("tbody tr").filter(has_text=merchant_id)
    left_row.wait_for(state="visible", timeout=3000)
    row_index = left_row.evaluate('(row) => Array.from(row.parentNode.children).indexOf(row)')
    right_wrapper = page.locator(".DTFC_RightBodyLiner")
    corresponding_right_row = right_wrapper.locator("tbody tr").nth(row_index)
    risk_control_audit_button = corresponding_right_row.get_by_text("Risk Control Audit")
    if merchant_status_content == "Pending Risk Control Audit":
        risk_control_audit_button.click()

        page.pause()
        # 上传风控报告
        page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
        page.locator("#reportForm1").click()
        page.locator("#reportForm2").click()
        page.locator("#reportForm3").click()

        page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：风控报告上传成功，风险控制审计通过")
        page.get_by_role("button", name="Approve").click()
        # page.locator("#btnSubmitSure").click()
        page.locator("#btnSurePass").click()

        # page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：风险控制审计通过")
        # page.locator("#toRiskAudit").click()

        # page.get_by_role("link", name="None").click()

        page.wait_for_timeout(1000)
        page.reload(wait_until="networkidle")
        merchant_status2 = row.locator("td").nth(6)
        merchant_status_content2 = merchant_status2.text_content()
        if merchant_status_content2 == "Pending Legal Audit":
            print("✅风险审核通过，下一步：Request Activation")
        else:
            print(f"⚠️风险审核未通过，{merchant_status_content2}")
    else:
        print("⚠️提示：商户状态不是Pending Risk Control Audit,不需要再进行该流程")