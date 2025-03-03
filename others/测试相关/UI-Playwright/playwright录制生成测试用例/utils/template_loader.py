from typing import List, Dict

from jinja2 import Environment, FileSystemLoader
import os


def generate_page_object(page_name: str, elements: List[Dict]) -> str:
    # env = Environment(loader=FileSystemLoader("utils/templates"))
    # 修改模板加载路径（第7行）
    env = Environment(loader=FileSystemLoader(
        os.path.join(os.path.dirname(__file__), "templates")  # 使用绝对路径
    ))

    template = env.get_template("page_template.j2")

    return template.render(
        page_name=page_name,
        elements=elements
    )


# 模板文件 utils/templates/page_template.j2 内容：
"""
from .base_page import BasePage

class {{ page_name }}Page(BasePage):
    {% for element in elements %}
    @property
    def {{ element.id or element.name }}_element(self):
        return self.page.locator("{{ 'id=' + element.id if element.id else '[name="' + element.name + '"]' }}")
    {% endfor %}

    def perform_action(self, data: dict):
        {% for element in elements if element.tag == 'input' %}
        self.{{ element.id }}_element.fill(data.get("{{ element.id }}", ""))
        {% endfor %}
        {% for element in elements if element.tag == 'button' %}
        self.{{ element.id }}_element.click()
        {% endfor %}
"""
if __name__ == "__main__":
    page_name = "Login"
    elements = [{'id': 'user-name', 'name': 'user-name', 'type': 'text'},
 {'id': 'password', 'name': 'password', 'type': 'password'},
 {'id': 'login-button', 'name': 'login-button', 'type': 'submit'}]

    page_object = generate_page_object(page_name, elements)
    print(page_object)