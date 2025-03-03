from pprint import pprint

from bs4 import BeautifulSoup
import requests

# def extract_page_objects(url):
#     """
#     爬取页面并提取控件信息，生成 Page Object 类元素
#     :param url: 页面 URL
#     :return: 控件信息字典
#     """
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     pprint(soup)
#
#     # # 提取按钮
#     # buttons = {button.get("id"): button for button in soup.find_all("button") if button.get("id")}
#     # # 提取输入框
#     # inputs = {input.get("id"): input for input in soup.find_all("input") if input.get("id")}
#     buttons = []
#     for button in soup.find_all("button"):
#         button_id = button.get("id")
#         button_name = button.get('name')
#         button_data_test = button.get('data-test')
#         if button_id:
#             buttons[button_id] = button
#         elif button_name:
#             buttons[button_name] = button
#         elif button_data_test:
#             buttons[button_data_test] = button
#
#     inputs = []
#     for input in soup.find_all("input"):
#         input_id = input.get("id")
#         input_name = input.get('name')
#         input_data_test = input.get('data-test')
#         if input_id:
#             inputs[input_id] = input
#         elif input_name:
#             inputs[input_name] = input
#         elif input_data_test:
#             inputs[input_data_test] = input
#             # buttons.append({"id": button_id, "name": button_name, "data-test": button_data_test})
#     pprint(soup.find_all("button"))
#     pprint(soup.find_all("input"))
#     return {"buttons": buttons, "inputs": inputs}
#
# # 示例：提取登录页面的控件信息
# # url = "https://m.payok.com/payok-register-register.html?_gl=1*19b9lq2*_ga*OTM0NzE3MTM1LjE3NDAzNzkzOTQ.*_ga_4GFDPR3XPW*MTc0MDM3OTM5NC4xLjAuMTc0MDM3OTM5NC42MC4wLjE5NzYzNzc1Mzc."
# url = "https://www.saucedemo.com/"
# page_objects = extract_page_objects(url)
# print("页面控件信息：")
# pprint(page_objects)

from pprint import pprint
from playwright.sync_api import sync_playwright

def extract_page_objects(url):
    """
    使用Playwright爬取页面并提取控件信息，生成 Page Object 类元素
    :param url: 页面 URL
    :return: 控件信息字典
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        controls = {
            "buttons": {},
            "inputs": {},
            # "other_elements": {}
        }

        # 提取所有交互元素
        for element in page.query_selector_all("*"):
            tag = element.evaluate("el => el.tagName.toLowerCase()")
            element_type = element.get_attribute("type")

            identifier = element.get_attribute("data-test") \
                        or element.get_attribute("id") \
                        or element.get_attribute("name")

            if identifier:
                if tag == "button" or (tag == "input" and element_type == "submit"):
                    controls["buttons"][identifier] = identifier
                elif tag == "input":
                    controls["inputs"][identifier] = identifier
                # else:
                #     controls["other_elements"][identifier] = identifier

        browser.close()
        # return {"buttons": buttons, "inputs": inputs}
        return controls

# 示例：提取登录页面的控件信息
# url = "https://www.saucedemo.com/"
url = "https://m.payok.com/payok-register-register.html?_gl=1*19b9lq2*_ga*OTM0NzE3MTM1LjE3NDAzNzkzOTQ.*_ga_4GFDPR3XPW*MTc0MDM3OTM5NC4xLjAuMTc0MDM3OTM5NC42MC4wLjE5NzYzNzc1Mzc."
page_objects =extract_page_objects(url)
print("页面控件信息：")
pprint(page_objects)
