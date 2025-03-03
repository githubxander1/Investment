def generate_page_object(page_elements, class_name: str = "LoginPage") -> str:
    """生成Page Object模型代码

    Args:
        page_elements: 页面元素列表
        class_name: 生成的类名（默认：LoginPage）

    Returns:
        str: 生成的Page Object类代码
    """
    class_template = f"""from playwright.sync_api import Page

class {class_name}:
    def __init__(self, page: Page):
        self.page = page
        self._init_elements()
        
    def _init_elements(self):"""

    element_methods = []

    for idx, element in enumerate(page_elements, 1):
        # 生成定位器
        locator = ""
        if element["id"]:
            locator = f'id={element["id"]}'
        elif element["name"]:
            locator = f'[name="{element["name"]}"]'
        else:
            locator = f'xpath=//*[@id or @name][{idx}]'  # 兜底定位

        # 生成元素名称
        element_name = element["id"] or element["name"] or f"element_{idx}"
        element_name = element_name.replace("-", "_").lower()

        # 添加定位器初始化
        class_template += f"\n        self.{element_name} = self.page.locator('{locator}')"

        # 扩展类型判断逻辑
        element_type = element.get("type", "").lower()
        input_types = {"text", "password", "email", "number", "search", "tel"}
        clickable_types = {"button", "submit", "reset", "checkbox", "radio"}

        # 生成操作方法（新增标签类型判断）
        if element_type in input_types or element.get("tag") == "textarea":
            method = f"""
    def input_{element_name}(self, text: str):
        self.{element_name}.fill(text)
        return self"""
            element_methods.append(method)
        elif element_type in clickable_types or element.get("tag") == "button":
            method = f"""
    def click_{element_name}(self):
        self.{element_name}.click()
        return self"""
            element_methods.append(method)

    return class_template + "\n\n".join(element_methods)


# 使用示例
from element_scraper import scrape_page_elements
page_objects = scrape_page_elements("https://www.saucedemo.com/")
# page_objects = scrape_page_elements("https://m.payok.com/payok-register-register.html?_gl=1*19b9lq2*_ga*OTM0NzE3MTM1LjE3NDAzNzkzOTQ.*_ga_4GFDPR3XPW*MTc0MDM3OTM5NC4xLjAuMTc0MDM3OTM5NC42MC4wLjE5NzYzNzc1Mzc.")
po_code = generate_page_object(page_objects)
# with open("LoginPage.py", "w") as f:
#     f.write(po_code)
print(po_code)
