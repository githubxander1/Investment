# conftest.py
import pytest

from others.测试相关.api_mind.logic.login import login


@pytest.fixture(scope="session", autouse=True)
def token():
    """
    全局 fixture，用于在所有测试用例中自动注入登录后的 token。
    """
    print("\n登录并获取 token")
    email = "2695418206@qq.com"
    pw = "f2d8ddfc169a0ee6f8b0ecd924b1d300"
    token = login(email, pw)[1]
    print(f"获取到的 token: {token}")
    return token

@pytest.fixture(autouse=True)
def auto_print():
    """
    自动调用的前置和后置操作。
    """
    print("自动调用的前置")
    yield
    print("自动调用的后置")
