from common.base_api import BaseAPI

class PublicChooseShareCustomDetailPage(BaseAPI):
    def get_share_custom_detail(self, share_code):
        url = f"/publicChoose/shareCustomDetail?shareCode={share_code}"
        return self.send_request("GET", url)