import logging
import time

import uiautomator2

logging.basicConfig(level=logging.INFO)

d = uiautomator2.connect()
d.implicitly_wait(10)

confirm_button = d.xpath('//*[contains(@text,"合同号111")]')
if confirm_button.exists:
    logging.info("交易委托成功")
else:
    logging.info("交易委托失败")