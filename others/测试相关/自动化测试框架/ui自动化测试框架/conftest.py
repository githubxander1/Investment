import pytest

from utils.browser import get_driver
from utils.logger import setup_logger

setup_logger()

@pytest.fixture(scope='function')
def driver():
    driver = get_driver()
    yield driver
    driver.quit()