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
    Strategy_id_to_name, Strategy_ids, Ai_Strategy_holding_file,
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
        account_info = AccountInfo()
        update_success = account_info.update_holding_info_for_account(account_name)
        if not update_success:
            logger.warning(f"更新{account_name}账户持仓数据失败")
            return False
            
        # 读取并缓存账户持仓数据
        try:
            with pd.ExcelFile(account_file, engine='openpyxl') as xls:
                sheet_name = f"{account_name}_持仓数据"
                if sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    if not df.empty and '标的名称' in df.columns:
                        self._account_holding_cache = df[['标的名称']].copy()
                        self._account_holding_cache['账户'] = account_name
                        logger.info(f"✅ 成功缓存{account_name}账户的持仓数据，共 {len(self._account_holding_cache)} 条记录")
                    else:
                        self._account_holding_cache = pd.DataFrame(columns=['标的名称', '账户'])
                        logger.warning(f"{account_name}账户持仓数据为空或不包含标的名称列")
                else:
                    self._account_holding_cache = pd.DataFrame(columns=['标的名称', '账户'])
                    logger.warning(f"账户文件中没有{account_name}的持仓数据表: {sheet_name}")
            self._last_account_update_time = time.time()
            self._account_updated_in_this_run = True
            return True
        except Exception as e:
            logger.error(f"读取{account_name}账户持仓文件失败: {e}")
            return False

    # 获取账户持仓数据差异
    def get_difference_holding(self, holding_file, account_file, account_name=None):
        """
        对比账户实际持仓与策略/组合今日持仓数据，找出差异：
            - 需要卖出：在账户中存在，但不在策略/组合今日持仓中；
            - 需要买入：在策略/组合今日持仓中存在，但不在账户中；
        """
        logger.info("-" * 50)
        logger.info(f"开始：对比账户实际持仓与{holding_file}数据...")
        if account_name is None:
            account_name = self.account_name

        try:
            # 检查必要文件是否存在
            required_files = {
                "账户持仓文件": account_file,
                "策略/组合持仓文件": holding_file,
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
                            strategy_df = pd.read_excel(xls, sheet_name=today)
                            if strategy_df.empty:
                                logger.warning("策略/组合持仓文件为空")
                                strategy_df = pd.DataFrame(columns=['标的名称'])
                        else:
                            logger.warning(f"策略/组合持仓文件中没有今天的sheet: {today}")
                            strategy_df = pd.DataFrame(columns=['标的名称'])
                else:
                    logger.warning("策略/组合持仓文件不存在")
                    strategy_df = pd.DataFrame(columns=['标的名称'])
            except Exception as e:
                logger.error(f"读取策略/组合持仓文件失败: {e}")
                strategy_df = pd.DataFrame(columns=['标的名称'])

            # 需要排除的标的名称
            excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

            # 1. 找出需要卖出的标的（在账户中存在，但不在策略/组合今日持仓中，且不在排除列表中）
            if not self._account_holding_cache.empty and not strategy_df.empty:
                to_sell_candidates = self._account_holding_cache[~self._account_holding_cache['标的名称'].isin(strategy_df['标的名称'])]
                to_sell = to_sell_candidates[~to_sell_candidates['标的名称'].isin(excluded_holdings)].copy()
            elif not self._account_holding_cache.empty:
                # 如果策略/组合持仓为空，则所有账户持仓都是需要卖出的（除去排除项）
                to_sell = self._account_holding_cache[~self._account_holding_cache['标的名称'].isin(excluded_holdings)].copy()
            else:
                to_sell = pd.DataFrame(columns=self._account_holding_cache.columns) if self._account_holding_cache is not None and not self._account_holding_cache.empty else pd.DataFrame()

            if not to_sell.empty:
                logger.warning(f"⚠️ 发现需卖出的标的: {len(to_sell)} 条")
                # 添加操作列
                to_sell['操作'] = '卖出'
            else:
                logger.info("✅ 当前无需卖出的标的")

            # 2. 找出需要买入的标的（在策略/组合今日持仓中存在，但不在账户中，且不在排除列表中）
            if not strategy_df.empty and not self._account_holding_cache.empty:
                to_buy_candidates = strategy_df[~strategy_df['标的名称'].isin(self._account_holding_cache['标的名称'])]
                to_buy = to_buy_candidates[~to_buy_candidates['标的名称'].isin(excluded_holdings)]
            elif not strategy_df.empty:
                # 如果账户持仓为空，则所有策略/组合持仓都是需要买入的（除去排除项）
                to_buy = strategy_df[~strategy_df['标的名称'].isin(excluded_holdings)]
            else:
                to_buy = pd.DataFrame(columns=['标的名称'])

            if not to_buy.empty:
                logger.warning(f"⚠️ 发现需买入的标的: {len(to_buy)} 条")
                # 添加操作列
                to_buy['操作'] = '买入'
            else:
                logger.info("✅ 当前无需买入的标的")

            # 构建完整差异报告
            difference_report = {
                "to_sell": to_sell,
                "to_buy": to_buy
            }
            logger.info("完成：对比持仓差异")
            logger.info("-" * 50)
            return difference_report

        except Exception as e:
            error_msg = f"处理持仓差异时发生错误: {e}"
            logger.error(error_msg, exc_info=True)
            return {"error": error_msg}

    def operate_result(self, holding_file, portfolio_today_file, account_name=None):
        """
        执行调仓操作，包含异常处理和重试机制
        """
        if account_name is None:
            account_name = self.account_name

        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                # 获取持仓差异（首次获取，使用缓存）
                diff_result = self.get_difference_holding(holding_file, Account_holding_file, account_name)

                if 'error' in diff_result:
                    logger.error(f"获取持仓差异失败: {diff_result['error']}")
                    return False

                to_sell = diff_result.get('to_sell', pd.DataFrame())
                to_buy = diff_result.get('to_buy', pd.DataFrame())

                # 检查是否需要执行任何操作
                if to_sell.empty and to_buy.empty:
                    logger.info("✅ 当前无持仓差异，无需执行交易")
                    return True

                # 读取操作历史记录
                try:
                    history_df = read_operation_history(OPERATION_HISTORY_FILE)
                except Exception as e:
                    logger.error(f"读取操作历史记录失败: {e}")
                    history_df = pd.DataFrame(columns=['标的名称', '操作', '新比例%'])

                # 准备所有操作的列表
                all_operations = []

                # 添加卖出操作（先执行卖出）
                if not to_sell.empty:
                    logger.info("🔍 检查卖出操作是否已执行...")
                    for _, row in to_sell.iterrows():
                        stock_name = row['标的名称']
                        operation = '卖出'
                        new_ratio = 0

                        # 检查是否已在历史记录中
                        if not history_df.empty:
                            exists = history_df[
                                (history_df['标的名称'] == stock_name) &
                                (history_df['操作'] == operation) &
                                (abs(history_df['新比例%'] - new_ratio) < 0.01)
                            ]

                            if not exists.empty:
                                logger.info(f"✅ 卖出 {stock_name} 已在历史记录中存在，跳过")
                                continue

                        all_operations.append({
                            'stock_name': stock_name,
                            'operation': operation,
                            'new_ratio': new_ratio,
                            'strategy_name': 'AI市场追踪策略' if account_name == "川财证券" else '组合策略'
                        })

                # 添加买入操作（后执行买入）
                if not to_buy.empty:
                    logger.info("🔍 检查买入操作是否已执行...")
                    # 按最新价从低到高排序买入操作
                    to_buy_sorted = to_buy.sort_values('最新价', ascending=True) if '最新价' in to_buy.columns else to_buy
                    if not to_buy_sorted.empty:
                        logger.info(f"📈 买入顺序（按价格从低到高）")

                    for _, row in to_buy_sorted.iterrows():
                        stock_name = row['标的名称']
                        operation = '买入'
                        new_ratio = None  # 买入时无需新比例

                        # 检查是否已在历史记录中
                        if not history_df.empty:
                            # 对于买入操作，我们检查是否已经买入该股票
                            exists = history_df[
                                (history_df['标的名称'] == stock_name) &
                                (history_df['操作'] == operation)
                            ]

                            if not exists.empty:
                                logger.info(f"✅ 买入 {stock_name} 已在历史记录中存在，跳过")
                                continue

                        all_operations.append({
                            'stock_name': stock_name,
                            'operation': operation,
                            'new_ratio': new_ratio,
                            'strategy_name': 'AI市场追踪策略' if account_name == "川财证券" else '组合策略'
                        })

                # 检查是否有需要执行的操作
                if not all_operations:
                    logger.info("✅ 所有操作均已执行过，无需重复操作")
                    return True

                # 准备保存到今日调仓文件的数据
                today_trades = []

                # 标记是否执行了任何交易操作
                any_trade_executed = False

                # 遍历每一项操作，执行交易
                for op in all_operations:
                    stock_name = op['stock_name']
                    operation = op['operation']
                    new_ratio = op['new_ratio']
                    strategy_name = op['strategy_name']

                    logger.info(f"🛠️ 要处理: {operation} {stock_name}")

                    # 切换到对应账户
                    self.common_page.change_account(account_name)
                    logger.info(f"✅ 已切换到账户: {account_name}")

                    # 调用交易逻辑
                    status, info = self.trader.operate_stock(
                        operation=operation,
                        stock_name=stock_name,
                        volume=100 if operation == "买入" else None,
                        new_ratio=new_ratio
                    )

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

                    # 添加到今日调仓数据中
                    today_trades.append({
                        '名称': strategy_name,  # 策略名称
                        '操作': operation,
                        '标的名称': stock_name,
                        '代码': '',  # 代码信息在当前数据中不可用
                        '最新价': 0,  # 价格信息在当前数据中不可用
                        '新比例%': new_ratio if new_ratio is not None else 0,
                        '市场': '沪深A股',  # 默认市场
                        '时间': datetime.datetime.now().strftime('%Y-%m-%d')
                    })

                # 只有在执行了交易操作后，才标记需要更新账户数据
                if any_trade_executed:
                    self._account_updated_in_this_run = False  # 下次需要更新账户数据
                    logger.info("✅ 标记下次需要更新账户数据")

                # 将今日调仓数据保存到对应文件
                if today_trades:
                    today_trades_df = pd.DataFrame(today_trades)
                    today = datetime.datetime.now().strftime('%Y-%m-%d')

                    try:
                        # 如果文件存在，读取现有数据
                        if os.path.exists(portfolio_today_file):
                            with pd.ExcelFile(portfolio_today_file) as xls:
                                # 读取除今天以外的所有现有工作表
                                all_sheets_data = {}
                                for sheet_name in xls.sheet_names:
                                    if sheet_name != today:
                                        all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

                            # 将今天的数据放在第一位
                            all_sheets_data = {today: today_trades_df, **all_sheets_data}
                        else:
                            # 文件不存在，创建新文件
                            all_sheets_data = {today: today_trades_df}

                        # 写入所有数据到Excel文件
                        with pd.ExcelWriter(portfolio_today_file, engine='openpyxl') as writer:
                            for sheet_name, df in all_sheets_data.items():
                                df.to_excel(writer, sheet_name=sheet_name, index=False)

                        logger.info(f"✅ 今日调仓数据已保存到 {portfolio_today_file}，sheet: {today}")
                    except Exception as e:
                        logger.error(f"❌ 保存今日调仓数据失败: {e}")

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