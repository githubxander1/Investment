import time
import uiautomator2
from Investment.THS.AutoTrade.pages.base.page_base import BasePage
from Investment.THS.AutoTrade.pages.base.page_common import CommonPage
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger('page_trading.log')

class TradingPage(BasePage):
    """
    交易页面类，提供交易相关操作
    """

    def __init__(self, d=None):
        super().__init__(d)
        self.common_page = CommonPage(d)

        # 交易相关元素
        self.trade_button_entry = self.d(resourceId="com.hexin.plat.android:id/menu_holdings_image")
        self.back_button = self.d(resourceId='com.hexin.plat.android:id/title_bar_left_container')
        self.moni = self.d(resourceId="com.hexin.plat.android:id/tab_mn")
        self.Agu = self.d(resourceId="com.hexin.plat.android:id/tab_a")
        self.current_account = self.d(resourceId="com.hexin.plat.android:id/page_title_view")
        self.keyong = self.d(resourceId="com.hexin.plat.android:id/capital_cell_title")[4]
        self.current_text = self.d(resourceId="com.hexin.plat.android:id/currency_text", text="人民币账户 A股")
        self.share_button = self.d(resourceId="com.hexin.plat.android:id/share_container")
        self.search_button = self.d(resourceId="com.hexin.plat.android:id/search_container")
        self.confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        self.prompt_content = self.d(resourceId="com.hexin.plat.android:id/prompt_content")
        self.diolog_title = self.d(resourceId="com.hexin.plat.android:id/dialog_title")
        self.content_layout = self.d(resourceId="com.hexin.plat.android:id/content_layout")

    def click_back(self):
        """
        点击返回按钮

        Returns:
            bool: 点击是否成功
        """
        back_button = self.d(resourceId='com.hexin.plat.android:id/title_bar_left_container')
        if back_button.exists:
            back_button.click()
            logger.info("点击返回按钮")
            return True
        else:
            error_msg = "返回按钮未找到"
            logger.warning(error_msg)
            send_notification(error_msg)
            return False

    def click_trade_entry(self):
        """
        点击交易入口按钮

        Returns:
            bool: 点击是否成功
        """
        trade_entry = self.d(resourceId='com.hexin.plat.android:id/title', text='交易')
        if trade_entry.exists:
            trade_entry.click()
            # 断言selected为 true
            if not trade_entry.info.get('selected', False):
                trade_entry.click()
                logger.info("点击交易按钮(外)")
            return True
        else:
            error_msg = "交易按钮(外)未找到"
            logger.warning(error_msg)
            send_notification(error_msg)
            return False

    def click_holding_stock_entry(self):
        """
        点击持仓入口按钮

        Returns:
            bool: 点击是否成功
        """
        operate_entry = self.d(resourceId='com.hexin.plat.android:id/menu_holdings_text', text='持仓')
        if operate_entry.exists:
            operate_entry.click()
            # 确保状态已切换为选中，如果不是选中状态，则点击
            if not operate_entry.info.get('selected', False):
                operate_entry.click()
                logger.info("点击持仓按钮(外)")
            return True
        else:
            error_msg = "持仓按钮(外)未找到"
            logger.warning(error_msg)
            send_notification(error_msg)
            return False

    def click_operate_entry(self, operation):
        """
        点击外面入口处的操作按钮

        Args:
            operation: 操作类型("买入"或"卖出")

        Returns:
            bool: 点击是否成功
        """
        if operation == '买入':
            buy_entry = self.d(resourceId='com.hexin.plat.android:id/menu_buy_text')
            if buy_entry.exists:
                buy_entry.click()
                # 确保状态已切换为选中，如果不是选中状态，则点击
                if not buy_entry.info.get('selected', False):
                    buy_entry.click()
                logger.info("点击买入按钮(外)")
                return True
            else:
                error_msg = "买入按钮(外)未找到"
                logger.warning(error_msg)
                send_notification(error_msg)
                return False
        elif operation == '卖出':
            sale_entry = self.d(resourceId='com.hexin.plat.android:id/menu_sale_text')
            if sale_entry.exists:
                sale_entry.click()
                # 确保状态已切换为选中，如果不是选中状态，则点击
                if not sale_entry.info.get('selected', False):
                    sale_entry.click()
                    logger.info("点击卖出按钮(外)")
                return True
            else:
                error_msg = "卖出按钮(外)未找到"
                logger.warning(error_msg)
                send_notification(error_msg)
                return False
        else:
            error_msg = "未知操作"
            logger.error(error_msg)
            send_notification(error_msg)
            raise ValueError(error_msg)

    def click_holding_stock_button(self):
        """
        点击持仓按钮(里面)
        """
        holding_button = self.d(className='android.widget.TextView', text='持仓')
        #'(//*[@resource-id="com.hexin.plat.android:id/btn"])[4]'
        # 检查按钮是否已经选中，如果没有选中则点击
        if holding_button.exists:
            # 获取按钮的selected属性
            selected = holding_button.info.get('selected', False)
            if not selected:
                holding_button.click()
                logger.info("点击持仓按钮(里)")
            else:
                logger.info("持仓按钮(里)已处于选中状态")
        else:
            # 如果无法确定状态，直接点击
            holding_button.click()
            logger.info("点击持仓按钮(里)")

    def click_operate_button(self, operation):
        """
        点击里面的tab栏操作按钮

        Args:
            operation: 操作类型("买入"或"卖出")

        Returns:
            bool: 点击是否成功
        """
        if operation == '买入':
            buy_button = self.d(className='android.widget.TextView', text='买入')
            # 检查按钮是否存在并安全点击
            if buy_button.exists:
                selected = buy_button.info.get('selected', False)
                if not selected:
                    buy_button.click()
                    logger.info("点击买入按钮(里)")
                else:
                    logger.info("买入按钮(里)已处于选中状态")
                return True
            else:
                error_msg = "买入按钮未找到"
                logger.warning(error_msg)
                send_notification(error_msg)
                return False
        elif operation == '卖出':
            sale_button = self.d(className='android.widget.TextView', text='卖出')
            # 检查按钮是否存在并安全点击
            if sale_button.exists:
                selected = sale_button.info.get('selected', False)
                if not selected:
                    sale_button.click()
                    logger.info("点击卖出按钮(里)")
                else:
                    logger.info("卖出按钮(里)已处于选中状态")
                return True
            else:
                error_msg = "卖出按钮未找到"
                logger.warning(error_msg)
                send_notification(error_msg)
                return False
        else:
            error_msg = "未知操作"
            logger.error(error_msg)
            send_notification(error_msg)
            raise ValueError(error_msg)

    def click_refresh_button(self):
        """
        点击刷新按钮

        Returns:
            bool: 点击是否成功
        """
        refresh_button = self.d(resourceId='com.hexin.plat.android:id/refresh_container')
        if refresh_button.exists:
            refresh_button.click()
            logger.info("点击刷新按钮")
            return True
        else:
            error_msg = "刷新按钮未找到"
            logger.warning(error_msg)
            send_notification(error_msg)
            return False

    def search_stock(self, stock_name):
        """
        搜索股票

        Args:
            stock_name: 股票名称
        """
        stock_search = self.d(resourceId='com.hexin.plat.android:id/content_stock')
        stock_search.click()
        logger.info(f"点击股票搜索框")

        auto_search = self.d(text="股票代码/简拼")
        clear = self.d(resourceId='com.hexin.plat.android:id/clearable_edittext_btn_clear')
        if clear.exists():
            clear.click()
            logger.info("清除股票代码")
        time.sleep(1)

        auto_search.send_keys(stock_name)
        logger.info(f"输入股票名称: {stock_name}")
        time.sleep(1)

        # 如果clear按钮在，则点击匹配，如果找不到，则pass，继续下一步
        clear = self.d(resourceId='com.hexin.plat.android:id/clearable_edittext_btn_clear')
        if clear.exists():
            # 显式等待搜索结果加载
            recycler_view = self.d(resourceId='com.hexin.plat.android:id/recyclerView')
            if recycler_view.wait(timeout=5):  # 等待最多5秒
                first_item = recycler_view.child(index=0)
                time.sleep(1)
                first_item.click()
                logger.info("点击匹配的第一个股票")
                time.sleep(1)
                cancel_button = self.d(resourceId='com.hexin.plat.android:id/close_btn')
                if cancel_button.exists:
                    first_item.click()
                    logger.info("再次点击匹配的第一个股票")
            else:
                error_msg = "未找到搜索结果列表，尝试使用股票代码搜索"
                logger.warning(error_msg)
                send_notification(error_msg)
                # 如果没找到，尝试输入股票代码
                stock_code = self._get_stock_code(stock_name)  # 自定义方法：通过名称获取股票代码
                if stock_code:
                    clear.click()
                    auto_search.send_keys(stock_code)
                    time.sleep(1)
                    if recycler_view.wait(timeout=5):
                        first_item = recycler_view.child(index=0)
                        first_item.click()
                        logger.info("点击匹配的第一个股票（使用代码搜索）")
                    else:
                        error_msg = "使用代码搜索仍无法找到匹配项"
                        logger.warning(error_msg)
                        send_notification(error_msg)
                else:
                    error_msg = "无法获取股票代码，跳过点击"
                    logger.warning(error_msg)
                    send_notification(error_msg)

        time.sleep(2)

    def input_volume(self, volume):
        """
        输入交易数量

        Args:
            volume: 交易数量

        Returns:
            tuple: (是否成功, 实际输入的数量)
        """
        volumn_input = self.d(resourceId="com.hexin.plat.android:id/stockvolume").child(index=0)
        volumn_input.send_keys(volume)
        # volume_text = self.d(className='android.widget.EditText')[3].get_text()# 会报错
        volume_text = int(self.d(resourceId="com.hexin.plat.android:id/stockvolume").child(index=0).get_text())
        if volume_text == volume:
            logger.info(f"输入数量:{volume}手")
            return True, volume_text
        else:
            error_msg = f"输入数量错误 {volume_text}"
            logger.warning(error_msg)
            send_notification(error_msg)
            return False, volume_text

    def click_half_volume(self):
        """
        点击半仓按钮
        """
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='1/2仓')
        volumn.click()
        logger.info("输入数量: 半仓")

    def click_total_volume(self):
        """
        点击全仓按钮
        """
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='全仓')
        volume = self.d(className='android.widget.EditText')[2]
        # logger.info("获取买入数量")
        if volume.get_text() != '0':
            volumn.click()
            logger.info("输入数量: 全仓")
        else:
            pass

    def get_price_by_volume(self):
        """
        获取根据输入数量自动计算的金额

        Returns:
            str: 金额
        """
        price = self.d(resourceId='com.hexin.plat.android:id/couldbuy_volumn').get_text()
        logger.info("获取金额: " + price)
        return price

    def click_submit_button(self, operation):
        """
        点击提交按钮

        Args:
            operation: 操作类型("买入"或"卖出")

        Returns:
            bool: 点击是否成功
        """
        if operation == '买入':
            submit_button = self.d(className='android.widget.TextView', textMatches='.*买 入.*')
        elif operation == '卖出':
            submit_button = self.d(className='android.widget.TextView', textMatches='.*卖 出.*')
        else:
            error_msg = "Invalid operation"
            logger.error(error_msg)
            send_notification(error_msg)
            raise ValueError(error_msg)

        # 检查按钮是否存在再点击
        if submit_button.exists:
            submit_button.click()
            logger.info(f"点击按钮: {operation} (提交)")
            return True
        else:
            error_msg = f"提交按钮 {operation} 未找到"
            logger.error(error_msg)
            send_notification(error_msg)
            return False

    def _get_real_price(self):
        """
        获取当前股票实时价格

        Returns:
            float: 实时价格
        """
        # price = self.d(className='android.widget.EditText')[1].get_text()
        price_layout = self.d(resourceId="com.hexin.plat.android:id/stockprice")
        #获取layout下方的edittext里的文本
        price_edit = price_layout.child(className='android.widget.EditText')
        for _ in range(3):
            try:
                price_text = price_edit.get_text()
                if price_text and price_text != 'None':
                    return float(price_text)
                else:
                    logger.warning("价格为空，等待刷新...")
                    time.sleep(1)
            except (ValueError, TypeError) as e:
                error_msg = f"解析价格失败: {e}"
                logger.warning(error_msg)
                send_notification(error_msg)
                time.sleep(1)
        error_msg = "无法获取实时价格"
        logger.error(error_msg)
        send_notification(error_msg)
        raise ValueError(error_msg)

    def dialog_handle(self):
        """
        点击 提交 后
        处理交易后的各种弹窗情况
        1. 委托确认弹窗
        2. 资金不足弹窗
        3. 其他异常弹窗

        Returns:
            tuple: (是否成功, 弹窗信息)
        """
        logger.info('-'*50)
        logger.info("开始处理弹窗")

        try:
            # 定位弹窗相关控件

            # dialog_title = self.d(resourceId='com.hexin.plat.android:id/dialog_title')

            # 尝试通过content_layout获取弹窗内容
            # prompt_text = self.get_dialog_content_by_layout()
            # if not prompt_text:
                # 如果通过content_layout获取失败，使用原有方式获取
            time.sleep(1)
            prompt_content = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
            prompt_text = prompt_content.get_text() if prompt_content.exists else "未找到弹窗内容"
            if prompt_content.exists:
                print("弹窗内容: " + prompt_text)
            else:
                print("prompt_content定位失败，未找到弹窗内容")
            # prompt_content_second = self.d(className='android.widget.TextView')[2] if len(
            #     self.d(className='android.widget.TextView')) > 2 else None
            # if prompt_content_second.exists:
            #     print("弹窗内容: " + prompt_content_second.get_text())
            # else:
            #     print("prompt_content_second定位失败，未找到弹窗内容")
            # prompt_content_third = self.d(className='android.widget.TextView')[3] if len(
            #     self.d(className='android.widget.TextView')) > 3 else None
            # if prompt_content_third.exists:
            #     print("弹窗内容: " + prompt_content_third.get_text())
            # else:
            #     print("prompt_content_third定位失败，未找到弹窗内容")

            # prompt_text = prompt_content.get_text() if prompt_content.exists else prompt_content_second.get_text() if prompt_content_second.exists else prompt_content_third.get_text() if prompt_content_third.exists else "未找到弹窗内容"
            #
            confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
            confirm_button_second = self.d(resourceId="com.hexin.plat.android:id/left_btn") #资金不足时的确定按钮
            confirm_buttons = confirm_button if confirm_button.exists else confirm_button_second if confirm_button_second.exists else "未找到确定按钮"
            # 获取弹窗标题和内容
            # title_text = dialog_title.get_text() if dialog_title.exists else "未获取到弹窗标题内容"

            time.sleep(1)
            # 检查是否委托已提交
            if '委托已提交' in prompt_text:
                confirm_buttons.click()
                logger.info("委托已提交,点击确定按钮")
                # 处理st股的确认弹窗
                if confirm_buttons.exists:
                    confirm_buttons.click()
                    logger.info("处理st股的确认弹窗，再次点击确认按钮")
                return True, prompt_text
            else:
                # 处理委托失败的情况
                # time.sleep(1)
                # logger.info("尝试查找报错弹窗...")

                # 尝试多种方式定位确认按钮
                ok_btn = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
                left_btn = self.d(resourceId="com.hexin.plat.android:id/left_btn")
                positive_btn = self.d(resourceId="com.hexin.plat.android:id/positiveButton")
                button_ok = self.d(text="确定")

                # 按优先级点击按钮
                confirm_btn = None
                if ok_btn.exists:
                    confirm_btn = ok_btn
                    logger.debug("找到ok_btn")
                elif left_btn.exists:
                    confirm_btn = left_btn
                    logger.debug("找到left_btn")
                elif positive_btn.exists:
                    confirm_btn = positive_btn
                    logger.debug("找到positiveButton")
                elif button_ok.exists:
                    confirm_btn = button_ok
                    logger.debug("找到文本为'确定'的按钮")

                if confirm_btn:
                    confirm_btn.click()
                    logger.info("点击确认按钮")
                else:
                    # error_msg = prompt_text
                    logger.warning(prompt_text)
                    send_notification(prompt_text)
                    # 尝试点击屏幕中央位置
                    self.d.click(0.5, 0.5)
                    logger.info("尝试点击屏幕中央位置")
                return False, prompt_text

            # # 处理成功提交的情况
            # if any(keyword in title_text for keyword in ['委托买入确认', '委托卖出确认']):
            #     logger.info("检测到'委托确认'提示")
            #     confirm_buttons.click()
            #     logger.info("点击确定按钮(委托确认)")
            #     time.sleep(1)
            #
            #     # 尝试多种方式定位弹窗元素
            #     # prompt_text = self.get_dialog_content_by_layout()
            #     # if not prompt_text:
            #     #     # 方式1: 标准ID定位
            #     dialog_title_new = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
            #     prompt_content = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
            #     prompt_content_second = self.d(className='android.widget.TextView', index=1)
            #     prompt_content_second = self.d(className='android.widget.TextView', index=2)
            #     prompt_content_third = self.d(className='android.widget.TextView', index=3)
            #
            #     # 方式2: 通过文本特征定位
            #     fund_error_elements = self.d(textContains='可用资金不足')
            #     lack_error_elements = self.d(textContains='不足')
            #
            #     # 获取新弹窗的标题和内容
            #     new_title_text = ""
            #     new_prompt_text = ""
            #
            #     if dialog_title_new.exists:
            #         new_title_text = dialog_title_new.get_text()
            #         logger.debug(f"新弹窗标题: {new_title_text}")
            #     if prompt_content.exists:
            #         new_prompt_text = prompt_content.get_text()
            #         logger.debug(f"弹窗内容(ID方式): {new_prompt_text}")
            #     elif prompt_content_second.exists:
            #         new_prompt_text = prompt_content_second.get_text()
            #         logger.debug(f"弹窗内容(ID方式): {new_prompt_text}")
            #     elif prompt_content_third.exists:
            #         new_prompt_text = prompt_content_third.get_text()
            #         logger.debug(f"新弹窗内容(ID方式): {new_prompt_text}")
            #     elif fund_error_elements.exists or lack_error_elements.exists:
            #         # 如果通过ID找不到，尝试通过文本特征
            #         if fund_error_elements.exists:
            #             new_prompt_text = fund_error_elements.get_text()
            #             logger.debug(f"新弹窗内容(文本特征'资金'): {new_prompt_text}")
            #         elif lack_error_elements.exists:
            #             new_prompt_text = lack_error_elements.get_text()
            #             logger.debug(f"新弹窗内容(文本特征'不足'): {new_prompt_text}")
            #     #
            #     # # 尝试多种方式定位确认按钮
            #     # ok_btn = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
            #     # left_btn = self.d(resourceId="com.hexin.plat.android:id/left_btn")
            #     # positive_btn = self.d(resourceId="com.hexin.plat.android:id/positiveButton")
            #     # button_ok = self.d(text="确定")
            #     #
            #     # # 按优先级点击按钮
            #     # confirm_btn = None
            #     # if ok_btn.exists:
            #     #     confirm_btn = ok_btn
            #     #     logger.debug("找到ok_btn")
            #     # elif left_btn.exists:
            #     #     confirm_btn = left_btn
            #     #     logger.debug("找到left_btn")
            #     # elif positive_btn.exists:
            #     #     confirm_btn = positive_btn
            #     #     logger.debug("找到positiveButton")
            #     # elif button_ok.exists:
            #     #     confirm_btn = button_ok
            #     #     logger.debug("找到文本为'确定'的按钮")
            #     #
            #     # if confirm_btn:
            #     #     confirm_btn.click()
            #     #     logger.info("点击确认按钮")
            #     # else:
            #     #     error_msg = "未找到确认按钮"
            #     #     logger.warning(error_msg)
            #     #     send_notification(error_msg)
            #     #     # 尝试点击屏幕中央位置
            #     #     self.d.click(0.5, 0.5)
            #     #     logger.info("尝试点击屏幕中央位置")
            #
            #     time.sleep(1)
            #     # 检查是否委托已提交
            #     if '委托已提交' in new_prompt_text:
            #         confirm_buttons.click()
            #         logger.info("委托已提交")
            #         # 处理st股的确认弹窗
            #         if confirm_buttons.exists:
            #             confirm_buttons.click()
            #             logger.info("再次点击确认按钮")
            #         return True, new_prompt_text
            #     else:
            #         # 处理委托失败的情况
            #         time.sleep(1)
            #         logger.info("尝试查找报错弹窗...")
            #
            #         # 尝试多种方式定位确认按钮
            #         ok_btn = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
            #         left_btn = self.d(resourceId="com.hexin.plat.android:id/left_btn")
            #         positive_btn = self.d(resourceId="com.hexin.plat.android:id/positiveButton")
            #         button_ok = self.d(text="确定")
            #
            #         # 按优先级点击按钮
            #         confirm_btn = None
            #         if ok_btn.exists:
            #             confirm_btn = ok_btn
            #             logger.debug("找到ok_btn")
            #         elif left_btn.exists:
            #             confirm_btn = left_btn
            #             logger.debug("找到left_btn")
            #         elif positive_btn.exists:
            #             confirm_btn = positive_btn
            #             logger.debug("找到positiveButton")
            #         elif button_ok.exists:
            #             confirm_btn = button_ok
            #             logger.debug("找到文本为'确定'的按钮")
            #
            #         if confirm_btn:
            #             confirm_btn.click()
            #             logger.info("点击确认按钮")
            #         else:
            #             error_msg = "未找到确认按钮"
            #             logger.warning(error_msg)
            #             send_notification(error_msg)
            #             # 尝试点击屏幕中央位置
            #             self.d.click(0.5, 0.5)
            #             logger.info("尝试点击屏幕中央位置")
            #
            #         # 尝试多种方式定位弹窗元素
            #         # 方式1: 标准ID定位
            #         dialog_title_new = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
            #         prompt_content = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
            #         prompt_content_second = self.d(className='android.widget.TextView', index=2)
            #         prompt_content_third = self.d(className='android.widget.TextView', index=3)
            #
            #         # 方式2: 通过文本特征定位
            #         fund_error_elements = self.d(textContains='可用资金不足')
            #         lack_error_elements = self.d(textContains='不足')
            #
            #         new_title_text = ""
            #         new_prompt_text = ""
            #
            #         # 尝试获取内容
            #         if prompt_content.exists:
            #             new_prompt_text = prompt_content.get_text()
            #             logger.debug(f"弹窗内容(ID方式): {new_prompt_text}")
            #         elif prompt_content_second.exists:
            #             new_prompt_text = prompt_content_second.get_text()
            #             logger.debug(f"弹窗内容(ID方式): {new_prompt_text}")
            #         elif prompt_content_third.exists:
            #             new_prompt_text = prompt_content_third.get_text()
            #             logger.debug(f"新弹窗内容(ID方式): {new_prompt_text}")
            #         elif fund_error_elements.exists or lack_error_elements.exists:
            #             # 如果通过ID找不到，尝试通过文本特征
            #             if fund_error_elements.exists:
            #                 new_prompt_text = fund_error_elements.get_text()
            #                 logger.debug(f"新弹窗内容(文本特征'资金'): {new_prompt_text}")
            #             elif lack_error_elements.exists:
            #                 new_prompt_text = lack_error_elements.get_text()
            #                 logger.debug(f"新弹窗内容(文本特征'不足'): {new_prompt_text}")
            #         else:
            #             # 如果所有方式都获取不到内容，使用默认提示
            #             new_prompt_text = "无法获取弹窗具体内容"
            #
            #         logger.warning(f"委托失败，{new_prompt_text}")
            #         return False, new_prompt_text
            # else:
            #     # 处理其他情况
            #     confirm_button_to_click = confirm_button if confirm_button.exists else confirm_button_second if confirm_button_second.exists else None
            #     if confirm_button_to_click:
            #         time.sleep(1)
            #         confirm_button_to_click.click()
            #         logger.info("点击确定按钮")#资金不足
            #         time.sleep(1)
            #
            #
            #     error_msg = f"未检测到'委托确认'提示，弹窗内容: {prompt_text}"
            #     logger.warning(error_msg)
            #     send_notification(error_msg)
            #     return False, prompt_text

        except Exception as e:
            error_msg = f"处理弹窗时发生异常: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return False, error_msg
    def dialog_handle1(self):
        """
        处理交易后的各种弹窗情况

        Returns:
            tuple: (是否成功, 弹窗信息)
        """
        logger.info('-'*50)
        logger.info("开始处理弹窗")
        # 定位弹窗相关控件
        dialog_title = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
        dialog_title_text = dialog_title.get_text() if dialog_title.exists else "未获取到弹窗标题"

        # 尝试通过content_layout获取弹窗内容
        prompt_text = self.get_dialog_content_by_layout()
        if not prompt_text:
            # 如果通过content_layout获取失败，使用原有方式获取
            prompt_content = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
            prompt_content_second = self.d(className='android.widget.TextView')[2] if len(
                self.d(className='android.widget.TextView')) > 2 else None
            prompt_content_third = self.d(className='android.widget.TextView')[3] if len(
                self.d(className='android.widget.TextView')) > 3 else None

            prompt_text = prompt_content.get_text() if prompt_content.exists else prompt_content_second.get_text() if prompt_content_second.exists else prompt_content_third.get_text() if prompt_content_third.exists else "未找到弹窗内容"

        confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        confirm_button_second = self.d(resourceId="com.hexin.plat.android:id/left_btn") #资金不足时的确定按钮
        confirm_buttons = confirm_button if confirm_button.exists else confirm_button_second if confirm_button_second.exists else "未找到确定按钮"

        try:
            # 获取弹窗标题和内容
            title_text = dialog_title.get_text() if dialog_title.exists else ""

            # 处理成功提交的情况
            if any(keyword in title_text for keyword in ['委托买入确认', '委托卖出确认']):
                logger.info("检测到'委托确认'提示")
                time.sleep(1)

                # 尝试多种方式定位弹窗元素
                prompt_text = self.get_dialog_content_by_layout()
                if not prompt_text:
                    # 方式1: 标准ID定位
                    dialog_title_new = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
                    prompt_content = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
                    prompt_content_second = self.d(className='android.widget.TextView', index=1)
                    prompt_content_second = self.d(className='android.widget.TextView', index=2)
                    prompt_content_third = self.d(className='android.widget.TextView', index=3)

                    # 方式2: 通过文本特征定位
                    fund_error_elements = self.d(textContains='可用资金不足')
                    lack_error_elements = self.d(textContains='不足')

                    # 获取新弹窗的标题和内容
                    new_title_text = ""
                    new_prompt_text = ""

                    if dialog_title_new.exists:
                        new_title_text = dialog_title_new.get_text()
                        logger.debug(f"新弹窗标题: {new_title_text}")
                    if prompt_content.exists:
                        new_prompt_text = prompt_content.get_text()
                        logger.debug(f"弹窗内容(ID方式): {new_prompt_text}")
                    elif prompt_content_second.exists:
                        new_prompt_text = prompt_content_second.get_text()
                        logger.debug(f"弹窗内容(ID方式): {new_prompt_text}")
                    elif prompt_content_third.exists:
                        new_prompt_text = prompt_content_third.get_text()
                        logger.debug(f"新弹窗内容(ID方式): {new_prompt_text}")
                    elif fund_error_elements.exists or lack_error_elements.exists:
                        # 如果通过ID找不到，尝试通过文本特征
                        if fund_error_elements.exists:
                            new_prompt_text = fund_error_elements.get_text()
                            logger.debug(f"新弹窗内容(文本特征'资金'): {new_prompt_text}")
                        elif lack_error_elements.exists:
                            new_prompt_text = lack_error_elements.get_text()
                            logger.debug(f"新弹窗内容(文本特征'不足'): {new_prompt_text}")

                # 尝试多种方式定位确认按钮
                ok_btn = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
                left_btn = self.d(resourceId="com.hexin.plat.android:id/left_btn")
                positive_btn = self.d(resourceId="com.hexin.plat.android:id/positiveButton")
                button_ok = self.d(text="确定")

                # 按优先级点击按钮
                confirm_btn = None
                if ok_btn.exists:
                    confirm_btn = ok_btn
                    logger.debug("找到ok_btn")
                elif left_btn.exists:
                    confirm_btn = left_btn
                    logger.debug("找到left_btn")
                elif positive_btn.exists:
                    confirm_btn = positive_btn
                    logger.debug("找到positiveButton")
                elif button_ok.exists:
                    confirm_btn = button_ok
                    logger.debug("找到文本为'确定'的按钮")

                if confirm_btn:
                    confirm_btn.click()
                    logger.info("点击确认按钮")
                else:
                    error_msg = "未找到确认按钮"
                    logger.warning(error_msg)
                    send_notification(error_msg)
                    # 尝试点击屏幕中央位置
                    self.d.click(0.5, 0.5)
                    logger.info("尝试点击屏幕中央位置")

                time.sleep(1)
                # 检查是否委托已提交
                if '委托已提交' in new_prompt_text:
                    confirm_buttons.click()
                    logger.info("委托已提交")
                    # 处理st股的确认弹窗
                    if confirm_buttons.exists:
                        confirm_buttons.click()
                        logger.info("再次点击确认按钮")
                    return True, new_prompt_text
                else:
                    # 处理委托失败的情况
                    time.sleep(1)
                    logger.info("尝试查找报错弹窗...")

                    # 尝试多种方式定位确认按钮
                    ok_btn = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
                    left_btn = self.d(resourceId="com.hexin.plat.android:id/left_btn")
                    positive_btn = self.d(resourceId="com.hexin.plat.android:id/positiveButton")
                    button_ok = self.d(text="确定")

                    # 按优先级点击按钮
                    confirm_btn = None
                    if ok_btn.exists:
                        confirm_btn = ok_btn
                        logger.debug("找到ok_btn")
                    elif left_btn.exists:
                        confirm_btn = left_btn
                        logger.debug("找到left_btn")
                    elif positive_btn.exists:
                        confirm_btn = positive_btn
                        logger.debug("找到positiveButton")
                    elif button_ok.exists:
                        confirm_btn = button_ok
                        logger.debug("找到文本为'确定'的按钮")

                    if confirm_btn:
                        confirm_btn.click()
                        logger.info("点击确认按钮")
                    else:
                        error_msg = "未找到确认按钮"
                        logger.warning(error_msg)
                        send_notification(error_msg)
                        # 尝试点击屏幕中央位置
                        self.d.click(0.5, 0.5)
                        logger.info("尝试点击屏幕中央位置")

                    # 尝试多种方式定位弹窗元素
                    # 方式1: 标准ID定位
                    dialog_title_new = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
                    prompt_content = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
                    prompt_content_second = self.d(className='android.widget.TextView', index=2)
                    prompt_content_third = self.d(className='android.widget.TextView', index=3)

                    # 方式2: 通过文本特征定位
                    fund_error_elements = self.d(textContains='可用资金不足')
                    lack_error_elements = self.d(textContains='不足')

                    new_title_text = ""
                    new_prompt_text = ""

                    # 尝试获取内容
                    if prompt_content.exists:
                        new_prompt_text = prompt_content.get_text()
                        logger.debug(f"弹窗内容(ID方式): {new_prompt_text}")
                    elif prompt_content_second.exists:
                        new_prompt_text = prompt_content_second.get_text()
                        logger.debug(f"弹窗内容(ID方式): {new_prompt_text}")
                    elif prompt_content_third.exists:
                        new_prompt_text = prompt_content_third.get_text()
                        logger.debug(f"新弹窗内容(ID方式): {new_prompt_text}")
                    elif fund_error_elements.exists or lack_error_elements.exists:
                        # 如果通过ID找不到，尝试通过文本特征
                        if fund_error_elements.exists:
                            new_prompt_text = fund_error_elements.get_text()
                            logger.debug(f"新弹窗内容(文本特征'资金'): {new_prompt_text}")
                        elif lack_error_elements.exists:
                            new_prompt_text = lack_error_elements.get_text()
                            logger.debug(f"新弹窗内容(文本特征'不足'): {new_prompt_text}")
                    else:
                        # 如果所有方式都获取不到内容，使用默认提示
                        new_prompt_text = "无法获取弹窗具体内容"

                    logger.warning(f"委托失败，{new_prompt_text}")
                    return False, new_prompt_text
            else:
                # 处理其他情况
                confirm_button_to_click = confirm_button if confirm_button.exists else confirm_button_second if confirm_button_second.exists else None
                if confirm_button_to_click:
                    time.sleep(1)
                    confirm_button_to_click.click()

                error_msg = f"未检测到'委托确认'提示，弹窗内容: {prompt_text}"
                logger.warning(error_msg)
                send_notification(error_msg)
                return False, prompt_text

        except Exception as e:
            error_msg = f"处理弹窗时发生异常: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return False, error_msg

    def get_dialog_content_by_layout(self):
        """
        通过定位content_layout获取弹窗内容

        Returns:
            str: 弹窗文本内容
        """
        try:
            # content_layout = self.d(resourceId="com.hexin.plat.android:id/content_layout")
            content_layout = self.d(resourceId="com.hexin.plat.android:id/ll_adjust_align_tv")
            if content_layout.exists:
                # 查找content_layout下的TextView
                text_view = content_layout.child(className="android.widget.TextView")
                if text_view.exists:
                    view_text = text_view.get_text()
                    logger.info(f"通过content_layout获取到弹窗文本：{view_text}")
                    return view_text
        except Exception as e:
            logger.error(f"获取弹窗内容失败: {e}")
        return None

    def _extract_trade_info(self, prompt_text):
        """
        从提示文本中提取股票名称、代码和数量

        Args:
            prompt_text: 提示文本

        Returns:
            tuple: (股票名称, 股票代码, 数量)
        """
        if not prompt_text:
            return None, None, None

        # 使用正则表达式提取信息
        import re

        # 提取股票名称（通常在文本开头或中间）
        name_pattern = r'(?:[A-Za-z\u4e00-\u9fa5]+(?:\s*[\u4e00-\u9fa5]+)*)'
        name_match = re.search(name_pattern, prompt_text)
        stock_name = name_match.group(0) if name_match else None

        # 提取股票代码（通常是6位数字）
        code_pattern = r'\d{6}'
        code_match = re.search(code_pattern, prompt_text)
        stock_code = code_match.group(0) if code_match else None

        # 提取数量（通常是数字，可能带单位）
        volume_pattern = r'(\d+)(?:手|股)?'
        volume_match = re.search(volume_pattern, prompt_text)
        volume = int(volume_match.group(1)) if volume_match else None

        return stock_name, stock_code, volume

    def update_holding_info_all(self, account_info):
        """
        更新所有账户持仓信息

        Args:
            account_info: AccountInfo实例
        """
        self.click_holding_stock_button()
        self.click_refresh_button()
        time.sleep(0.5)
        try:
            account_info.update_holding_info_all()
            logger.info("更新持仓信息")
        except Exception as e:
            error_msg = f"更新账户数据时发生异常: {e}"
            logger.error(error_msg)
            send_notification(error_msg)