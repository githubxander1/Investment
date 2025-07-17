from Investment.THS.AutoTrade.pages.page_logic import THSPage
from Investment.THS.AutoTrade.scripts.account_info import AccountInfo

import uiautomator2 as u2

from Investment.THS.AutoTrade.scripts.volume_calculate import calculate_sell_volume, calculate_buy_volume
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger('trade.log')

class TradeLogic:
    def __init__(self, account):
        self.d = u2.connect()
        self.account = AccountInfo()
        self.ths_page = THSPage(self.d)


    def buy_volume(self, operation,stock_name):
        # 1. 可用资金
        available_funds = self.account.get_buying_power()

        # 2. 买入
        # 这里假设有一个买入函数
        self.ths_page.click_operate_button(operation)

        # 3. 搜索股票
        self.ths_page.search_stock(stock_name)

        # 4. 实时价格
        real_time_price = self.ths_page._get_real_price()

        # 5. 计算数量-买（可用资金 实时价格）
        volume = self.calculate_buy_volume(available_funds, real_time_price)
        if volume <= 100:
            return "不足100股，跳过"

        # 执行实际购买
        # result = self.account.execute_buy(stock_name, volume)
        return volume

    def calculate_buy_volume(self, funds, price):
        return int(funds / price)

    def sell_volume(self, operation, stock_name, ratio=0):
        # 1. 持仓可用
        stock_exist,available_positions = self.account.get_stock_available(stock_name)

        # 2. 卖出
        self.ths_page.click_operate_button(operation)

        # 3. 是否持仓
        if not stock_exist:
            error_info = f"{stock_name} 未持仓"
            return False, error_info

        # 4. 计算数量-卖（持仓可用 比例）
        volume = self.calculate_sell_volume(available_positions, ratio)

        # 执行实际卖出
        # result = self.account.execute_sell(stock_name, volume)
        return volume

    def calculate_sell_volume(self, positions, ratio):
        if ratio == 0:
            return positions
        else:
            return positions // 2

    # def submit_trade(self, stock_code, volume, action):
    #     # 输入数量
    #     # 点击提交
    #     if action == 'buy':
    #         result = self.buy_logic(stock_code)
    #     elif action == 'sell':
    #         result = self.sell_logic(stock_code)
    #     else:
    #         result = "Invalid action."
    #
    #     # 通知结果
    #     self.notify_result(result)
    #     return result
    #
    # def notify_result(self, result):
    #     # 通知结果的逻辑
    #     pass
    def operate_stock(self, operation, stock_name):
        """
        确保在账户页
        更新账户数据：买入时的可用自己，卖出时的可用数量
        且换到买卖tab
        搜索标的
        获取实时价格
        计算数量
        提交
        发送通知
        """
        # self.goto_account_page()
        self.ths_page.ensure_on_account_page()
        try:
            self._current_stock_name = stock_name
            account_info = AccountInfo()

            # 初始化资金: 可用资金,可卖数量,卖出比例
            buy_available = None
            sale_available = None
            new_ratio = None

            self.ths_page.click_holding_stock_button()
            if operation == "买入":
                buy_available = account_info.get_buying_power()
            else:
                stock_exist, sale_available = account_info.get_stock_available(self._current_stock_name)
                if not stock_exist:
                    error_info = f"{self._current_stock_name} 没有持仓"
                    return False, error_info

                new_ratio = 10
                volume = calculate_sell_volume(sale_available, new_ratio)



            # # 点击按钮 买/卖 操作按钮（tab)
            self.ths_page.click_operate_button(operation)
            # 搜索股票
            self.ths_page.search_stock(stock_name)

            if operation == "买入":
                # 获取实时价格
                real_price = self.ths_page._get_real_price()
                if not real_price:
                    return False, "无法获取实时价格", None

                volume = calculate_buy_volume(real_price, buy_available)

            # # 计算交易数量
            # success, msg, calculate_volume = self._calculate_volume(operation, real_price, buy_available, sale_available, new_ratio)
            # if not success:
            #     logger.warning(f"{operation} {stock_name} 失败: {msg}")
            #     return False, msg
            # self.click_submit_button(operation)

            # 交易开始，发送通知
            # send_notification(f"开始 {operation} 流程 {stock_name}  {calculate_volume}股")

            # 输入交易数量
            self.ths_page.input_volume(int(self.ths_page.volume))
            # 点击提交按钮
            self.ths_page.click_submit_button(operation)
            # 处理弹窗
            success, info = self.ths_page.dialog_handle()
            # 点击返回
            # self.click_back()
            # 发送交易结果通知
            # send_notification(f"{operation} {stock_name} {calculate_volume}股 {success} {info}")
            # if success:
            #     time.sleep(1)
            #     self.update_holding_info_all()
            logger.info(f"{operation} {stock_name} {self.volume}股 {success} {info}")
            return success, info
        except Exception as e:
            calculate_volume = "未知"
            logger.error(f"{operation} {stock_name} {calculate_volume} 股失败: {e}", exc_info=True)
            return False, f"{operation} {stock_name} {calculate_volume} 股失败: {e}"
