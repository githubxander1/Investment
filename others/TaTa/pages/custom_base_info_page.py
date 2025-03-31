from common.base_api import BaseAPI

class CustomBaseInfoPage(BaseAPI):
    def get_custom_base_info(self):
        url = "/custom/base-info"
        return self.send_request("GET", url)