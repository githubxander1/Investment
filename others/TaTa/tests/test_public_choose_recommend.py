import unittest
from pages.public_choose_recommend_page import PublicChooseRecommendPage
from login import login_h5_get_token

class TestPublicChooseRecommend(unittest.TestCase):
    def setUp(self):
        token = login_h5_get_token()["data"]["token"]
        self.page = PublicChooseRecommendPage(token)

    def test_get_recommend(self):
        response = self.page.get_recommend()
        self.assertEqual(response["code"], 200)

if __name__ == "__main__":
    unittest.main()