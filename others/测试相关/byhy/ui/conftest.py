import json

import pytest
from playwright.sync_api import sync_playwright


def pytest_generate_tests(metafunc):
    if 'customer_data' in metafunc.fixturenames:
        with open('data/customer_data.json', 'r', encoding='utf-8') as f:
            customer_data = json.load(f)
        metafunc.parametrize("customer_data", customer_data)

    if 'medicine_data' in metafunc.fixturenames:
        with open('data/medicine_data.json', 'r', encoding='utf-8') as f:
            medicine_data = json.load(f)
        metafunc.parametrize("medicine_data", medicine_data)

    if 'order_data' in metafunc.fixturenames:
        with open('data/order_data.json', 'r', encoding='utf-8') as f:
            order_data = json.load(f)
        metafunc.parametrize("order_data", order_data)

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()
