import pytest
import yaml
from playwright.sync_api import Page
from pages.login_page import LoginPage


def load_test_data():
    with open("data/login_data.yaml") as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize("test_case", load_test_data())
def test_login(page: Page, test_case):
    login_page = LoginPage(page)
    login_page.navigate("https://example.com/login")
    login_page.perform_action(test_case["data"])

    if "success" in test_case["expected"]:
        assert page.url == "https://example.com/dashboard"
    else:
        error_message = page.query_selector(".error-message")
        assert error_message is not None