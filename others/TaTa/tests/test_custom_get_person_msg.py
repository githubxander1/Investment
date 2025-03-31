import unittest
from pages.custom_get_person_msg_page import CustomGetPersonMsgPage
from login import login_h5_get_token

class TestCustomGetPersonMsg(unittest.TestCase):
    def setUp(self):
        token = login_h5_get_token()["data"]["token"]
        self.page = CustomGetPersonMsgPage(token)

    def test_get_person_msg(self):
        response = self.page.get_person_msg()
        self.assertEqual(response["code"], 200)

if __name__ == "__main__":
    unittest.main()