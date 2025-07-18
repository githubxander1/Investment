from Investment.THS.AutoTrade.pages.page import THSPage
from Investment.THS.AutoTrade.pages.account_info import AccountInfo

import uiautomator2 as u2

# from Investment.THS.AutoTrade.scripts.volume_calculate import calculate_sell_volume, calculate_buy_volume
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.pages.page_common import CommonPage

logger = setup_logger('trade.log')
common_page = CommonPage()

class TradeLogic:
    def __init__(self):
        self.d = u2.connect()
        self.account = AccountInfo()
        self.ths_page = THSPage(self.d)
        self._current_stock_name = None
        self.VOLUME_MAX_BUY = 5000

    def calculate_buy_volume(self, real_price, buying_power):
        """
        根据可用资金和价格计算买入数量
        :param real_price: 实时价格
        :param buying_power: 可用资金
        :return: 计算出的股数，或 None 表示失败
        """
        try:
            if buying_power is None or real_price is None:
                return None

            volume = int((buying_power if buying_power < self.VOLUME_MAX_BUY else self.VOLUME_MAX_BUY) / real_price)
            volume = (volume // 100) * 100  # 对齐100股整数倍
            if volume < 100:
                logger.warning("买入数量不足100股")
                return None
            return volume
        except Exception as e:
            logger.error(f"买入数量计算失败: {e}")
            return None

    def calculate_sell_volume(self, available_shares, new_ratio=None):
        """
        根据可用数量和策略比例计算卖出数量
        :param available_shares: 可卖数量
        :param new_ratio: 新仓位比例（可选）
        :return: 卖出数量，或 None 表示失败
        """
        try:
            if available_shares <= 0:
                logger.warning("无可用数量")
                return None

            if new_ratio is not None and new_ratio != 0:
                volume = int(available_shares * 0.5)  # 半仓卖出
            else:
                volume = available_shares  # 全部卖出

            volume = (volume // 100) * 100
            if volume < 100:
                logger.warning("卖出数量不足100股")
                return None

            return volume
        except Exception as e:
            logger.error(f"卖出数量计算失败: {e}")
            return None

    def buy_volume(self, operation,stock_name):
        # 1. 可用资金
        available_funds = self.account.get_buying_power()

        # 2. 买入
        self.ths_page.click_operate_button(operation)

        # 3. 搜索股票
        self.ths_page.search_stock(stock_name)

        # 4. 实时价格
        real_time_price = self.ths_page._get_real_price()

        # 5. 计算数量-买（可用资金 实时价格）
        volume = self.calculate_buy_volume(available_funds, real_time_price)
        return volume

    def sell_volume(self, operation, stock_name, ratio=0):
        # 1. 持仓可用
        stock_exist, available_positions = self.account.get_stock_available(stock_name)

        # 2. 卖出
        self.ths_page.click_operate_button(operation)

        # 3. 是否持仓
        if not stock_exist:
            error_info = f"{stock_name} 未持仓"
            return False, error_info

        # 4. 计算数量-卖（持仓可用 比例）
        volume = self.calculate_sell_volume(available_positions, ratio)
        return volume

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
        # self.ths_page.ensure_on_account_page()
        common_page.goto_account_page()
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
                volume = self.calculate_sell_volume(sale_available, new_ratio)


            # # 点击按钮 买/卖 操作按钮（tab)
            self.ths_page.click_operate_button(operation)
            # 搜索股票
            self.ths_page.search_stock(stock_name)

            if operation == "买入":
                # 获取实时价格
                real_price = self.ths_page._get_real_price()
                if not real_price:
                    return False, "无法获取实时价格", None

                volume = self.calculate_buy_volume(real_price, buy_available)

            # 输入交易数量
            self.ths_page.input_volume(int(volume))
            # 点击提交按钮
            self.ths_page.click_submit_button(operation)
            # 处理弹窗
            success, info = self.ths_page.dialog_handle()
            # 点击返回
            # self.click_back()
            # 发送交易结果通知
            send_notification(f"{operation} {stock_name} {volume}股 {success} {info}")
            # if success:
            #     time.sleep(1)
            #     self.update_holding_info_all()
            logger.info(f"{operation} {stock_name} {volume}股 {success} {info}")
            return success, info
        except Exception as e:
            calculate_volume = "未知"
            logger.error(f"{operation} {stock_name} {calculate_volume} 股失败: {e}", exc_info=True)
            return False, f"{operation} {stock_name} {calculate_volume} 股失败: {e}"

if __name__ == '__main__':
    trader = TradeLogic()
    trader.operate_stock('卖出', '工商银行')