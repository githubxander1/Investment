import unittest
from pages.public_choose_like_page import PublicChooseLikePage
from login import login_h5_get_token

class TestPublicChooseLike(unittest.TestCase):
    def setUp(self):
        token = login_h5_get_token()["data"]["token"]
        self.page = PublicChooseLikePage(token)

    def test_like(self):
        custom_id = 1  # 替换为实际的 custom_id
        response = self.page.like(custom_id)
        self.assertEqual(response["code"], 200)

if __name__ == "__main__":
    unittest.main()