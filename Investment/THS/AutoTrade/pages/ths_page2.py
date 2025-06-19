# ths_page2.py
import time
from pydoc import classname

import pandas as pd
import uiautomator2
# from sympy.physics.units import volume
from uiautomator2 import UiObjectNotFoundError

from Investment.THS.AutoTrade.config.settings import THS_AUTO_TRADE_LOG_FILE_PAGE, Account_holding_stockes_info_file
from Investment.THS.AutoTrade.scripts.账户持仓信息 import update_holding_info
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_PAGE)

# d = uiautomator2.connect()
# d.implicitly_wait(10)

class THSPage:
    def __init__(self, d):
        self.d = d
        self.d.implicitly_wait(10)
        self._current_stock_name = None  # 新增用于保存当前股票名称

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

    def click_holding_stock(self):
        holding_button = self.d(className='android.widget.TextView', text='持仓')
        holding_button.click()
        logger.info("点击持仓按钮")

    def click_refresh_button(self):
        refresh_button = self.d(resourceId='com.hexin.plat.android:id/refresh_button')
        refresh_button.click()
        logger.info("点击刷新按钮")

    def search_stock(self, stock_name):
        stock_search = self.d(resourceId='com.hexin.plat.android:id/content_stock')
        stock_search.click()
        logger.info(f"点击股票搜索框: {stock_name}")

        auto_search = self.d(resourceId='com.hexin.plat.android:id/auto_stockcode', text='股票代码/简拼')
        clear = self.d(resourceId='com.hexin.plat.android:id/clearable_edittext_btn_clear')
        if clear.exists():
            clear.click()
            logger.info("清除股票代码")
        time.sleep(1)

        auto_search.send_keys(stock_name)
        logger.info(f"输入股票名称: {stock_name}")
        time.sleep(1)

        # 如果clear按钮在，则点击匹配，如果找不到，则pass，继续下一步
        if clear.exists():
            recycler_view = self.d(resourceId='com.hexin.plat.android:id/recyclerView')
            if recycler_view.exists:
                first_item = recycler_view.child(index=0)
                first_item.click()
                logger.info("点击匹配的第一个股票")
                time.sleep(1)
            else:
                logger.info("没有匹配到股票或已选中")
        time.sleep(2)

    def input_volume(self, volume):
        volumn = self.d(className='android.widget.EditText')[2]
        volumn.send_keys(volume)
        logger.info(f"输入买入数量: {volume}手")

    def half_volume(self):
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='1/2仓')
        volumn.click()
        logger.info("输入买入数量: 半仓")

    def total_volume(self):
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='全仓')
        volume = self.d(className='android.widget.EditText')[2]
        logger.info("获取买入数量")
        if volume.get_text() != '0':
            volumn.click()
            logger.info("输入买入数量: 全仓")
        else:
            pass

    # 输入数量后系统自动计算的价格
    def get_price_by_volume(self):
        price = self.d(resourceId='com.hexin.plat.android:id/couldbuy_volumn')
        return price.get_text()

    def click_button_by_text(self, text):
        button = self.d(className='android.widget.TextView', text=text)
        button.click()
        logger.info(f"点击按钮: {text}")

    def confirm_transaction(self):
        # dialog_info = self.d(className='android.widget.Button')[1]
        # dialog_info.click()
        # logger.info("点击确认按钮")

        #弹窗提示：委托数量必须大于0

        dialog_title = self.d(resourceId='com.hexin.plat.android:id/dialog_title')#弹窗标题
        if dialog_title.exists:
            dialog_info =self.d.xpath('//*[@resource-id="com.hexin.plat.android:id/prompt_content"]')
            dialog_info =self.d(resourceId="com.hexin.plat.android:id/prompt_content")
            logger.info(f"弹窗内容：{dialog_info}")
            self.dialog_confirm()
            logger.info("点击弹窗确认按钮")

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

    # def handle_dialog(self):
    #     dialog_title = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
    #
    #     dialog_volume_zero_info = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
    #
    #     dialog_sus_info = self.d.xpath('//*[contains(@text,"委托已提交")]')
    #     dialog_info_transfered_founds = self.d.xpath('//*[contains(@text,"转入资金")]')
    #     #定义委托数量不足100股的提示
    #     dialog_info_scroll_content = self.d.xpath('//android.widget.TextView)[2]')
    #     time.sleep(1)
    #     if dialog_sus_info.exists:
    #         self.dialog_confirm()
    #         logger.info("委托已提交")
    #         return True, "委托已提交"
    #     elif dialog_info_transfered_founds.exists:
    #         info = self.d(resourceId='com.hexin.plat.android:id/content_scroll').get_text()
    #         dialog_confirm = self.d(resourceId='com.hexin.plat.android:id/left_btn', text='确定')
    #         dialog_confirm.click()
    #         logger.info(f"失败,{info}")
    #         return False, info
    #     elif dialog_volume_zero_info.exists:
    #         info = dialog_volume_zero_info.get_text()
    #         time.sleep(1)
    #         self.dialog_confirm()
    #         time.sleep(1)
    #         logger.info(f"失败,{info}")
    #         return False, info
    #     elif dialog_info_scroll_content.exists:
    #         info = dialog_info_scroll_content.get_text()
    #         time.sleep(1)
    #         self.dialog_confirm()
    #         time.sleep(1)
    #         logger.info(f"失败,{info}")
    #         return False, info
    #
    #     elif dialog_title.exists:
    #         self.dialog_sell_confirm()
    #         return True, "卖出操作成功"
    #
    #     else:
    #         try:
    #             dialog_info = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
    #             info = dialog_info.get_text()
    #             self.dialog_confirm()
    #             logger.info(f"失败,{info}")
    #             return False, info
    #         except UiObjectNotFoundError:
    #             logger.info("未找到任何对话框")
    #             return False, "未找到任何对话框"

    def _calculate_volume(self, operation: str, new_ratio: float = None):
        """
        根据当前持仓和策略动态计算交易数量
        :param operation: '买入' 或 '卖出'
        :param new_ratio: 新仓位比例（可选）
        :return: tuple(success: bool, message: str, volume: int | None)
        """
        volume_max = 4000

        # from Investment.THS.AutoTrade.scripts.账户持仓信息 import Account_holding_stockes_info_file
        import pandas as pd

        if operation == "买入":
            holding_stock_df = pd.read_excel(Account_holding_stockes_info_file, sheet_name="表头数据", thousands=',')

            buy_available = float(holding_stock_df['可用'].iloc[0])
            logger.info(f"可用金额: {buy_available}")

            real_price = self._get_real_price()
            logger.info(f"实时价格: {real_price}")

            if buy_available < volume_max:# 如果可用金额小于4000，则使用可用金额
                volume = int(buy_available / real_price)
            else:
                volume = int(volume_max / real_price)

            volume = (volume // 100) * 100
            if volume < 100:
                buy_failed_info = "交易数量不足100股"
                logger.info("交易数量不足100股")
                return False, '失败', buy_failed_info  # 返回False表示交易失败
            logger.info(f"买入操作 - 实时价格: {real_price}, 数量: {volume}")
            return True, '股数计算成功', volume

        elif operation == "卖出":
            holding_stock_df = pd.read_excel(Account_holding_stockes_info_file, sheet_name="持仓数据", thousands=',')

            if self._current_stock_name in holding_stock_df['标的名称'].values:
                sale_available = int(holding_stock_df[holding_stock_df['标的名称'] == self._current_stock_name]['持仓/可用'].str.split('/').str[1].iloc[0])
                if sale_available is None or sale_available == 0:
                    logger.error("无持仓数量")
                    #退出，不继续下一步，直接退出
                    return False, '失败', '无持仓数量'
                if new_ratio is not None and new_ratio != 0:
                    volume = int(sale_available * 0.5)  # 半仓卖出
                else:
                    volume = sale_available  # 全部卖出

                volume = (volume // 100) * 100
                if volume < 100:
                    logger.warning(f"卖出数量小于100股，将不卖出")
                    return False, '失败', '卖出数量不足100'

                real_price = self._get_real_price()
                logger.info(f"实时价格: {real_price}")
                logger.info(f"卖出操作 - 数量: {volume} (共可用：{sale_available})")
                return True, '成功', volume
            else:
                logger.warning(f"{self._current_stock_name} 不在持仓列表中")
                return False, '不在持仓列表', 0


        else:
            logger.warning("未知操作类型")
            return False, '未知操作类型',0

    def _get_real_price(self):
        """获取当前股票实时价格"""
        for _ in range(3):  # 尝试3次
            price_element = self.d(className='android.widget.EditText')[1]
            text = price_element.get_text()
            try:
                return float(text)
            except ValueError:
                logger.error("无法解析价格文本")
                return None
        raise ValueError("无法获取实时价格")


    # def get_dialog_elements(self):
    #     """获取所有可能的弹窗元素"""
    #     return {
    #         '''
    #         1.委托成功
    #         2.资金不足
    #         3.委托数量要大于0
    #
    #         '''
    #         "submit_success": self.d.xpath('//*[contains(@text,"委托已提交")]'),
    #         "transfer_funds": self.d.xpath('//*[contains(@text,"转入资金")]'),
    #
    #         "dialog_title": self.d(resourceId='com.hexin.plat.android:id/dialog_title'),
    #         "prompt_content": self.d(resourceId='com.hexin.plat.android:id/prompt_content'),
    #         "scroll_content": self.d.xpath('//android.widget.TextView)[3]'),#可用资金不足是[3]
    #         # "content_scroll": self.d(resourceId='com.hexin.plat.android:id/content_scroll'),
    #         "confirm_button": self.d(resourceId='com.hexin.plat.android/id/ok_btn', text='确定'),
    #         "sell_confirm_button": self.d(resourceId='com.hexin.plat.android:id/left_btn', text='确定')
    #     }

    def dialog_handle(self):
        """处理交易后的各种弹窗情况"""
        logger.info("开始处理弹窗")
        # dialog_elements = self.get_dialog_elements()
        # time.sleep(1)
        #弹窗标题里有：委托买入确认
        submit_success= self.d.xpath('//*[contains(@text,"委托已提交")]')
        transfer_funds= self.d.xpath('//*[contains(@text,"转入资金")]')

        dialog_title= self.d(resourceId='com.hexin.plat.android:id/dialog_title')
        prompt_content= self.d(resourceId='com.hexin.plat.android:id/prompt_content')
        scroll_content= self.d(className='//android.widget.TextView)[3]')  # 可用资金不足是[3]
        # scroll_content_enougth= self.d(className='//android.widget.TextView)')  # 可用资金不足是[3]
        scroll_content_enougth= self.d.xpath('//*[@text="委托数量不符合交易规则。 A股最少买入100股，买入数量为100及其整数倍； '
                                             '可转债最少买入10张，买入数量为10及其整数倍； 可转债以外的债券最少买入1000张，买入数量为1000及其整数倍； '
                                             '科创板最少买入200股，后续买入允许1股增加，即201股下单；更多疑问请客服咨询委托数量。"]')
        # content_scroll= self.d(resourceId='com.hexin.plat.android:id/content_scroll')
        # confirm_button= self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        confirm_button= self.d.xpath('//*[@resource-id="com.hexin.plat.android:id/ok_btn"]')
        confirm_button_second= self.d(resourceId="com.hexin.plat.android:id/left_btn")
        sell_confirm_button= self.d(resourceId='com.hexin.plat.android:id/left_btn', text='确定')

        # 处理买入成功提交的情况
        if '委托买入确认' in dialog_title.get_text():
            logger.info("检测到'委托买入确认'提示")
            confirm_button.click()
            confirm_button.click()
            logger.info("点击确认按钮")
            if scroll_content_enougth.exists:#可删除，逻辑已前置
                error_info = scroll_content_enougth.get_text()
                # if '买入最少100股' in scroll_content_enougth.get_text():
                #     logger.info("检测到'买入最少100股'提示")
                confirm_button_second.click()
                # confirm_button.click()

                logger.info("点击确认按钮")
                # send_notification(f"买入失败，{error_info}")
                logger.error(f"失败，{error_info}")
                return False, f"失败，{error_info}"

            logger.info("委托已提交")
            return True, "委托已提交"

        else:
            if prompt_content.exists:
                error_info = prompt_content.get_text()
                confirm_button.click()
            elif scroll_content.exists:
                error_info = scroll_content.get_text()
                confirm_button.click()
            else:
                error_info = "未知错误"
                # confirm_button.click()

            return False, f"{error_info}"

        # # 处理卖出操作的特殊情况
        # elif dialog_title"].exists:
        #     logger.info("检测到对话框标题，执行卖出确认")
        #     self.dialog_sell_confirm()
        #     return True, "卖出操作成功"

        # # 处理需要转入资金的情况
        # elif transfer_funds.exists:
        #     logger.info("检测到'转入资金'提示")
        #     info = scroll_content.get_text() if scroll_content.exists else "未知错误"
        #     confirm_button.click()
        #     logger.info(f"失败,{info}")
        #     return False, info

        # # 处理委托数量为0的情况
        # elif volume_zero"].exists:
        #     info = volume_zero"].get_text()
        #     logger.info(f"检测到'委托数量必须大于0'提示: {info}")
        #     confirm_button"].click()
        #     logger.info("点击确认按钮")
        #     logger.info(f"失败,{info}")
        #     return False, info

        # # 处理滚动内容的错误信息
        # elif scroll_content"].exists:
        #     info = scroll_content"].get_text()
        #     logger.info(f"检测到滚动内容错误信息: {info}")
        #     confirm_button"].click()
        #     logger.info("点击确认按钮")
        #     logger.info(f"失败,{info}")
        #     return False, info


        # 处理其他未预见的弹窗
        # try:
        #     if prompt_content.exists:
        #         info = prompt_content.get_text()
        #         logger.info(f"检测到其他提示信息: {info}")
        #         self.dialog_confirm()
        #         logger.info(f"失败,{info}")
        #         return False, info
        #     else:
        #         logger.info("未找到任何对话框")
        #         return False, "未找到任何对话框"
        # except UiObjectNotFoundError:
        #     logger.warning("找不到预期的弹窗元素")
        #     return False, "弹窗识别异常"

    # def confirm_transaction(self):
    #     """点击确认按钮并处理可能出现的弹窗"""
    #     logger.info("点击交易确认按钮")
    #     # 尝试点击确认按钮
    #     try:
    #         dialog_info = self.d(className='android.widget.Button')[1]
    #         if dialog_info.exists:
    #             dialog_info.click()
    #             logger.info("点击确认按钮成功")
    #         else:
    #             logger.warning("确认按钮不存在")
    #     except UiObjectNotFoundError:
    #         logger.warning("找不到确认按钮")

    def buy_stock(self, stock_name, volume=None):
        try:
            self._current_stock_name = stock_name
            self.click_trade_entry()
            self.buy_entry()
            self.search_stock(stock_name)

            success, msg, calculate_volume = self._calculate_volume('买入')
            if not success:
                logger.warning(f"买入失败: {msg}")
                return False, msg

            if volume is None:
                volume = calculate_volume
                logger.info(f"开始买入流程 {stock_name}  {volume}股")
            else:
                logger.info(f"开始买入流程 {stock_name}  {volume}股")

            self.input_volume(int(volume))
            self.click_button_by_text('买 入')
            success, info = self.dialog_handle()
            self.click_holding_stock()
            self.click_refresh_button()
            # #点击持仓按钮(text='持仓‘），执行‘账户持仓信息.py’文件 '//*[@text="持仓"]
            # refresh_button = self.d(resourceId="com.hexin.plat.android:id/refresh_img")
            # refresh_button.click()
            update_holding_info()
            # time.sleep(1)
            self.click_back()
            return success, info
        except Exception as e:
            logger.error(f"买入 {stock_name} {volume} 股失败: {e}", exc_info=True)
            return False, f"买入 {stock_name} {volume} 股失败: {e}"

    def sell_stock(self, stock_name, new_ratio=None):
        try:
            self._current_stock_name = stock_name

            # 先检查持仓情况
            holding_stock_df = pd.read_excel(Account_holding_stockes_info_file, sheet_name="持仓数据")
            holding_stock = holding_stock_df[holding_stock_df['标的名称'] == stock_name]

            if holding_stock.empty:
                logger.warning(f"{stock_name} 不在持仓列表中")
                return False, f"{stock_name} 不在持仓列表中"

            available = int(holding_stock['持仓/可用'].str.split('/').str[1].iloc[0])
            if available <= 0:
                logger.warning(f"{stock_name} 可用数量为0，无法卖出")
                return False, f"{stock_name} 可用数量为0，无法卖出"

            # 根据 new_ratio 决定卖出数量
            quantity = self._calculate_volume("卖出", new_ratio=new_ratio)
            if not quantity:
                return False, f"计算卖出数量失败"

            logger.info(f"开始卖出流程 {stock_name} {quantity}股")

            self.click_trade_entry()
            self.sell_entry()
            self.search_stock(stock_name)

            self.click_button_by_text('卖 出')
            time.sleep(1)
            success, info = self.dialog_handle()
            time.sleep(1)
            self.click_holding_stock()
            self.click_refresh_button()
            update_holding_info()

            self.click_back()
            return success, info

        except Exception as e:
            logger.error(f"卖出 {stock_name} 股失败: {e}", exc_info=True)
            return False, f"卖出 {stock_name} 股失败: {e}"
        #

if __name__ == '__main__':
    d = uiautomator2.connect()
    pom = THSPage(d)
    pom.get_price_by_volume()
#     # pom.sell_stock('中国电信','半仓')
#     pom.sell_stock('英维克','半仓')
