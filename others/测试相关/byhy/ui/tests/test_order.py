import pytest

from others.测试相关.byhy.ui.pom.login_page import LoginPage
from others.测试相关.byhy.ui.pom.order_page import OrderPage


@pytest.mark.parametrize("name, customer_id, keyword", [
    ("订单1", "80", "11"),
    ("订单2", "81", "12")
])
def test_add_order(page, name, customer_id, keyword):
    login_page = LoginPage(page)
    order_page = OrderPage(page)

    login_page.navigate()
    login_page.login("byhy", "88888888")
    order_page.navigate()
    order_page.add_order(name, customer_id, keyword)
# import pytest
# from pom.login_page import LoginPage
# from pom.order_page import OrderPage
#
# def test_add_order(pom, order_data):
#     login_page = LoginPage(pom)
#     order_page = OrderPage(pom)
#
#     login_page.navigate()
#     login_page.login("byhy", "88888888")
#     order_page.navigate()
#     order_page.add_order(order_data['name'], order_data['customer_id'], order_data['keyword'])
