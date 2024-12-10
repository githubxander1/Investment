# pages/chatHome.py
import time

from appium.webdriver.common.touch_action import TouchAction

# from ..base.basePage import BasePage
from CompanyProject.APP_Fastbull2.base.basePage import BasePage
class ChatHome(BasePage):
    def __init__(self):
        super().__init__()
        self.to_chat = self.d(resourceId="com.bv.fastbull:id/tv_title", text="聊天")
        self.contact = self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.widget.ImageView[1]')
        self.edittext = self.d.xpath('//android.widget.EditText')
        self.global_search = self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.widget.ImageView[1]')
        self.conversation1 = self.d.xpath('//*[@resource-id="com.bv.fastbull:id/rv_session"]/android.view.ViewGroup[1]')
        self.cancel = self.d(description="取消")

        self.back =self.d(resourceId="com.bv.fastbull:id/iv_back")

    def click_back(self):
        self.back.click()

    def click_to_chat(self):
        self.to_chat.click()

    def click_contact(self):
        self.contact.click()

    def click_conversation(self):
        # time.sleep(3)
        # self.conversation1.click()
        self.d.click(0.551, 0.367)

    # def long_press_conversation(self):
    #     # 长按会话列表中的某个会话
    #     # conversation = self.d(resourceId="com.bv.fastbull:id/conversation_list_item", text=conversation_text)
    #     # if conversation1.exists:
    #     self.conversation1.long_click()
    #     # else:
    #     #     raise ValueError(f"Conversation with text '{conversation_text}' not found")

    # def long_press_conversation(self):
    #     # 长按会话列表中的某个会话
    #     # 使用特定的坐标进行长按操作
    #     action = TouchAction(self.d)
    #     action.long_press(x=0.551, y=0.367).release().perform()
    def click_global_search(self):
        self.global_search.click()

    def click_cancel(self):
        self.cancel.click()

    def send_text(self, text):
        self.edittext.set_text(str(text))

    def search(self, text):
        self.click_global_search()
        self.send_text(text)


