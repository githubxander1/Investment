import pytest
from utils.logger import setup_logger

from api.auth_api import AuthAPI
from api.chat_api import ChatAPI
from api.comment_api import CommentAPI
from api.password_api import PasswordAPI

setup_logger()

@pytest.fixture(scope='function')
def auth_api():
    base_url = "YOUR_TEST_ENV_BASE_URL"
    api = AuthAPI(base_url)
    return api

@pytest.fixture(scope='function')
def comment_api(auth_api):
    base_url = "YOUR_TEST_ENV_BASE_URL"
    login_response = auth_api.login('default_user', 'default_password')
    token = login_response['token']
    api = CommentAPI(base_url, token)
    return api

@pytest.fixture(scope='function')
def chat_api(auth_api):
    base_url = "YOUR_TEST_ENV_BASE_URL"
    login_response = auth_api.login('default_user', 'default_password')
    token = login_response['token']
    api = ChatAPI(base_url, token)
    return api

@pytest.fixture(scope='function')
def password_api(auth_api):
    base_url = "YOUR_TEST_ENV_BASE_URL"
    login_response = auth_api.login('default_user', 'default_password')
    token = login_response['token']
    api = PasswordAPI(base_url, token)
    return api