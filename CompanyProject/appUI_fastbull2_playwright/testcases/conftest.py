import pytest
from playwright.sync_api import sync_playwright

from CompanyProject.appUI_fastbull2_playwright.pages.login_pagessss import LoginPage


@pytest.fixture(scope='module')
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope='module')
def setup(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    yield login_page, page
    page.close()
    context.close()
    browser.close()
