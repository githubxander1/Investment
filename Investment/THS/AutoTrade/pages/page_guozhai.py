# page_guozhai.py
import time

import uiautomator2 as u2

from Investment.THS.AutoTrade.pages.page_logic import THSPage
from Investment.THS.AutoTrade.scripts.account_info import click_holding_stock_button
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger('nihuigou.log')

# d = u2.connect()
class GuozhaiPage(THSPage):
    def __init__(self, d):
        super().__init__(d)
        prompt_content = self.d(resourceId="com.hexin.plat.android:id/prompt_content")
        confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        back_button = self.d(resourceId="com.hexin.plat.android:id/title_bar_img")
    def is_on_home_page(self):
        """判断是否在首页"""
        return self.d(resourceId="com.hexin.plat.android:id/tab_mn").exists()

    def is_on_guozhai_list_page(self):
        """判断是否在国债逆回购列表页"""
        return self.d(text="我要回购").exists()

    def is_on_holding_list_page(self):
        """判断是否在持仓列表页"""
        return self.d(text="可用").exists()

    def _enter_guozhai_page(self):
        """进入国债逆回购页面"""
        if self.is_on_guozhai_list_page():
            return True

        # 点击持仓按钮
        self.click_holding_stock_button()

        # 点击国债逆回购入口
        right_icons = self.d(resourceId="com.hexin.plat.android:id/title_right_image")
        if right_icons.count >= 2:
            right_icons[1].click()
            return self.wait_for_element(self.d(text="我要回购"), timeout=5)
        return False


    def _find_and_click_product(self, target_name):
        """查找并点击目标产品"""
        self.d.swipe(0.5, 0.8, 0.5, 0.2)
        time.sleep(1)
        # 优先通过文本定位
        elements = self.d(text=target_name)
        if elements.exists():
            elements[0].click()
            return True

        # 尝试通过分类查找
        # category = self.d(resourceId="com.hexin.plat.android:id/tv_title", text="沪深市场")
        # if category.exists():
        #     category.click()

        # 滑动查找
        for _ in range(5):
            elements = self.d(text=target_name)
            if elements.exists():
                elements[0].click()
                return True
            time.sleep(1)
        return False
    def wait_for_element(self, selector, timeout=10):
        """
        等待元素出现
        """
        for _ in range(timeout):
            if selector.exists():
                return True
            time.sleep(1)
        return False

    def scroll_to_find_element(self, text, max_swipe=5):
        """
        滑动查找指定文本的 TextView 元素
        :param text: 要查找的文本
        :param max_swipe: 最大滑动次数
        :return: 找到的元素或 None
        """
        for _ in range(max_swipe):
            elements = self.d(className="android.widget.TextView", text=text)
            if elements:
                return elements[0]
            self.d.swipe(0.5, 0.8, 0.5, 0.2)
            time.sleep(1)
        return None
    def assert_on_gc001_page(self, timeout=10):
        """
        断言当前页面是否为 GC001(1天期) 页面
        :param timeout: 最大等待时间
        :return: 成功返回 True，失败返回 False
        """
        try:
            # element = self.d.xpath('//android.widget.TextView[contains(@text, "GC001(1天期)")]')
            element = self.d(resourceId="com.hexin.plat.android:id/stock_pinzhong")
            if element.exists:
                logger.info("当前页面为 GC001(1天期)")
                return True
            else:
                logger.error("当前页面不是 GC001(1天期)")
                return False
        except Exception as e:
            logger.error(f"断言失败: {e}")
            return False

    def _perform_borrow_operation(self):
        """执行借出操作"""
        borrow_btn = self.d(resourceId="com.hexin.plat.android:id/btn_jiechu")
        if not self.wait_for_element(borrow_btn, timeout=5):
            return False

        borrow_btn.click()

        # 检查是否需要登录态
        # if self.d(text="立即登录").exists():
        #     logger.warning("需要登录才能操作")
        #     return False
        # 点击确认
        self.d(resourceId="com.hexin.plat.android:id/ok_btn").click()

        return True


    def _handle_transaction_confirm(self, prompt_content, confirm_button, back_button):
        """处理交易确认流程"""
        # 等待弹窗出现
        if not self.wait_for_element(prompt_content, timeout=10):
            return False, "未检测到操作结果"

        prompt_text = prompt_content.get_text()
        logger.info(f"操作提示: {prompt_text}")

        if '委托已提交' in prompt_text:
            confirm_button.click()
            logger.info("交易成功")
            return True, "操作成功"

        # 错误处理
        logger.warning(f"交易失败: {prompt_text}")
        confirm_button.click()

        # 返回持仓页
        back_button.click()
        time.sleep(1)
        back_button.click()

        return False, prompt_text


    def wait_for_element(self, element, timeout=10):
        """显式等待元素出现"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if element.exists():
                return True
            time.sleep(0.5)
        return False

    def guozhai_operation(self):
        logger.info("---------------------国债逆回购任务开始执行---------------------")
        prompt_content = self.d(resourceId="com.hexin.plat.android:id/prompt_content")
        confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        back_button = self.d(resourceId="com.hexin.plat.android:id/title_bar_img")

        try:
            # 1. 确保在首页
            while not self.is_on_holding_list_page():
                if back_button.exists():
                    back_button.click()
                    time.sleep(1)
                else:
                    logger.error("无法返回持仓列表页")
                    return False, "无法返回持仓列表页"

            # 2. 进入国债逆回购入口
            if not self._enter_guozhai_page():
                return False, "进入国债逆回购入口失败"

            # 3. 查找1天期产品
            if not self._find_and_click_product("1天期"):
                return False, "未找到目标产品"

            # 断言当前是否为 GC001(1天期) 页面
            if not self.assert_on_gc001_page():
                back_button.click()
                return False, "当前页面不是 GC001(1天期)"

            # 4. 执行借出操作
            if not self._perform_borrow_operation():
                return False, "借出操作失败"

            # 5. 处理交易确认
            result = self._handle_transaction_confirm(prompt_content, confirm_button, back_button)
            logger.info(f"---------------------国债逆回购任务执行完毕---------------------")
            return result

        except Exception as e:
            logger.error(f"操作失败: {str(e)}", exc_info=True)
            return False, f"操作失败: {str(e)}"
    # def guozhai_operation(d):
    #     logger.info("---------------------国债逆回购任务开始执行---------------------")
    #     prompt_content = d(resourceId="com.hexin.plat.android:id/prompt_content")
    #     confirm_button = d(resourceId="com.hexin.plat.android:id/ok_btn")
    #     back_button = d(resourceId="com.hexin.plat.android:id/title_bar_img")
    #
    #     try:
    #         # 点击右上角第二个图标（通常是国债逆回购入口）
    #         ths = THSPage(d)
    #         ths.click_holding_stock_button()
    #         d(resourceId="com.hexin.plat.android:id/title_right_image")[1].click()
    #         logger.info("点击国债逆回购入口")
    #
    #         # 下滑到出现“沪市”位置，然后点击 stock_list 下的第一个 LinearLayout
    #         d.swipe(0.5, 0.8, 0.5, 0.2)
    #         logger.info("下滑到‘沪市’")
    #
    #         # 点击第一个线性布局（通常为第一个国债逆回购选项）
    #         yitianqi = d(className="android.widget.LinearLayout")[20]
    #         yitianqi.click()
    #         logger.info("点击‘一天期’")
    #
    #         # 点击“借出”按钮
    #         d(resourceId="com.hexin.plat.android:id/btn_jiechu").click()
    #         logger.info("点击‘借出’按钮")
    #
    #         '''
    #         资金够：
    #             确认委托弹窗，点确认
    #             已委托，再点确认
    #         资金不够或时间不对
    #
    #
    #         '''
    #         # 获取 content_layout 里的所有 TextView 内容
    #         content_layout = d(resourceId="com.hexin.plat.android:id/content_layout")
    #         # 检查弹窗内容，判断是否为资金不足的情况
    #         if prompt_content.exists:
    #             prompt_text = prompt_content.get_text()
    #             if not '委托已提交' in prompt_text:
    #                 logger.warning(f"委托失败: {prompt_text}")
    #                 time.sleep(1)
    #                 confirm_button.click()
    #                 back_button.click()
    #                 back_button.click()
    #                 send_notification(f"国债逆回购任务失败: {prompt_text}")
    #                 return False, prompt_text
    #
    #         elif content_layout.exists:
    #             text_views = content_layout.child(className="android.widget.TextView")
    #             content_texts = []
    #             for tv in text_views:
    #                 content_texts.append(tv.get_text())
    #             # print(f"弹窗内容: {content_texts}")
    #             if '您是否确认以上委托？' in content_texts:
    #                 confirm_button.click()
    #                 if prompt_content.exists:
    #                     prompt_text = prompt_content.get_text()
    #                     if not '委托已提交' in prompt_text:
    #                         logger.warning(f"委托失败: {prompt_text}")
    #                         confirm_button.click()
    #                         back_button.click()
    #                         back_button.click()
    #                         send_notification(f"国债逆回购任务失败: {prompt_text}")
    #                         return False, prompt_text
    #                     confirm_button.click()
    #                     logger.info(f"国债逆回购委托成功：{content_texts}")
    #             else:
    #                 logger.warning("委托失败")
    #                 return False, f"委托失败: {content_texts}"
    #         else:
    #             error_info = "弹窗不存在"
    #             logger.warning(error_info)
    #             return False, error_info
    #
    #         # # 点击“确认借出”按钮
    #         # if confirm_button.exists:
    #         #     confirm_button.click()
    #         #     logger.info("点击‘确认借出’按钮")
    #         # else:
    #         #     error_info = "确定按钮不存在"
    #         #     logger.warning(error_info)
    #         #     return False, error_info
    #
    #         # # 获取提示内容并打印（如果需要）
    #         # if prompt_content.exists:
    #         #     print(f"弹窗内容: {prompt_content.get_text()}")
    #
    #         # # 返回上级页面
    #         # if back_button.exists:
    #         #     back_button.click()
    #         #     back_button.click()
    #         #     logger.info("返回上级页面")
    #         # else:
    #         #     logger.warning("返回按钮不存在")
    #
    #         logger.info("---------------------国债逆回购任务执行完毕---------------------")
    #         return True, "操作成功"
    #
    #     except Exception as e:
    #         logger.error(f"错误: {e}")
    #         return False, str(e)

if __name__ == '__main__':
    d = u2.connect()
    guozhai = GuozhaiPage(d)
    success, message = guozhai.guozhai_operation()
    if success:
        print("Operation succeeded.")
    else:
        print(f"Operation failed: {message}")
