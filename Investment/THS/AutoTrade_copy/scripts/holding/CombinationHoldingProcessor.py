import datetime
import os

import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import (
    Combination_holding_file, all_ids, id_to_name, Combination_headers
)
from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.format_data import determine_market

logger = setup_logger(__name__)

class CombinationHoldingProcessor(CommonHoldingProcessor):
    def __init__(self):
        super().__init__(account_name="中泰证券")

    def get_portfolio_holding_data(self, portfolio_id):
        """获取单个组合的持仓数据"""
        url = f"https://t.10jqka.com.cn/portfolio/relocate/user/getPortfolioHoldingData?id={portfolio_id}"
        headers = Combination_headers

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            positions = data["result"]["positions"]

            holding_data = []
            for position in positions:
                code = str(position.get("code", "")).zfill(6)
                holding_data.append({
                    "策略名称": id_to_name.get(portfolio_id, f'组合{portfolio_id}'),
                    "操作": '买入',
                    "标的名称": position.get("name", ""),
                    "代码": code,
                    "最新价": position["price"],
                    "新比例%": position.get("positionRealRatio", 0) * 100,
                    "市场": determine_market(code),
                    "成本价": position["costPrice"],
                    "收益率(%)": position.get("incomeRate", 0) * 100,
                    "盈亏比例(%)": position.get("profitLossRate", 0) * 100,
                    "时间": datetime.datetime.now().strftime('%Y-%m-%d')
                })

            return pd.DataFrame(holding_data)

        except requests.exceptions.RequestException as e:
            logger.error(f"请求组合{id}持仓数据失败: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"处理组合{id}持仓数据时出错: {e}")
            return pd.DataFrame()


if __name__ == '__main__':
    processor = CombinationHoldingProcessor()
    success = processor.execute_combination_trades()
    if not success:
        # logger.info("✅ 组合策略调仓执行完成")
    # else:
        logger.error("❌ 组合策略调仓执行失败")
