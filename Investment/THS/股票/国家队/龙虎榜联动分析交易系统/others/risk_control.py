class RiskManager:
    def __init__(self, max_position=0.1, stop_loss=0.05, take_profit=0.1):
        self.max_position = max_position  # 最大单笔仓位比例
        self.stop_loss = stop_loss        # 止损比例
        self.take_profit = take_profit    # 止盈比例

    def check_stop_loss(self, current_price, buy_price):
        if (buy_price - current_price) / buy_price >= self.stop_loss:
            return True
        return False

    def check_take_profit(self, current_price, buy_price):
        if (current_price - buy_price) / buy_price >= self.take_profit:
            return True
        return False

    def get_position_size(self, account_value, price):
        size = int((account_value * self.max_position) // price)
        return size
