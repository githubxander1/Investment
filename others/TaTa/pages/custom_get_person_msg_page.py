from common.base_api import BaseAPI

class CustomGetPersonMsgPage(BaseAPI):
    def get_person_msg(self):
        url = "/custom/getPersonMsg"
        return self.send_request("GET", url)