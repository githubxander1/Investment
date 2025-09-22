import datetime
import os
import traceback
from pprint import pprint

import pandas as pd
import requests
from fake_useragent import UserAgent

from Investment.THS.AutoTrade.config.settings import (
    Combination_headers, id_to_name, Combination_holding_file,
    Account_holding_file
)
from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger("combination_holding_processor.log")

ua = UserAgent()

# 策略名称到组合ID的映射
STRATEGY_TO_COMBINATION_ID = {
    '逻辑为王': '9800',    # 对应中山证券
    '一枝梨花': '20811'    # 对应中泰证券
}

# 账户到策略的映射
ACCOUNT_TO_STRATEGY = {
    '中山证券': '逻辑为王',
    '中泰证券': '一枝梨花'
}


def determine_market(code):
    """根据股票代码确定市场"""
    if code.startswith('6') or code.startswith('5'):
        return '沪A'
    elif code.startswith(('0', '3', '15', '16')):
        return '深A'
    elif code.startswith(('4', '8')):
        return '北交所'
    else:
        return '未知'


def save_to_operation_history_excel(new_data, file_path, sheet_name, index=False):
    """保存数据到Excel文件"""
    all_sheets_data = {}
    if os.path.exists(file_path):
        with pd.ExcelFile(file_path, engine='openpyxl') as xls:
            existing_sheets = xls.sheet_names
            for sheet in existing_sheets:
                all_sheets_data[sheet] = pd.read_excel(xls, sheet_name=sheet)

    all_sheets_data[sheet_name] = new_data

    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        for sheet_name, df in all_sheets_data.items():
            df.to_excel(writer, index=index, sheet_name=sheet_name)


