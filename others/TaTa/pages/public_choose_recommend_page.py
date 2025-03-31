from common.base_api import BaseAPI

class PublicChooseRecommendPage(BaseAPI):
    def get_recommend(self):
        url = "/publicChoose/recommend"
        return self.send_request("GET", url)