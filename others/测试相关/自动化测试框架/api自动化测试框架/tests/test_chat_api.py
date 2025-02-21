from utils.retry_decorator import retry

@retry(3)
def test_send_message(chat_api):
    response = chat_api.send_message("Hello!")
    assert 'id' in response

@retry(3)
def test_send_file(chat_api):
    file_path = "test_file.txt"
    response = chat_api.send_file(file_path)
    assert 'id' in response