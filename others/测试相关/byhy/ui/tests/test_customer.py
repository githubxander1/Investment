import pytest

from others.测试相关.byhy.ui.pom.customer_page import CustomerPage
from others.测试相关.byhy.ui.pom.login_page import LoginPage


def test_add_customer(page, customer_data):
    login_page = LoginPage(page)
    customer_page = CustomerPage(page)

    login_page.navigate()
    login_page.login("byhy", "88888888")
    customer_page.add_customer(customer_data['name'], customer_data['phone'], customer_data['address'])
    customer_page.delete_customer()
