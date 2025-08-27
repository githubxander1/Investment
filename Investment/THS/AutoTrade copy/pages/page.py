# page.py
import time

import uiautomator2
import uiautomator2 as u2

from Investment.THS.AutoTrade.pages.page_common import CommonPage
# from Investment.THS.AutoTrade.pages.page_guozhai import GuozhaiPage
# from Demos.RegCreateKeyTransacted import classname

from Investment.THS.AutoTrade.pages.account_info import AccountInfo
# from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import THS_AUTO_TRADE_LOG_FILE_PAGE

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_PAGE)

common_page = CommonPage()
account_info =  AccountInfo()
# trader = TradeLogic()
# d = u2.connect()
class THSPage:

    def __init__(self, d):
        self.d = d
        self.d.implicitly_wait(20)
        self._current_stock_name = None  # 新增用于保存当前股票名称
        self._current_account = None
        self._current_page = None

        # back_button = self.d('com.hexin.plat.android:id/title_bar_left_container')
        self.trade_button_entry = self.d(resourceId="com.hexin.plat.android:id/menu_holdings_image")
        # self.trade_button_entry = self.d(className="android.widget.RelativeLayout")[24]
        self.back_button = self.d(resourceId='com.hexin.plat.android:id/title_bar_left_container')

        self.moni = self.d(resourceId="com.hexin.plat.android:id/tab_mn")
        self.Agu = self.d(resourceId="com.hexin.plat.android:id/tab_a")
        self.current_account = self.d(resourceId="com.hexin.plat.android:id/page_title_view")

        # 账户页
        self.keyong = self.d(resourceId="com.hexin.plat.android:id/capital_cell_title")[4]
        self.current_text = self.d(resourceId="com.hexin.plat.android:id/currency_text", text="人民币账户 A股")
        self.share_button = self.d(resourceId="com.hexin.plat.android:id/share_container")
        self.search_button = self.d(resourceId="com.hexin.plat.android:id/search_container")

        # 国债
        self.back_button = self.d(resourceId="com.hexin.plat.android:id/title_bar_img")
        self.confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        self.prompt_content = self.d(resourceId="com.hexin.plat.android:id/prompt_content")
        # self.ths = THSPage(d)

        self.guozhai_entry_button = self.d(resourceId="com.hexin.plat.android:id/title_right_image")[1]
        self.guozhailist_assert_button = self.d(text="我要回购")

        self.borrow_btn = self.d(resourceId="com.hexin.plat.android:id/btn_jiechu")

        # 弹窗
        self.diolog_title = self.d(resourceId="com.hexin.plat.android:id/dialog_title")

        self.content_layout = self.d(resourceId="com.hexin.plat.android:id/content_layout")


    def click_back(self):
        back_button = self.d(resourceId='com.hexin.plat.android:id/title_bar_left_container')
        if back_button.exists:
            back_button.click()
            logger.info("点击返回按钮")
            return True
        else:
            logger.warning("返回按钮未找到")
            return False

    # 交易入口页
    def click_trade_entry(self):
        trade_entry = self.d(resourceId='com.hexin.plat.android:id/title', text='交易')
        if trade_entry.exists:
            trade_entry.click()
            logger.info("点击交易按钮(外)")
            return True
        else:
            logger.warning("交易按钮(外)未找到")
            return False

    def click_holding_stock_entry(self): #持仓-入口处
        operate_entry = self.d(resourceId='com.hexin.plat.android:id/menu_holdings_text', text='持仓')
        if operate_entry.exists:
            operate_entry.click()
            logger.info("点击持仓按钮(外)")
            return True
        else:
            logger.warning("持仓按钮(外)未找到")
            return False

    def click_operate_entry(self,operation):
        """外面入口处的操作按钮"""
        if operation == '买入':
            buy_entry = self.d(resourceId='com.hexin.plat.android:id/menu_buy_text')
            if buy_entry.exists:
                buy_entry.click()
                logger.info("点击买入按钮(外)")
                return True
            else:
                logger.warning("买入按钮(外)未找到")
                return False
        elif operation == '卖出':
            sale_entry = self.d(resourceId='com.hexin.plat.android:id/menu_sale_text')
            if sale_entry.exists:
                sale_entry.click()
                logger.info("点击卖出按钮(外)")
                return True
            else:
                logger.warning("卖出按钮(外)未找到")
                return False
        else:
            raise ValueError("未知操作")

    # 账户页
    def click_holding_stock_button(self): # 持仓-里面
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


    def click_operate_button(self,operation):
        """里面的tab栏"""
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
                logger.warning("买入按钮未找到")
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
                logger.warning("卖出按钮未找到")
                return False
        else:
            raise ValueError("未知操作")

    # def click_submit_button(self,operation):
    #     operation_submit_button = self.d(className='android.widget.TextView', text=operation)
    #     operation_submit_button.click()
    #     logger.info(f'点击 {operation} (提交)')

    def click_refresh_button(self):
        refresh_button = self.d(resourceId='com.hexin.plat.android:id/refresh_container')
        if refresh_button.exists:
            refresh_button.click()
            logger.info("点击刷新按钮")
            return True
        else:
            logger.warning("刷新按钮未找到")
            return False

    def search_stock(self, stock_name):
        stock_search = self.d(resourceId='com.hexin.plat.android:id/content_stock')
        stock_search.click()
        logger.info(f"点击股票搜索框")

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
            # 显式等待搜索结果加载
            recycler_view = self.d(resourceId='com.hexin.plat.android:id/recyclerView')
            if recycler_view.wait(timeout=5):  # 等待最多5秒
                first_item = recycler_view.child(index=0)
                first_item.click()
                logger.info("点击匹配的第一个股票")
                time.sleep(1)
            else:
                logger.warning("未找到搜索结果列表，尝试使用股票代码搜索")
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
                        logger.warning("使用代码搜索仍无法找到匹配项")
                else:
                    logger.warning("无法获取股票代码，跳过点击")

        time.sleep(2)

    def input_volume(self, volume):
        # volumn_input = self.d(className='android.widget.EditText')[3]
        volumn_input = self.d(resourceId="com.hexin.plat.android:id/stockvolume").child(index=0)
        volumn_input.send_keys(volume)
        logger.info(f"输入数量: {volume}手")

    def click_half_volume(self):
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='1/2仓')
        volumn.click()
        logger.info("输入数量: 半仓")

    def click_total_volume(self):
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='全仓')
        volume = self.d(className='android.widget.EditText')[2]
        # logger.info("获取买入数量")
        if volume.get_text() != '0':
            volumn.click()
            logger.info("输入数量: 全仓")
        else:
            pass

    # 输入数量后系统自动计算的金额
    def get_price_by_volume(self):
        price = self.d(resourceId='com.hexin.plat.android:id/couldbuy_volumn').get_text()
        logger.info("获取金额: " + price)
        return price

    def click_submit_button(self, operation):
        if operation == '买入':
            # operate_button = self.d(className='android.widget.TextView', text='买 入')
            #换成包含文本‘买 入’的定位方式
            submit_button = self.d(className='android.widget.TextView', textMatches='.*买 入.*')
        elif operation == '卖出':
            # operate_button = self.d(className='android.widget.TextView', text='卖 出')
            submit_button = self.d(className='android.widget.TextView', textMatches='.*卖 出.*')
        else:
            raise ValueError("Invalid operation")

        # 检查按钮是否存在再点击
        if submit_button.exists:
            submit_button.click()
            logger.info(f"点击按钮: {operation} (提交)")
            return True
        else:
            logger.error(f"提交按钮 {operation} 未找到")
            return False

    def _get_real_price(self):
        """获取当前股票实时价格"""
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
                logger.warning(f"解析价格失败: {e}")
                time.sleep(1)
        raise ValueError("无法获取实时价格")
        # return None

    # def calculate_volume(self, operation: str, real_price=None, buy_available=None, sale_available=None, new_ratio: float = None, ):
    #     """
    #     根据当前持仓和策略动态计算交易数量
    #     :param operation: '买入' 或 '卖出'
    #     :param new_ratio: 新仓位比例（可选）
    #     :param real_price: 实时价格
    #     :param buy_available: 可用资金
    #     :param sale_available: 可卖数量
    #     :return: tuple(success: bool, message: str, volume: int | None)
    #     """
    #     try:
    #         if operation == "买入":
    #             if not real_price:
    #                 return False, "无法获取实时价格", None
    #
    #             if not buy_available:
    #                 return False, "无法获取可用资金", None
    #
    #             volume = trader.calculate_buy_volume(real_price, buy_available)
    #             if not volume:
    #                 return False, "买入数量计算失败", None
    #
    #             logger.info(f"实时价格: {real_price}, 操作数量: {volume}, 共{operation}: {real_price * volume}")
    #             return True, '数量计算成功', volume
    #
    #         elif operation == "卖出":
    #             if not sale_available:
    #                 return False, f'{self._current_stock_name} 没有可用持仓', None
    #
    #             volume = trader.calculate_sell_volume(sale_available, new_ratio)
    #             if not volume:
    #                 return False, "卖出数量计算失败", None
    #
    #             logger.info(f"{operation}数量: {volume} (共可用：{sale_available})")
    #             return True, '数量计算成功', volume
    #
    #         else:
    #             logger.warning("未知操作类型")
    #             return False, '失败', None
    #
    #     except Exception as e:
    #         logger.error(f"数量计算失败: {e}", exc_info=True)
    #         return False, '失败', None

    def dialog_handle(self):
        """处理交易后的各种弹窗情况"""
        logger.info("开始处理弹窗")

        # 定位弹窗相关控件
        dialog_title = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
        prompt_content = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
        prompt_content_second = self.d(className='//android.widget.TextView')[2]
        confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        confirm_button_second = self.d(resourceId="com.hexin.plat.android:id/left_btn") #资金不足时的确定按钮

        try:
            # 处理成功提交的情况
            title_text = dialog_title.get_text() if dialog_title.exists else ""
            if any(keyword in title_text for keyword in ['委托买入确认', '委托卖出确认']):
               logger.info("检测到'委托确认'提示")
               confirm_button.click()
               logger.info("点击确认按钮")

               # 处理委托已提交后的情况
               prompt_text = prompt_content.get_text() if prompt_content.exists else ""
               logger.info(f"提示信息：{prompt_text}")
               if '委托已提交' in prompt_text:
                   confirm_button.click()
                   logger.info("委托已提交")
                   return True, "委托已提交"
               # elif '资金不足提示' in prompt_text:
               #     error_info = prompt_content_second.get_text()
               #     confirm_button_second.click()
               #     logger.warning(error_info)
               #     return False, "可用资金不足"
               else:
                   try:
                       if prompt_content.exists:
                          error_info = prompt_content.get_text()
                       elif prompt_content_second.exists and len(prompt_content_second) > 2:
                          error_info = prompt_content_second[2].get_text()
                       else:
                          error_info = "无提示信息"

                       if confirm_button.exists:
                          confirm_button.click()
                       elif confirm_button_second.exists:
                         confirm_button_second.click()
                       else:
                           logger.warning("未找到确认按钮")
                           return False, "未找到确认按钮"
                   except Exception as e:
                       logger.error(f"点击确认按钮失败: {e}")
                       return False, f"点击确认按钮失败: {e}"

                   logger.warning(error_info)
                   return False, error_info
            else:
                warning_info = "未检测到'委托确认'提示"
                logger.info(warning_info)
                return False, warning_info
        except Exception as e:
            logger.error(f"处理弹窗时发生异常: {e}")
            return False, f"处理弹窗时发生异常: {e}"


    def update_holding_info_all(self):
        """
        点击持仓按钮（里）
        点击刷新
        开始更新
        """
        self.click_holding_stock_button()
        self.click_refresh_button()
        time.sleep(0.5)
        account_info.update_holding_info_all()
        logger.info("更新持仓信息")
    # def ensure_on_account_page(self):
    #     """确保当前在账户页"""
    #     current_page = common_page.where_page()
    #     logger.info(f"当前页面: {current_page}")
    #
    #     # 确保在账户页
    #     if not current_page == "账户页":
    #         if current_page == "首页":
    #             # 如果没有可用按钮，则点击持仓入口
    #             self.trade_button_entry.click()
    #             time.sleep(1)
    #             if not self.search_button.exists:
    #                 print("没有分享按钮")
    #                 self.click_holding_stock_entry()
    #         elif current_page == "交易页":
    #             self.click_holding_stock_entry()
    #         elif current_page == "国债列表页":
    #             self.click_back()
    #         elif current_page == "国债品种页":
    #             self.click_back()
    #             self.click_back()
    #         else:
    #             logger.error("无法返回账户页")
    #             return False
    #         logger.info("已切换至: 账户页")
    #     else:
    #         return True
    # def operate_stock(self, operation, stock_name):
    #     """
    #     确保在账户页
    #     更新账户数据：买入时的可用自己，卖出时的可用数量
    #     且换到买卖tab
    #     搜索标的
    #     获取实时价格
    #     计算数量
    #     提交
    #     发送通知
    #     """
    #     # self.goto_account_page()
    #     self.ensure_on_account_page()
    #     try:
    #         self._current_stock_name = stock_name
    #         account_info = AccountInfo()
    #
    #         # 初始化资金: 可用资金,可卖数量,卖出比例
    #         buy_available = None
    #         sale_available = None
    #         new_ratio = None
    #
    #         self.click_holding_stock_button()
    #         if operation == "买入":
    #             buy_available = account_info.get_buying_power()
    #         else:
    #             stock_exist, sale_available = account_info.get_stock_available(self._current_stock_name)
    #             if not stock_exist:
    #                 error_info = f"{self._current_stock_name} 没有持仓"
    #                 return False, error_info
    #
    #             new_ratio = 10
    #             volume = calculate_sell_volume(sale_available, new_ratio)
    #
    #
    #
    #         # # 点击按钮 买/卖 操作按钮（tab)
    #         self.click_operate_button(operation)
    #         # 搜索股票
    #         self.search_stock(stock_name)
    #
    #         if operation == "买入":
    #             # 获取实时价格
    #             real_price = self._get_real_price()
    #             if not real_price:
    #                 return False, "无法获取实时价格", None
    #
    #             volume = calculate_buy_volume(real_price, buy_available)
    #
    #         # # 计算交易数量
    #         # success, msg, calculate_volume = self.calculate_volume(operation, real_price, buy_available, sale_available, new_ratio)
    #         # if not success:
    #         #     logger.warning(f"{operation} {stock_name} 失败: {msg}")
    #         #     return False, msg
    #         # self.click_submit_button(operation)
    #
    #         # 交易开始，发送通知
    #         # send_notification(f"开始 {operation} 流程 {stock_name}  {calculate_volume}股")
    #
    #         # 输入交易数量
    #         self.input_volume(int(volume))
    #         # 点击提交按钮
    #         self.click_submit_button(operation)
    #         # 处理弹窗
    #         success, info = self.dialog_handle()
    #         # 点击返回
    #         # self.click_back()
    #         # 发送交易结果通知
    #         # send_notification(f"{operation} {stock_name} {calculate_volume}股 {success} {info}")
    #         # if success:
    #         #     time.sleep(1)
    #         #     self.update_holding_info_all()
    #         logger.info(f"{operation} {stock_name} {volume}股 {success} {info}")
    #         return success, info
    #     except Exception as e:
    #         calculate_volume = "未知"
    #         logger.error(f"{operation} {stock_name} {calculate_volume} 股失败: {e}", exc_info=True)
    #         return False, f"{operation} {stock_name} {calculate_volume} 股失败: {e}"

    # def is_on_guozhai_page(self):
    #     return self.d(text="我要回购").exists()
    # def is_on_jiechu_page(self):
    #     return self.d(resourceId="com.hexin.plat.android:id/btn_jie_chu").exists()
    # def is_on_holding_page(self):
    #     return self.d(resourceId="com.hexin.plat.android:id/menu_holdings_text", text="持仓").exists()
    # def is_on_home_page(self):
    #     """判断是否在首页"""
    #     return self.d(resourceId="com.hexin.plat.android:id/tab_mn").exists()
    #
    # def is_on_holding_list_page(self):
    #     """判断是否在持仓列表页"""
    #     return self.d(text="可用").exists()


if __name__ == '__main__':
    pass
    d = uiautomator2.connect()

    # d.screenshot("screenshot1.png")
    ths = THSPage(d)
    ths.click_holding_stock_button()
    # pom.guozhai_operation()
    # if ths.operate_stock('卖出', '东方创业'):
    #     # ths.trade_button_entry.click()
    #     print("True")
    # else:
    #     print("False")
    # pom.trade_button_entry.click()
    # pom.common_page("长城证券")
    # pom.common_page("川财证券")
    # pom.common_page("模拟")
    # ths.ensure_on_account_page()
    # ths.operate_stock("买入", "超讯通讯", 200)
    # print(pom.where_page())
    # pom.get_price_by_volume()
#     # pom.sell_stock('中国电信','半仓')
#     pom.sell_stock('英维克','半仓')
