# ths_page.py
import time
import pandas as pd
import uiautomator2

from Investment.THS.AutoTrade.config.settings import THS_AUTO_TRADE_LOG_FILE_PAGE, Account_holding_stockes_info_file
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification
# from Investment.THS.AutoTrade.scripts.数据处理 import new_ratio

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_PAGE)


class THSPage:
    def __init__(self, d):
        self.d = d
        self.d.implicitly_wait(10)
        self._current_stock_name = None

    # 元素定位
    # 搜索框
    def search_editor(self):
        return self.d(resourceId="com.hexin.plat.android:id/text_switcher")

    # 搜索框输入
    def search_input(self):
        return self.d(resourceId="com.hexin.plat.android:id/search_input")

    # 搜索匹配结果
    def stock_name(self):
        return self.d(resourceId="com.hexin.plat.android:id/stock_name")[0]

    # 下单
    def xiadan(self):
        return self.d(resourceId="com.hexin.plat.android:id/xiadan")

    # 买入
    def buy_button_entry(self):
        return self.d(resourceId="com.hexin.plat.android:id/buy_button")

    # 卖出
    def sale_button_entry(self):
        return self.d(resourceId="com.hexin.plat.android:id/sale_button")

    # 买入数量
    def buy_number(self):
        return self.d(text="买入数量")

    # 卖出数量
    def sale_number(self):
        return self.d(text="卖出数量")



    # 仓位选择
    def total_quantity(self):
        # return self.d(resourceId="com.hexin.plat.android:id/key_all", text='全仓')
        return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='全仓')

    def half_quantity(self):
        return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='1/2仓')

    def third_quantity(self):
        return self.d(resourceId="com.hexin.plat.android:id/tv_flashorder_cangwei", text='1/3仓')

    def operate_button_keyboard(self):
        return self.d(resourceId="com.hexin.plat.android:id/keyboard_key_imeaction")

    # 输入数量后系统自动计算的价格
    def get_price_by_volume(self):
        # '//*[@resource-id="com.hexin.plat.android:id/couldbuy_volumn"]
        price = self.d(resourceId='com.hexin.plat.android:id/couldbuy_volumn')
        return price.get_text()

    # confirm_selector = self.d(resourceId="com.hexin.plat.android:id/confirm_btn_view")
    def confirm_buy_button(self):
        return self.d(resourceId="com.hexin.plat.android:id/confirm_btn_view")

    # 股票余额不够
    def insufficient_balance(self):
        return self.d(resourceId="com.hexin.plat.android:id/prompt_content", text='股票余额不足 ,不允许卖空')
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

    #定义一个实时价格的函数
    def get_real_price(self):
        """获取当前股票实时价格"""
        for _ in range(3): # 尝试3次
            price_element = self.d(className='android.widget.EditText')[1]
            text = price_element.get_text()
            # print("当前价格:", price_element.get_text())
            try:
                return float(text)
            except ValueError:
                logger.error("无法解析价格文本")
                return None
        raise ValueError("无法获取实时价格")

    def calculate_volume(self, operation: str, new_ratio: float = None):
        """
        根据当前持仓和策略动态计算交易数量
        :param operation: '买入' 或 '卖出'
        :param new_ratio: 新仓位比例（可选）
        :return: 交易股数
        """
        volume_max = 4000
        if not self._current_stock_name:
            logger.warning("未设置标的名称")
            return 0

        stock_name = self._current_stock_name

        if operation == "买入":
            holding_stock_df = pd.read_excel(Account_holding_stockes_info_file, sheet_name="表头数据")
            available = int(holding_stock_df['可用'])

            real_price = self.get_real_price()

            if available < volume_max:
                volume_max = available
            volume = int(volume_max / real_price)  # 固定金额买入
            logger.info(f"买入操作 - 实时价格: {real_price}, 数量: {volume}")
            return volume

        elif operation == "卖出":
            holding_stock_df = pd.read_excel(Account_holding_stockes_info_file, sheet_name="持仓数据")
            holding_stock = holding_stock_df[holding_stock_df['标的名称'] == stock_name]

            if not holding_stock.empty:
                available = int(holding_stock['持仓/可用'].str.split('/').str[1].iloc[0])
                if new_ratio is not None and new_ratio != 0:
                    volume = int(available * 0.5)  # 半仓卖出
                else:
                    volume = available  # 全部卖出
            else:
                logger.warning(f"{stock_name} 不在持仓列表中")
                volume = 0

            logger.info(f"卖出操作 - 数量: {volume}")
            return volume

        else:
            logger.warning("未知操作类型")
            return 0

    def buy_stock(self, stock_name):
        try:
            self._current_stock_name = stock_name
            quantity = self.calculate_volume("买入")

            logger.info(f"开始买入流程 {stock_name}  {quantity}股")
            send_notification(f"开始买入流程 {stock_name}  {quantity}股")
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
            self.wait_and_click(self.confirm_buy_button(), "confirm_buy_button")
            time.sleep(2)

            if self.withdraw_button().exists:
                logger.info(f"买入成功 {stock_name}  {quantity}股")
                self.return_to_search_page()
                return True, "买入成功"
            else:
                logger.error(f"买入失败 {stock_name}: 确认按钮点击后未显示撤单按钮")
                self.return_to_search_page()
                return False, "确认按钮异常"

        except Exception as e:
            logger.error(f"买入失败 {stock_name}: {e}", exc_info=True)
            return False, str(e)

    def sell_stock(self, stock_name, new_ratio=None):
        try:
            self._current_stock_name = stock_name
            quantity = self.calculate_volume("卖出", new_ratio=new_ratio)

            logger.info(f"开始卖出流程 {stock_name} {quantity}股")
            send_notification(f"开始卖出流程 {stock_name} {quantity}股")
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
            self.wait_and_click(self.sale_button(), "sale_button")
            time.sleep(1)
            self.wait_and_click(self.confirm_sale_button(), "confirm_sale_button")
            time.sleep(2)

            if self.withdraw_button().exists:
                logger.info(f"卖出成功 {stock_name}  {quantity}股")
                self.return_to_search_page()
                return True, "卖出成功"
            else:
                logger.error(f"卖出失败 {stock_name}: 确认按钮不可点击")
                self.return_to_search_page()
                return False, "确认按钮不可点击"

        except Exception as e:
            logger.error(f"卖出失败：{stock_name}: {e}", exc_info=True)
            return False, str(e)

if __name__ == '__main__':
    d = uiautomator2.connect()
    #打印结构树
    # print(f"当前屏幕结构树:\n {d.dump_hierarchy()}")
    pom = THSPage(d)
    # def get1():
    #     '//*[@resource-id="com.hexin.plat.android:id/two_text_value"]'
    #     win = self.d(resourceId='com.hexin.plat.android:id/two_text_value')
    #     return win.get_text()

    # pom.get_real_price()
    print(pom.get_real_price())