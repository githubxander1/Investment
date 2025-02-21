def test_get_user_info(user_api):
    response = user_api.get_user_info(1)
    assert response.status_code == 200