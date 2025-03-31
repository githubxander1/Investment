import unittest
from pages.public_choose_collect_page import PublicChooseCollectPage
from login import login_h5_get_token

class TestPublicChooseCollect(unittest.TestCase):
    def setUp(self):
        token = login_h5_get_token()["data"]["token"]
        self.page = PublicChooseCollectPage(token)

    def test_collect(self):
        custom_id = 1  # 替换为实际的 custom_id
        response = self.page.collect(custom_id)
        self.assertEqual(response["code"], 200)

if __name__ == "__main__":
    unittest.main()