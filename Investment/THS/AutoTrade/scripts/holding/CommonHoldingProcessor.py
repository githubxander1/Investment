"""
通用持仓处理器模块

该模块提供了一个通用的持仓处理框架，用于:
1. 获取和保存策略持仓数据
2. 对比账户实际持仓与策略持仓数据，找出差异
3. 执行调仓操作（买入/卖出）
4. 管理操作历史记录
5. 缓存账户持仓数据以提高性能

主要功能:
- save_all_strategy_holding_data: 获取并保存所有策略持仓数据
- get_difference_holding: 对比账户与策略持仓差异
- operate_result: 执行调仓操作
- _update_account_holding_cache: 更新账户持仓缓存
"""

import time
import sys
import os
import datetime
import traceback
from datetime import datetime as dt
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

    def filter_executed_operations(self, diff_result, account_name):
        """
        过滤已执行的操作，只返回未执行的操作记录
        
        :param diff_result: extract_different_holding函数返回的结果，包含to_sell和to_buy两个DataFrame
        :return: 未执行的操作记录
        """
        logger.info("开始过滤已执行的操作记录...")
        
        # 读取操作历史记录
        try:
            # 使用read_portfolio_or_operation_data读取Trade_history文件
            trade_history_df = read_today_trade_history(Trade_history,account_name)
            if isinstance(trade_history_df, list):
                trade_history_df = trade_history_df[0] if trade_history_df else pd.DataFrame()
            
            logger.info(f"成功读取操作历史记录，共 {len(trade_history_df)} 条记录")
        except Exception as e:
            logger.error(f"读取操作历史记录失败: {e}")
            trade_history_df = pd.DataFrame()
        
        # 获取需要卖出和买入的记录
        to_sell = diff_result.get('to_sell', pd.DataFrame())
        to_buy = diff_result.get('to_buy', pd.DataFrame())
        
        logger.info(f"待处理 - 需要卖出: {len(to_sell)} 条，需要买入: {len(to_buy)} 条")
        
        # 过滤已执行的卖出操作
        if not to_sell.empty and not trade_history_df.empty:
            # 创建一个布尔索引，标记哪些操作已经执行过
            sell_executed_mask = pd.Series([False] * len(to_sell), index=to_sell.index)
            
            for idx, sell_row in to_sell.iterrows():
                stock_name = sell_row.get('股票名称') or sell_row.get('标的名称')
                operation = '卖出'
                
                if pd.isna(stock_name):
                    continue
                    
                # 检查是否已执行过该操作
                executed = trade_history_df[
                    (trade_history_df['标的名称'] == stock_name) & 
                    (trade_history_df['操作'] == operation)
                ]
                
                if not executed.empty:
                    sell_executed_mask.loc[idx] = True
                    logger.info(f"已执行过卖出操作: {stock_name}")
            
            # 只保留未执行的操作
            to_sell_filtered = to_sell[~sell_executed_mask]
        else:
            to_sell_filtered = to_sell
            
        # 过滤已执行的买入操作
        if not to_buy.empty and not trade_history_df.empty:
            # 创建一个布尔索引，标记哪些操作已经执行过
            buy_executed_mask = pd.Series([False] * len(to_buy), index=to_buy.index)
            
            for idx, buy_row in to_buy.iterrows():
                stock_name = buy_row.get('股票名称') or buy_row.get('标的名称')
                operation = '买入'
                new_ratio = buy_row.get('新比例%', 0)
                
                if pd.isna(stock_name):
                    continue
                    
                # 检查是否已执行过该操作（需要匹配股票名称、操作类型和比例）
                executed = trade_history_df[
                    (trade_history_df['标的名称'] == stock_name) & 
                    (trade_history_df['操作'] == operation) &
                    (abs(trade_history_df['新比例%'] - new_ratio) < 0.01)
                ]
                
                if not executed.empty:
                    buy_executed_mask.loc[idx] = True
                    logger.info(f"已执行过买入操作: {stock_name} ({new_ratio}%)")
            
            # 只保留未执行的操作
            to_buy_filtered = to_buy[~buy_executed_mask]
        else:
            to_buy_filtered = to_buy
            
        logger.info(f"过滤后 - 需要卖出: {len(to_sell_filtered)} 条，需要买入: {len(to_buy_filtered)} 条")
        
        # 返回过滤后的结果
        return {
            "to_sell": to_sell_filtered,
            "to_buy": to_buy_filtered
        }
        
    def extract_different_holding(self, account_file, account_name, strategy_file, strategy_name):
        import pandas as pd
        from datetime import datetime
        import os
        

        # 检查文件是否存在
        if not os.path.exists(account_file):
            logger.error(f"账户持仓文件不存在: {account_file}")
            return {"error": "账户持仓文件不存在"}
            
        if not os.path.exists(strategy_file):
            logger.error(f"组合持仓文件不存在: {strategy_file}")
            return {"error": "组合持仓文件不存在"}
        
        try:
            # 读取证券账户持仓数据
            greatwall_holdings = pd.DataFrame()
            try:
                with pd.ExcelFile(account_file, engine='openpyxl') as xls:
                    # 读取证券的持仓数据
                    sheet_name = account_name
                    if sheet_name in xls.sheet_names:
                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        if not df.empty and '股票名称' in df.columns:
                            # 只保留股票名称列
                            greatwall_holdings = df.copy()
                            greatwall_holdings['账户'] = account_name
                            logger.info(f"✅ 成功读取证券账户的持仓数据，共 {len(greatwall_holdings)} 条记录\n{greatwall_holdings}")
                        else:
                            logger.warning(f"证券账户持仓数据为空或不包含股票名称列")
                    else:
                        logger.warning(f"账户文件中没有证券的持仓数据表: {sheet_name}")
                        return {"error": "账户文件中没有证券的持仓数据表"}
            except Exception as e:
                logger.error(f"读取证券账户持仓文件失败: {e}")
                return {"error": f"读取证券账户持仓文件失败: {e}"}

            if greatwall_holdings.empty:
                logger.info("证券账户无持仓数据")
                return {"to_sell": pd.DataFrame(), "to_buy": pd.DataFrame()}

            # 读取""策略持仓数据
            logicofking_holdings = pd.DataFrame()
            try:
                today = str(datetime.today().strftime('%Y-%m-%d'))
                if os.path.exists(strategy_file):
                    with pd.ExcelFile(strategy_file, engine='openpyxl') as xls:
                        if today in xls.sheet_names:
                            df = pd.read_excel(xls, sheet_name=today)
                            # 筛选出""策略的持仓
                            df = df[df['名称'] == strategy_name] if '名称' in df.columns else df
                            if not df.empty and '股票名称' in df.columns:
                                logicofking_holdings = df.copy()
                                logicofking_holdings['策略'] = strategy_name
                                logger.info(f"✅ 成功读取策略的持仓数据，共 {len(logicofking_holdings)} 条记录\n{logicofking_holdings}")
                            else:
                                logger.warning("策略持仓数据为空或不包含股票名称列")
                        else:
                            logger.warning(f"组合持仓文件中没有今天的sheet: {today}")
                else:
                    logger.warning("组合持仓文件不存在")
            except Exception as e:
                logger.error(f"读取策略持仓文件失败: {e}")
                return {"error": f"读取策略持仓文件失败: {e}"}

            # 需要排除的股票名称
            excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

            # 标准化股票名称
            from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe_stock_names
            greatwall_holdings = standardize_dataframe_stock_names(greatwall_holdings)
            if not logicofking_holdings.empty:
                logicofking_holdings = standardize_dataframe_stock_names(logicofking_holdings)

            # 1. 找出需要卖出的标的（在证券账户中存在，但在策略中不存在，且不在排除列表中）
            if not greatwall_holdings.empty and not logicofking_holdings.empty:
                to_sell_candidates = greatwall_holdings[~greatwall_holdings['股票名称'].isin(logicofking_holdings['股票名称'])]
                to_sell = to_sell_candidates[~to_sell_candidates['股票名称'].isin(excluded_holdings)].copy()
                # 索引从1开始
                to_sell.index = range(1, len(to_sell) + 1)
                # 去掉‘持有金额’为0的
                to_sell = to_sell[to_sell['持有金额'] != 0]
            elif not greatwall_holdings.empty:
                # 如果策略持仓为空，则所有证券账户持仓都是需要卖出的（除去排除项）
                to_sell = greatwall_holdings[~greatwall_holdings['股票名称'].isin(excluded_holdings)].copy()
            else:
                to_sell = pd.DataFrame(columns=greatwall_holdings.columns) if not greatwall_holdings.empty else pd.DataFrame()

            # 确保to_sell包含标的名称列
            if not to_sell.empty and '标的名称' not in to_sell.columns:
                to_sell['标的名称'] = to_sell['股票名称']

            if not to_sell.empty:
                to_sell['操作'] = '卖出'
                logger.warning(f"⚠️ 发现需卖出的标的: {len(to_sell)} 条\n{to_sell}")
            else:
                logger.info("✅ 当前无需卖出的标的")

            # 2. 找出需要买入的标的（在策略中存在，但在证券账户中不存在，且不在排除列表中）
            if not logicofking_holdings.empty and not greatwall_holdings.empty:
                to_buy_candidates = logicofking_holdings[~logicofking_holdings['股票名称'].isin(greatwall_holdings['股票名称'])]
                to_buy = to_buy_candidates[~to_buy_candidates['股票名称'].isin(excluded_holdings)]
                to_buy.index = range(1, len(to_buy) + 1)
            elif not logicofking_holdings.empty:
                # 如果证券账户持仓为空，则所有策略持仓都是需要买入的（除去排除项）
                to_buy = logicofking_holdings[~logicofking_holdings['股票名称'].isin(excluded_holdings)]
            else:
                to_buy = pd.DataFrame(columns=['股票名称'])

            # 确保to_buy包含标的名称列
            if not to_buy.empty and '标的名称' not in to_buy.columns:
                to_buy['标的名称'] = to_buy['股票名称']

            if not to_buy.empty:
                to_buy['操作'] = '买入'
                logger.warning(f"⚠️ 发现需买入的标的: {len(to_buy)} 条\n{to_buy}")
            else:
                logger.info("✅ 当前无需买入的标的")

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

            return difference_report

        except Exception as e:
            error_msg = f"处理证券与策略持仓差异时发生错误: {e}"
            logger.error(error_msg, exc_info=True)
            return {"error": error_msg}

    def _should_update_account_data(self):
        """判断是否需要更新账户数据"""
        current_time = time.time()
        # 以下情况需要更新账户数据：
        # 1. 本轮尚未更新过账户数据
        # 2. 缓存已过期
        # 3. 没有缓存数据
        should_update = (not self._account_updated_in_this_run and
                (current_time - self._last_account_update_time > self._account_cache_valid_duration or
                 self._account_holding_cache is None))
        logger.debug(f"检查是否需要更新账户数据: should_update={should_update}, "
                    f"account_updated_in_this_run={self._account_updated_in_this_run}, "
                    f"time_diff={current_time - self._last_account_update_time}, "
                    f"cache_valid_duration={self._account_cache_valid_duration}, "
                    f"account_holding_cache is None={self._account_holding_cache is None}")
        return should_update

    def _update_account_holding_cache(self, account_file, account_name):
        """更新账户持仓缓存"""
        logger.info(f"正在更新{account_name}账户持仓数据...")
        try:
            # 调用外部脚本同步账户数据
            import subprocess
            import sys
            import os
            
            # 获取脚本目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            refresh_script = os.path.join(script_dir, "reflash_account_holding.py")
            account_holding_script = os.path.join(script_dir, "account_holding.py")
            
            # 先运行账户同步脚本
            if os.path.exists(refresh_script):
                logger.info("执行账户数据同步...")
                result = subprocess.run([sys.executable, refresh_script], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    logger.info("账户数据同步完成")
                else:
                    logger.warning(f"账户数据同步脚本执行失败: {result.stderr}")
            else:
                logger.warning(f"账户同步脚本不存在: {refresh_script}")
            
            # 再运行账户持仓获取脚本
            if os.path.exists(account_holding_script):
                logger.info("执行账户持仓数据获取...")
                result = subprocess.run([sys.executable, account_holding_script], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    logger.info("账户持仓数据获取完成")
                else:
                    logger.warning(f"账户持仓数据获取脚本执行失败: {result.stderr}")
            else:
                logger.warning(f"账户持仓数据获取脚本不存在: {account_holding_script}")

            # 读取指定账户持仓数据
            account_df = pd.DataFrame()
            try:
                with pd.ExcelFile(account_file, engine='openpyxl') as xls:
                    # 只读取指定账户的持仓数据
                    sheet_name = f"{account_name}_持仓数据"
                    if sheet_name in xls.sheet_names:
                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        if not df.empty and '股票名称' in df.columns:
                            # 只保留股票名称列
                            # account_df = df[['股票名称']].copy()
                            account_df = df.copy()
                            # 保留沪深A股的

                            account_df['账户'] = account_name
                            logger.info(f"✅ 成功缓存{account_name}账户的持仓数据，共 {len(account_df)} 条记录")
                        else:
                            logger.warning(f"{account_name}账户持仓数据为空或不包含股票名称列")
                    else:
                        logger.warning(f"账户文件中没有{account_name}的持仓数据表: {sheet_name}")
            except Exception as e:
                logger.error(f"读取{account_name}账户持仓文件失败: {e}")
                return False

            if account_df.empty:
                logger.info(f"{account_name}账户无持仓数据")

            # 更新缓存
            self._account_holding_cache = account_df
            self._last_account_update_time = time.time()
            self._account_updated_in_this_run = True  # 标记本轮已更新账户数据
            return True
        except subprocess.TimeoutExpired:
            logger.error("执行外部脚本超时")
            return False
        except Exception as e:
            logger.error(f"更新{account_name}账户持仓缓存时出错: {e}")
            return False

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

    # 获取账户持仓数据差异
    def get_difference_holding(self, holding_file, account_file, account_name=None):
        """
        对比账户实际持仓与策略/组合今日持仓数据，找出差异：
            - 需要卖出：在账户中存在，但不在策略/组合今日持仓中；
            - 需要买入：在策略/组合今日持仓中存在，但不在账户中；
        :param holding_file: 持仓文件路径
        :param account_file: 账户文件路径
        :param account_name: 账户名称
        # :param strategy_filter: 策略过滤函数，用于筛选特定策略的数据
        """
        logger.info("-" * 50)
        logger.info(f"开始：对比账户实际持仓与{holding_file}数据...")
        if account_name is None:
            account_name = self.account_name

        try:
            # 检查必要文件是否存在
            required_files = {
                "账户持仓文件": account_file,
                "接口持仓文件": holding_file,
            }

            for file_desc, file_path in required_files.items():
                if not os.path.exists(file_path):
                    logger.error(f"{file_desc}不存在: {file_path}")
                    return {"error": f"{file_desc}不存在"}

            # # 判断是否需要更新账户数据
            # if self._should_update_account_data():
            #     update_result = self._update_account_holding_cache(account_file, account_name)
            #     if not update_result:
            #         return {"error": f"更新{account_name}账户持仓数据失败"}
            # else:
            #     logger.info(f"✅ 使用缓存的{account_name}账户持仓数据")

            # 读取策略/组合今日持仓数据（这部分始终实时读取，不缓存）
            today = str(datetime.date.today())
            try:
                if os.path.exists(holding_file):
                    with pd.ExcelFile(holding_file, engine='openpyxl') as xls:
                        if today in xls.sheet_names:
                            today_strategy_df = pd.read_excel(xls, sheet_name=today)
                            if today_strategy_df.empty:
                                logger.warning("接口持仓文件为空")
                                today_strategy_df = pd.DataFrame(columns=['股票名称'])
                        else:
                            logger.warning(f"接口持仓文件中没有今天的sheet: {today}")
                            today_strategy_df = pd.DataFrame(columns=['股票名称'])
                else:
                    logger.warning("接口持仓文件不存在")
                    today_strategy_df = pd.DataFrame(columns=['股票名称'])
            except Exception as e:
                logger.error(f"读取接口持仓文件失败: {e}")
                today_strategy_df = pd.DataFrame(columns=['股票名称'])

            # 应用策略过滤器（如果提供）
            # if strategy_filter and not today_strategy_df.empty and '名称' in today_strategy_df.columns:
            #     today_strategy_df = today_strategy_df[today_strategy_df.apply(strategy_filter, axis=1)]
            #     logger.info(f"应用策略过滤器后，策略数据条数: {len(today_strategy_df)}")

            # 需要排除的股票名称
            excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

            # 标准化股票名称
            from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe_stock_names
            if not self._account_holding_cache.empty:
                self._account_holding_cache = standardize_dataframe_stock_names(self._account_holding_cache)
            if not today_strategy_df.empty:
                today_strategy_df = standardize_dataframe_stock_names(today_strategy_df)

            # 1. 找出需要卖出的标的（在账户中存在，但不在策略/组合今日持仓中，且不在排除列表中）
            if not self._account_holding_cache.empty and not today_strategy_df.empty:
                to_sell_candidates = self._account_holding_cache[~self._account_holding_cache['股票名称'].isin(today_strategy_df['股票名称'])]
                to_sell_df = to_sell_candidates[~to_sell_candidates['股票名称'].isin(excluded_holdings)].copy()
            elif not self._account_holding_cache.empty:
                # 如果策略/组合持仓为空，则所有账户持仓都是需要卖出的（除去排除项）
                to_sell_df = self._account_holding_cache[~self._account_holding_cache['股票名称'].isin(excluded_holdings)].copy()
            else:
                to_sell_df = pd.DataFrame(columns=self._account_holding_cache.columns) if self._account_holding_cache is not None and not self._account_holding_cache.empty else pd.DataFrame()

            # 确保卖出DataFrame包含必要的列，使其与买入DataFrame结构一致
            required_columns = ['名称', '股票名称', '代码', '市场', '最新价', '新比例%', '时间', '行业', '账户名']
            for col in required_columns:
                if col not in to_sell_df.columns:
                    to_sell_df[col] = None

            if not to_sell_df.empty:
                # logger.warning(f"⚠️ 发现需卖出的标的: {len(to_sell_df)} 条\n{to_sell_df[['股票名称']].to_string(index=False)}")
                to_sell_df['操作'] = '卖出'
                logger.warning(f"⚠️ 发现需卖出的标的: {len(to_sell_df)} 条\n{to_sell_df}")
                # 添加操作列
                # 打印具体需要卖出的股票
                # logger.info(f"具体需卖出的标的:")
            else:
                logger.info("✅ 当前无需卖出的标的")

            # 2. 找出需要买入的标的（在策略/组合今日持仓中存在，但不在账户中，且不在排除列表中）
            if not today_strategy_df.empty and not self._account_holding_cache.empty:
                to_buy_candidates = today_strategy_df[~today_strategy_df['股票名称'].isin(self._account_holding_cache['股票名称'])]
                to_buy_df = to_buy_candidates[~to_buy_candidates['股票名称'].isin(excluded_holdings)]
            elif not today_strategy_df.empty:
                # 如果账户持仓为空，则所有策略/组合持仓都是需要买入的（除去排除项）
                to_buy_df = today_strategy_df[~today_strategy_df['股票名称'].isin(excluded_holdings)]
            else:
                to_buy_df = pd.DataFrame(columns=['股票名称'])

            # 确保买入DataFrame包含必要的列，使其与卖出DataFrame结构一致
            for col in required_columns:
                if col not in to_buy_df.columns:
                    to_buy_df[col] = None

            if not to_buy_df.empty:
                # logger.warning(f"⚠️ 发现需买入的标的: {len(to_buy_df)} 条\n{to_buy_df[['股票名称']].to_string(index=False)}")
                to_buy_df['操作'] = '买入'
                logger.warning(f"⚠️ 发现需买入的标的: {len(to_buy_df)} 条\n{to_buy_df}")
                # 添加操作列
               # 打印具体需要买入的股票
                # logger.info(f"具体需买入的标的:}")
            else:
                logger.info("✅ 当前无需买入的标的")

            # 合并两个df，确保列顺序一致
            # 先确保两个DataFrame都有相同的列
            common_columns = list(set(to_sell_df.columns) | set(to_buy_df.columns))
            for col in common_columns:
                if col not in to_sell_df.columns:
                    to_sell_df[col] = None
                if col not in to_buy_df.columns:
                    to_buy_df[col] = None
            
            # 按照统一的列顺序重新排列
            column_order = ['名称', '股票名称', '代码', '市场', '最新价', '新比例%', '时间', '行业', '账户名', '操作']
            # 添加其他可能存在的列
            for col in common_columns:
                if col not in column_order:
                    column_order.append(col)
            
            to_sell_df = to_sell_df[column_order]
            to_buy_df = to_buy_df[column_order]

            # 合并两个df
            difference_report = pd.concat([to_sell_df, to_buy_df], ignore_index=True)
            # # 构建完整差异报告
            # difference_report = {
            #     "to_sell": to_sell_df,
            #     "to_buy": to_buy_df
            # }
            logger.info(f"完成：对比持仓差异")
            # logger.info(f"完成：对比持仓差异 {len(difference_report)}条 \n{difference_report}")
            logger.info("-" * 50)
            return difference_report

        except Exception as e:
            error_msg = f"处理持仓差异时发生错误: {e}"
            logger.error(error_msg, exc_info=True)
            return {"error": error_msg}

    def operate_result(self, holding_file, Account_holding_file, account_name=None, strategy_filter=None):
        """
        执行调仓操作，包含异常处理和重试机制
        :param holding_file: 持仓文件路径
        :param Account_holding_file: 今日调仓文件路径
        :param account_name: 账户名称
        :param strategy_filter: 策略过滤函数，用于筛选特定策略的数据
        """
        if account_name is None:
            account_name = self.account_name

        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                # 1.获取持仓差异（首次获取，使用缓存）
                diff_result_df = self.get_difference_holding(holding_file, Account_holding_file, account_name)

                if 'error' in diff_result_df:
                    logger.error(f"获取持仓差异失败: {diff_result_df['error']}")
                    return False

                # 2.过滤已执行的操作
                filtered_diff_result = self.filter_executed_operations(diff_result_df, account_name)
                
                to_sell = filtered_diff_result.get('to_sell', pd.DataFrame())
                to_buy = filtered_diff_result.get('to_buy', pd.DataFrame())
                
                # 应用策略过滤器（如果提供）
                if strategy_filter:
                    # 对买入和卖出操作都应用过滤器
                    if not to_sell.empty and '名称' in to_sell.columns:
                        to_sell = to_sell[to_sell.apply(strategy_filter, axis=1)]
                        
                    if not to_buy.empty and '名称' in to_buy.columns:
                        to_buy = to_buy[to_buy.apply(strategy_filter, axis=1)]
                        
                    logger.info(f"应用策略过滤器后，需卖出: {len(to_sell)} 条，需买入: {len(to_buy)} 条")

                # 3.检查是否需要执行任何操作
                if to_sell.empty and to_buy.empty:
                    logger.info("✅ 当前无持仓差异，无需执行交易")
                    return True

                # 标记是否执行了任何交易操作
                any_trade_executed = False

                # 遍历每一项卖出操作，执行交易
                for idx, op in to_sell.iterrows():
                    stock_name = op['股票名称'] if '股票名称' in op else op['标的名称']
                    operation = op['操作']
                    # 安全获取可能不存在的字段
                    new_ratio = op.get('新比例%', None)
                    strategy_name = op.get('名称', None)
                    account_name_op = op.get('账户名', self.account_name)  # 使用默认账户名
                    code = op.get('代码', None)

                    logger.info(f"🛠️ 要处理: {operation} {stock_name} {new_ratio} {strategy_name} {account_name_op}")

                    # 切换到对应账户
                    self.common_page.change_account(account_name_op)
                    logger.info(f"✅ 已切换到账户: {account_name_op}")

                    # 调用交易逻辑
                    status, info = self.trader.operate_stock(operation, stock_name, new_ratio)

                    # 检查交易是否成功执行
                    if status is None:
                        logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                        continue

                    # 标记已执行交易
                    any_trade_executed = True

                    # 构造记录
                    operate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    record = pd.DataFrame([{
                        '名称': strategy_name if strategy_name is not None else '',
                        '股票名称': stock_name,
                        '操作': operation,
                        '新比例%': new_ratio if new_ratio is not None else 0,
                        '状态': status,
                        '信息': info,
                        '账户': account_name_op,  # 执行账户
                        '时间': operate_time
                    }])

                    # 写入历史
                    write_operation_history(record)
                    logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

                # 遍历每一项买入操作，执行交易
                for idx, op in to_buy.iterrows():
                    stock_name = op['股票名称'] if '股票名称' in op else op['标的名称']
                    operation = op['操作']
                    # 安全获取可能不存在的字段
                    new_ratio = op.get('新比例%', None)
                    strategy_name = op.get('名称', None)
                    account_name_op = op.get('账户名', self.account_name)  # 使用默认账户名
                    code = op.get('代码', None)

                    logger.info(f"🛠️ 要处理: {operation} {stock_name} {new_ratio} {strategy_name} {account_name_op}")

                    # 切换到对应账户
                    self.common_page.change_account(account_name_op)
                    logger.info(f"✅ 已切换到账户: {account_name_op}")

                    # 特殊处理：AI市场追踪策略买入时使用固定股数100股
                    if strategy_name == "AI市场追踪策略" and operation == "买入":
                        fixed_volume = 100  # 固定买入100股
                        logger.info(f"🎯 AI市场追踪策略特殊处理: 买入 {stock_name} 固定数量 {fixed_volume} 股")
                        status, info = self.trader.operate_stock(operation, stock_name, volume=fixed_volume)
                    else:
                        # 默认处理：使用固定数量或新比例%
                        status, info = self.trader.operate_stock(operation, stock_name, new_ratio)

                    # 检查交易是否成功执行
                    if status is None:
                        logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                        continue

                    # 标记已执行交易
                    any_trade_executed = True

                    # 构造记录
                    operate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    record = pd.DataFrame([{
                        '名称': strategy_name if strategy_name is not None else '',
                        '股票名称': stock_name,
                        '操作': operation,
                        '新比例%': new_ratio if new_ratio is not None else 0,
                        '状态': status,
                        '信息': info,
                        '账户': account_name_op,  # 执行账户
                        '时间': operate_time
                    }])

                    # 写入历史
                    write_operation_history(record)
                    logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

                # 只有在执行了交易操作后，才标记需要更新账户数据
                if any_trade_executed:
                    self._account_updated_in_this_run = False  # 下次需要更新账户数据
                    logger.info("✅ 标记下次需要更新账户数据")

                return True  # 成功执行

            except Exception as e:
                retry_count += 1
                error_msg = f"❌ 第 {retry_count} 次执行出现异常: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_msg)

                # 发送通知
                send_notification(f"策略调仓执行异常: {str(e)}")

                if retry_count < max_retries:
                    logger.info(f"等待10秒后进行第 {retry_count + 1} 次重试...")
                    time.sleep(10)

                    # 尝试重新进入交易页面
                    try:
                        self.common_page.goto_trade_page()
                        logger.info("✅ 成功重新进入交易页面")
                    except Exception as page_error:
                        logger.error(f"重新进入交易页面失败: {str(page_error)}")
                else:
                    logger.error("❌ 已达到最大重试次数，程序终止")
                    send_notification("策略调仓执行失败，已达到最大重试次数")
                    return False

        return False

    def reset_cache(self):
        """重置缓存"""
        self._account_holding_cache = None
        self._last_account_update_time = 0
        self._account_updated_in_this_run = False
        logger.info("✅ 缓存已重置")

    def get_real_time_price(self, stock_name):
        """
        获取股票实时价格（简化实现，实际应调用真实接口）
        :param stock_name: 股票名称
        :return: 实时价格
        """
        # 这里应该调用实际的接口获取实时价格
        # 作为示例，我们返回一个固定价格
        # 在实际应用中，应根据股票名称获取对应代码，然后调用行情接口获取实时价格
        
        # 示例实现：返回随机价格作为演示
        import random
        price = round(random.uniform(5, 50), 2)  # 5到50之间的随机价格
        logger.info(f"获取股票 {stock_name} 实时价格: {price}")
        return price

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
        
        try:
            # 读取账户信息
            if not os.path.exists(account_file):
                logger.error(f"账户持仓文件不存在: {account_file}")
                return None
                
            with pd.ExcelFile(account_file, engine='openpyxl') as xls:
                # 读取账户表头数据（包含可用余额）
                header_sheet_name = f"{account_name}_表头数据"
                if header_sheet_name in xls.sheet_names:
                    header_df = pd.read_excel(xls, sheet_name=header_sheet_name)
                    if not header_df.empty:
                        # 获取可用余额
                        available_balance = float(str(header_df.iloc[0]['可用']).replace(',', ''))
                        logger.info(f"账户 {account_name} 可用余额: {available_balance}")
                    else:
                        logger.error(f"账户 {account_name} 表头数据为空")
                        return None
                else:
                    logger.error(f"账户文件中不存在表头数据表: {header_sheet_name}")
                    return None
                    
                # 读取账户持仓数据
                holding_sheet_name = f"{account_name}_持仓数据"
                if holding_sheet_name in xls.sheet_names:
                    holding_df = pd.read_excel(xls, sheet_name=holding_sheet_name)
                    if not holding_df.empty and '标的名称' in holding_df.columns:
                        logger.info(f"成功读取账户 {account_name} 的持仓数据，共 {len(holding_df)} 条记录")
                    else:
                        logger.warning(f"账户 {account_name} 持仓数据为空或不包含标的名称列")
                        holding_df = pd.DataFrame()
                else:
                    logger.warning(f"账户文件中没有 {account_name} 的持仓数据表: {holding_sheet_name}")
                    holding_df = pd.DataFrame()
            
            # 计算买入股数
            if operation_type == '买入':
                # 获取实时价格
                real_price = self.get_real_time_price(stock_name)
                
                # 计算目标金额 = 可用余额 * 新比例%
                target_amount = available_balance * (float(new_ratio) / 100)
                logger.info(f"目标投资金额: {available_balance} * {new_ratio}% = {target_amount}")
                
                # 计算股数 = 目标金额 / 实时价格
                volume = int(target_amount / real_price)
                logger.info(f"计算股数: {target_amount} / {real_price} = {volume}")
                
                # 转换为100的倍数
                volume = (volume // 100) * 100
                if volume < 100:
                    logger.warning("计算出的买入股数不足100股")
                    return None
                    
                logger.info(f"买入 {stock_name}，股数: {volume}")
                return volume
                
            # 计算卖出股数
            elif operation_type == '卖出':
                if holding_df.empty:
                    logger.error("账户持仓数据为空，无法计算卖出数量")
                    return None
                    
                # 查找要卖出的股票
                stock_row = holding_df[holding_df['标的名称'] == stock_name]
                if stock_row.empty:
                    logger.error(f"在账户持仓中未找到股票: {stock_name}")
                    return None
                    
                stock_row = stock_row.iloc[0]
                # 获取持有数量
                holding_shares = int(stock_row.get('持仓', 0))
                logger.info(f"股票 {stock_name} 当前持有数量: {holding_shares}")
                
                # 如果新比例为0或未提供，则全仓卖出
                if new_ratio is None or float(new_ratio) <= 0:
                    volume = holding_shares
                    logger.info(f"新比例为0或未提供，全仓卖出 {stock_name}: {volume} 股")
                else:
                    # 计算需要保留的股数
                    keep_shares = int(holding_shares * (float(new_ratio) / 100))
                    # 计算需要卖出的股数
                    volume = holding_shares - keep_shares
                    logger.info(f"按比例计算卖出: 持有{holding_shares}股, 新比例{new_ratio}%, 保留{keep_shares}股, 卖出{volume}股")
                
                # 转换为100的倍数
                volume = (volume // 100) * 100
                if volume < 100:
                    logger.warning(f"计算出的卖出股数不足100股: {volume}")
                    
                logger.info(f"卖出 {stock_name}，股数: {volume}")
                return volume
                
            else:
                logger.error(f"不支持的操作类型: {operation_type}")
                return None
                
        except Exception as e:
            logger.error(f"计算交易股数时发生错误: {e}")
            return None

    def demo_calculate_trade(self):
        """
        演示如何使用calculate_trade_volume函数
        """
        # 示例参数
        account_file = Account_holding_file  # 账户持仓文件
        account_name = "川财证券"  # 账户名称
        strategy_name = "逻辑为王"  # 策略名称
        stock_name = "先进数通"  # 股票名称
        new_ratio = 32.87  # 新比例
        operation_type = "买入"  # 操作类型
        
        # 计算买入股数
        volume = self.calculate_trade_volume(
            account_file=account_file,
            account_name=account_name,
            strategy_name=strategy_name,
            stock_name=stock_name,
            new_ratio=new_ratio,
            operation_type=operation_type
        )
        
        if volume:
            logger.info(f"计算结果: {operation_type} {stock_name} {volume} 股")
        else:
            logger.error("计算失败")

    def operate_strategy(self, strategy_name: str, account_name: str = None) -> bool:
        """执行策略"""
        diff = com.extract_different_holding(account_file, account_name, strategy_file, strategy_name)
        filtered_result = com.filter_executed_operations(diff, account_name)
        to_sell = filtered_result.get('to_sell', pd.DataFrame())
        to_buy = filtered_result.get('to_buy', pd.DataFrame())

        # 标记是否执行了任何交易操作
        any_trade_executed = False

        # 遍历每一项卖出操作，执行交易
        for idx, op in to_sell.iterrows():
            stock_name = op['股票名称'] if '股票名称' in op else op['标的名称']
            operation = op['操作']
            # 安全获取可能不存在的字段
            new_ratio = op.get('新比例%', None)
            if operation == '卖出':
                new_ratio = 0

            logger.info(f"🛠️ 开始处理: {operation} {stock_name} {new_ratio} {strategy_name} {account_name}")

            # 切换到对应账户
            self.common_page.change_account(account_name)
            logger.info(f"✅ 已切换到账户: {account_name}")

            # 调用交易逻辑
            status, info = self.trader.operate_stock(operation, stock_name, new_ratio)

            # 检查交易是否成功执行
            if status is None:
                logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                continue

            # 标记已执行交易
            any_trade_executed = True

        # 遍历每一项买入操作，执行交易
        for idx, op in to_buy.iterrows():
            stock_name = op['股票名称'] if '股票名称' in op else op['标的名称']
            operation = op['操作']
            # 安全获取可能不存在的字段
            new_ratio = op.get('新比例%', None)

            logger.info(f"🛠️ 开始处理: {operation} {stock_name} {new_ratio} {strategy_name} {account_name}")

            # 切换到对应账户
            self.common_page.change_account(account_name)
            logger.info(f"✅ 已切换到账户: {account_name}")

            # 调用交易逻辑
            status, info = self.trader.operate_stock(operation, stock_name, new_ratio)

            # 检查交易是否成功执行
            if status is None:
                logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                continue

            # 标记已执行交易
            any_trade_executed = True

        print(diff)
        print('-' * 50)
        print("需要卖出的股票:")
        print(to_sell)
        print("需要买入的股票:")
        print(to_buy)

if __name__ == '__main__':
    # 定义文件路径
    # account_holding_main()
    # account_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Account_position.xlsx"
    # strategy_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Strategy_position.xlsx"
    # trade_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\portfolio\trade_operations.xlsx"
    com = CommonHoldingProcessor()

    strategy_file =r"E:\git_documents\Investment\Investment\THS\AutoTrade\data\position\Strategy_position.xlsx"
    account_file = r'E:\git_documents\Investment\Investment\THS\AutoTrade\data\position\Account_position.xlsx'
    trade_file = r'E:\git_documents\Investment\Investment\THS\AutoTrade\data\portfolio\trade_operations.xlsx'
    account_name = '川财证券'
    strategy_name = 'AI市场追踪策略'
    # diff = com.get_difference_holding(account_file, '长城证券',strategy_file, 'AI市场追踪策略' )
    # diff = com.get_difference_holding(r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Combination_position.xlsx", r'D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\account_info.xlsx',account_name="中泰证券")
    diff = com.extract_different_holding(account_file, account_name, strategy_file, strategy_name)
    to_operate = com.filter_executed_operations(diff,account_name)

    com.operate_strategy(strategy_name,account_name)
    print(diff)
    print('-'*50)
    print(to_operate)