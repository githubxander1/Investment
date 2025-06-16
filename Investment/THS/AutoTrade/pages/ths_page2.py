# ths_page2.py
import time

from uiautomator2 import UiObjectNotFoundError

from Investment.THS.AutoTrade.config.settings import THS_AUTO_TRADE_LOG_FILE_PAGE
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_PAGE)

# d = uiautomator2.connect()
# d.implicitly_wait(10)

class THSPage:
    def __init__(self, d):
        # self.dialog_volume_zero_info = None
        self.d = d
        self.d.implicitly_wait(10)

    def click_back(self):
        click_back = self.d(resourceId='com.hexin.plat.android:id/title_bar_left_container')
        click_back.click()
        logger.info("点击返回按钮")

    def click_trade_entry(self):
        trade_entry = self.d(resourceId='com.hexin.plat.android:id/title', text='交易')
        trade_entry.click()
        logger.info("点击交易按钮")

    def buy_entry(self):
        buy_entry = self.d(resourceId='com.hexin.plat.android:id/menu_buy_text')
        buy_entry.click()
        logger.info("点击买入按钮")

    def sell_entry(self):
        sell_entry = self.d(resourceId='com.hexin.plat.android:id/menu_sale_text')
        sell_entry.click()
        logger.info("点击卖出按钮")

    def search_stock(self, stock_name):
        stock_search = self.d(resourceId='com.hexin.plat.android:id/content_stock')
        stock_search.click()
        logger.info("点击股票搜索框")

        auto_search = self.d(resourceId='com.hexin.plat.android:id/auto_stockcode', text='股票代码/简拼')
        clear = self.d(resourceId='com.hexin.plat.android:id/clearable_edittext_btn_clear')
        if clear.exists():
            clear.click()
        logger.info("清除股票代码")
        time.sleep(1)

        auto_search.send_keys(stock_name)
        auto_search.send_keys(stock_name)
        logger.info(f"输入股票名称: {stock_name}")
        time.sleep(1)

        recycler_view = self.d(resourceId='com.hexin.plat.android:id/recyclerView')
        if recycler_view.exists:
            first_item = recycler_view.child(index=0)
            first_item.click()
            logger.info("点击匹配的的第一个股票")
            time.sleep(1)
        else:
            logger.info("没有匹配到股票或已选中")

    def input_volume(self, volume):
        volumn = self.d(className='android.widget.EditText')[2]
        volumn.send_keys(volume)
        logger.info(f"输入买入数量: {volume}")

    def half_volume(self):
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='1/2仓')
        volumn.click()
        logger.info("输入买入数量: 半仓")

    def total_volume(self):
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='全仓')
        volume = self.d(className='android.widget.EditText')[2]
        logger.info("获取买入数量")
        if volume.get_text() != 0:
            volumn.click()
            logger.info("输入买入数量: 全仓")
        else:
            pass
            # self.total_volume()
        logger.info("输入买入数量: 全仓")

    def click_button_by_text(self, text):
        button = self.d(className='android.widget.TextView', text=text)
        button.click()
        logger.info(f"点击按钮: {text}")

    def confirm_transaction(self):
        dialog_info = self.d(className='android.widget.Button')[1]
        dialog_info.click()
        logger.info("点击确认按钮")

    def dialog_confirm(self):
        dialog_confirm = self.d(resourceId='com.hexin.plat.android:id/ok_btn', text='确定')
        dialog_confirm.click()
        logger.info("点击弹窗确认按钮")

    def dialog_sell_confirm(self):
        dialog_confirm = self.d(resourceId='com.hexin.plat.android:id/ok_btn', text='确定')
        dialog_confirm.click()
        logger.info("点击弹窗确认按钮")

    def dialog_sell_confirm2(self):
        dialog_confirm = self.d(resourceId='com.hexin.plat.android:id/ok_btn', text='确认卖出')
        dialog_confirm.click()
        logger.info("点击弹窗确认按钮")

    def dialog_buy_confirm(self):
        dialog_confirm = self.d(resourceId='com.hexin.plat.android:id/left_btn', text='确定')
        dialog_confirm.click()
        logger.info("点击弹窗确认按钮")

    def handle_dialog(self):
        dialog_title = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
        self.dialog_volume_zero_info = self.d(resourceId='com.hexin.plat.android:id/prompt_content')#委托数量必须大于0

        dialog_sus_info = self.d.xpath('//*[contains(@text,"委托已提交")]')
        # self.dialog_salevolume_zero = self.d.xpath('//*[contains(@text,"委托数量必须大于")]')

        dialog_confirm = self.d(resourceId='com.hexin.plat.android:id/left_btn', text='确定')
        dialog_info_transferred_founds = self.d.xpath('//*[contains(@text,"转入资金")]')

        # sell_confirm_title = self.d(resourceId='com.hexin.plat.android:id/dialog_title', text='确定')
        time.sleep(1)
        if dialog_sus_info.exists:
            self.dialog_confirm()
            logger.info("委托已提交")
            return True, "委托已提交"
        elif dialog_info_transferred_founds.exists:
            info = self.d(resourceId='com.hexin.plat.android:id/content_scroll')
            info = info.get_text()
            # self.dialog_sell_confirm()
            dialog_confirm.click()
            logger.info(f"失败,{info}")
            return False, info
        elif self.dialog_volume_zero_info.exists:#委托数量必须大于0
            info = self.dialog_volume_zero_info.get_text()
            time.sleep(1)
            self.dialog_confirm()
            time.sleep(1)
            # self.click_back()
            # self.dialog_confirm()
            logger.info(f"失败,{info}")
            return False, info
        elif dialog_title.exists:
            # info = self.dialog_salevolume_zero.get_text()
            self.dialog_sell_confirm()

        else:
            try:
                dialog_info = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
                info = dialog_info.get_text()
                self.dialog_confirm()
                logger.info(f"失败,{info}")
                return False, info
            except UiObjectNotFoundError:
                logger.info("未找到任何对话框")
                return False, "未找到任何对话框"

    def buy_stock(self, stock_name, volume):
        try:
            self.click_trade_entry()
            self.buy_entry()
            self.search_stock(stock_name)
            self.input_volume(volume)
            # self.click_button_by_text('买 入(模拟炒股)')
            self.click_button_by_text('买 入')
            self.confirm_transaction()
            time.sleep(1)
            success, info = self.handle_dialog()
            time.sleep(1)
            self.click_back()
            return success, info
        except Exception as e:
            logger.error(f"买入 {stock_name} {volume} 股失败: {e}", exc_info=True)
            return False, f"买入 {stock_name} {volume} 股失败: {e}"

    def sell_stock(self, stock_name, volume):
        try:
            self.click_trade_entry()
            self.sell_entry()
            self.search_stock(stock_name)
            if volume == '全仓' or volume == '半仓':
                self.total_volume()
                # self.click_button_by_text('卖 出(模拟炒股)')
                self.click_button_by_text('卖 出')
                time.sleep(1)# 未持仓，委托数量为0
                self.dialog_volume_zero_info = self.d(
                    resourceId='com.hexin.plat.android:id/prompt_content')  # 委托数量必须大于0
                if self.dialog_volume_zero_info.exists:# 委托数量必须大于
                    self.handle_dialog()
                else:
                    self.dialog_sell_confirm2()#委托确认卖出弹窗
                    self.dialog_sell_confirm()
                    self.click_back()
            else:
                self.input_volume(volume)
                # self.click_button_by_text('卖 出(模拟炒股)')
                self.click_button_by_text('卖 出')
                self.confirm_transaction()
                time.sleep(1)
                success, info = self.handle_dialog()
                time.sleep(1)
                self.click_back()
                return success, info
        except Exception as e:
            logger.error(f"卖出 {stock_name} {volume} 股失败: {e}", exc_info=True)
            return False, f"卖出 {stock_name} {volume} 股失败: {e}"

# if __name__ == '__main__':
#
#     d = uiautomator2.connect()
#     pom = THSPage(d)
#     # pom.sell_stock('中国电信','半仓')
#     pom.sell_stock('英维克','半仓')
