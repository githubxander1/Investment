from uiautomator2 import connect

class U2Utils:
    def __init__(self, device_name='127.0.0.1:21503'):
        self.d = connect(device_name)

    def open_app(self, package_name='com.bv.fastbull'):
        self.d.app_start(package_name)

    def close_app(self, package_name='com.bv.fastbull'):
        self.d.app_stop(package_name)

    def find_element(self, selector):
        return self.d(resourceId=selector)

    def click_element(self, selector):
        self.d(resourceId=selector).click()

    def fill_element(self, selector, text):
        self.d(resourceId=selector).set_text(text)

    def is_element_visible(self, selector):
        return self.d(resourceId=selector).exists

# if __name__ == '__main__':
#     u2 = U2Utils()
#     u2.open_app()
    # u2.click_element('com.bv.fastbull:id/iv_avatar')