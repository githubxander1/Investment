import datetime
import os
from pprint import pprint

import pandas as pd
import requests
from fake_useragent import UserAgent

from Investment.THS.AutoTrade.config.settings import (
    Combination_headers, id_to_name, Account_holding_file, Combination_ids
)
from Investment.THS.AutoTrade.scripts.holding.account_info import AccountInfo
from Investment.THS.AutoTrade.pages.trading.trade_logic import TradeLogic
# from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

from Investment.THS.AutoTrade.utils.format_data import standardize_dataframe_stock_names

logger = setup_logger("combination_holding_processor.log")

ua = UserAgent()

# 账户到策略的映射
ACCOUNT_TO_STRATEGY = {
    '中山证券': '逻辑为王'
    # '中泰证券': '一枝梨花'
}

# 添加全局变量来跟踪是否需要更新账户数据
account_update_needed = True

class CombinationHoldingProcessor:
    def __init__(self):
        self.strategy_name = '逻辑为王'
        self.account_name = "川财证券"
        self.trader = TradeLogic()
        self.common_page = self.trader.common_page

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
                # print(positions)

                # 检查是否有持仓数据
                if not positions:
                    logger.info(f"组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})当前无持仓")
                    return pd.DataFrame()

                holding_data = []
                for position in positions:
                    code = str(position.get("code", "")).zfill(6)
                    from Investment.THS.AutoTrade.utils.format_data import determine_market
                    holding_data.append({
                        "策略名称": id_to_name.get(portfolio_id, f'组合{portfolio_id}'),
                        "股票名称": position.get("name", ""),
                        "代码": code,
                        "最新价": position.get("price", 0),
                        "成本价": position.get("costPrice", 0),
                        "新比例%": round(position.get("positionRealRatio", 0) * 100),
                        "市场": determine_market(code),
                        "收益率(%)": position.get("incomeRate", 0) * 100,
                        "盈亏比例(%)": position.get("profitLossRate", 0) * 100,
                        "时间": datetime.datetime.now().strftime('%m-%d %H:%M:%S')
                    })

                result_df = pd.DataFrame(holding_data)
                # 控制台输出展示要全,宽度最大，列宽最大，不要换行，回车
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.max_colwidth', None)
                pd.set_option('display.width', None)


                # pd.set_option('display.max_columns', None)
                # pd.set_option('display.max_colwidth', None)

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

    def _calculate_trade_volume_optimized(self, account_summary_df, account_holdings_df, strategy_holdings_df, strategy_name, stock_name, new_ratio, operation_type):
        """
        优化的计算交易数量函数，不读取文件，直接使用内存中的数据
        
        :param account_summary_df: 账户汇总数据DataFrame
        :param account_holdings_df: 账户持仓数据DataFrame
        :param strategy_holdings_df: 策略持仓数据DataFrame
        :param strategy_name: 策略名称
        :param stock_name: 股票名称
        :param new_ratio: 新持仓比例(%)
        :param operation_type: 操作类型('买入' 或 '卖出')
        :return: 计算出的交易股数
        """
        logger.info(f"开始计算交易股数(优化版): 股票={stock_name}, 操作={operation_type}, 新比例={new_ratio}%")
        
        # 从账户汇总数据中提取总资产等信息
        account_asset = 0.0
        account_balance = 0.0
        
        if account_summary_df is not None and not account_summary_df.empty:
            if '总资产' in account_summary_df.columns:
                # 修复：正确处理可能包含逗号的数字字符串
                total_asset_text = str(account_summary_df['总资产'].iloc[0]).replace(',', '')
                try:
                    account_asset = float(total_asset_text) if not account_summary_df.empty else 0.0
                except ValueError:
                    logger.warning(f"无法将总资产转换为浮点数: {total_asset_text}")
                    account_asset = 0.0
            if '可用' in account_summary_df.columns:
                # 修复：正确处理可能包含逗号的数字字符串
                available_text = str(account_summary_df['可用'].iloc[0]).replace(',', '')
                try:
                    account_balance = float(available_text) if not account_summary_df.empty else 0.0
                except ValueError:
                    logger.warning(f"无法将可用金额转换为浮点数: {available_text}")
                    account_balance = 0.0
        
        # 从账户持仓数据中提取股票信息
        stock_available = 0
        stock_ratio = 0
        stock_price = 0.0
        
        if account_holdings_df is not None and not account_holdings_df.empty:
            stock_data = account_holdings_df[account_holdings_df['股票名称'] == stock_name]
            if not stock_data.empty:
                if '可用' in stock_data.columns:
                    stock_available = int(stock_data['可用'].iloc[0]) if not pd.isna(stock_data['可用'].iloc[0]) else 0
                if '持仓占比' in stock_data.columns:
                    stock_ratio = float(stock_data['持仓占比'].iloc[0]) if not pd.isna(stock_data['持仓占比'].iloc[0]) else 0
                if '当前价' in stock_data.columns:
                    stock_price = float(stock_data['当前价'].iloc[0]) if not pd.isna(stock_data['当前价'].iloc[0]) else 0
        
        # 如果账户中没有该股票的价格信息，尝试从策略数据中获取
        if stock_price <= 0 and strategy_holdings_df is not None and not strategy_holdings_df.empty:
            strategy_stock_data = strategy_holdings_df[
                (strategy_holdings_df['策略名称'] == strategy_name) &
                (strategy_holdings_df['股票名称'] == stock_name)
            ]
            if not strategy_stock_data.empty and '最新价' in strategy_stock_data.columns:
                stock_price = float(strategy_stock_data['最新价'].iloc[0]) if not pd.isna(strategy_stock_data['最新价'].iloc[0]) else 0.01
        
        # 确保所有数值都是正确的数据类型
        try:
            account_asset = float(account_asset) if account_asset is not None else 0.0
            stock_price = float(stock_price) if stock_price is not None else 0.01
            # 检查new_ratio是否为有效值
            if new_ratio is not None and not (isinstance(new_ratio, float) and pd.isna(new_ratio)):
                new_ratio = float(new_ratio)
            else:
                new_ratio = 0.0
            stock_available = int(stock_available) if stock_available is not None else 0
        except (ValueError, TypeError) as e:
            logger.error(f"数据类型转换错误: {e}")
            return None
        
        # 计算买入或卖出股数
        try:
            if operation_type == '买入':
                volume = self.trader.calculate_buy_volume(account_asset, stock_price, new_ratio)
                logger.info(f"买入 {stock_name}，股数: {volume}")
                return volume

            elif operation_type == '卖出':
                volume = self.trader.calculate_sell_volume(account_asset, stock_available, stock_price, new_ratio)
                logger.info(f"卖出 {stock_name}，股数: {volume}")
                return volume
                
            else:
                logger.error(f"不支持的操作类型: {operation_type}")
                return None
                
        except Exception as e:
            logger.error(f"计算交易股数时发生错误: {e}")
            return None

    def _update_strategy_holdings(self):
        """
        更新策略持仓数据
        """
        logger.info("🔄 开始更新策略持仓数据...")
        strategy_holdings = []
        for id in Combination_ids:  # 只处理映射中的组合
            positions_df = self.get_single_holding_data(id)
            # 只保留沪深A股的
            if not positions_df.empty and '市场' in positions_df.columns:
                positions_df = positions_df[positions_df['市场'].isin(['沪深A股'])]
            # 检查并添加非空数据
            if positions_df is not None and not positions_df.empty:
                strategy_holdings.append(positions_df)
            else:
                logger.info(f"没有获取到组合数据，组合ID: {id}")

        # 检查是否获取到任何数据
        if not strategy_holdings:
            logger.warning("未获取到任何组合持仓数据")
            return None

        # 策略持仓汇总
        strategy_holdings_df = pd.concat(strategy_holdings, ignore_index=True)
        logger.info(f"策略持仓数据:{len(strategy_holdings_df)}\n{strategy_holdings_df}")
        return strategy_holdings_df

    def _update_account_holdings(self):
        """
        更新账户持仓数据
        """
        global account_update_needed
        account_holdings_df = pd.DataFrame()
        account_summary_df = pd.DataFrame()
        
        # 判断是否需要更新账户数据
        # if account_update_needed:
        logger.info("🔄 开始更新账户数据...")
        account_info = AccountInfo()
        update_success = True

        # 更新指定账户
        logger.info(f"正在更新账户 {self.account_name} 的数据...")
        # 修复：正确处理update_holding_info_for_account的返回值
        update_result = account_info.update_holding_info_for_account(self.account_name)
        if update_result is False:
            logger.warning(f"⚠️ 账户 {self.account_name} 数据更新失败")
            update_success = False

        # 处理更新结果
        if update_success:
            logger.info("✅ 所需账户数据更新完成")
            # 重置更新标志
            account_update_needed = False
            # 从文件中读取更新后的数据
            try:
                if os.path.exists(Account_holding_file):
                    account_holdings_df = pd.read_excel(Account_holding_file, sheet_name=self.account_name)
                    account_summary_df = pd.read_excel(Account_holding_file, sheet_name='账户汇总')
                    account_summary_df = account_summary_df[account_summary_df['账户名'] == self.account_name]
                else:
                    logger.warning("账户持仓文件不存在")
                    account_holdings_df = pd.DataFrame()
                    account_summary_df = pd.DataFrame()
            except Exception as e:
                logger.error(f"读取账户持仓数据失败: {e}")
                account_holdings_df = pd.DataFrame()
                account_summary_df = pd.DataFrame()
        else:
            logger.warning("⚠️ 账户数据更新失败，将继续使用现有数据执行交易")
            return None, None

        return account_summary_df, account_holdings_df

    def _extract_strategy_holdings(self, strategy_holdings_df):
        """
        筛选出指定策略的股票持仓信息
        """
        strategy_holdings_extracted_df = strategy_holdings_df[strategy_holdings_df['策略名称'] == self.strategy_name] if '策略名称' in strategy_holdings_df.columns else strategy_holdings_df
        
        if not strategy_holdings_extracted_df.empty and ('股票名称' in strategy_holdings_extracted_df.columns or '标的名称' in strategy_holdings_extracted_df.columns):
            strategy_holding = strategy_holdings_extracted_df.copy()
            logger.info(
                f"✅ 成功获取策略 {self.strategy_name} 的持仓数据，共 {len(strategy_holding)} 条记录")
        else:
            strategy_holding = pd.DataFrame()
            logger.warning(f"策略 {self.strategy_name} 持仓数据为空或不包含股票名称列")
            
        return strategy_holding

    def _standardize_data(self, account_holdings_df, strategy_holding):
        """
        标准化股票名称和处理数据格式
        """
        account_holdings = account_holdings_df.copy() if not account_holdings_df.empty else pd.DataFrame()
        
        # 需要排除的股票名称
        excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

        # 标准化股票名称
        # from utils.format_data import standardize_dataframe_stock_names
        # 确保列名统一（账户持仓）
        if not account_holdings.empty:
            if '股票名称' not in account_holdings.columns and '标的名称' in account_holdings.columns:
                account_holdings.rename(columns={'标的名称': '股票名称'}, inplace=True)
            account_holdings = standardize_dataframe_stock_names(account_holdings)

        # 确保列名统一（策略持仓）
        if not strategy_holding.empty:
            if '股票名称' not in strategy_holding.columns and '标的名称' in strategy_holding.columns:
                strategy_holding.rename(columns={'标的名称': '股票名称'}, inplace=True)
            strategy_holding = standardize_dataframe_stock_names(strategy_holding)

        # 对持仓占比和新比例%进行四舍五入取整处理
        if '持仓占比' in account_holdings.columns:
            account_holdings['持仓占比'] = account_holdings['持仓占比'].round(0).astype(int)

        if '新比例%' in strategy_holding.columns:
            strategy_holding['新比例%'] = strategy_holding['新比例%'].round(0).astype(int)

        # 去掉'持有金额'为0的
        if '持有金额' in account_holdings.columns:
            account_holdings = account_holdings[account_holdings['持有金额'] > 0]
            
        return account_holdings, strategy_holding, excluded_holdings

    def _identify_sell_operations(self, account_holdings, strategy_holding, excluded_holdings):
        """
        找出需要卖出的标的
        """
        # 在证券账户中存在，但在策略中不存在的股票（需要全部卖出）
        to_sell = pd.DataFrame()
        if not account_holdings.empty and not strategy_holding.empty:
            # 在证券账户中存在，但在策略中不存在的股票（需要全部卖出）
            to_sell_candidates = account_holdings[
                ~account_holdings['股票名称'].isin(strategy_holding['股票名称'])]

            # 证券账户和策略持仓都存在，但是策略持仓里的'新比例%'的值比证券账户的'持仓占比'小的股票（需要部分卖出）
            # 先找出共同持有的股票
            common_stocks = account_holdings[
                account_holdings['股票名称'].isin(strategy_holding['股票名称'])]

            # 合并策略数据以便比较
            merged_data = pd.merge(common_stocks, strategy_holding[['股票名称', '新比例%']], on='股票名称',
                                   how='left')

            # 找出策略持仓比例小于账户持仓比例的股票（需要卖出到目标比例）
            # 优化：只有当差异大于等于10%时才考虑卖出，避免小幅度调整触发交易
            if '持仓占比' in merged_data.columns:
                to_sell_candidates2 = merged_data[
                    (merged_data['新比例%'] < merged_data['持仓占比']) &
                    ((merged_data['持仓占比'] - merged_data['新比例%']) >= 10)
                    ]
                # 确保新比例列没有NaN值
                to_sell_candidates2 = to_sell_candidates2[to_sell_candidates2['新比例%'].notna()]
            else:
                to_sell_candidates2 = pd.DataFrame()

            # 合并两种需要卖出的情况
            to_sell = pd.concat([to_sell_candidates, to_sell_candidates2]).drop_duplicates(subset=['股票名称'])
            to_sell = to_sell[~to_sell['股票名称'].isin(excluded_holdings)].copy()
        elif not account_holdings.empty:
            # 如果策略持仓为空，则所有证券账户持仓都是需要卖出的（除去排除项）
            to_sell = account_holdings[~account_holdings['股票名称'].isin(excluded_holdings)].copy()
        else:
            to_sell = pd.DataFrame(columns=account_holdings.columns) if not account_holdings.empty else pd.DataFrame()

        # 确保to_sell包含股票名称列
        if not to_sell.empty and '股票名称' not in to_sell.columns and '标的名称' in to_sell.columns:
            to_sell.rename(columns={'标的名称': '股票名称'}, inplace=True)

        if not to_sell.empty:
            to_sell['操作'] = '卖出'
            logger.info(f"⚠️ 发现需卖出的标的: {len(to_sell)} 条")
        else:
            logger.info("✅ 当前无需卖出的标的")
            
        return to_sell

    def _identify_buy_operations(self, account_holdings, strategy_holding, excluded_holdings):
        """
        找出需要买入的标的
        """
        to_buy = pd.DataFrame()
        if not strategy_holding.empty:
            if not account_holdings.empty:
                # 在策略中存在，但在证券账户中不存在的股票（需要买入到目标比例）
                to_buy_candidates = strategy_holding[
                    ~strategy_holding['股票名称'].isin(account_holdings['股票名称'])]

                # 证券账户和策略持仓都存在，但是策略持仓里的'新比例%'的值比证券账户的'持仓占比'大的股票（需要买入到目标比例）
                # 找出共同持有的股票
                common_stocks_buy = strategy_holding[
                    strategy_holding['股票名称'].isin(account_holdings['股票名称'])]

                # 合并账户数据以便比较
                merged_data_buy = pd.merge(common_stocks_buy, account_holdings[['股票名称', '持仓占比']],
                                           on='股票名称',
                                           how='left') if '持仓占比' in account_holdings.columns else pd.DataFrame()

                # 找出策略持仓比例大于账户持仓比例的股票（需要买入到目标比例）
                # 优化：只有当差异大于等于10%时才考虑买入，避免小幅度调整触发交易
                if not merged_data_buy.empty:
                    to_buy_candidates2 = merged_data_buy[
                        (merged_data_buy['新比例%'] > merged_data_buy['持仓占比']) &
                        ((merged_data_buy['新比例%'] - merged_data_buy['持仓占比']) >= 10)
                        ]
                    # 确保新比例列没有NaN值
                    to_buy_candidates2 = to_buy_candidates2[to_buy_candidates2['新比例%'].notna()]
                else:
                    to_buy_candidates2 = pd.DataFrame()

                # 合并两种需要买入的情况
                to_buy = pd.concat([to_buy_candidates, to_buy_candidates2]).drop_duplicates(subset=['股票名称'])
                to_buy = to_buy[~to_buy['股票名称'].isin(excluded_holdings)]
            else:
                # 如果账户持仓为空，则策略中的所有股票都需要买入
                logger.info("账户持仓为空，策略中的所有股票都需要买入")
                to_buy = strategy_holding.copy()
                to_buy = to_buy[~to_buy['股票名称'].isin(excluded_holdings)]

            # 只保留市场为沪深A股的
            if '市场' in to_buy.columns:
                to_buy = to_buy[to_buy['市场'].isin(['沪深A股'])]
        else:
            to_buy = pd.DataFrame(columns=['股票名称'])

        # 确保to_buy包含股票名称列
        if not to_buy.empty and '股票名称' not in to_buy.columns and '标的名称' in to_buy.columns:
            to_buy.rename(columns={'标的名称': '股票名称'}, inplace=True)

        if not to_buy.empty:
            to_buy['操作'] = '买入'
            logger.info(f"⚠️ 发现需买入的标的: {len(to_buy)} 条")
        else:
            logger.info("✅ 当前无需买入的标的")
            
        return to_buy

    def _execute_sell_operations(self, to_sell, account_summary_df, account_holdings_df, strategy_holding):
        """
        执行卖出操作
        """
        any_trade_executed = False
        
        # 遍历每一项卖出操作，执行交易
        for idx, op in to_sell.iterrows():
            stock_name = op['股票名称'] if '股票名称' in op else op['标的名称']
            operation = op['操作']
            # 安全获取可能不存在的字段
            new_ratio = op.get('新比例%', None)  # 对于卖出操作，获取策略中的目标比例

            # 检查new_ratio是否为有效值
            # 对于卖出操作，如果new_ratio为NaN或None，表示需要全部卖出，设置为0
            if new_ratio is None or (isinstance(new_ratio, float) and pd.isna(new_ratio)):
                new_ratio = 0  # 全部卖出
                logger.info(f"⚠️ {operation} {stock_name} 的新比例无效({op.get('新比例%', None)})，设置为0表示全部卖出")

            # 计算交易数量：对于卖出操作，使用策略中的目标比例
            volume = self._calculate_trade_volume_optimized(
                account_summary_df, account_holdings_df, strategy_holding,
                self.strategy_name, stock_name, new_ratio, operation)
            logger.info(f"🛠️ 卖出 {stock_name}，目标比例:{new_ratio}，交易数量:{volume}")

            # 如果交易数量为None或小于等于0，则跳过
            if volume is None or volume <= 0:
                logger.warning(f"⚠️ {operation} {stock_name} 交易数量无效({volume})，跳过交易")
                continue

            logger.info(
                f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{self.strategy_name} 账户:{self.account_name}")

            # 切换到对应账户
            self.common_page.change_account(self.account_name)
            logger.info(f"✅ 已切换到账户: {self.account_name}")

            # 调用交易逻辑
            status, info = self.trader.operate_stock(operation, stock_name, volume)

            # 检查交易是否成功执行
            if status is None:
                logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                continue

            # 标记已执行交易
            any_trade_executed = True
            # 标记下次需要更新账户数据
            global account_update_needed
            account_update_needed = True
            
        return any_trade_executed

    def _execute_buy_operations(self, to_buy, account_summary_df, account_holdings_df, strategy_holding):
        """
        执行买入操作
        """
        any_trade_executed = False
        
        # 按最新价升序排列买入操作
        if not to_buy.empty and '最新价' in to_buy.columns:
            to_buy = to_buy.sort_values(by='最新价', ascending=True)

        # 遍历每一项买入操作，执行交易
        for idx, op in to_buy.iterrows():
            stock_name = op['股票名称'] if '股票名称' in op else op['标的名称']
            operation = op['操作']
            # 安全获取可能不存在的字段
            new_ratio = op.get('新比例%', None)  # 对于买入操作，获取策略中的目标比例

            # 检查new_ratio是否为有效值
            if new_ratio is None or (isinstance(new_ratio, float) and pd.isna(new_ratio)):
                logger.warning(f"⚠️ {operation} {stock_name} 的新比例无效({new_ratio})，跳过交易")
                continue

            # 计算交易数量：对于买入操作，使用策略中的目标比例
            volume = self._calculate_trade_volume_optimized(
                account_summary_df, account_holdings_df, strategy_holding,
                self.strategy_name, stock_name, new_ratio, operation)
            logger.info(f"🛠️ 买入 {stock_name}，目标比例:{new_ratio}，交易数量:{volume}")

            # 如果交易数量为None或小于等于0，则跳过
            if volume is None or volume <= 0:
                logger.warning(f"⚠️ {operation} {stock_name} 交易数量无效({volume})，跳过交易")
                continue

            logger.info(
                f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{self.strategy_name} 账户:{self.account_name}")

            # 切换到对应账户
            self.common_page.change_account(self.account_name)
            logger.info(f"✅ 已切换到账户: {self.account_name}")

            # 调用交易逻辑
            status, info = self.trader.operate_stock(operation, stock_name, volume)

            # 检查交易是否成功执行
            if status is None:
                logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                continue

            # 标记已执行交易
            any_trade_executed = True
            # 标记下次需要更新账户数据
            global account_update_needed
            account_update_needed = True
            
        return any_trade_executed

    def operate_strategy_with_account(self):
        '''
        整合
        1.更新策略持仓
        2.更新账户持仓
        3.以策略为准，根据股票名称，持仓比例找出需要买入和卖出的,去掉'持有金额'为0的,对持仓占比和新比例%进行四舍五入取整处理,允许比例差异在10%以内的股票不计入操作范围
        4.执行交易：先卖出，再按价格升序依次买入
        '''
        try:
            # 1. 更新策略持仓
            strategy_holdings_df = self._update_strategy_holdings()
            if strategy_holdings_df is None:
                return False

            # 2. 更新账户持仓
            account_summary_df, account_holdings_df = self._update_account_holdings()
            if account_summary_df is None or account_holdings_df is None:
                return False

            # 3. 筛选出指定策略的股票持仓信息
            strategy_holding = self._extract_strategy_holdings(strategy_holdings_df)

            # 4. 标准化数据
            account_holdings, strategy_holding, excluded_holdings = self._standardize_data(account_holdings_df, strategy_holding)

            # 5. 找出需要卖出的标的
            to_sell = self._identify_sell_operations(account_holdings, strategy_holding, excluded_holdings)

            # 6. 找出需要买入的标的
            to_buy = self._identify_buy_operations(account_holdings, strategy_holding, excluded_holdings)

            # # 7. 构建完整差异报告
            # difference_report = {
            #     "to_sell": to_sell,
            #     "to_buy": to_buy
            # }

            logger.info(f"📊 最终差异报告 - 需要卖出: {len(to_sell)} 条, 需要买入: {len(to_buy)} 条")
            
            # 8. 执行交易：先卖出，再按价格升序依次买入
            # 8.1 执行卖出操作
            any_trade_executed = self._execute_sell_operations(to_sell, account_summary_df, account_holdings_df, strategy_holding)
            
            # 8.2 执行买入操作
            buy_executed = self._execute_buy_operations(to_buy, account_summary_df, account_holdings_df, strategy_holding)
            any_trade_executed = any_trade_executed or buy_executed

            # 9. 处理交易执行结果
            if any_trade_executed:
                logger.info("✅ 交易执行完成")
                # send_notification(f"✅ 账户 {self.account_name} 对应的策略 {self.strategy_name} 交易执行完成")
            else:
                logger.info("✅ 无需执行交易")

            logger.info(f"完成比较账户 {self.account_name} 与策略 {self.strategy_name} 的持仓差异并执行交易")
            return True

        except Exception as e:
            error_msg = f"处理证券与策略 {self.strategy_name} 持仓差异并执行交易时发生错误: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return False


if __name__ == '__main__':
    processor = CombinationHoldingProcessor()
    success = processor.operate_strategy_with_account()
    if success:
        logger.info("🎉 组合策略调仓任务成功完成")
    else:
        logger.error("❌ 组合策略调仓任务失败")