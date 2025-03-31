import unittest
from pages.public_choose_share_custom_detail_page import PublicChooseShareCustomDetailPage
from login import login_h5_get_token

class TestPublicChooseShareCustomDetail(unittest.TestCase):
    def setUp(self):
        token = login_h5_get_token()["data"]["token"]
        self.page = PublicChooseShareCustomDetailPage(token)

    def test_get_share_custom_detail(self):
        share_code = "abc123"  # 替换为实际的 share_code
        response = self.page.get_share_custom_detail(share_code)
        self.assertEqual(response["code"], 200)

if __name__ == "__main__":
    unittest.main()