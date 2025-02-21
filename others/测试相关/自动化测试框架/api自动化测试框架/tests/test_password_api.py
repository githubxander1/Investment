from utils.retry_decorator import retry

@retry(3)
def test_change_password(password_api):
    response = password_api.change_password("old_password", "new_password")
    assert 'success' in response and response['success']