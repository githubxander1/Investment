import pytest

from others.测试相关.byhy.ui.pom.login_page import LoginPage
from others.测试相关.byhy.ui.pom.medicine_page import MedicinePage


@pytest.mark.parametrize("name, medicine_id, description", [
    ("新增药品1", "001", "描述随风倒随风倒十分"),
    ("新增药品2", "002", "描述随风倒随风倒十分")
])
def test_add_medicine(page, name, medicine_id, description):
    login_page = LoginPage(page)
    medicine_page = MedicinePage(page)

    login_page.navigate()
    login_page.login("byhy", "88888888")
    medicine_page.navigate()
    medicine_page.add_medicine(name, medicine_id, description)
