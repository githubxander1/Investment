import logging
import time

# import uiautomator2 as u2
# from others.量化投资.THS.自动化交易_同花顺.ths_main import logger
from others.量化投资.THS.自动化交易_同花顺.ths_logger import logger


class THSPage:
    def __init__(self, d):
        self.d = d

    # 元素定位
    def search_editor(self):
        return self.d(resourceId="com.hexin.plat.android:id/text_switcher")

    def search_input(self):
        return self.d(resourceId="com.hexin.plat.android:id/search_input")

    def stock_name(self):
        return self.d(resourceId="com.hexin.plat.android:id/stock_name")[0]

    def xiadan(self):
        return self.d(resourceId="com.hexin.plat.android:id/xiadan")

    def buy_button_entry(self):
        return self.d(resourceId="com.hexin.plat.android:id/buy_button")

    def sale_button_entry(self):
        return self.d(resourceId="com.hexin.plat.android:id/sale_button")

    def buy_number(self):
        return self.d(text="买入数量")

    def sale_number(self):
        return self.d(text="卖出数量")

    def total_quantity(self):
        # return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='全仓')
        return self.d(resourceId="com.hexin.plat.android:id/key_all", text='全仓')

    def half_quantity(self):
        return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='1/2仓')
        # return self.d(resourceId="com.hexin.plat.android:id/key_half", text='半仓')
        # return self.d(resourceId="com.hexin.plat.android:id/key_half")

    def third_quantity(self):
        return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='1/3仓')

    def operate_button_keyboard(self):
        return self.d(resourceId="com.hexin.plat.android:id/keyboard_key_imeaction")

    def confirm_button(self):
        return self.d(resourceId="com.hexin.plat.android:id/confirm_btn_view")

    def sale_button(self):
        return self.d(resourceId="com.hexin.plat.android:id/order_button")

    def stock_log_button(self):
        return self.d(resourceId="com.hexin.plat.android:id/iv_stock_log")

    def input_stock_log(self, text):
        self.d(resourceId="com.hexin.plat.android:id/editText").set_text(text)

    def save_stock_log(self):
        self.d(resourceId="com.hexin.plat.android:id/publishTv").click()

    def back_button_details(self):
        return self.d(resourceId="com.hexin.plat.android:id/backButton")

    def back_button_search(self):
        return self.d(resourceId="com.hexin.plat.android:id/back_up")

    # 操作方法
    def wait_and_click(self, selector, method_name=None):
        try:
            if selector:
                selector.click()
                logger.info(f"点击: {method_name or 'unknown method'}")
            else:
                logger.error(f"元素未找到 {method_name or 'unknown method'}")
        except Exception as e:
            logger.error(f"元素点击失败 {method_name or 'unknown method'}. 信息: {e}", exc_info=True)

    def set_text(self, selector, text, method_name=None):
        try:
            if selector:
                selector.set_text(text)
                logger.info(f"输入 '{text}' 在 {method_name or 'unknown method'}")
            else:
                logger.error(f"元素未找到 {method_name or 'unknown method'}")
        except Exception as e:
            logger.error(f"输入失败 {method_name or 'unknown method'}. 信息: {e}", exc_info=True)

    # 写买卖操作日志
    def record_stock_log(self, text):
        self.wait_and_click(self.stock_log_button(), "stock_log_button")
        self.set_text(self.input_stock_log(text), text, "input_stock_log")
        self.wait_and_click(self.save_stock_log(), "save_stock_log")

    def buy_stock(self, stock_name, quantity):
        try:
            logger.info(f"开始买入流程 {stock_name}  {quantity}股")
            self.wait_and_click(self.search_editor(), "search_editor")
            self.set_text(self.search_input(), stock_name, "search_input")
            time.sleep(3)  # 等待搜索结果加载
            self.wait_and_click(self.stock_name(), "stock_name")
            self.wait_and_click(self.xiadan(), "xiadan")
            self.wait_and_click(self.buy_button_entry(), "buy_button_entry")
            time.sleep(1)
            self.set_text(self.buy_number(), str(quantity), "buy_number")
            time.sleep(1)
            self.operate_button_keyboard().click()
            time.sleep(1)
            self.wait_and_click(self.confirm_button(), "confirm_button")
            time.sleep(1)
            # self.wait_and_click(self.record_stock_log('测试输入买入记录'))
            logger.info(f"买入成功 {stock_name}  {quantity}股")
            # 返回
            self.wait_and_click(self.back_button_details(), "back_button_details")
            self.wait_and_click(self.back_button_search(), "back_button_search")
        except Exception as e:
            logger.error(f"买入失败 {stock_name}: {e}", exc_info=True)

    def sell_stock(self, stock_name, quantity):
        try:
            logger.info(f"开始卖出流程 {stock_name} {quantity}股")
            self.wait_and_click(self.search_editor(), "search_editor")
            self.set_text(self.search_input(), stock_name, "search_input")
            time.sleep(3)  # 等待搜索结果加载
            self.wait_and_click(self.stock_name(), "stock_name")
            self.wait_and_click(self.xiadan(), "xiadan")
            self.wait_and_click(self.sale_button_entry(), "sale_button_entry")
            time.sleep(1)
            self.wait_and_click(self.half_quantity(), "half_quantity")
            time.sleep(1)
            self.wait_and_click(self.sale_button(), "sale_button")
            time.sleep(1)
            self.wait_and_click(self.confirm_button(), "confirm_button")
            time.sleep(1)
            # self.wait_and_click(self.record_stock_log('测试输入记录'))
            logger.info(f"卖出成功 {stock_name}  {quantity}股")
            # 返回
            self.wait_and_click(self.back_button_details(), "back_button_details")
            self.wait_and_click(self.back_button_search(), "back_button_search")
        except Exception as e:
            logger.error(f"卖出失败： {stock_name}: {e}", exc_info=True)
