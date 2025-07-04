# page_logic.py
import pandas as pd
import time

import uiautomator2

from Investment.THS.AutoTrade.scripts.account_info import update_holding_info, get_buying_power, get_stock_available
from Investment.THS.AutoTrade.scripts.volume_calculate import calculate_buy_volume, calculate_sell_volume
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import THS_AUTO_TRADE_LOG_FILE_PAGE
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_PAGE)

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
    def click_holding_stock_entry(self):
        operate_entry = self.d(resourceId='com.hexin.plat.android:id/menu_holdings_text', text='持仓')
        operate_entry.click()
        logger.info("点击持仓按钮")
    def click_operate_entry(self,operation):
        if operation == '买入':
            buy_entry = self.d(resourceId='com.hexin.plat.android:id/menu_buy_text')
            buy_entry.click()
            logger.info("点击买入按钮")
        elif operation == '卖出':
            sale_entry = self.d(resourceId='com.hexin.plat.android:id/menu_sale_text')
            sale_entry.click()
            logger.info("点击卖出按钮")
        else:
            raise ValueError("Invalid operation")

    def click_holding_stock_button(self):
        holding_button = self.d(className='android.widget.TextView', text='持仓')
        holding_button.click()
        logger.info("点击持仓按钮")

        # # 等待持仓页面加载完成
        # self.a_hold = self.d(className='android.widget.TextView')[34]
        # if not self.a_hold.wait.exists(timeout=5000):
        #     logger.error("持仓页面加载失败")
        #     return False

    def click_operate_button(self,operation):
        operation_button = self.d(className='android.widget.TextView', text=operation)
        operation_button.click()
        logger.info(f'点击{operation}')

    def click_refresh_button(self):
        refresh_button = self.d(resourceId='com.hexin.plat.android:id/refresh_container')
        refresh_button.click()
        logger.info("点击刷新按钮")

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
        volumn_input = self.d(className='android.widget.EditText')[2]
        volumn_input.send_keys(volume)
        logger.info(f"输入数量: {volume}手")

    def half_volume(self):
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='1/2仓')
        volumn.click()
        logger.info("输入数量: 半仓")

    def total_volume(self):
        volumn = self.d(resourceId='com.hexin.plat.android:id/tv_flashorder_cangwei', text='全仓')
        volume = self.d(className='android.widget.EditText')[2]
        # logger.info("获取买入数量")
        if volume.get_text() != '0':
            volumn.click()
            logger.info("输入数量: 全仓")
        else:
            pass

    # 输入数量后系统自动计算的价格
    def get_price_by_volume(self):
        price = self.d(resourceId='com.hexin.plat.android:id/couldbuy_volumn').get_text()
        logger.info("获取价格: " + price)
        return price

    def click_button_by_operation(self, operation):
        if operation == '买入':
            operate_button = self.d(className='android.widget.TextView', text='买 入')
        elif operation == '卖出':
            operate_button = self.d(className='android.widget.TextView', text='卖 出')
        else:
            raise ValueError("Invalid operation")
        operate_button.click()
        logger.info(f"点击按钮: {operation}")

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

    def _calculate_volume(self, operation: str, new_ratio: float = None):
        """
        根据当前持仓和策略动态计算交易数量
        :param operation: '买入' 或 '卖出'
        :param new_ratio: 新仓位比例（可选）
        :return: tuple(success: bool, message: str, volume: int | None)
        """
        try:
            if operation == "买入":
                real_price = self._get_real_price()
                if not real_price:
                    return False, "无法获取实时价格", None

                self.click_holding_stock_button()
                buy_available = get_buying_power()
                if not buy_available:
                    return False, "无法获取可用资金", None

                volume = calculate_buy_volume(real_price, buy_available)
                if not volume:
                    return False, "买入数量计算失败", None

                logger.info(f"实时价格: {real_price}, 操作数量: {volume}, 共{operation}: {real_price * volume}")
                return True, '数量计算成功', volume

            elif operation == "卖出":
                self.click_holding_stock_button()
                sale_available = get_stock_available(self._current_stock_name)
                if not sale_available:
                    return False, f'{self._current_stock_name} 没有可用持仓', None

                volume = calculate_sell_volume(sale_available, new_ratio)
                if not volume:
                    return False, "卖出数量计算失败", None

                logger.info(f"{operation}数量: {volume} (共可用：{sale_available})")
                return True, '数量计算成功', volume

            else:
                logger.warning("未知操作类型")
                return False, '失败', None

        except Exception as e:
            logger.error(f"数量计算失败: {e}", exc_info=True)
            return False, '失败', None

    # def _calculate_volume(self, operation: str, new_ratio: float = None):
    #     """
    #     根据当前持仓和策略动态计算交易数量
    #     :param operation: '买入' 或 '卖出'
    #     :param new_ratio: 新仓位比例（可选）
    #     :return: tuple(success: bool, message: str, volume: int | None)
    #     """
    #     volume_max = 4500
    #     logger.info('开始计算交易数量....')
    #     try:
    #         if operation == "买入":
    #             '''
    #             最大买入4500元
    #             如果可用金额小于4500，买入数量= 可用金额 / 实时价格
    #             如果可用金额大于4500，买入数量= 4500 / 实时价格
    #             '''
    #             # 只获取表头信息中的可用资金
    #             self.click_holding_stock_button()
    #             header_info = extract_header_info()
    #             if header_info.empty:
    #                 return False, "无法获取账户表头信息", None
    #
    #             buy_available = float(header_info["可用"].iloc[0].replace(',', ''))
    #             logger.info(f"可用金额: {buy_available}")
    #
    #             time.sleep(1)
    #             real_price = self._get_real_price()
    #             if not real_price:
    #                 return False, "无法获取实时价格", None
    #
    #             if buy_available < volume_max:# 如果可用金额小于4500，则使用可用金额
    #                 volume = int(buy_available / real_price)
    #             else:
    #                 volume = int(volume_max / real_price)
    #
    #             volume = (volume // 100) * 100
    #             if volume < 100:
    #                 warning_info = '交易数量不足100股'
    #                 logger.warning(f"{warning_info}")
    #                 return False, warning_info, "交易数量不足100股"  # 返回False表示交易失败
    #             else:
    #                 logger.info(f"实时价格: {real_price}, 操作数量: {volume}, 共{operation}: {real_price * volume}")
    #                 return True, '数量计算成功', volume
    #
    #         elif operation == "卖出":
    #             # 只获取目标股票的持仓信息
    #             self.click_holding_stock_button()
    #             stock_holding = get_stock_holding(self._current_stock_name)
    #             if not stock_holding:
    #                 logger.info(f'{self._current_stock_name} 没有持仓')
    #             else:
    #                 position_available = stock_holding.get("持仓/可用", "")
    #                 # print(f"持仓/可用: {position_available}")
    #                 # print(f"可用为: {position_available}")
    #
    #                 if isinstance(position_available, str):
    #                     parts = position_available.strip().split('/')
    #                     if len(parts) >= 2:
    #                         position = float(parts[0])
    #                         sale_available = float(parts[1])
    #                         logger.info(f"持仓: {position}, 可用: {sale_available}")
    #
    #             if sale_available <= 0:
    #                 warning_info = '无可用数量'
    #                 logger.warning(warning_info)
    #                 return False, warning_info, None
    #
    #             if new_ratio is not None and new_ratio != 0:
    #                 volume = int(sale_available * 0.5)  # 半仓卖出
    #             else:
    #                 volume = sale_available  # 全部卖出
    #
    #             volume = (volume // 100) * 100
    #             if volume < 100:
    #                 warning_info = '卖出数量不足100股'
    #                 logger.warning(warning_info)
    #                 return False, warning_info, None
    #
    #             logger.info(f"{operation}数量: {volume} (共可用：{sale_available})")
    #             return True, '数量计算成功', volume
    #
    #         else:
    #             logger.warning("未知操作类型")
    #             return False, '失败', '未知操作'
    #
    #     except Exception as e:
    #         logger.error(f"数量计算失败: {e}", exc_info=True)
    #         return False, '失败', '数量计算失败'

    def dialog_handle(self):
        """处理交易后的各种弹窗情况"""
        logger.info("开始处理弹窗")
        #弹窗标题里有：委托买入确认
        # submit_success= self.d.xpath('//*[contains(@text,"委托已提交")]')
        # transfer_funds= self.d.xpath('//*[contains(@text,"转入资金")]')

        # 定位弹窗相关控件
        dialog_title = self.d(resourceId='com.hexin.plat.android:id/dialog_title')
        prompt_content = self.d(resourceId='com.hexin.plat.android:id/prompt_content')
        # scroll_content = self.d.xpath('(//android.widget.TextView)[3]')  # 可用资金不足是[3]
        confirm_button = self.d(resourceId="com.hexin.plat.android:id/ok_btn")
        # confirm_button_second = self.d(resourceId="com.hexin.plat.android:id/left_btn")

        # 处理成功提交的情况
        # if dialog_title.exists:
        title_text = dialog_title.get_text()
        if any(keyword in title_text for keyword in ['委托买入确认', '委托卖出确认']):
           logger.info("检测到'委托确认'提示")
           confirm_button.click()
           logger.info("点击确认按钮")

           prompt_text = prompt_content.get_text()
           logger.info(f"提示信息：{prompt_text}")
           if '委托已提交' in prompt_text:
               confirm_button.click()
               logger.info("委托已提交")
               return True, "委托已提交"
           else:
               error_info = prompt_text
               confirm_button.click()
               logger.warning(error_info)
               return False, error_info
        else:
            warning_info = "未检测到'委托确认'提示"
            logger.info(warning_info)
            return False, warning_info

    def update_holding_info(self):
        self.click_holding_stock_button()
        self.click_refresh_button()
        time.sleep(0.5)
        update_holding_info()
        logger.info("更新持仓信息")

    def operate_stock(self,operation, stock_name):
        """交易-持仓(初始化)-买卖操作"""
        try:
            self._current_stock_name = stock_name
            #点击交易入口
            self.click_trade_entry()
            #点击买/卖按钮
            self.click_operate_entry(operation)
            #更新持仓数据
            # 点击持仓按钮
            # self.click_holding_stock_button()
            # 更新持仓数据
            # self.update_holding_info()
            # 搜索股票
            self.search_stock(stock_name)

            # 计算交易数量
            success, msg, calculate_volume = self._calculate_volume(operation)
            if not success:
                logger.warning(f"{operation} {stock_name} 失败: {msg}")
                return False, msg

            # 交易开始，发送通知
            send_notification(f"开始 {operation} 流程 {stock_name}  {calculate_volume}股")

            # 点击买/卖操作按钮
            self.click_operate_button(operation)
            # 输入交易数量
            self.input_volume(int(calculate_volume))
            # 点击交易按钮
            self.click_button_by_operation(operation)
            # 处理弹窗
            success, info = self.dialog_handle()
            # 点击返回
            self.click_back()
            # 发送交易结果通知
            send_notification(f"{operation} {stock_name}  {calculate_volume}股 {success} {info}")
            if success:
                update_holding_info()
            logger.info(f"{operation} {stock_name} {calculate_volume}股 {success} {info}")
            return success, info
        except Exception as e:
            calculate_volume = "未知"
            logger.error(f"{operation} {stock_name} {calculate_volume} 股失败: {e}", exc_info=True)
            return False, f"{operation} {stock_name} {calculate_volume} 股失败: {e}"

if __name__ == '__main__':
    # pass
    d = uiautomator2.connect()
    d.screenshot("screenshot1.png")
    # pom = THSPage(d)
    # pom.get_price_by_volume()
#     # pom.sell_stock('中国电信','半仓')
#     pom.sell_stock('英维克','半仓')
