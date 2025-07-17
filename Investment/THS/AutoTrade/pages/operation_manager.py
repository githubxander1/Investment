from Investment.THS.AutoTrade.scripts.volume_calculate import calculate_buy_volume, calculate_sell_volume
from Investment.THS.AutoTrade.scripts.account_info import get_buying_power, get_stock_available

class TradeOperationManager:
    def __init__(self, ths_page):
        self.ths_page = ths_page

    def execute_buy(self, stock_name):
        """执行买入操作"""
        real_price = self.ths_page.get_real_price()
        buy_available = get_buying_power()

        if not real_price or not buy_available:
            return False, "无法获取价格或可用资金"

        volume = calculate_buy_volume(real_price, buy_available)
        if not volume:
            return False, "买入数量计算失败"

        self.ths_page.input_volume(volume)
        self.ths_page.confirm_operation()
        return True, f"买入 {stock_name} {volume} 股成功"

    def execute_sell(self, stock_name, new_ratio=None):
        """执行卖出操作"""
        sale_available = get_stock_available(stock_name)

        if not sale_available:
            return False, f"{stock_name} 不在持仓中"

        volume = calculate_sell_volume(sale_available, new_ratio)
        if not volume:
            return False, "卖出数量计算失败"

        self.ths_page.input_volume(volume)
        self.ths_page.confirm_operation()
        return True, f"卖出 {stock_name} {volume} 股成功"
