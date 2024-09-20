import pytest
from CompanyProject.appUI_fastbull_selenium.pages.login_and_register.login_page import LoginPage

@pytest.fixture(scope='module')
def setup():
    login_page = LoginPage()
    login_page.open_app()
    yield login_page
    login_page.close_app()