class CombinationHoldingProcessor(CommonHoldingProcessor):
    def __init__(self):
        super().__init__(account_name="中山证券")  # 默认账户设为中山证券

    # 获取单个组合的持仓数据
    def get_single_holding_data(self, portfolio_id):
        """获取单个组合的持仓数据"""
        url = f"https://t.10jqka.com.cn/portfolio/relocate/user/getPortfolioHoldingData?id={portfolio_id}"
        headers = Combination_headers

        # 实现重试机制和超时处理
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=10)  # 增加超时设置
                response.raise_for_status()

                data = response.json()
                # pprint(data)

                # 检查返回数据是否有效
                if not isinstance(data, dict) or "result" not in data or "positions" not in data["result"]:
                    logger.warning(f"组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})返回数据格式异常: {data}")
                    if attempt == max_retries - 1:
                        return pd.DataFrame()
                    continue

                positions = data["result"]["positions"]

                # 检查是否有持仓数据
                if not positions:
                    logger.info(f"组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})当前无持仓")
                    return pd.DataFrame()

                holding_data = []
                for position in positions:
                    # 数据验证
                    if not isinstance(position, dict):
                        logger.warning(f"组合{portfolio_id}中的持仓数据格式异常: {position}")
                        continue

                    code = str(position.get("code", "")).zfill(6)
                    holding_data.append({
                        "名称": id_to_name.get(portfolio_id, f'组合{portfolio_id}'),
                        # "操作": '买入',
                        "标的名称": position.get("name", ""),
                        "代码": code,
                        "最新价": position.get("price", 0),
                        "新比例%": position.get("positionRealRatio", 0) * 100,
                        "市场": determine_market(code),
                        "成本价": position.get("costPrice", 0),
                        "收益率(%)": position.get("incomeRate", 0) * 100,
                        "盈亏比例(%)": position.get("profitLossRate", 0) * 100,
                        "时间": datetime.datetime.now().strftime('%Y-%m-%d')
                    })

                result_df = pd.DataFrame(holding_data)
                logger.debug(f"成功获取组合{portfolio_id}的持仓数据，共{len(result_df)}条")
                return result_df

            except requests.exceptions.RequestException as e:
                logger.error(f"请求组合{portfolio_id}持仓数据失败: {e}")
                if attempt == max_retries - 1:
                    return pd.DataFrame()
            except Exception as e:
                logger.error(f"处理组合{portfolio_id}持仓数据时出错: {e}")
                if attempt == max_retries - 1:
                    return pd.DataFrame()

        return pd.DataFrame()

    def save_all_combination_holding_data(self):
        """
        获取所有组合的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
        """
        all_holdings = []
        for id in STRATEGY_TO_COMBINATION_ID.values():  # 只处理映射中的组合
            positions_df = self.get_single_holding_data(id)
            # 只保留沪深A股的
            if not positions_df.empty and '市场' in positions_df.columns:
                positions_df = positions_df[positions_df['市场'].isin(['沪A', '深A'])]
            logger.info(f"组合{id}持仓数据:{len(positions_df)}\n{positions_df}")
            if positions_df is not None and not positions_df.empty:
                all_holdings.append(positions_df)
            else:
                logger.info(f"没有获取到组合数据，组合ID: {id}")

        today = str(datetime.date.today())
        if not all_holdings:
            logger.warning("未获取到任何组合持仓数据")
            return

        all_holdings_df = pd.concat(all_holdings, ignore_index=True)

        file_path = Combination_holding_file

        # 创建一个字典来存储所有工作表数据
        all_sheets_data = {}

        try:
            # 如果文件存在，读取现有数据
            if os.path.exists(file_path):
                with pd.ExcelFile(file_path, engine='openpyxl') as xls:
                    existing_sheets = xls.sheet_names

                    # 读取除当天以外的其他工作表
                    for sheet_name in existing_sheets:
                        if sheet_name != today:
                            all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

            # 添加当天的数据
            all_sheets_data[today] = all_holdings_df

            # 写入所有数据到Excel文件
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                for sheet_name, df in all_sheets_data.items():
                    df.to_excel(writer, index=False, sheet_name=sheet_name)

            logger.info(f"✅ 所有组合持仓数据已保存至 {file_path}")
            return True

        except Exception as e:
            logger.error(f"❌ 保存组合持仓数据失败: {e}")
            send_notification(f"❌ 保存组合持仓数据失败: {e}")
            return False


    def execute_combination_trades(self):
        """
        执行组合策略调仓操作
        """
        try:
            logger.info("🚀 开始执行组合策略调仓操作...")

            # 1. 获取并保存最新的组合持仓数据
            self.save_all_combination_holding_data()

            # 2. 为中山证券和中泰证券分别执行交易
            for account_name, strategy_name in ACCOUNT_TO_STRATEGY.items():
                logger.info(f"🔄 处理账户 {account_name} 对应的策略 {strategy_name}")
                
                # 获取对应的组合ID
                combination_id = STRATEGY_TO_COMBINATION_ID.get(strategy_name)
                if not combination_id:
                    logger.error(f"未找到策略 {strategy_name} 对应的组合ID")
                    continue

                # 获取该组合的持仓数据
                combination_data = self.get_single_holding_data(combination_id)
                
                if combination_data.empty:
                    logger.info(f"策略 {strategy_name} 当前无持仓数据")
                    continue

                # 设置当前账户
                self.account_name = account_name
                
                # 执行交易操作
                success = self.operate_strategy(
                    Account_holding_file,
                    account_name,
                    Combination_holding_file,
                    strategy_name
                )

                if success:
                    logger.info(f"✅ 账户 {account_name} 对应的策略 {strategy_name} 调仓执行完成")
                    send_notification(f"✅ 账户 {account_name} 对应的策略 {strategy_name} 调仓执行完成")
                else:
                    error_msg = f"❌ 账户 {account_name} 对应的策略 {strategy_name} 调仓执行失败"
                    logger.error(error_msg)
                    send_notification(error_msg)

            logger.info("🎉 组合策略调仓任务完成")
            return True

        except Exception as e:
            error_msg = f"执行组合策略调仓操作时出错: {e}\n{traceback.format_exc()}"
            logger.error(error_msg)
            send_notification(error_msg)
            return False



if __name__ == '__main__':
    processor = CombinationHoldingProcessor()
    success = processor.execute_combination_trades()
    if success:
        logger.info("🎉 组合策略调仓任务成功完成")
    else:
        logger.error("❌ 组合策略调仓任务失败")