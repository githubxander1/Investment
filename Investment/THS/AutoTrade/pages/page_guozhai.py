# page_guozhai.py
import time
# import logging
import uiautomator2 as u2

from Investment.THS.AutoTrade.pages.page_common import ChangeAccount
from Investment.THS.AutoTrade.pages.page_logic import THSPage
# from Investment.THS.AutoTrade.scripts.account_info import click_holding_stock_button
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

# from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger('nihuigou.log')

# ths = THSPage(u2.connect())
change_account = ChangeAccount()

class GuozhaiPage(THSPage):
    def __init__(self, d):
        super().__init__(d)
        # 移除提前初始化的冗余元素，改用动态获取
        self.back_button = self.d(resourceId="com.hexin.plat.android:id/title_bar_img")
        self.confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        self.prompt_content = self.d(resourceId="com.hexin.plat.android:id/prompt_content")
        self.ths = THSPage(d)

        self.guozhai_entry_button = self.d(resourceId="com.hexin.plat.android:id/title_right_image")[1]
        self.guozhailist_assert_button = d(text="我要回购")

        self.borrow_btn = self.d(resourceId="com.hexin.plat.android:id/btn_jiechu")

        #弹窗
        self.diolog_title = self.d(resourceId="com.hexin.plat.android:id/dialog_title")

        self.content_layout = d(resourceId="com.hexin.plat.android:id/content_layout")
    def _find_and_click_product(self, target_name, max_swipe=5):
        """
        支持方向控制的滑动查找
        :param target_name: 目标文本
        :param max_swipe: 最大滑动次数
        :param direction: 'vertical' 或 'horizontal'
        """
        target = self.d(text=target_name)
        # rate = self.d(resourceId="com.hexin.plat.android:id/nianhuayilv")[2]
        more = self.d(resourceId="com.hexin.plat.android:id/more")[2]
        for _ in range(max_swipe):
            # 自适应滑动方向
            while True:
                self.d.swipe(0.5, 0.8, 0.5, 0.2)  # 纵向滑动
                if more.exists():
                    logger.info(f"滑动到 {target_name}")
                    break
                # if direction == 'vertical':
                # else:
                #     self.d.swipe(0.8, 0.5, 0.2, 0.5)  # 横向滑动
                time.sleep(1.5)


            if target:
                time.sleep(1.5)
                target[0].click()
                logger.info(f"点击 {target_name} 成功")
                return True

            time.sleep(1)
        return False

    # def wait_for_element(self, selector, timeout=10):
    #     """
    #     显式等待元素出现
    #     :param selector: 元素定位器
    #     :param timeout: 超时时间
    #     :return: 是否找到
    #     """
    #     start_time = time.time()
    #     while time.time() - start_time < timeout:
    #         if selector.exists():
    #             return True
    #         time.sleep(0.5)
    #     return False

    def assert_on_gc001_page(self):
        """
        使用XPath模糊匹配断言当前页面为 GC001(1天期)
        :param timeout: 最大等待时间
        :return: 成功返回 True，失败返回 False
        """
        try:
            element = self.d.xpath('//android.widget.TextView[contains(@text, "GC001(1天期)")]')
            # element = self.d(resourceId="com.hexin.plat.android:id/stock_pinzhong")
            time.sleep(1)
            if element.exists:
                logger.info("当前页面为 GC001(1天期)")
                return True
            logger.error("当前页面不是 GC001(1天期)")
            return False
        except Exception as e:
            logger.error(f"断言失败: {e}", exc_info=True)
            return False

    # def _perform_borrow_operation(self, timeout=5):
    #     """执行借出操作"""
    #     borrow_btn = self.d(resourceId="com.hexin.plat.android:id/btn_jiechu")
    #     if not self.wait_for_element(borrow_btn, timeout):
    #         logger.error("借出按钮未出现")
    #         return False
    #
    #     self.borrow_btn.click()
    #     # 点击确认
    #     # ok_button = self.d(resourceId=self.confirm_button)
    #     # if not self.wait_for_element(ok_button, timeout=3):
    #     # logger.error("确认按钮未出现")
    #     # return False
    #
    #     self.confirm_button.click()
    #     return True

    def _handle_transaction_confirm(self):
        """处理交易确认流程"""
        # logger.info(f"操作提示: {prompt_text}")

        # 获取 content_layout 里的所有 TextView 内容
        if self.diolog_title.exists():
            dialog_title_text = self.diolog_title.get_text()
            if '借出资金确认' in dialog_title_text:
                text_views = self.content_layout.child(className="android.widget.TextView")
                content_texts = []
                for tv in text_views:
                    content_texts.append(tv.get_text())
                self.confirm_button.click()
                # logger.info(f": {content_texts}")
                prompt_text = self.prompt_content.get_text()
                if '委托已提交' in prompt_text:
                    self.confirm_button.click()
                    logger.info(f"委托成功: {prompt_text}, 内容:{content_texts}")
                    return True
                else:
                    time.sleep(1)
                    self.confirm_button.click()
                    self.back_button.click()
                    self.back_button.click()
                    logger.warning(f"委托失败: {prompt_text}, 返回账户页")
                    send_notification(f"国债逆回购任务失败: {prompt_text}")
                    return False, prompt_text
            else:
                logger.error(f"非委托弹窗")
        else:
            logger.warning("无法找到弹窗标题")
            # # 资金够，确认委托
            # elif self.content_layout.exists:
            #     text_views = self.content_layout.child(className="android.widget.TextView")
            #     content_texts = []
            #     for tv in text_views:
            #         content_texts.append(tv.get_text())
            #     # print(f"弹窗内容: {content_texts}")
            #     if '您是否确认以上委托？' in content_texts:
            #         self.confirm_button.click()
            #         if self.prompt_content.exists:
            #             prompt_text = self.prompt_content.get_text()
            #             if not '委托已提交' in prompt_text:
            #                 logger.warning(f"委托失败: {prompt_text}")
            #                 self.confirm_button.click()
            #                 self.back_button.click()
            #                 self.back_button.click()
            #                 send_notification(f"国债逆回购任务失败: {prompt_text}")
            #                 return False, prompt_text
            #             self.confirm_button.click()
            #             logger.info(f"国债逆回购委托成功：{content_texts}")
            #         else:
            #             logger.info("非委托成功弹窗")
            #     else:
            #         logger.warning("非确认委托弹窗")
            #         return False, f"委托失败: {content_texts}"
        # # 检查弹窗内容，判断是否为资金不足的情况
        # if self.prompt_content.exists:
        #     # prompt_text = self.prompt_content.get_text()
        #     if not '委托已提交' in prompt_text:
        #         logger.warning(f"委托失败: {prompt_text}")
        #         time.sleep(1)
        #         self.confirm_button.click()
        #         self.back_button.click()
        #         self.back_button.click()
        #         send_notification(f"国债逆回购任务失败: {prompt_text}")
        #         return False, prompt_text
        #     else:
        #         logger.info(f"委托成功: {prompt_text}")
        # # 资金够，确认委托
        # elif self.content_layout.exists:
        #     text_views = self.content_layout.child(className="android.widget.TextView")
        #     content_texts = []
        #     for tv in text_views:
        #         content_texts.append(tv.get_text())
        #     # print(f"弹窗内容: {content_texts}")
        #     if '您是否确认以上委托？' in content_texts:
        #         self.confirm_button.click()
        #         if self.prompt_content.exists:
        #             prompt_text = self.prompt_content.get_text()
        #             if not '委托已提交' in prompt_text:
        #                 logger.warning(f"委托失败: {prompt_text}")
        #                 self.confirm_button.click()
        #                 self.back_button.click()
        #                 self.back_button.click()
        #                 send_notification(f"国债逆回购任务失败: {prompt_text}")
        #                 return False, prompt_text
        #             self.confirm_button.click()
        #             logger.info(f"国债逆回购委托成功：{content_texts}")
        #         else:
        #             logger.info("非委托成功弹窗")
        #     else:
        #         logger.warning("非确认委托弹窗")
        #         return False, f"委托失败: {content_texts}"
        # else:
        #     error_info = "弹窗不存在"
        #     logger.warning(error_info)
        #     return False, error_info

        # if '委托已提交' in prompt_text:
        #     self.confirm_button.click()
        #     logger.info("逆回购交易成功")
        #     return True, "操作成功"
        #
        # # 错误处理
        # self.confirm_button.click()
        # logger.warning(f"交易失败: {prompt_text}")
        #
        # # 返回持仓页
        # self.back_button.click()
        # time.sleep(1)
        # self.back_button.click()
        # logger.info("已返回持仓列表页")
        # return False, prompt_text

    def guozhai_operation(self):
        """国债逆回购主流程"""
        logger.info("---------------------国债逆回购任务开始执行---------------------")
        try:
            # 1. 确保在账户页
            time.sleep(1)
            if not change_account.goto_account_page():
                return False, "无法返回持仓列表页"

            # 2. 进入国债逆回购入口
            if not self.guozhai_entry_button.exists():
                return False, "进入国债逆回购入口失败"
            else:
                self.guozhai_entry_button.click()
                logger.info("已进入: 国债逆回购入口")

            # 3. 查找并点击产品
            if not self._find_and_click_product("1天期"):
                return False, "未找到目标产品"


            # 4. 验证页面匹配
            if not self.assert_on_gc001_page():
                self.back_button.click()
                time.sleep(1)
                self.back_button.click()
                return False, "当前页面不是 GC001(1天期)"

            time.sleep(1)
            # 5. 执行借出操作
            if not self.borrow_btn.exists():
                return False, "借出操作失败"
            else:
                # pass
                self.borrow_btn.click()
                logger.info("已点击: 借出按钮")

            # 6. 处理交易确认
            result = self._handle_transaction_confirm()
            logger.info(f"---------------------国债逆回购任务执行完毕---------------------")
            return result
            # else:
            #     return False, "当前页面不是 GC001(1天期)"

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
