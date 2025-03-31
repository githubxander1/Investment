from common.base_api import BaseAPI

class PublicChooseLikePage(BaseAPI):
    def like(self, custom_id):
        url = "/publicChoose/like"
        payload = {
            "customId": custom_id
        }
        return self.send_request("POST", url, json=payload)