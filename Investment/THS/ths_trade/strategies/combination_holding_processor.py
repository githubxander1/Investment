#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
组合持仓处理器 - 整合到ths_trade项目
用于管理和调整证券账户与策略持仓之间的差异
"""

import os
import json
import logging
import traceback
import pandas as pd
import requests
from datetime import datetime

# 使用统一的日志记录器
from Investment.THS.ths_trade.utils.logger import setup_logger
from Investment.THS.ths_trade.utils.notification import send_trade_notification as send_notification
from Investment.THS.ths_trade.pages.account.account_info import AccountInfo
from Investment.THS.ths_trade.pages.trading.trade_logic import TradeLogic
from Investment.THS.ths_trade.utils.common_utils import get_full_stock_code, is_trading_time

# 设置日志
logger = setup_logger('combination_holding_processor.log')

# 导入配置（如果需要）
try:
    from Investment.THS.AutoTrade.config.settings import Combination_headers, id_to_name
except ImportError:
    logger.warning("无法导入AutoTrade配置，使用默认值")
    Combination_headers = {}
    id_to_name = {}


class CombinationHoldingProcessor:
    """
    组合持仓处理器
    用于比较账户持仓与策略持仓，并执行调仓操作
    """
    
    def __init__(self, strategy_name="逻辑为王", account_name="川财证券"):
        """
        初始化组合持仓处理器
        
        Args:
            strategy_name: 策略名称
            account_name: 账户名称
        """
        self.strategy_name = strategy_name
        self.account_name = account_name
        
        # 初始化交易相关的组件
        self.account_info = AccountInfo(account_name)
        self.trader = TradeLogic(account_name)
        
        logger.info(f"初始化组合持仓处理器 - 策略: {strategy_name}, 账户: {account_name}")

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
                    logger.warning(
                        f"组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})返回数据格式异常: {data}")
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
    
    def _calculate_trade_volume_optimized(self, account_summary_df, account_holdings_df, 
                                        strategy_holding, strategy_name, stock_name, 
                                        target_ratio, operation):
        """
        优化的交易数量计算方法
        根据账户资产、持仓比例和股票价格计算买入/卖出股数
        """
        try:
            # 如果账户汇总数据为空，无法计算
            if account_summary_df.empty:
                logger.warning("账户汇总数据为空，无法计算交易数量")
                return None
            
            # 获取总资产
            total_asset = float(account_summary_df.iloc[0].get('总资产', 0))
            if total_asset <= 0:
                logger.warning("账户总资产无效，无法计算交易数量")
                return None
            
            # 计算目标金额
            target_amount = total_asset * (target_ratio / 100)
            
            # 如果是卖出操作，先获取当前持仓
            current_volume = 0
            current_cost = 0
            
            if not account_holdings_df.empty and stock_name in account_holdings_df.get('股票名称', []).values:
                holding_row = account_holdings_df[account_holdings_df['股票名称'] == stock_name].iloc[0]
                current_volume = int(holding_row.get('持有数量', 0))
                current_cost = float(holding_row.get('最新价', 0) or 0)
            
            # 如果当前价格未知，尝试从策略持仓中获取
            if current_cost <= 0 and not strategy_holding.empty:
                strategy_row = strategy_holding[strategy_holding['股票名称'] == stock_name]
                if not strategy_row.empty:
                    current_cost = float(strategy_row.iloc[0].get('最新价', 0) or 0)
            
            # 如果价格仍然未知，无法计算
            if current_cost <= 0:
                logger.warning(f"无法获取 {stock_name} 的价格信息，无法计算交易数量")
                return None
            
            # 计算交易数量
            if operation == "买入":
                # 买入：根据目标金额和当前价格计算
                trade_volume = int(target_amount / current_cost)
                # 确保是100的整数倍（A股交易规则）
                trade_volume = (trade_volume // 100) * 100
            else:  # 卖出
                if target_ratio == 0:
                    # 全部卖出
                    trade_volume = current_volume
                else:
                    # 部分卖出：计算目标持仓数量并减去当前持仓
                    target_volume = int(target_amount / current_cost)
                    trade_volume = current_volume - target_volume
                
                # 确保是100的整数倍
                trade_volume = (trade_volume // 100) * 100
            
            # 确保交易数量为正数
            trade_volume = max(0, trade_volume)
            
            logger.info(f"计算交易数量: {stock_name} {operation} {trade_volume}股 (价格: {current_cost}, 目标比例: {target_ratio}%)")
            return trade_volume
            
        except Exception as e:
            logger.error(f"计算交易数量时出错: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def _update_strategy_holdings(self):
        """
        更新策略持仓数据
        从数据源获取最新的策略持仓信息
        """
        try:
            # 在实际应用中，这里应该从数据源获取策略持仓
            # 这里返回一个空的DataFrame作为示例
            logger.info(f"更新策略 {self.strategy_name} 的持仓数据")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"更新策略持仓数据失败: {e}")
            return None
    
    def _extract_strategy_holdings(self, strategy_holdings_df):
        """
        筛选出指定策略的股票持仓信息
        """
        strategy_holdings_extracted_df = strategy_holdings_df[strategy_holdings_df['策略名称'] == self.strategy_name] if '策略名称' in strategy_holdings_df.columns else strategy_holdings_df
        
        if not strategy_holdings_extracted_df.empty and ('股票名称' in strategy_holdings_extracted_df.columns or '标的名称' in strategy_holdings_extracted_df.columns):
            strategy_holding = strategy_holdings_extracted_df.copy()
            logger.info(f"✅ 成功获取策略 {self.strategy_name} 的持仓数据，共 {len(strategy_holding)} 条记录")
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

            logger.info(f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{self.strategy_name} 账户:{self.account_name}")

            # 检查是否为交易时间
            if not is_trading_time():
                logger.warning(f"当前非交易时间，无法执行卖出操作")
                continue

            # 获取股票代码
            stock_code = None
            # 尝试从account_holdings_df中获取股票代码
            if not account_holdings_df.empty:
                stock_row = account_holdings_df[account_holdings_df['证券名称'] == stock_name]
                if not stock_row.empty:
                    stock_code = stock_row.iloc[0]['证券代码']
                    logger.info(f"找到股票代码: {stock_code}")

            # 如果找不到股票代码，尝试获取最新价（这里简化处理）
            price = None
            if not account_holdings_df.empty and stock_code:
                stock_row = account_holdings_df[account_holdings_df['证券代码'] == stock_code]
                if not stock_row.empty:
                    price = stock_row.iloc[0].get('最新价', None) or stock_row.iloc[0].get('当前价', None)

            if not price:
                # 如果没有价格，设置一个默认值或跳过
                logger.warning(f"无法获取{stock_name}的价格信息，尝试使用默认价格")
                continue

            # 使用ths_trade的交易逻辑执行卖出
            result = self.trader.sell_stock_with_logic(
                stock_code=stock_code,
                price=price,
                volume=volume,
                stock_name=stock_name
            )

            # 检查交易是否成功执行
            if result and result.get('success'):
                logger.info(f"✅ {operation} {stock_name} 交易执行成功: {result.get('message', '成功')}")
                # 标记已执行交易
                any_trade_executed = True
                # 标记下次需要更新账户数据
                global account_update_needed
                account_update_needed = True
            else:
                error_msg = result.get('message', '交易失败') if result else '交易失败'
                logger.error(f"❌ {operation} {stock_name} 交易执行失败: {error_msg}")
                continue
            
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

            logger.info(f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{self.strategy_name} 账户:{self.account_name}")

            # 检查是否为交易时间
            if not is_trading_time():
                logger.warning(f"当前非交易时间，无法执行买入操作")
                continue

            # 获取股票代码
            stock_code = None
            # 尝试从to_buy中获取股票代码
            if '证券代码' in op:
                stock_code = op['证券代码']
            elif '股票代码' in op:
                stock_code = op['股票代码']

            # 获取价格
            price = op.get('最新价', None) or op.get('当前价', None)
            if not price and not account_holdings_df.empty and stock_code:
                # 尝试从account_holdings_df中获取价格
                stock_row = account_holdings_df[account_holdings_df['证券代码'] == stock_code]
                if not stock_row.empty:
                    price = stock_row.iloc[0].get('最新价', None) or stock_row.iloc[0].get('当前价', None)

            if not price:
                # 如果没有价格，跳过交易
                logger.warning(f"无法获取{stock_name}的价格信息，跳过交易")
                continue

            # 使用ths_trade的交易逻辑执行买入
            result = self.trader.buy_stock_with_logic(
                stock_code=stock_code,
                price=price,
                volume=volume,
                stock_name=stock_name
            )

            # 检查交易是否成功执行
            if result and result.get('success'):
                logger.info(f"✅ {operation} {stock_name} 交易执行成功: {result.get('message', '成功')}")
                # 标记已执行交易
                any_trade_executed = True
                # 标记下次需要更新账户数据
                global account_update_needed
                account_update_needed = True
            else:
                error_msg = result.get('message', '交易失败') if result else '交易失败'
                logger.error(f"❌ {operation} {stock_name} 交易执行失败: {error_msg}")
                continue
            
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
            logger.info(f"正在更新账户 {self.account_name} 的数据...")
            account_summary_df, account_holdings_df = self.account_info.update_holding_info_for_account(self.account_name)

            # 3. 筛选出指定策略的股票持仓信息
            strategy_holding = self._extract_strategy_holdings(strategy_holdings_df)

            # 4. 标准化数据
            excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

            # 5. 找出需要卖出的标的
            to_sell = self._identify_sell_operations(account_holdings_df, strategy_holding, excluded_holdings)

            # 6. 找出需要买入的标的
            to_buy = self._identify_buy_operations(account_holdings_df, strategy_holding, excluded_holdings)

            logger.info(f"📊 最终差异报告 - 需要卖出: {len(to_sell)} 条, 需要买入: {len(to_buy)} 条")
            
            # 7. 执行交易：先卖出，再按价格升序依次买入
            # 7.1 执行卖出操作
            any_trade_executed = self._execute_sell_operations(to_sell, account_summary_df, account_holdings_df, strategy_holding)
            
            # 7.2 执行买入操作
            buy_executed = self._execute_buy_operations(to_buy, account_summary_df, account_holdings_df, strategy_holding)
            any_trade_executed = any_trade_executed or buy_executed

            # 8. 处理交易执行结果
            if any_trade_executed:
                logger.info("✅ 交易执行完成")
            else:
                logger.info("✅ 无需执行交易")

            logger.info(f"完成比较账户 {self.account_name} 与策略 {self.strategy_name} 的持仓差异并执行交易")
            return True

        except Exception as e:
            error_msg = f"处理证券与策略 {self.strategy_name} 持仓差异并执行交易时发生错误: {e}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            send_notification(error_msg)
            return False

# 全局变量
global account_update_needed
account_update_needed = False

if __name__ == '__main__':
    # 示例用法
    processor = CombinationHoldingProcessor(strategy_name="逻辑为王", account_name="川财证券")
    success = processor.operate_strategy_with_account()
    if success:
        logger.info("🎉 组合策略调仓任务成功完成")
    else:
        logger.error("❌ 组合策略调仓任务失败")