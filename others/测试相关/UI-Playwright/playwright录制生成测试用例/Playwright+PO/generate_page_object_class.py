def generate_page_object_class(page_name, controls):
    """
    根据控件信息生成 Page Object 类
    :param page_name: 页面名称
    :param controls: 控件信息
    :return: Page Object 类代码
    """
    class_template = f"""
    class {page_name}Page:
        def __init__(self, page):
            self.page = page
    """

    # 添加控件定位和操作方法
    for control_type, elements in controls.items():
        for element_id, element in elements.items():
            locator = f"self.page.locator(\"{element_id}\")"
            class_template += f"""
        def get_{element_id}(self):
            return {locator}
        def click_{element_id}(self):
            {locator}.click()
        """
    if control_type == "inputs":
        class_template += f"""
        def fill_{element_id}(self, text):
            {locator}.fill(text)
        """

    return class_template

# 示例：生成登录页面的 Page Object 类
from extract_page_objects import page_objects
page_name = "Login"
page_object_code = generate_page_object_class(page_name, page_objects)
#保存到文件
# with open(f"{page_name}_page.py", "w") as f:
#     f.write(page_object_code)
print(page_object_code)