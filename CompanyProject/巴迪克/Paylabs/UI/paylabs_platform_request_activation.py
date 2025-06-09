import logging
from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


def platform_request_activation(page,merchant_id):
    # 激活请求
    page.get_by_role("link", name="ﶇ Merchant ").click()
    page.get_by_role("link", name="Merchant List").click()

    # page.pause()
    page.wait_for_timeout(1000)
    # 移动滑块
    scroll_div = page.wait_for_selector('#scrollDiv')  # 等待目标 div 加载
    scroll_div_table = page.query_selector('#scrollDivTable')  # 获取 scrollDivTable 的宽度
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')  # 滚动到最右侧

    row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    #
    # # 查找该行中的 Setting Sales 按钮
    # setting_sales_button = row.locator("button[name='btnSetSales']")
    # activate_request_button = row.locator("#btnOnlineApply").first
    request_activate_button = row.get_by_role('button', name="Request Activation ")
    try:
        # 等待按钮可点击
        # page.pause()
        # 尝试直接使用 JavaScript 点击按钮
        page.evaluate('(button) => button.click()', request_activate_button.element_handle())
    except Exception as e:
        print(f"点击设置sales按钮失败：{e}")

    # request_audio = page.locator("button[name=\"btnOnlineApply\"]").nth(2)
    # request_audio2 = page.locator("tbody").filter(
    #     has_text="DataRequest ActivationSystem ConfigurationDataConfiguration Status Store List").locator(
    #     "button[name=\"btnOnlineApply\"]")
    # request_audio3 = page.locator("tbody").filter(
    #     has_text="DataRequest ActivationSystem ConfigurationDataSystem ConfigurationDataSystem").locator(
    #     "button[name=\"btnOnlineApply\"]")
    # request_audio4 = page.locator("tbody").filter(
    #     has_text="DataConfiguration Status Store List System ConfigurationDataConfiguration").locator(
    #     "button[name=\"btnOnlineApply\"]")
    # # #merchant-datatable_wrapper > div:nth-child(2) > div > div.DTFC_ScrollWrapper > div.DTFC_RightWrapper > div.DTFC_RightBodyWrapper > div > table > tbody > tr:nth-child(4) > td > div > button.btn.btn-blue.font-12.mr-1.online-apply.w-53
    # # //*[@id="merchant-datatable_wrapper"]/div[2]/div/div[1]/div[3]/div[2]/div/table/tbody/tr[4]/td/div/button[2]
    # try:
    #     if request_audio.is_visible():
    #         request_audio.click()
    #     elif request_audio2.is_visible():
    #         request_audio2.click()
    #     elif request_audio4.is_visible():
    #         request_audio4.click()
    #     else:
    #         request_audio3.click()
    # except Exception as e:
    #     print(f"点击request_audio按钮时发生错误:{e}")


    # page.get_by_role("button", name="H5 Display").click()
    page.locator("#nav_1 div").filter(has_text="DanamonVA Settlement Type").get_by_role("button").click()
    page.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("label").first.click()
    # page.locator("#nav_1 div").filter(has_text="DanamonVA Settlement Type").get_by_role("button").click()
    page.locator("#rate232").fill("99")
    page.locator("#fee232").fill('10000')
    page.locator("#transSharingRate232").fill("0")
    page.locator("#transSharingFee232").fill("0")
    page.pause()
    # page.locator("#merVatSel1242").select_option("0")
    # page.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("select[name=\"selMerVat\"]").select_option(
    #     "0.11")

    page.get_by_role("cell", name="Non-active").locator("label").click()
    page.get_by_role("cell", name="Active").get_by_role("list").click()

    # page.pause()
    page.get_by_role("button", name="Select all").click()
    # page.pause()
    page.get_by_role("cell", name="Merchant Cost ").click()
    # page.locator("button[name=\"btnSelectCancel\"]").click()
    page.get_by_role("cell", name="*Merchant Fee % Sample:0.7000").get_by_role("textbox").first.fill("99")
    page.get_by_role("textbox", name="1000").fill("10000")
    # page.get_by_role("cell", name="*Merchant Fee 4 % Sample:0.").get_by_role("combobox").select_option("0.11")
    page.get_by_role("cell", name="*Merchant Fee 99 % Sample:0.").get_by_role("combobox").select_option("0.11")
    page.get_by_role("textbox", name="Merchant RSA Public Key").fill("123456789")

    # page.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("select[name=\"selMerVat\"]").select_option("0.11")
    # page.get_by_role("link", name="E-Money/Wallet").click()
    # page.get_by_role("listitem").filter(has_text="DANA Paylabs").locator("label").first.click()
    # page.locator("#nav_2 div").filter(has_text="DANABALANCE Settlement Type").get_by_role("button").click()
    # page.get_by_role("listitem").filter(has_text="DANA Paylabs").locator("select[name=\"selMerVat\"]").select_option("0.11")
    # page.get_by_role("link", name="CreditCard").click()
    # page.locator("#nav_3 > li > .form-row > div > .form-d-flex > .w-70-px > .pr-4").first.click()
    # page.locator("#nav_3 > li > .form-row > div:nth-child(3) > div > div:nth-child(5)").first.click()
    # page.locator("#nav_3 div").filter(has_text="CIMBCC Settlement Type").get_by_role("button").click()
    # page.get_by_role("link", name="QRIS", exact=True).click()
    # page.locator("#nav_4 div").filter(has_text="StaticQRIS Settlement Type").get_by_role("button").click()
    # page.locator("#nav_4 > li > .form-row > div > .form-d-flex > .w-70-px > .pr-4").first.click()
    # page.locator("#rate1231").fill("0.0001")
    # page.locator("#transSharingRate1231").fill("0.0001")
    # page.get_by_role("link", name="Payin Cash Outlet").click()
    # page.get_by_role("listitem").filter(has_text="POS Paylabs SettlementChannel").locator("label").first.click()
    # page.locator("#rate1239").fill("0.0001")
    # page.locator("#transSharingRate1239").fill("0.0001")
    # page.get_by_role("button", name="H5 Hidden").click()
    # page.get_by_role("link", name="CardlessCredit").click()
    # page.locator("#nav_6 div").filter(has_text="Indodana Settlement Type").get_by_role("button").click()
    # page.get_by_role("listitem").filter(has_text="TestBankVA Paylabs").locator("label").first.click()
    # page.locator("#transSharingRate1218").fill("0.0001")
    # page.get_by_role("cell", name="Non-active").locator("label").click()
    # page.get_by_role("cell", name="Active").get_by_role("list").click()
    # page.get_by_role("button", name="Select all").click()
    # page.locator("button[name=\"btnSelectCancel\"]").click()
    # page.get_by_role("cell", name="Active").get_by_role("list").click()
    # page.get_by_role("treeitem", name="BANK BNI", exact=True).locator("span").click()
    # page.get_by_role("cell", name="*Merchant Fee % Sample:0.7000").get_by_role("textbox").first.fill("0.01")
    # page.get_by_role("textbox", name="1000").fill("0.05")
    # page.get_by_role("textbox", name="Not involved in profit sharing").click()
    # page.get_by_role("treeitem", name="test-S -").click()
    # page.locator("#btnConfirm").click()
    # page.get_by_role("textbox", name="111111").click()
    # page.locator("#select2-agentMans-container").click()
    # page.get_by_role("treeitem", name="[667665] - dgadfag").click()
    # page.get_by_role("textbox", name="Choose...").click()
    # page.get_by_role("treeitem", name="test-A -").click()
    # page.locator("#btnConfirm").click()
    # page2.get_by_role("textbox", name="Max 200 characters can be").fill("request 审核通过")
    # page2.get_by_role("button", name="Comment").click()
    # page.pause()
    page.get_by_role("button", name="Submit Request").click()
    print("激活请求提交成功")