import logging
import os

from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


def sales_submit_merchant_info(page, email, merchant_id, pdf_file_path):
    link_merchant = page.get_by_role("link", name="ﱖ Merchant ")
    if link_merchant.get_attribute("class") != "active":
        page.get_by_role("link", name="ﱖ Merchant ").click()
        page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()

        # link_merchant.click()

    page.wait_for_timeout(1000)

    row = page.locator("tbody tr").filter(has_text=merchant_id)
    merchant_status = row.locator("td").nth(2)
    merchant_status_content = merchant_status.text_content()
    left_wrapper = page.locator(".dataTables_scrollBody")
    left_row = left_wrapper.locator("tbody tr").filter(has_text=merchant_id)
    left_row.wait_for(state="visible",timeout=3000)
    row_index = left_row.evaluate('(row) => Array.from(row.parentNode.children).indexOf(row)')
    right_wrapper = page.locator(".DTFC_RightBodyLiner")
    corresponding_right_row = right_wrapper.locator("tbody tr").nth(row_index)
    submit_button = corresponding_right_row.get_by_text("Submit")
    if merchant_status_content == "Pending complete the information":
        with page.expect_popup() as popup_info:
            submit_button.click()
        page = popup_info.value
        page.wait_for_timeout(1000)
        page.get_by_role("textbox", name="Company Name *").fill(email)
        page.get_by_role("textbox", name="Company Brand Name").fill(email)
        page.get_by_role("textbox", name="Company Abbreviation").fill("公司缩写")
        page.get_by_label("Types of Companies *").select_option("100")
        page.get_by_role("textbox", name="Official Website *").click()
        page.get_by_label("Types of Companies *").select_option("105")
        # page1.get_by_label("Types of Companies *").select_option("100")
        page.get_by_role("textbox", name="Official Website *").fill(
            "http://paylabs-test.com/sales/paylabs-merchant-info.html?k=1bdd7098b1cebd36e3d4be0028b9a7c3")
        page.get_by_role("textbox", name="Company Address *").fill("广东省深圳市南山区桃源街道中广时代广场001")
        page.get_by_role("textbox", name="PIC Name *").fill("PIC名称")
        page.get_by_role("textbox", name="PIC Contact Number *").fill("123456789")
        page.get_by_role("textbox", name="PIC Email *").fill("1@qq.com")
        page.get_by_role("textbox", name="PIC Address").fill("广东省深圳市南山区桃源街道中广时代广场001")
        page.locator("#select2-merchantType-container").click()
        page.get_by_role("treeitem", name="Advertising").click()
        page.get_by_role("textbox", name="Default Amount Range (Upper").fill("100")
        page.get_by_role("textbox", name="Default Amount Range", exact=True).fill("1000")
        page.get_by_role("textbox", name="Default Transaction Range (").fill("2147")
        page.get_by_role("textbox", name="Default Transaction Range", exact=True).fill("3000")
        page.get_by_role("textbox", name="Default Income Range (Upper").fill("100")
        page.get_by_role("textbox", name="Default Income Range", exact=True).fill("1000")
        page.get_by_role("textbox", name="##.###.###.#-###.###").fill("00.000.000.0-000.000")
        page.locator("#checkNPWP").click()
        page.get_by_role("textbox", name="LawanTransaksiID").fill("13546512456")
        page.get_by_role("textbox", name="NIK").fill("124")
        page.locator("#checkNIK").click()
        page.get_by_role("textbox", name="Account Number *").fill("15354879")
        page.get_by_role("textbox", name="Account Name *").fill("账户名称")
        page.get_by_role("textbox", name="Bank Name *").fill("中国人民银行")
        page.get_by_role("textbox", name="SWIFT Code *").fill("1236547")
        page.get_by_role("textbox", name="Business Contact *").fill("商务联系人")
        page.get_by_role("textbox", name="Technical Contact *").fill("技术联系人")
        page.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")
        page.get_by_role("textbox", name="Technical Contact Email *").fill("1@qq.com")
        page.get_by_role("textbox", name="Finance Contact *").fill("财务联系人")
        page.get_by_role("textbox", name="Finance Contact Number *").fill("15318544154")
        page.get_by_role("textbox", name="Business Contact Number *").fill("15318544154")
        page.get_by_role("textbox", name="Business Contact Email *").fill("1@qq.com")
        page.get_by_role("textbox", name="Finance Contact Email *").fill("1@qq.com")
        page.get_by_role("textbox", name="CS Contact", exact=True).fill("CS联系人")
        page.get_by_role("textbox", name="CS Contact Number").fill("15318544154")
        page.get_by_role("textbox", name="CS Contact Email").fill("1@qq.com")

        # def upload_file(file_path, form_id):
        #     if not os.path.exists(file_path):
        #         print(f"文件不存在: {file_path}")
        #         return
        #
        #     # print(f"文件存在: {file_path}")
        #
        #     # 监听 file_chooser 事件
        #     page.on('filechooser', lambda file_chooser: file_chooser.set_files(file_path))
        #     page.locator(f"#btnUpload{form_id}").click()
        #
        # #
        # # # 上传文件
        # upload_file(pdf_file_path, "11")
        # upload_file(pdf_file_path, "12")
        # upload_file(pdf_file_path, "13")
        # upload_file(pdf_file_path, "14")
        # upload_file(pdf_file_path, "15")
        # upload_file(pdf_file_path, "16")
        # upload_file(pdf_file_path, "17")
        # upload_file(pdf_file_path, "18")
        # upload_file(pdf_file_path, "22")  #
        # upload_file(pdf_file_path, "24")
        page.pause()

        page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
        page.wait_for_selector("#btnUpload12").click()
        # page.locator("#btnUpload12").click()

        # page.locator("#btnUpload12").click()
        page.locator("#btnUpload13").click()
        # page.locator("#btnUpload14").click()
        page.locator("#btnUpload15").click()
        page.locator("#btnUpload16").click()
        # page.locator("#btnUpload17").click()
        page.locator("#btnUpload18").click()
        # page.locator("#btnUpload22").click()
        page.locator("#btnUpload24").click()

        # page.get_by_role("heading", name="").locator("i").click()
        # page.pause()
        page.locator("#addTemp div").nth(1).click()
        page.locator("#select2-selTempsModal-container").click()
        # page.get_by_role("treeitem", name="Power of Attorney").click()
        select_bank_account_book = page.get_by_role("treeitem", name="Copy of Bank Account Book")
        # select_bank_account_book = page.get_by_role("treeitem", name="Power of Attorney")
        # aria - disabled = "true" 如果select_bank_account_book元素的aria-disabled属性为true，则表示该元素被禁用，无法被点击。点击cancel按钮
        if select_bank_account_book.is_disabled():
            page.get_by_role("button", name="Cancel").click()
        else:
            select_bank_account_book.click()
            page.locator("#merFormModal i").click()

            page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
            page.locator("#temps-modal").click()
            page.wait_for_timeout(1000)
            page.locator("#btnSureTempModal").click()  # id="btnSureTempModal"

        page.get_by_text("I declare that the application information submitted by the merchant for").click()
        page.get_by_text("I declare that the above").click()

        page.get_by_role("button", name="Save").click()

        page.wait_for_timeout(1000)
        page.locator("#btnSubmit").click()
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="I got it").click()

        page.wait_for_timeout(1000)
        merchant_status_content = row.locator("td").nth(2).text_content()
        if merchant_status_content == "Pending Risk Control Audit":
            print("✅资料提交成功，下一步：Pending Risk Control Audit")
        else:
            print(f"⚠️提示：销售设置失败,{merchant_status_content}")
    else:
        print("⚠️提示：商户状态不是Pending complete the information，不需要再提交资料")
    # else:
    #     logging.info("商户已提交")
