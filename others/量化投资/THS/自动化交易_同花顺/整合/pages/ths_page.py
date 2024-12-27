# ths_page.py
import logging
import time
from others.量化投资.THS.自动化交易_同花顺.ths_logger import setup_logger
# logger = setup_logger(r'/zothers/量化投资/THS/自动化交易_同花顺/保存的数据/同花顺自动化交易.log')
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import THS_AUTO_TRADE_LOG_FILE_PAGE
from others.量化投资.THS.自动化交易_同花顺.整合.utils.ths_logger import setup_logger

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_PAGE)
class THSPage:
    def __init__(self, d):
        self.d = d
        self.d.implicit_wait(10)

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

    # 股票余额不够
    def insufficient_balance(self):
        return self.d(resourceId="com.hexin.plat.android:id/prompt_content", text='股票余额不足 ,不允许卖空')

    def total_quantity(self):
        # return self.d(resourceId="com.hexin.plat.android:id/key_all", text='全仓')
        return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='全仓')

    def half_quantity(self):
        return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='1/2仓')

    def third_quantity(self):
        return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='1/3仓')

    def operate_button_keyboard(self):
        return self.d(resourceId="com.hexin.plat.android:id/keyboard_key_imeaction")

    # confirm_selector = self.d(resourceId="com.hexin.plat.android:id/confirm_btn_view")
    def confirm_buy_button(self):
        return self.d(resourceId="com.hexin.plat.android:id/confirm_btn_view")

    def sale_button(self):
        return self.d(resourceId="com.hexin.plat.android:id/order_button")
    def confirm_sale_button(self):
        return self.d(resourceId="com.hexin.plat.android:id/confirm_btn_view")

    def withdraw_button(self):
        return self.d(resourceId="com.hexin.plat.android:id/confirm_btn_view", text='撤单')

    def buy_fail_dialog_text(self):
        text = '柜台 :可用余额不够'
        # 使用f-string进行格式化，以便在正则表达式中包含特定文案
        regex_pattern = fr"^.*{text}.*$"

        # 使用uiautomator2的d()函数进行定位
        return self.d(text=regex_pattern)

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

    # def trade_money(self):
    #     return self.d(resouceId="com.hexin.plat.android:id/trade_money")

    def trade_money(self):
        return self.d(className="android.widget.EditText", text="0")
    # 写买卖操作日志
    def record_stock_log(self, text):
        self.wait_and_click(self.stock_log_button(), "stock_log_button")
        self.set_text(self.input_stock_log(text), text, "input_stock_log")
        self.wait_and_click(self.save_stock_log(), "save_stock_log")

    def return_to_search_page(self):
        self.wait_and_click(self.back_button_details(), "back_button_details")
        logger.info('从详情页返回到搜索页')
        self.wait_and_click(self.back_button_search(), "back_button_search")
        logger.info(f"返回到搜索页")
    def buy_stock(self, stock_name, quantity):
        try:
            logger.info(f"开始买入流程 {stock_name}  {quantity}股")
            self.wait_and_click(self.search_editor(), "search_editor")
            self.set_text(self.search_input(), stock_name, "search_input")
            time.sleep(3)  # 等待搜索结果加载
            self.wait_and_click(self.stock_name(), "stock_name")
            time.sleep(1)
            self.wait_and_click(self.xiadan(), "xiadan")
            time.sleep(1)
            self.wait_and_click(self.buy_button_entry(), "buy_button_entry")
            time.sleep(1)
            self.set_text(self.buy_number(), str(quantity), "buy_number")
            time.sleep(1)
            self.operate_button_keyboard().click()
            time.sleep(1)
            # confirm_buy_button = self.confirm_buy_button()
            # if confirm_buy_button.info.get('enabled', False):
            self.wait_and_click(self.confirm_buy_button(), "confirm_buy_button")
            time.sleep(2)
            if self.withdraw_button().exists:
                logger.info(f"买入成功 {stock_name}  {quantity}股")
                time.sleep(1)
                self.wait_and_click(self.return_to_search_page(), "return_to_search_page")
                return True
            elif self.buy_fail_dialog_text().exists:
                logger.error(f"买入失败 {stock_name}: 资金不足")
                time.sleep(1)
                self.wait_and_click(self.return_to_search_page(), "return_to_search_page")
            else:
                logger.error(f"买入失败 {stock_name}: 确认按钮点击后未显示撤单按钮")
                time.sleep(1)
                self.wait_and_click(self.return_to_search_page(), "return_to_search_page")
                return False
        except Exception as e:
            logger.error(f"买入失败 {stock_name}: {e}", exc_info=True)
            return False

    def sell_stock(self, stock_name, quantity):
        try:
            logger.info(f"开始卖出流程 {stock_name} {quantity}股")
            self.wait_and_click(self.search_editor(), "search_editor")
            self.set_text(self.search_input(), stock_name, "search_input")
            time.sleep(3)  # 等待搜索结果加载
            self.wait_and_click(self.stock_name(), "stock_name")
            time.sleep(1)
            self.wait_and_click(self.xiadan(), "xiadan")
            time.sleep(1)
            self.wait_and_click(self.sale_button_entry(), "sale_button_entry")
            time.sleep(1)

            self.wait_and_click(self.half_quantity(), "half_quantity")

            # trade_money = self.trade_money()
            # if trade_money.exists:
            #     if trade_money.get_text() == '0':
            #         self.wait_and_click(self.total_quantity())
            self.wait_and_click(self.sale_button(), "sale_button")
            time.sleep(1)
            self.wait_and_click(self.confirm_sale_button(), "confirm_sale_button")
            time.sleep(2)
            if self.withdraw_button().exists:
                logger.info(f"卖出成功 {stock_name}  {quantity}股")
                time.sleep(1)
                self.wait_and_click(self.return_to_search_page(), "return_to_search_page")
                return True
            else:
                logger.error(f"卖出失败 {stock_name}: 确认按钮不可点击")
                time.sleep(1)
                self.wait_and_click(self.return_to_search_page(), "return_to_search_page")
                return False
        except Exception as e:
            logger.error(f"卖出失败： {stock_name}: {e}", exc_info=True)
            return False
