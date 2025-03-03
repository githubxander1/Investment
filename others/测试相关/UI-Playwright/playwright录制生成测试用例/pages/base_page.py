from playwright.sync_api import Page
from typing import Optional

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def click_with_retry(self, locator: str, retries: int = 3) -> None:
        for attempt in range(retries):
            try:
                self.page.click(locator)
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                self.page.reload()

    def take_screenshot(self, name: str) -> None:
        self.page.screenshot(path=f"screenshots/{name}.png")