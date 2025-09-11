import os
import datetime
import traceback
from pprint import pprint

import fake_useragent
import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import (
    Strategy_id_to_name, Strategy_ids, Ai_Strategy_holding_file,
    Strategy_portfolio_today_file, OPERATION_HISTORY_FILE, Account_holding_file
)
from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.format_data import determine_market, normalize_time

logger = setup_logger(__name__)
ua = fake_useragent.UserAgent()

class StrategyHoldingProcessor(CommonHoldingProcessor):
    def __init__(self):
        super().__init__(account_name="川财证券")

    def get_latest_position(self, strategy_id):
        """获取单个策略的最新持仓数据"""
        url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit?strategyId={strategy_id}"
        headers = {"User-Agent": ua.random}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = data.get('result', {})
            position_stocks = result.get('positionStocks', [])

            position_stocks_results = []
            for position_stock_info in position_stocks:
                stk_code = str(position_stock_info.get('stkCode', '').split('.')[0]).zfill(6)
                position_stocks_results.append({
                    '名称': Strategy_id_to_name.get(strategy_id, f'策略{strategy_id}'),
                    '标的名称': position_stock_info.get('stkName', ''),
                    '代码': stk_code,
                    '市场': determine_market(stk_code),
                    '最新价': round(float(position_stock_info.get('price', 0)), 2),
                    '新比例%': round(float(position_stock_info.get('positionRatio', 0)) * 100, 2),
                    '时间': datetime.datetime.now().strftime('%Y-%m-%d'),
                    '行业': position_stock_info.get('industry', ''),
                })

            position_stocks_df = pd.DataFrame(position_stocks_results)
            return position_stocks_df
        except requests.RequestException as e:
            logger.error(f"请求失败 (Strategy ID: {strategy_id}): {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"处理策略{strategy_id}数据时出错: {e}")
            return pd.DataFrame()

    def save_all_strategy_holding_data(self):
        """
        获取所有策略的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
        """
        all_holdings = []
        for id in Strategy_ids:
            positions_df = self.get_latest_position(id)
            # 只保留沪深A股的
            positions_df = positions_df[positions_df['市场'] == '沪深A股']
            # 按价格从低到高排序
            positions_df = positions_df.sort_values('最新价', ascending=True)
            logger.info(f"{id}持仓数据:{len(positions_df)}\n{positions_df} ")
            if positions_df is not None and not positions_df.empty:
                all_holdings.append(positions_df)
            else:
                logger.info(f"没有获取到策略数据，策略ID: {id}")

        today = str(datetime.date.today())
        if not all_holdings:
            logger.warning("未获取到任何策略持仓数据")
            return

        all_holdings_df = pd.concat(all_holdings, ignore_index=False)
        # 从1开始计数
        all_holdings_df.index = all_holdings_df.index + 1

        file_path = Ai_Strategy_holding_file

        # 创建一个字典来存储所有工作表数据
        all_sheets_data = {}

        try:
            # 如果文件存在，读取现有数据
            if os.path.exists(file_path):
                with pd.ExcelFile(file_path) as xls:
                    existing_sheets = xls.sheet_names
                    logger.info(f"保存前文件中已存在的工作表: {file_path}\n{existing_sheets}")

                # 读取除今天以外的所有现有工作表
                with pd.ExcelFile(file_path) as xls:
                    for sheet_name in existing_sheets:
                        if sheet_name != today:
                            all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

            # 将今天的数据放在第一位
            all_sheets_data = {today: all_holdings_df, **all_sheets_data}
            logger.info(f"即将保存的所有工作表: {list(all_sheets_data.keys())}")

            # 写入所有数据到Excel文件（覆盖模式），注意不保存索引
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                for sheet_name, df in all_sheets_data.items():
                    logger.info(f"正在保存工作表: {sheet_name}")
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            logger.info(f"✅ 所有持仓数据已保存，{today} 数据位于第一个 sheet，共 {len(all_holdings_df)} 条")

        except Exception as e:
            logger.error(f"❌ 保存持仓数据失败: {e}")
            # 如果出错，至少保存今天的数据
            try:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    all_holdings_df.to_excel(writer, sheet_name=today, index=False)
                logger.info(f"✅ 文件保存完成，sheet: {today}")
            except Exception as e2:
                logger.error(f"❌ 保存今日数据也失败了: {e2}")

    def execute_strategy_trades(self):
        """执行AI策略的调仓操作"""
        try:
            # 保存最新持仓数据
            self.save_all_strategy_holding_data()

            # 执行调仓操作
            success = self.operate_result(
                holding_file=Ai_Strategy_holding_file,
                portfolio_today_file=Strategy_portfolio_today_file,
                account_name="川财证券"
            )

            return success
        except Exception as e:
            logger.error(f"执行AI策略调仓操作时出错: {e}")
            return False

if __name__ == '__main__':
    processor = StrategyHoldingProcessor()
    success = processor.execute_strategy_trades()
    if success:
        logger.info("✅ AI策略调仓执行完成")
    else:
        logger.error("❌ AI策略调仓执行失败")
