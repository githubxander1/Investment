from utils.retry_decorator import retry

@retry(3)
def test_login(auth_api):
    response = auth_api.login('default_user', 'default_password')
    assert 'token' in response