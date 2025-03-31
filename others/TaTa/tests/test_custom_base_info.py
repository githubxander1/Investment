import unittest
from pages.custom_base_info_page import CustomBaseInfoPage
from login import login_h5_get_token

class TestCustomBaseInfo(unittest.TestCase):
    def setUp(self):
        token = login_h5_get_token()["data"]["token"]
        self.page = CustomBaseInfoPage(token)

    def test_get_custom_base_info(self):
        response = self.page.get_custom_base_info()
        self.assertEqual(response["code"], 200)

if __name__ == "__main__":
    unittest.main()