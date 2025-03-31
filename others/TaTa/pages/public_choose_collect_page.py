from common.base_api import BaseAPI

class PublicChooseCollectPage(BaseAPI):
    def collect(self, custom_id):
        url = "/publicChoose/collect"
        payload = {
            "customId": custom_id
        }
        return self.send_request("POST", url, json=payload)