from pprint import pprint

from playwright.sync_api import sync_playwright
from typing import List, Dict


def scrape_page_elements(url: str) -> List[Dict]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # 获取关键交互元素（输入框、按钮等）
        elements = page.query_selector_all("input, button, [role='button'], textarea, select")
        element_data = []

        for element in elements:
            element_info = {
                # "tag": element.tag_name.lower(),
                "id": element.get_attribute("id") or "",
                "name": element.get_attribute("name") or "",
                "type": element.get_attribute("type") or "button"
            }
            element_data.append(element_info)

        browser.close()
        return element_data

# 示例：提取登录页面的控件信息
url = "https://www.saucedemo.com/"
# url = "https://m.payok.com/payok-register-register.html?_gl=1*19b9lq2*_ga*OTM0NzE3MTM1LjE3NDAzNzkzOTQ.*_ga_4GFDPR3XPW*MTc0MDM3OTM5NC4xLjAuMTc0MDM3OTM5NC42MC4wLjE5NzYzNzc1Mzc."
page_objects =scrape_page_elements(url)
#保存到文件
# with open("page_objects.py", "w") as f:
#     f.write(str(page_objects))
print("页面控件信息：")
pprint(page_objects)