from CompanyProject.appUI_fastbull_selenium.utils.u2_utils import U2Utils
from ..utils.u2_utils import U2Utils

class BasePage(U2Utils):
    def __init__(self, device_name='127.0.0.1:21503'):
        super().__init__(device_name)
