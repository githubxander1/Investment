import re
import time
import uiautomator2 as u2

from pages.base.page_base import BasePage
from pages.base.page_common import CommonPage
from utils.logger import setup_logger
from utils.notification import send_notification

logger = setup_logger('national_debt.log')

class NationalDebtPage(BasePage):
    """
    国债逆回购页面类，提供国债逆回购相关操作
    """

    def __init__(self, d=None):
        super().__init__(d)
        self.common_page = CommonPage(d)
        
        # 国债相关元素
        self.back_button = self.d(resourceId="com.hexin.plat.android:id/title_bar_img")
        self.confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        self.prompt_content = self.d(resourceId="com.hexin.plat.android:id/prompt_content")
        self.guozhai_entry_button = self.d(resourceId="com.hexin.plat.android:id/title_right_image")[1]
        self.guozhailist_assert_button = self.d(text="我要回购")
        self.borrow_btn = self.d(resourceId="com.hexin.plat.android:id/btn_jiechu")
        self.diolog_title = self.d(resourceId="com.hexin.plat.android:id/dialog_title")
        self.content_layout = self.d(resourceId="com.hexin.plat.android:id/content_layout")
        self.change_button = self.d(resourceId="com.hexin.plat.android:id/right_arrow_button")

    def _find_and_click_product(self, target_name, max_swipe=5):
        """
        查找并点击产品，支持最大滑动次数和超时控制
        
        Args:
            target_name: 目标文本
            max_swipe: 最大滑动次数
            
        Returns:
            bool: 是否成功点击产品
        """
        target = self.d(text=target_name)
        more = self.d(resourceId="com.hexin.plat.android:id/more")[2]
        for _ in range(max_swipe):
            # 纵向滑动
            self.d.swipe(0.5, 0.8, 0.5, 0.2)
            if more.exists():
                logger.info(f"已滑动到底部")
            time.sleep(1.5)

            if target[0].exists():
                time.sleep(1.5)
                # 检查元素是否可见和可点击
                if target[0].info.get('visible', False) and target[0].info.get('clickable', False):
                    target.click()
                    logger.info(f"点击 {target_name} 成功")
                    # 等待点击效果
                    time.sleep(0.5)
                    return True
                else:
                    logger.warning(f"{target_name} 不可见或不可点击")

            time.sleep(1)
        logger.warning(f"未找到 {target_name}，已滑动到底部")
        return False

    def assert_on_gc001_page(self):
        """
        使用XPath模糊匹配断言当前页面为 GC001(1天期)
        
        Returns:
            bool: 是否在GC001页面
        """
        try:
            element = self.d.xpath('//android.widget.TextView[contains(@text, "GC001(1天期)")]')
            time.sleep(1)
            if element.exists:
                logger.info("当前页面为 GC001(1天期)")
                return True
            logger.error("当前页面不是 GC001(1天期)")
            return False
        except Exception as e:
            logger.error(f"断言失败: {e}", exc_info=True)
            return False

    def _handle_transaction_confirm(self):
        """
        处理交易确认流程
        
        Returns:
            tuple: (是否成功, 消息)
        """
        # 获取 content_layout 里的所有 TextView 内容
        if self.diolog_title.exists():
            dialog_title_text = self.diolog_title.get_text()
            if '借出资金确认' in dialog_title_text:
                text_views = self.content_layout.child(className="android.widget.TextView")
                content_texts = []
                for tv in text_views:
                    content_texts.append(tv.get_text())
                # 检查确认按钮是否可见和可点击
                if self.confirm_button.info.get('visible', False) and self.confirm_button.info.get('clickable', False):
                    self.confirm_button.click()
                    prompt_text = self.prompt_content.get_text()
                    if '委托已提交' in prompt_text:
                        # 检查确认按钮是否可见和可点击
                        if self.confirm_button.info.get('visible', False) and self.confirm_button.info.get('clickable', False):
                            self.confirm_button.click()
                        if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                            self.back_button.click()
                        if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                            self.back_button.click()
                        logger.info(f"委托成功: {prompt_text}, 内容:{content_texts}")
                        return True, '委托成功'
                    else:
                        time.sleep(1)
                        # 检查确认按钮是否可见和可点击
                        if self.confirm_button.info.get('visible', False) and self.confirm_button.info.get('clickable', False):
                            self.confirm_button.click()
                        if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                            self.back_button.click()
                        if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                            self.back_button.click()
                        logger.warning(f"委托失败: {prompt_text}, 返回账户页")
                        return False, prompt_text
                else:
                    logger.warning("确认按钮不可点击或不可见")
                    return False, "确认按钮不可点击"
            else:
                prompt_text = self.prompt_content.get_text()
                # 检查确认按钮是否可见和可点击
                if self.confirm_button.info.get('visible', False) and self.confirm_button.info.get('clickable', False):
                    self.confirm_button.click()
                if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                    self.back_button.click()
                if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                    self.back_button.click()
                logger.error(f"委托失败: {prompt_text}")
                return False, prompt_text
        else:
            logger.warning("无法找到弹窗标题")
            return False, "委托失败"

    def guozhai_operation(self):
        """
        国债逆回购主流程
        
        Returns:
            tuple: (是否成功, 消息)
        """
        logger.info("---------------------国债逆回购任务开始执行---------------------")
        try:
            # 1. 确保在账户页
            time.sleep(1)
            if not self.common_page.goto_account_page():
                error_msg = "无法返回账户页"
                logger.error(error_msg)
                send_notification(f"国债逆回购任务失败: {error_msg}")
                # 检查返回按钮是否可见和可点击
                if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                    self.back_button()
                return False, error_msg

            # 2. 进入国债逆回购入口
            if not self.guozhai_entry_button.exists():
                error_msg = "进入国债逆回购入口失败"
                logger.error(error_msg)
                send_notification(f"国债逆回购任务失败: {error_msg}")
                return False, error_msg
            else:
                # 检查元素是否可见和可点击
                if self.guozhai_entry_button.info.get('visible', False) and self.guozhai_entry_button.info.get('clickable', False):
                    self.guozhai_entry_button.click()
                    logger.info("已进入: 国债逆回购入口")
                    # 等待点击效果
                    time.sleep(0.5)
                else:
                    logger.warning("国债逆回购入口按钮不可点击或不可见")
                    return False, "国债逆回购入口按钮不可点击"

            # 3. 查找并点击产品
            if not self._find_and_click_product("1天期"):
                error_msg = "未找到目标产品"
                logger.error(error_msg)
                send_notification(f"国债逆回购任务失败: {error_msg}")
                return False, error_msg

            # 4. 验证页面匹配
            if not self.assert_on_gc001_page():
                error_msg = "当前页面不是 GC001(1天期)"
                logger.error(error_msg)
                # 检查返回按钮是否可见和可点击
                if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                    self.back_button.click()
                    time.sleep(1)
                    if self.back_button.info.get('visible', False) and self.back_button.info.get('clickable', False):
                        self.back_button.click()
                send_notification(f"国债逆回购任务失败: {error_msg}")
                return False, error_msg

            time.sleep(1)

            # 5. 执行借出操作
            if not self.borrow_btn.exists():
                error_msg = "借出操作失败"
                logger.error(error_msg)
                send_notification(f"国债逆回购任务失败: {error_msg}")
                return False, error_msg
            else:
                # 检查元素是否可见和可点击
                if self.borrow_btn.info.get('visible', False) and self.borrow_btn.info.get('clickable', False):
                    self.borrow_btn.click()
                    logger.info("已点击: 借出按钮")
                    # 等待点击效果
                    time.sleep(0.5)
                else:
                    logger.warning("借出按钮不可点击或不可见")
                    return False, "借出按钮不可点击"

            # 6. 处理交易确认
            result = self._handle_transaction_confirm()
            success, message = result

            # 发送通知
            send_notification(f"国债逆回购任务完成: {success} {message}")
            logger.info(f"---------------------国债逆回购任务执行完毕---------------------")
            return result

        except Exception as e:
            error_msg = f"操作失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            send_notification(f"国债逆回购任务异常终止: {error_msg}")
            return False, error_msg

    def guozhai_change_account(self, account_name):
        """
        切换账户
        
        Args:
            account_name: 账户名称
            
        Returns:
            bool: 是否成功切换账户
        """
        self.change_button = self.d(resourceId="com.hexin.plat.android:id/right_arrow_button")
        account = self.d(className="android.widget.TextView", text=account_name)

        # 提取 //android.widget.TextView[@text="长城证券 **5735"] 里取汉字
        current_account_element = self.d(resourceId="com.hexin.plat.android:id/account_info_view")
        if current_account_element.exists():
            current_account_text = current_account_element.get_text()
            if current_account_text:
                # 修复：检查正则表达式是否匹配到内容
                match = re.search(r"[\u4e00-\u9fa5]+", current_account_text)
                if match:
                    current_account = match.group()
                    print(f"当前账户: {current_account}")
                else:
                    logger.warning(f"无法从账户信息中提取中文名称: {current_account_text}")
                    current_account = ""
            else:
                logger.warning("获取到的账户信息为空")
                current_account = ""
        else:
            logger.warning("未找到账户信息元素")
            current_account = ""

        if current_account == account_name:
            logger.info(f"当前账户: {current_account}, 不用切换账户")
            return True

        # 检查切换按钮是否可见和可点击
        if self.change_button.info.get('visible', False) and self.change_button.info.get('clickable', False):
            self.change_button.click()
            logger.info("已点击: 账户切换按钮")
            # 等待点击效果
            time.sleep(0.5)
            if account.exists():
                # 检查账户按钮是否可见和可点击
                if account.info.get('visible', False) and account.info.get('clickable', False):
                    account.click()
                    logger.info(f"已切换账户: {account_name}")
                    # 等待点击效果
                    time.sleep(0.5)
                    return True
                else:
                    logger.warning(f"账户 {account_name} 按钮不可点击或不可见")
                    return False
            else:
                logger.warning(f"无法找到账户: {account_name}")
                return False
        else:
            logger.warning("账户切换按钮不可点击或不可见")
            return False