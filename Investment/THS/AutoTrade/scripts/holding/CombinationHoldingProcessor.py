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
                    "名称": id_to_name.get(portfolio_id, f'组合{portfolio_id}'),
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
            logger.error(f"请求组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})持仓数据失败: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"处理组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})持仓数据时出错: {e}")
            return pd.DataFrame()

    def save_all_combination_holding_data(self):
        """
        获取所有组合的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
        保持索引，从1开始
        """
        logger.info("📂 开始获取并保存所有组合持仓数据")
        
        # 获取所有组合的持仓数据
        all_holdings = []
        for id in all_ids:
            positions_df = self.get_portfolio_holding_data(id)
            # 索引从1开始
            # positions_df = positions_df.reset_index(drop=True)
            positions_df.index = positions_df.index + 1

            # 只保留沪深A股的
            positions_df = positions_df[positions_df['市场'] == '沪深A股']
            # 按价格从低到高排序
            positions_df = positions_df.sort_values('最新价', ascending=True)
            
            if positions_df is not None and not positions_df.empty:
                logger.info(f"📊 组合{id}({id_to_name.get(str(id), '未知组合')})持仓数据:{len(positions_df)}条")
                logger.debug(f"\n{positions_df}")
                all_holdings.append(positions_df)
            else:
                logger.info(f"⚠️ 没有获取到组合{id}({id_to_name.get(str(id), '未知组合')})的持仓数据")

        today = str(datetime.date.today())
        if not all_holdings:
            logger.warning("❌ 未获取到任何组合持仓数据")
            return

        all_holdings_df = pd.concat(all_holdings, ignore_index=True)
        logger.info(f"📈 总计获取到 {len(all_holdings_df)} 条持仓记录")

        file_path = Combination_holding_file

        # 创建一个字典来存储所有工作表数据
        all_sheets_data = {}

        try:
            # 如果文件存在，读取现有数据
            if os.path.exists(file_path):
                with pd.ExcelFile(file_path) as xls:
                    existing_sheets = xls.sheet_names
                    logger.info(f"💾 保存前文件中已存在的工作表: {existing_sheets}")

                # 读取除今天以外的所有现有工作表
                with pd.ExcelFile(file_path) as xls:
                    for sheet_name in existing_sheets:
                        if sheet_name != today:
                            all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

            # 将今天的数据放在第一位
            all_sheets_data = {today: all_holdings_df, **all_sheets_data}
            logger.info(f"📦 即将保存的所有工作表: {list(all_sheets_data.keys())}")

            # 写入所有数据到Excel文件（覆盖模式），注意不保存索引
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                for sheet_name, df in all_sheets_data.items():
                    logger.info(f"💾 正在保存工作表: {sheet_name} ({len(df)} 条记录)")
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

    def execute_combination_trades(self):
        """执行组合策略的调仓操作"""
        try:
            logger.info("🔄 开始执行组合策略调仓操作")
            
            # 保存最新持仓数据
            self.save_all_combination_holding_data()

            # 执行调仓操作
            from Investment.THS.AutoTrade.config.settings import Combination_portfolio_today_file
            success = self.operate_result(
                holding_file=Combination_holding_file,
                portfolio_today_file=Combination_portfolio_today_file,
                account_name="中泰证券"
            )

            if success:
                logger.info("✅ 组合策略调仓执行完成")
            else:
                logger.error("❌ 组合策略调仓执行失败")
                
            return success
        except Exception as e:
            logger.error(f"执行组合策略调仓操作时出错: {e}")
            return False

if __name__ == '__main__':
    processor = CombinationHoldingProcessor()
    success = processor.execute_combination_trades()
    if success:
        logger.info("🎉 组合策略调仓任务成功完成")
    else:
        logger.error("❌ 组合策略调仓任务失败")