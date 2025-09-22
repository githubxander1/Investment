"""
通用持仓处理器模块

"""
import sys
import os
import time
import datetime
import traceback
from pprint import pprint

import fake_useragent
import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import (
    Strategy_id_to_name, Strategy_ids, Strategy_holding_file,
    Strategy_portfolio_today_file, OPERATION_HISTORY_FILE, Account_holding_file,
    Strategy_holding_file, Lhw_ids, Lhw_ids_to_name, Lhw_holding_file,
    Combination_holding_file, all_ids, id_to_name, Trade_history
)
from Investment.THS.AutoTrade.pages.account_info import AccountInfo
from Investment.THS.AutoTrade.pages.page_common import CommonPage
from Investment.THS.AutoTrade.scripts.data_process import write_operation_history, save_to_excel_append, read_operation_history, read_portfolio_or_operation_data
from Investment.THS.AutoTrade.scripts.holding.trade_history import read_today_trade_history
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.format_data import determine_market, normalize_time
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger(__name__)
trader = TradeLogic()
ua = fake_useragent.UserAgent()
common_page = CommonPage()

class CommonHoldingProcessor:
    def __init__(self, account_name="川财证券"):
        self.account_name = account_name
        self.trader = TradeLogic()
        self.common_page = CommonPage()
        # 添加缓存机制
        self._account_holding_cache = None
        self._last_account_update_time = 0
        self._account_cache_valid_duration = 60  # 账户数据缓存1分钟
        self._account_updated_in_this_run = False  # 标记本轮是否已更新账户数据

    def extract_different_holding(self, account_file, account_name, strategy_file, strategy_name):
        import pandas as pd
        import os

        # 检查文件是否存在
        if not os.path.exists(account_file):
            print(f"账户持仓文件不存在: {account_file}")
            return {"error": "账户持仓文件不存在"}

        if not os.path.exists(strategy_file):
            print(f"组合持仓文件不存在: {strategy_file}")
            return {"error": "组合持仓文件不存在"}

        try:
            # 读取证券账户持仓数据
            account_holdings = pd.DataFrame()
            try:
                with pd.ExcelFile(account_file, engine='openpyxl') as xls:
                    # 读取证券的持仓数据
                    sheet_name = account_name
                    if sheet_name in xls.sheet_names:
                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        if not df.empty and '股票名称' in df.columns:
                            # 检查是否真的有持仓（排除"无持仓"的情况）
                            if len(df) == 1 and df.iloc[0]['股票名称'] == '无持仓':
                                print(f"证券账户 {account_name} 无持仓数据")
                                account_holdings = pd.DataFrame()
                            else:
                                # 只保留股票名称列
                                account_holdings = df.copy()
                                account_holdings['账户'] = account_name
                                # 去掉持有金额为0或0.0的
                                account_holdings = account_holdings[account_holdings['持有金额'] > 0]
                                print(
                                    f"✅ 成功读取证券账户的持仓数据，共 {len(account_holdings)} 条记录\n{account_holdings}")
                        else:
                            print(f"证券账户持仓数据为空或不包含股票名称列")
                    else:
                        print(f"账户文件中没有证券的持仓数据表: {sheet_name}")
                        return {"error": "账户文件中没有证券的持仓数据表"}
            except Exception as e:
                print(f"读取证券账户持仓文件失败: {e}")
                return {"error": f"读取证券账户持仓文件失败: {e}"}

            if account_holdings.empty:
                print("证券账户无持仓数据")
                return {"to_sell": pd.DataFrame(), "to_buy": pd.DataFrame()}

            # 读取策略持仓数据
            logicofking_holdings = pd.DataFrame()
            try:
                # 昨天的日期
                # yesterday = datetime.datetime.today() - datetime.timedelta(days=2)
                # today_str = yesterday.strftime('%Y-%m-%d')
                today_str = datetime.date.today().strftime('%Y-%m-%d')
                if os.path.exists(strategy_file):
                    with pd.ExcelFile(strategy_file, engine='openpyxl') as xls:
                        if today_str in xls.sheet_names:
                            df = pd.read_excel(xls, sheet_name=today_str)
                            # 筛选出策略的持仓
                            df = df[df['名称'] == strategy_name] if '名称' in df.columns else df
                            if not df.empty and '股票名称' in df.columns:
                                logicofking_holdings = df.copy()
                                print(
                                    f"✅ 成功读取策略的持仓数据，共 {len(logicofking_holdings)} 条记录\n{logicofking_holdings}")
                            else:
                                print("策略持仓数据为空或不包含股票名称列")
                        else:
                            print(f"组合持仓文件中没有今天的sheet: {today_str}")
                else:
                    print("组合持仓文件不存在")
            except Exception as e:
                print(f"读取策略持仓文件失败: {e}")
                return {"error": f"读取策略持仓文件失败: {e}"}

            # 需要排除的股票名称
            excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

            # 标准化股票名称
            from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe_stock_names
            account_holdings = standardize_dataframe_stock_names(account_holdings)
            if not logicofking_holdings.empty:
                logicofking_holdings = standardize_dataframe_stock_names(logicofking_holdings)

            # 确保账户持仓数据中的'持仓占比'以百分比形式存在，并创建'当前比例%'列
            # if '持仓占比' in account_holdings.columns:
            #     # 将原始的小数形式的持仓占比乘以100，转换为百分比，并四舍五入到两位小数
            #     # account_holdings['当前比例%'] = (account_holdings['持仓占比'] * 100).round(2)
            #     print(f"✅ 账户持仓占比已转换为百分比形式: {account_holdings[['股票名称', '持仓占比', '当前比例%']].head()}")
            # else:
            #     # 如果没有'持仓占比'列，则用0填充'当前比例%'
            #     account_holdings['当前比例%'] = 0.0

            # 确保策略持仓数据中的'新比例%'列存在，如果不存在则创建并填充0
            # if '新比例%' not in logicofking_holdings.columns:
            #     logicofking_holdings['新比例%'] = 0.0

            # 1. 找出需要卖出的标的（在证券账户中存在，但在策略中不存在，且不在排除列表中；如果证券账户和策略持仓都存在，但是策略持仓里的'新比例%'的值比证券账户的'持仓占比'小的）
            if not account_holdings.empty and not logicofking_holdings.empty:
                # 在证券账户中存在，但在策略中不存在的股票（需要全部卖出）
                to_sell_candidates = account_holdings[
                    ~account_holdings['股票名称'].isin(logicofking_holdings['股票名称'])]

                # 证券账户和策略持仓都存在，但是策略持仓里的'新比例%'的值比证券账户的'持仓占比'小的股票（需要部分卖出）
                # 先找出共同持有的股票
                common_stocks = account_holdings[
                    account_holdings['股票名称'].isin(logicofking_holdings['股票名称'])]

                # 合并策略数据以便比较
                merged_data = pd.merge(common_stocks, logicofking_holdings[['股票名称', '新比例%']], on='股票名称',
                                       how='left')

                # 找出策略持仓比例小于账户持仓比例的股票（需要卖出到目标比例）
                to_sell_candidates2 = merged_data[merged_data['新比例%'] < merged_data['持仓占比']]

                # 合并两种需要卖出的情况
                to_sell = pd.concat([to_sell_candidates, to_sell_candidates2]).drop_duplicates(subset=['股票名称'])
                to_sell = to_sell[~to_sell['股票名称'].isin(excluded_holdings)].copy()

                # 索引从1开始
                to_sell.index = range(1, len(to_sell) + 1)
                # 去掉'持有金额'为0的
                to_sell = to_sell[to_sell['持有金额'] != 0]
            elif not account_holdings.empty:
                # 如果策略持仓为空，则所有证券账户持仓都是需要卖出的（除去排除项）
                to_sell = account_holdings[~account_holdings['股票名称'].isin(excluded_holdings)].copy()
            else:
                to_sell = pd.DataFrame(
                    columns=account_holdings.columns) if not account_holdings.empty else pd.DataFrame()

            # 确保to_sell包含股票名称列
            if not to_sell.empty and '股票名称' not in to_sell.columns:
                to_sell['股票名称'] = to_sell['股票名称']

            if not to_sell.empty:
                to_sell['操作'] = '卖出'
                print(f"⚠️ 发现需卖出的标的: {len(to_sell)} 条")
                # 设置pandas显示选项，确保所有列都能完整显示
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.max_colwidth', None)
                # print(to_sell.to_string())
            else:
                print("✅ 当前无需卖出的标的")

            # 2. 找出需要买入的标的（在策略中存在，但在证券账户中不存在，且不在排除列表中；如果证券账户和策略持仓都存在，但是策略持仓里的'新比例%'的值比证券账户的'持仓占比'大的）
            if not logicofking_holdings.empty and not account_holdings.empty:
                # 在策略中存在，但在证券账户中不存在的股票（需要买入到目标比例）
                to_buy_candidates = logicofking_holdings[
                    ~logicofking_holdings['股票名称'].isin(account_holdings['股票名称'])]

                # 证券账户和策略持仓都存在，但是策略持仓里的'新比例%'的值比证券账户的'持仓占比'大的股票（需要买入到目标比例）
                # 找出共同持有的股票
                common_stocks_buy = logicofking_holdings[
                    logicofking_holdings['股票名称'].isin(account_holdings['股票名称'])]

                # 合并账户数据以便比较
                merged_data_buy = pd.merge(common_stocks_buy, account_holdings[['股票名称', '持仓占比']],
                                           on='股票名称', how='left')

                # 找出策略持仓比例大于账户持仓比例的股票（需要买入到目标比例）
                to_buy_candidates2 = merged_data_buy[merged_data_buy['新比例%'] > merged_data_buy['持仓占比']]

                # 合并两种需要买入的情况
                to_buy = pd.concat([to_buy_candidates, to_buy_candidates2]).drop_duplicates(subset=['股票名称'])
                to_buy = to_buy[~to_buy['股票名称'].isin(excluded_holdings)]

                # 只保留市场为沪深A股的
                if '市场' in to_buy.columns:
                    to_buy = to_buy[to_buy['市场'] == '沪深A股']
                to_buy.index = range(1, len(to_buy) + 1)
            elif not logicofking_holdings.empty:
                # 如果证券账户持仓为空，则所有策略持仓都是需要买入的（除去排除项）
                to_buy = logicofking_holdings[~logicofking_holdings['股票名称'].isin(excluded_holdings)]
                # 只保留市场为沪深A股的
                if '市场' in to_buy.columns:
                    to_buy = to_buy[to_buy['市场'] == '沪深A股']
            else:
                to_buy = pd.DataFrame(columns=['股票名称'])

            # 确保to_buy包含股票名称列
            if not to_buy.empty and '股票名称' not in to_buy.columns:
                to_buy['股票名称'] = to_buy['股票名称']

            if not to_buy.empty:
                to_buy['操作'] = '买入'
                print(f"⚠️ 发现需买入的标的: {len(to_buy)} 条")
                # 设置pandas显示选项，确保所有列都能完整显示
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.max_colwidth', None)
                # print(to_buy.to_string())
            else:
                print("✅ 当前无需买入的标的")

            # 合并to_buy和to_sell
            # difference_holding_df = pd.concat([to_sell, to_buy], ignore_index=True)
            # # 索引从1开始
            # difference_holding_df = difference_holding_df.reset_index(drop=True)
            # difference_holding_df.index = difference_holding_df.index + 1
            # 构建完整差异报告
            difference_report = {
                "to_sell": to_sell,
                "to_buy": to_buy
            }

            # # 为结果中的DataFrame添加'当前比例%'列，便于后续操作
            # if '当前比例%' not in to_sell.columns:
            #     to_sell['当前比例%'] = to_sell.get('持仓占比', 0) * 100
            # if '当前比例%' not in to_buy.columns:
            #     to_buy['当前比例%'] = 0.0

            print(f"📊 最终差异报告 - 需要卖出: {len(to_sell)} 条, 需要买入: {len(to_buy)} 条")
            if not to_sell.empty:
                # 为卖出报告添加目标比例和变化比例列
                to_sell_report = to_sell[['股票名称', '持有金额', '持有盈亏', '持有数量', '持仓占比']].copy()
                to_sell_report['目标比例'] = 0.0  # 卖出的目标比例为0
                # 修正：对于需要调整到目标比例的股票，目标比例应为策略中的新比例%
                for idx, row in to_sell_report.iterrows():
                    stock_name = row['股票名称']
                    # 查找该股票在策略中的目标比例
                    strategy_row = logicofking_holdings[logicofking_holdings['股票名称'] == stock_name]
                    if not strategy_row.empty:
                        target_ratio = float(strategy_row['新比例%'].iloc[0])
                        to_sell_report.at[idx, '目标比例'] = target_ratio

                to_sell_report['变化比例'] = to_sell_report['目标比例'] - to_sell_report['持仓占比']
                print(f"📈 需要卖出的股票及其当前/目标比例:\n{to_sell_report}")
            if not to_buy.empty:
                # 为买入报告添加原始比例和变化比例列
                to_buy_report = to_buy[['股票名称', '新比例%']].copy()
                to_buy_report['原始比例'] = 0.0  # 买入的原始比例为0（账户中没有该股票）
                # 修正：对于已持有的股票，原始比例应该是账户中的持仓比例
                for idx, row in to_buy_report.iterrows():
                    stock_name = row['股票名称']
                    # 查找该股票在账户中的原始比例
                    account_row = account_holdings[account_holdings['股票名称'] == stock_name]
                    if not account_row.empty:
                        original_ratio = float(account_row['持仓占比'].iloc[0])
                        to_buy_report.at[idx, '原始比例'] = original_ratio

                to_buy_report['变化比例'] = to_buy_report['新比例%'] - to_buy_report['原始比例']
                print(f"📈 需要买入的股票及其当前/目标比例:\n{to_buy_report}")

            return difference_report

        except Exception as e:
            error_msg = f"处理证券与策略持仓差异时发生错误: {e}"
            print(error_msg)
            return {"error": error_msg}
    def filter_executed_operations(self, diff_result, account_name):
        """
        过滤已执行的操作，只返回未执行的操作记录
        
        :param diff_result: extract_different_holding函数返回的结果，包含to_sell和to_buy两个DataFrame
        :return: 未执行的操作记录
        """
        print("开始过滤已执行的操作记录...")
        
        # 读取操作历史记录
        try:
            # 使用read_portfolio_or_operation_data读取Trade_history文件
            trade_history_df = read_today_trade_history(Trade_history,account_name)
            if isinstance(trade_history_df, list):
                trade_history_df = trade_history_df[0] if trade_history_df else pd.DataFrame()
            
            print(f"成功读取操作历史记录，共 {len(trade_history_df)} 条记录")
        except Exception as e:
            print(f"读取操作历史记录失败: {e}")
            trade_history_df = pd.DataFrame()
        
        # 获取需要卖出和买入的记录
        to_sell = diff_result.get('to_sell', pd.DataFrame())
        to_buy = diff_result.get('to_buy', pd.DataFrame())
        
        print(f"待处理 - 需要卖出: {len(to_sell)} 条，需要买入: {len(to_buy)} 条")
        
        # 过滤已执行的卖出操作
        if not to_sell.empty and not trade_history_df.empty:
            # 创建一个布尔索引，标记哪些操作已经执行过
            sell_executed_mask = pd.Series([False] * len(to_sell), index=to_sell.index)
            
            for idx, sell_row in to_sell.iterrows():
                stock_name = sell_row.get('股票名称') or sell_row.get('股票名称')
                operation = '卖出'
                
                if pd.isna(stock_name):
                    continue
                    
                # 检查是否已执行过该操作
                executed = trade_history_df[
                    (trade_history_df['股票名称'] == stock_name) & 
                    (trade_history_df['操作'] == operation)
                ]
                
                if not executed.empty:
                    sell_executed_mask.loc[idx] = True
                    print(f"已执行过卖出操作: {stock_name}")
            
            # 只保留未执行的操作
            to_sell_filtered = to_sell[~sell_executed_mask]
        else:
            to_sell_filtered = to_sell
            
        # 过滤已执行的买入操作
        if not to_buy.empty and not trade_history_df.empty:
            # 创建一个布尔索引，标记哪些操作已经执行过
            buy_executed_mask = pd.Series([False] * len(to_buy), index=to_buy.index)
            
            for idx, buy_row in to_buy.iterrows():
                stock_name = buy_row.get('股票名称') or buy_row.get('股票名称')
                operation = '买入'
                new_ratio = buy_row.get('新比例%', 0)
                
                if pd.isna(stock_name):
                    continue
                    
                # 检查是否已执行过该操作（需要匹配股票名称、操作类型和比例）
                executed = trade_history_df[
                    (trade_history_df['股票名称'] == stock_name) & 
                    (trade_history_df['操作'] == operation) &
                    (abs(trade_history_df['新比例%'] - new_ratio) < 0.01)
                ]
                
                if not executed.empty:
                    buy_executed_mask.loc[idx] = True
                    print(f"已执行过买入操作: {stock_name} ({new_ratio}%)")
            
            # 只保留未执行的操作
            to_buy_filtered = to_buy[~buy_executed_mask]
        else:
            to_buy_filtered = to_buy
            
        print(f"过滤后 - 需要卖出: {len(to_sell_filtered)} 条，需要买入: {len(to_buy_filtered)} 条")
        
        # 返回过滤后的结果
        return {
            "to_sell": to_sell_filtered,
            "to_buy": to_buy_filtered
        }

    def save_all_strategy_holding_data(self, get_all_strategy_data):
        """
        1.获取所有策略的持仓数据，
        2.并保存到 Excel 文件中，当天数据保存在第一个sheet
        3.返回当天的数据
        """
        logger.info("📂 开始获取并保存所有策略持仓数据")

        # 获取所有策略的持仓数据
        all_holdings = []
        success_count = 0  # 记录成功获取数据的策略数量
        total_count = len(Strategy_ids)  # 总策略数量

        for id in Strategy_ids:
            positions_df = self.get_latest_position(id)
            has_data = not positions_df.empty  # 记录是否获取到原始数据

            if positions_df is not None and not positions_df.empty:
                all_holdings.append(positions_df)
                success_count += 1
            elif has_data:
                # 获取到了数据但经过过滤后为空，也算成功获取
                success_count += 1
                logger.info(f"获取到策略数据但经过过滤后为空，策略ID: {id}")
            else:
                logger.info(f"没有获取到策略数据，策略ID: {id}")

        # 检查数据获取情况
        if success_count == 0:
            logger.error("❌ 未获取到任何策略持仓数据")
            send_notification("❌ 未获取到任何策略持仓数据")
            return False

        elif success_count < total_count:
            logger.warning(f"⚠️ 部分策略数据获取失败: {success_count}/{total_count}")
            send_notification(f"⚠️ 策略数据获取异常: {success_count}/{total_count} 个策略数据获取成功")

        # 汇总所有数据
        all_holdings_df = pd.concat(all_holdings, ignore_index=False)
        # 从1开始计数，只保留沪深A股的, 按价格从低到高排序
        all_holdings_df = all_holdings_df[all_holdings_df['市场'] == '沪深A股']
        all_holdings_df.sort_values('最新价', ascending=True)
        all_holdings_df.index = all_holdings_df.index + 1
        # 添加一列账户名
        # all_holdings_df['账户名'] = account_name

        today = str(datetime.date.today())
        # 提取出今天的数据df，时间列=今天
        today_holdings_df = all_holdings_df[all_holdings_df['时间'] == today]

        file_path = Strategy_holding_file

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
                    # logger.info(f"正在保存工作表: {sheet_name}")
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            logger.info(f"✅ 所有持仓数据已保存，{today} 数据位于第一个 sheet，共 {len(all_holdings_df)} 条")
            return True, today_holdings_df

        except Exception as e:
            logger.error(f"❌ 保存持仓数据失败: {e}")
            # 如果出错，至少保存今天的数据
            try:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    all_holdings_df.to_excel(writer, sheet_name=today, index=False)
                logger.info(f"✅ 文件保存完成，sheet: {today}")
                return True, today_holdings_df
            except Exception as e2:
                logger.error(f"❌ 保存今日数据也失败了: {e2}")
                send_notification(f"❌ 策略持仓数据保存失败: {e2}")
                return False

    def calculate_trade_volume(self, account_file, account_name, strategy_name, stock_name, new_ratio, operation_type):
        """
        根据账户信息和策略要求计算买入或卖出的股数
        
        :param account_file: 账户持仓文件路径
        :param account_name: 账户名称
        :param strategy_name: 策略名称
        :param stock_name: 股票名称
        :param new_ratio: 新持仓比例(%)
        :param operation_type: 操作类型('买入' 或 '卖出')
        :return: 计算出的交易股数
        """
        logger.info(f"开始计算交易股数: 账户={account_name}, 股票={stock_name}, 操作={operation_type}, 新比例={new_ratio}%")
        account_asset, account_balance, stock_available, stock_ratio, stock_price = self.trader.get_account_info(account_file, account_name, stock_name)
        try:
            # 读取账户信息
            if not os.path.exists(account_file):
                logger.error(f"账户持仓文件不存在: {account_file}")
                return None

            # 计算买入股数
            if operation_type == '买入':
                volume = self.trader.calculate_buy_volume(account_asset, new_ratio, stock_price)
                return  volume

            # 计算卖出股数
            elif operation_type == '卖出':
                # logger.info(f"卖出 {stock_name}，股数: {volume}")
                volume = self.trader.calculate_sell_volume(account_asset, stock_available, stock_price, new_ratio)
                return volume
                
            else:
                logger.error(f"不支持的操作类型: {operation_type}")
                return None
                
        except Exception as e:
            logger.error(f"计算交易股数时发生错误: {e}")
            return None

    def operate_strategy(self, account_file, account_name, strategy_file, strategy_name: str):
        """执行策略"""
        # 确保account_name有默认值
        if account_name is None:
            account_name = self.account_name
            
        diff = self.extract_different_holding(account_file, account_name, strategy_file, strategy_name)
        filtered_result = self.filter_executed_operations(diff, account_name)
        to_sell = filtered_result.get('to_sell', pd.DataFrame())
        to_buy = filtered_result.get('to_buy', pd.DataFrame())

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

            print(f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{strategy_name} 账户:{account_name}")

            # 切换到对应账户
            self.common_page.change_account(account_name)
            print(f"✅ 已切换到账户: {account_name}")

            # 计算交易数量：对于卖出操作，使用策略中的目标比例
            volume = self.calculate_trade_volume(account_file, account_name, strategy_name, stock_name, new_ratio, operation)

            # 调用交易逻辑
            status, info = self.trader.operate_stock(operation, stock_name, volume)

            # 检查交易是否成功执行
            if status is None:
                print(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                continue

            # 标记已执行交易
            any_trade_executed = True

        # 遍历每一项买入操作，执行交易
        for idx, op in to_buy.iterrows():
            stock_name = op['股票名称'] if '股票名称' in op else op['股票名称']
            operation = op['操作']
            # 安全获取可能不存在的字段
            new_ratio = op.get('新比例%', None)  # 对于买入操作，获取策略中的目标比例

            print(f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{strategy_name} 账户:{account_name}")

            # 切换到对应账户
            self.common_page.change_account(account_name)
            print(f"✅ 已切换到账户: {account_name}")

            # 计算交易数量：对于买入操作，使用策略中的目标比例
            volume = self.calculate_trade_volume(account_file, account_name, strategy_name, stock_name, new_ratio, operation)

            # 调用交易逻辑
            status, info = self.trader.operate_stock(operation, stock_name, volume)

            # 检查交易是否成功执行
            if status is None:
                print(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                continue

            # 标记已执行交易
            any_trade_executed = True

        print(diff)
        print('-' * 50)
        print("需要卖出的股票:")
        # 设置pandas显示选项，确保所有列都能完整显示
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        print(to_sell.to_string())
        print("需要买入的股票:")
        print(to_buy.to_string())


if __name__ == '__main__':
    # 定义文件路径
    # account_holding_main()
    account_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Account_position.xlsx"
    strategy_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Combination_position.xlsx"
    trade_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\portfolio\trade_operations.xlsx"
    
    # 设置pandas显示选项，确保所有列都能完整显示
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    com = CommonHoldingProcessor()

    # strategy_file =r"E:\git_documents\Investment\Investment\THS\AutoTrade\data\position\Strategy_position.xlsx"
    # account_file = r'E:\git_documents\Investment\Investment\THS\AutoTrade\data\position\account_info.xlsx'
    # trade_file = r'E:\git_documents\Investment\Investment\THS\AutoTrade\data\portfolio\trade_operations.xlsx'
    account_name = '中泰证券'
    strategy_name = '一枝梨花'
    # diff = com.get_difference_holding(account_file, '长城证券',strategy_file, 'AI市场追踪策略' )
    # diff = com.get_difference_holding(r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Combination_position.xlsx", r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\account_info.xlsx',account_name="中泰证券")
    # diff = com.extract_different_holding(account_file, account_name, strategy_file, strategy_name)
    # to_operate = com.filter_executed_operations(diff,account_name)

    # volume= com.calculate_trade_volume(account_file, account_name, strategy_name, '超讯通信', 10, '卖出')
    com.operate_strategy(account_file, account_name, strategy_file, strategy_name)
    # print(diff)
    # print('-'*50)
    # print(to_operate)