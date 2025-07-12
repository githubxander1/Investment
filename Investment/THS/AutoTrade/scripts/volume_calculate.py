# trade_utils.py

from Investment.THS.AutoTrade.utils.logger import setup_logger
logger = setup_logger('volume_calculate.log')

VOLUME_MAX_BUY = 5000

def calculate_buy_volume(real_price, buying_power):
    """
    根据可用资金和价格计算买入数量
    :param real_price: 实时价格
    :param buying_power: 可用资金
    :return: 计算出的股数，或 None 表示失败
    """
    try:
        if buying_power is None or real_price is None:
            return None

        volume = int((buying_power if buying_power < VOLUME_MAX_BUY else VOLUME_MAX_BUY) / real_price)
        volume = (volume // 100) * 100  # 对齐100股整数倍
        if volume < 100:
            logger.warning("买入数量不足100股")
            return None
        return volume
    except Exception as e:
        logger.error(f"买入数量计算失败: {e}")
        return None


def calculate_sell_volume(available_shares, new_ratio=None):
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
