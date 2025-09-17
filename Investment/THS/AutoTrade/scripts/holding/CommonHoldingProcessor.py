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
    Combination_holding_file, all_ids, id_to_name
)
from Investment.THS.AutoTrade.pages.account_info import AccountInfo
from Investment.THS.AutoTrade.pages.page_common import CommonPage
from Investment.THS.AutoTrade.scripts.data_process import write_operation_history, save_to_excel_append, read_operation_history
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
            account_info = AccountInfo()
            update_success = account_info.update_holding_info_for_account(account_name)
            if not update_success:
                logger.warning(f"更新{account_name}账户持仓数据失败")
                return False

            # 读取指定账户持仓数据
            account_df = pd.DataFrame()
            try:
                with pd.ExcelFile(account_file, engine='openpyxl') as xls:
                    # 只读取指定账户的持仓数据
                    sheet_name = f"{account_name}_持仓数据"
                    if sheet_name in xls.sheet_names:
                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        if not df.empty and '标的名称' in df.columns:
                            # 只保留标的名称列
                            account_df = df[['标的名称']].copy()
                            account_df['账户'] = account_name
                            logger.info(f"✅ 成功缓存{account_name}账户的持仓数据，共 {len(account_df)} 条记录")
                        else:
                            logger.warning(f"{account_name}账户持仓数据为空或不包含标的名称列")
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
    def get_difference_holding(self, holding_file, account_file, account_name=None, strategy_filter=None):
        """
        对比账户实际持仓与策略/组合今日持仓数据，找出差异：
            - 需要卖出：在账户中存在，但不在策略/组合今日持仓中；
            - 需要买入：在策略/组合今日持仓中存在，但不在账户中；
        :param holding_file: 持仓文件路径
        :param account_file: 账户文件路径
        :param account_name: 账户名称
        :param strategy_filter: 策略过滤函数，用于筛选特定策略的数据
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

            # 判断是否需要更新账户数据
            if self._should_update_account_data():
                update_result = self._update_account_holding_cache(account_file, account_name)
                if not update_result:
                    return {"error": f"更新{account_name}账户持仓数据失败"}
            else:
                logger.info(f"✅ 使用缓存的{account_name}账户持仓数据")

            # 读取策略/组合今日持仓数据（这部分始终实时读取，不缓存）
            today = str(datetime.date.today())
            try:
                if os.path.exists(holding_file):
                    with pd.ExcelFile(holding_file, engine='openpyxl') as xls:
                        if today in xls.sheet_names:
                            today_strategy_df = pd.read_excel(xls, sheet_name=today)
                            if today_strategy_df.empty:
                                logger.warning("接口持仓文件为空")
                                today_strategy_df = pd.DataFrame(columns=['标的名称'])
                        else:
                            logger.warning(f"接口持仓文件中没有今天的sheet: {today}")
                            today_strategy_df = pd.DataFrame(columns=['标的名称'])
                else:
                    logger.warning("接口持仓文件不存在")
                    today_strategy_df = pd.DataFrame(columns=['标的名称'])
            except Exception as e:
                logger.error(f"读取接口持仓文件失败: {e}")
                today_strategy_df = pd.DataFrame(columns=['标的名称'])

            # 应用策略过滤器（如果提供）
            if strategy_filter and not today_strategy_df.empty and '名称' in today_strategy_df.columns:
                today_strategy_df = today_strategy_df[today_strategy_df.apply(strategy_filter, axis=1)]
                logger.info(f"应用策略过滤器后，策略数据条数: {len(today_strategy_df)}")

            # 需要排除的标的名称
            excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

            # 标准化股票名称
            from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe_stock_names
            if not self._account_holding_cache.empty:
                self._account_holding_cache = standardize_dataframe_stock_names(self._account_holding_cache)
            if not today_strategy_df.empty:
                today_strategy_df = standardize_dataframe_stock_names(today_strategy_df)

            # 1. 找出需要卖出的标的（在账户中存在，但不在策略/组合今日持仓中，且不在排除列表中）
            if not self._account_holding_cache.empty and not today_strategy_df.empty:
                to_sell_candidates = self._account_holding_cache[~self._account_holding_cache['标的名称'].isin(today_strategy_df['标的名称'])]
                to_sell_df = to_sell_candidates[~to_sell_candidates['标的名称'].isin(excluded_holdings)].copy()
            elif not self._account_holding_cache.empty:
                # 如果策略/组合持仓为空，则所有账户持仓都是需要卖出的（除去排除项）
                to_sell_df = self._account_holding_cache[~self._account_holding_cache['标的名称'].isin(excluded_holdings)].copy()
            else:
                to_sell_df = pd.DataFrame(columns=self._account_holding_cache.columns) if self._account_holding_cache is not None and not self._account_holding_cache.empty else pd.DataFrame()

            if not to_sell_df.empty:
                # logger.warning(f"⚠️ 发现需卖出的标的: {len(to_sell_df)} 条\n{to_sell_df[['标的名称']].to_string(index=False)}")
                to_sell_df['操作'] = '卖出'
                logger.warning(f"⚠️ 发现需卖出的标的: {len(to_sell_df)} 条\n{to_sell_df}")
                # 添加操作列
                # 打印具体需要卖出的股票
                # logger.info(f"具体需卖出的标的:")
            else:
                logger.info("✅ 当前无需卖出的标的")

            # 2. 找出需要买入的标的（在策略/组合今日持仓中存在，但不在账户中，且不在排除列表中）
            if not today_strategy_df.empty and not self._account_holding_cache.empty:
                to_buy_candidates = today_strategy_df[~today_strategy_df['标的名称'].isin(self._account_holding_cache['标的名称'])]
                to_buy_df = to_buy_candidates[~to_buy_candidates['标的名称'].isin(excluded_holdings)]
            elif not today_strategy_df.empty:
                # 如果账户持仓为空，则所有策略/组合持仓都是需要买入的（除去排除项）
                to_buy_df = today_strategy_df[~today_strategy_df['标的名称'].isin(excluded_holdings)]
            else:
                to_buy_df = pd.DataFrame(columns=['标的名称'])

            if not to_buy_df.empty:
                # logger.warning(f"⚠️ 发现需买入的标的: {len(to_buy_df)} 条\n{to_buy_df[['标的名称']].to_string(index=False)}")
                to_buy_df['操作'] = '买入'
                logger.warning(f"⚠️ 发现需买入的标的: {len(to_buy_df)} 条\n{to_buy_df}")
                # 添加操作列
               # 打印具体需要买入的股票
                # logger.info(f"具体需买入的标的:}")
            else:
                logger.info("✅ 当前无需买入的标的")

            # 构建完整差异报告
            difference_report = {
                "to_sell": to_sell_df,
                "to_buy": to_buy_df
            }
            logger.info(f"完成：对比持仓差异")
            # logger.info(f"完成：对比持仓差异 {len(difference_report)}条 \n{difference_report}")
            logger.info("-" * 50)
            return difference_report

        except Exception as e:
            error_msg = f"处理持仓差异时发生错误: {e}"
            logger.error(error_msg, exc_info=True)
            return {"error": error_msg}

    def operate_result(self, holding_file, portfolio_today_file, account_name=None, strategy_filter=None):
        """
        执行调仓操作，包含异常处理和重试机制
        :param holding_file: 持仓文件路径
        :param portfolio_today_file: 今日调仓文件路径
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
                diff_result_df = self.get_difference_holding(holding_file, Account_holding_file, account_name, strategy_filter)

                if 'error' in diff_result_df:
                    logger.error(f"获取持仓差异失败: {diff_result_df['error']}")
                    return False

                to_sell = diff_result_df.get('to_sell', pd.DataFrame())
                to_buy = diff_result_df.get('to_buy', pd.DataFrame())
                
                # 应用策略过滤器（如果提供）
                if strategy_filter:
                    # 对买入和卖出操作都应用过滤器
                    if not to_sell.empty and '名称' in to_sell.columns:
                        to_sell = to_sell[to_sell.apply(strategy_filter, axis=1)]
                        
                    if not to_buy.empty and '名称' in to_buy.columns:
                        to_buy = to_buy[to_buy.apply(strategy_filter, axis=1)]
                        
                    logger.info(f"应用策略过滤器后，需卖出: {len(to_sell)} 条，需买入: {len(to_buy)} 条")

                # 2.检查是否需要执行任何操作
                if to_sell.empty and to_buy.empty:
                    logger.info("✅ 当前无持仓差异，无需执行交易")
                    return True

                # 提取difference_report里的’标的名称'列
                def extract_stock_to_operate():
                    '''
                    1.对比历史数据，提取要操作的

                    '''
                    # 读取操作历史记录
                    try:
                        history_df = read_operation_history(OPERATION_HISTORY_FILE)
                    except Exception as e:
                        logger.error(f"读取操作历史记录失败: {e}")
                        history_df = pd.DataFrame(columns=['标的名称', '操作', '新比例%'])

                    # 准备所有要操作的列表
                    all_operations = []
                    # 对比history_df和diff_result_df,找出差异
                    if not history_df.empty:
                        exists = history_df[
                            (history_df['标的名称'] == diff_result_df['标的名称']) &
                            (history_df['操作'] == diff_result_df['操作']) &
                            (abs(history_df['新比例%'] - new_ratio) < 0.01)
                        ]

                        if not exists.empty:
                            logger.info(f"✅ 卖出 {stock_name} 已在历史记录中存在，跳过")
                            all_operations.append([~exists])

                    # 检查是否有需要执行的操作
                    if not all_operations:
                        logger.info("✅ 所有操作均已执行过，无需重复操作")
                        return True

                    return all_operations

                all_operations = extract_stock_to_operate()

                # # 准备保存到今日调仓文件的数据
                # today_trades = []

                # 标记是否执行了任何交易操作
                any_trade_executed = False

                # 遍历每一项操作，执行交易
                for op in all_operations:
                    stock_name = op['标的名称']
                    operation = op['操作']
                    new_ratio = op['新比例%']
                    strategy_name = op['名称']
                    account_name = op['账户名']

                    code = op['代码']

                    logger.info(f"🛠️ 要处理: {operation} {stock_name} {new_ratio} {strategy_name} {account_name}")

                    # 切换到对应账户
                    self.common_page.change_account(account_name)
                    logger.info(f"✅ 已切换到账户: {account_name}")

                    # 调用交易逻辑
                    # 特殊处理：AI市场追踪策略买入时使用固定股数100股
                    if strategy_name == "AI市场追踪策略" and operation == "买入":
                        fixed_volume = 100  # 固定买入100股
                        logger.info(f"🎯 AI市场追踪策略特殊处理: 买入 {stock_name} 固定数量 {fixed_volume} 股")
                        status, info = self.trader.operate_stock(operation, stock_name, volume=fixed_volume)
                    else:
                        # 默认处理：使用固定数量或新比例%
                        # if operation == "买入":
                        status, info = self.trader.operate_stock(operation, stock_name, new_ratio)
                        # else:
                        #     status, info = self.trader.operate_stock(
                        #         operation=operation,
                        #         stock_name=stock_name,
                        #         volume=None,
                        #         new_ratio=new_ratio
                        #     )

                    # 检查交易是否成功执行
                    if status is None:
                        logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                        continue

                    # 标记已执行交易
                    any_trade_executed = True

                    # 构造记录
                    operate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    record = pd.DataFrame([{
                        '名称': strategy_name,
                        '标的名称': stock_name,
                        '操作': operation,
                        '新比例%': new_ratio if new_ratio is not None else 0,
                        '状态': status,
                        '信息': info,
                        '账户': account_name,  # 执行账户
                        '时间': operate_time
                    }])

                    # 写入历史
                    write_operation_history(record)
                    logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

                    # # 添加到今日调仓数据中
                    # # code =
                    # today_trades.append({
                    #     '名称': strategy_name,  # 策略名称
                    #     '操作': operation,
                    #     '标的名称': stock_name,
                    #     '代码': '',  # 代码信息在当前数据中不可用
                    #     '最新价': 0,  # 价格信息在当前数据中不可用
                    #     '新比例%': new_ratio if new_ratio is not None else 0,
                    #     '市场': '沪深A股',  # 默认市场
                    #     '时间': datetime.datetime.now().strftime('%Y-%m-%d')
                    # })

                # 只有在执行了交易操作后，才标记需要更新账户数据
                if any_trade_executed:
                    self._account_updated_in_this_run = False  # 下次需要更新账户数据
                    logger.info("✅ 标记下次需要更新账户数据")

                # # 将今日调仓数据保存到对应文件
                # if today_trades:
                #     today_trades_df = pd.DataFrame(today_trades)
                #     today = datetime.datetime.now().strftime('%Y-%m-%d')
                #
                #     try:
                #         # 如果文件存在，读取现有数据
                #         if os.path.exists(portfolio_today_file):
                #             with pd.ExcelFile(portfolio_today_file) as xls:
                #                 # 读取除今天以外的所有现有工作表
                #                 all_sheets_data = {}
                #                 for sheet_name in xls.sheet_names:
                #                     if sheet_name != today:
                #                         all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
                #
                #             # 将今天的数据放在第一位
                #             all_sheets_data = {today: today_trades_df, **all_sheets_data}
                #         else:
                #             # 文件不存在，创建新文件
                #             all_sheets_data = {today: today_trades_df}
                #
                #         # 写入所有数据到Excel文件
                #         with pd.ExcelWriter(portfolio_today_file, engine='openpyxl') as writer:
                #             for sheet_name, df in all_sheets_data.items():
                #                 df.to_excel(writer, sheet_name=sheet_name, index=False)
                #
                #         logger.info(f"✅ 今日调仓数据已保存到 {portfolio_today_file}，sheet: {today}")
                #     except Exception as e:
                #         logger.error(f"❌ 保存今日调仓数据失败: {e}")

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