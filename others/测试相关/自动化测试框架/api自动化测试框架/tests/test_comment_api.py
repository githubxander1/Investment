from utils.retry_decorator import retry

@retry(3)
def test_post_comment(comment_api):
    response = comment_api.post_comment("This is a test comment.")
    assert 'id' in response