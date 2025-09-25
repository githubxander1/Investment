import datetime
import os
import traceback
from pprint import pprint

import pandas as pd
import requests
from fake_useragent import UserAgent

from Investment.THS.AutoTrade.config.settings import (
    Combination_headers, id_to_name, Combination_holding_file,
    Account_holding_file, Trade_history, Combination_ids
)
from Investment.THS.AutoTrade.pages.account_info import AccountInfo
from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger("combination_holding_processor.log")

ua = UserAgent()

# 策略名称到组合ID的映射
# STRATEGY_TO_COMBINATION_ID = {
#     '逻辑为王': '9800',    # 对应中山证券
#     # '一枝梨花': '20811'    # 对应中泰证券
# }

# 账户到策略的映射
ACCOUNT_TO_STRATEGY = {
    '中山证券': '逻辑为王'
    # '中泰证券': '一枝梨花'
}

# 添加全局变量来跟踪是否需要更新账户数据
account_update_needed = True

# def save_to_operation_history_excel(new_data, file_path, sheet_name, index=False):
#     """保存数据到Excel文件"""
#     all_sheets_data = {}
#     if os.path.exists(file_path):
#         with pd.ExcelFile(file_path, engine='openpyxl') as xls:
#             existing_sheets = xls.sheet_names
#             for sheet in existing_sheets:
#                 all_sheets_data[sheet] = pd.read_excel(xls, sheet_name=sheet)
#
#     all_sheets_data[sheet_name] = new_data
#
#     with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
#         for sheet_name, df in all_sheets_data.items():
#             df.to_excel(writer, index=index, sheet_name=sheet_name)


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
                    code = str(position.get("code", "")).zfill(6)
                    from Investment.THS.AutoTrade.utils.format_data import determine_market
                    holding_data.append({
                        "名称": id_to_name.get(portfolio_id, f'组合{portfolio_id}'),
                        "股票名称": position.get("name", ""),
                        "代码": code,
                        "最新价": position.get("price", 0),
                        "新比例%": round(position.get("positionRealRatio", 0) * 100),
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
        for id in Combination_ids:  # 只处理映射中的组合
            positions_df = self.get_single_holding_data(id)
            # 只保留沪深A股的
            if not positions_df.empty and '市场' in positions_df.columns:
                positions_df = positions_df[positions_df['市场'].isin(['沪深A股'])]
            # logger.info(f"组合{id}持仓数据:{len(positions_df)}\n{positions_df}")
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

            logger.info(f"✅ 所有组合持仓数据已保存至 {file_path}\n{df}")
            return True

        except Exception as e:
            logger.error(f"❌ 保存组合持仓数据失败: {e}")
            send_notification(f"❌ 保存组合持仓数据失败: {e}")
            return False

    def execute_combination_trades(self):
        """执行组合交易"""
        try:
            logger.info("🚀 开始执行组合交易...")

            # 1.更新策略持仓数据
            save_result = self.save_all_combination_holding_data()
            if save_result:
                # 从文件中读取最新保存的数据用于显示
                try:
                    today = str(datetime.date.today())
                    # print(f"今天的日期为:{today} {type(today)}")
                    if os.path.exists(Combination_holding_file):
                        with pd.ExcelFile(Combination_holding_file, engine='openpyxl') as xls:
                            if today in xls.sheet_names:
                                strategy_df = pd.read_excel(xls, sheet_name=today)
                                logger.info(f"✅ 策略持仓数据已更新\n{strategy_df}")
                            else:
                                logger.warning("未找到今日策略持仓数据")
                    else:
                        logger.warning("策略持仓文件不存在")
                except Exception as e:
                    logger.error(f"读取策略持仓数据失败: {e}")
            else:
                logger.error("❌ 保存策略持仓数据失败")

            # 定义账户列表 - 只保留中山证券和中泰证券
            ACCOUNTS = ["中山证券", "中泰证券"]

            # 账户与策略映射关系
            ACCOUNT_STRATEGY_MAP = {
                "中山证券": "逻辑为王"
                # "中泰证券": "一枝梨花"
            }

            # 2.更新账户数据，只更新ACCOUNT_STRATEGY_MAP中的账户
            global account_update_needed
            if account_update_needed:
                logger.info("🔄 开始更新账户数据...")
                account_info = AccountInfo()
                update_success = True

                # 只更新需要的账户
                for account_name in ACCOUNT_STRATEGY_MAP.keys():
                    logger.info(f"正在更新账户 {account_name} 的数据...")
                    account_update_success = account_info.update_holding_info_for_account(account_name)
                    if not account_update_success:
                        logger.warning(f"⚠️ 账户 {account_name} 数据更新失败")
                        update_success = False

                if update_success:
                    logger.info("✅ 所需账户数据更新完成")
                    # 重置更新标志
                    account_update_needed = False
                else:
                    logger.warning("⚠️ 部分账户数据更新失败，将继续使用现有数据执行交易")
            else:
                logger.info("🔄 账户数据无需更新，使用上一轮数据")

            strategy_file = Combination_holding_file
            trade_file = Trade_history

            # account_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Account_position.xlsx"
            # 设置pandas显示选项，确保所有列都能完整显示
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)

            # 3.预先收集所有账户和策略的数据
            logger.info("🔍 预先收集所有账户和策略的数据...")
            processor_data = {}
            for account_name, strategy_name in ACCOUNT_STRATEGY_MAP.items():
                logger.info(f"🔄 收集账户 {account_name} 和策略 {strategy_name} 的数据")
                processor = CommonHoldingProcessor()
                diff = processor.extract_different_holding(
                    Account_holding_file,
                    account_name,
                    Combination_holding_file,
                    strategy_name
                )
                # filtered_result = processor.filter_executed_operations(diff, account_name)
                # processor_data[account_name] = {
                #     'processor': processor,
                #     'diff': diff,
                #     'filtered_result': filtered_result,
                #     'strategy_name': strategy_name
                # }

            # 为每个账户执行对应的策略
            execution_results = {}
            for account_name, data in processor_data.items():
                strategy_name = data['strategy_name']
                logger.info(f"🔄 处理账户 {account_name} 对应的策略 {strategy_name}")

                try:
                    # 执行策略
                    processor = data['processor']
                    to_sell = data['filtered_result'].get('to_sell', pd.DataFrame())
                    to_buy = data['filtered_result'].get('to_buy', pd.DataFrame())

                    # 只保留市场为沪深A股的
                    if not to_sell.empty and '市场' in to_sell.columns:
                        to_sell = to_sell[to_sell['市场'] == '沪深A股']
                    if not to_buy.empty and '市场' in to_buy.columns:
                        to_buy = to_buy[to_buy['市场'] == '沪深A股']

                    # 标记是否执行了任何交易操作
                    any_trade_executed = False

                    # 遍历每一项卖出操作，执行交易
                    for idx, op in to_sell.iterrows():
                        stock_name = op['股票名称'] if '股票名称' in op else op['股票名称']
                        operation = op['操作']
                        # 安全获取可能不存在的字段
                        new_ratio = op.get('新比例%', None)  # 对于卖出操作，获取策略中的目标比例

                        # 计算交易数量：对于卖出操作，使用策略中的目标比例
                        volume = processor.calculate_trade_volume(Account_holding_file, account_name, strategy_file,
                                                                  strategy_name, stock_name, new_ratio, operation)
                        logger.info(f"🛠️ 卖出 {stock_name}，目标比例:{new_ratio}，交易数量:{volume}")

                        logger.info(
                            f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{strategy_name} 账户:{account_name}")

                        # 切换到对应账户
                        processor.common_page.change_account(account_name)
                        logger.info(f"✅ 已切换到账户: {account_name}")

                        # 调用交易逻辑
                        status, info = processor.trader.operate_stock(operation, stock_name, volume)

                        # 检查交易是否成功执行
                        if status is None:
                            logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                            continue

                        # 标记已执行交易
                        any_trade_executed = True
                        # 标记下次需要更新账户数据
                        account_update_needed = True

                    # 遍历每一项买入操作，执行交易
                    for idx, op in to_buy.iterrows():
                        stock_name = op['股票名称'] if '股票名称' in op else op['股票名称']
                        operation = op['操作']
                        # 安全获取可能不存在的字段
                        new_ratio = op.get('新比例%', None)  # 对于买入操作，获取策略中的目标比例

                        # 计算交易数量：对于买入操作，使用策略中的目标比例
                        volume = processor.calculate_trade_volume(Account_holding_file, account_name, strategy_file,
                                                                  strategy_name, stock_name, new_ratio, operation)
                        logger.info(f"🛠️ 买入 {stock_name}，目标比例:{new_ratio}，交易数量:{volume}")

                        logger.info(
                            f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{strategy_name} 账户:{account_name}")

                        # 切换到对应账户
                        processor.common_page.change_account(account_name)
                        logger.info(f"✅ 已切换到账户: {account_name}")

                        # 调用交易逻辑
                        status, info = processor.trader.operate_stock(operation, stock_name, volume)

                        # 检查交易是否成功执行
                        if status is None:
                            logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                            continue

                        # 标记已执行交易
                        any_trade_executed = True
                        # 标记下次需要更新账户数据
                        account_update_needed = True

                    execution_results[account_name] = True
                    logger.info(f"✅ 账户 {account_name} 对应的策略 {strategy_name} 执行完成")
                    # send_notification(f"✅ 账户 {account_name} 对应的策略 {strategy_name} 执行完成")
                except Exception as e:
                    execution_results[account_name] = False
                    logger.error(f"❌ 账户 {account_name} 对应的策略 {strategy_name} 执行失败: {e}")
                    send_notification(f"❌ 账户 {account_name} 对应的策略 {strategy_name} 执行失败: {e}")

            # 检查执行结果
            all_success = all(execution_results.values())
            if all_success:
                logger.info("🎉 所有组合交易执行完成")
            else:
                failed_accounts = [acc for acc, success in execution_results.items() if not success]
                logger.error(f"❌ 以下账户交易执行失败: {failed_accounts}")

            return all_success
        except Exception as e:
            logger.error(f"❌ 组合交易执行异常: {e}")
            send_notification(f"组合交易执行异常: {e}")
            return False

    # def execute_combination_trades(self):
    #     """
    #     执行组合策略调仓操作
    #     """
    #     try:
    #         logger.info("🚀 开始执行组合策略调仓操作...")
    #
    #         # 1. 获取并保存最新的组合持仓数据
    #         self.save_all_combination_holding_data()
    #
    #         # 2. 为中山证券和中泰证券分别执行交易
    #         for account_name, strategy_name in ACCOUNT_TO_STRATEGY.items():
    #             logger.info(f"🔄 处理账户 {account_name} 对应的策略 {strategy_name}")
    #
    #             # 获取对应的组合ID
    #             combination_id = STRATEGY_TO_COMBINATION_ID.get(strategy_name)
    #             if not combination_id:
    #                 logger.error(f"未找到策略 {strategy_name} 对应的组合ID")
    #                 continue
    #
    #             # 获取该组合的持仓数据
    #             combination_data = self.get_single_holding_data(combination_id)
    #
    #             if combination_data.empty:
    #                 logger.info(f"策略 {strategy_name} 当前无持仓数据")
    #                 continue
    #
    #             # 设置当前账户
    #             self.account_name = account_name
    #
    #             # 执行交易操作 - 使用CommonHoldingProcessor中的方法
    #             success = self.operate_strategy(
    #                 Account_holding_file,
    #                 account_name,
    #                 Combination_holding_file,
    #                 strategy_name
    #             )
    #
    #             if success:
    #                 logger.info(f"✅ 账户 {account_name} 对应的策略 {strategy_name} 调仓执行完成")
    #                 send_notification(f"✅ 账户 {account_name} 对应的策略 {strategy_name} 调仓执行完成")
    #             else:
    #                 error_msg = f"❌ 账户 {account_name} 对应的策略 {strategy_name} 调仓执行失败"
    #                 logger.error(error_msg)
    #                 send_notification(error_msg)
    #
    #         logger.info("🎉 组合策略调仓任务完成")
    #         return True
    #
    #     except Exception as e:
    #         error_msg = f"执行组合策略调仓操作时出错: {e}\n{traceback.format_exc()}"
    #         logger.error(error_msg)
    #         send_notification(error_msg)
    #         return False



if __name__ == '__main__':
    processor = CombinationHoldingProcessor()
    success = processor.execute_combination_trades()
    if success:
        logger.info("🎉 组合策略调仓任务成功完成")
    else:
        logger.error("❌ 组合策略调仓任务失败")