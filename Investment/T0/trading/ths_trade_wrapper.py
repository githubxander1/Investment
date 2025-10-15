#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
同花顺交易包装器
为T0项目提供基于ths_trade的交易功能
"""
import logging
import os
from typing import Dict, Any, Optional

# 配置日志
logger = logging.getLogger('t0_ths_trade_wrapper')


class T0THSTradeWrapper:
    '''
    为T0项目提供的同花顺交易包装器
    针对T0交易的特殊需求进行优化
    '''
    
    def __init__(self, account_name: str = "默认T0账户", mock_mode: bool = False):
        """
        初始化交易包装器
        
        Args:
            account_name: 账户名称
            mock_mode: 是否使用模拟模式，默认为False
        """
        self.account_name = account_name
        self.is_success = False
        self.adapter = None
        self.is_mock = mock_mode  # 模拟模式标志
        
        # 如果指定了模拟模式，直接进入模拟模式
        if self.is_mock:
            logger.info(f"✅ 直接进入模拟模式，账户: {account_name}")
            self.is_success = True  # 模拟模式下初始化视为成功
            return
            
        # 初始化THS交易适配器
        try:
            # 尝试导入THS交易适配器
            from Investment.THS.ths_trade.applications.adapter.ths_trade_adapter import THSTradeAdapter
            
            # 检查当前工作目录，确保能找到配置文件
            current_dir = os.getcwd()
            logger.debug(f"当前工作目录: {current_dir}")
            
            self.adapter = THSTradeAdapter(account_name=account_name)
            if self.adapter.is_initialized():
                self.is_success = True
                logger.info(f"✅ T0 THS交易包装器初始化成功 - 账户: {account_name}")
            else:
                logger.error(f"❌ T0 THS交易包装器初始化失败 - 账户: {account_name}")
        except FileNotFoundError as e:
            # 文件找不到错误，切换到模拟模式
            logger.warning(f"⚠️ THS配置文件缺失: {e}")
            self.is_mock = True
            self.adapter = None
            self.is_success = True  # 模拟模式下初始化视为成功
            logger.info(f"✅ 已切换到模拟模式，账户: {account_name}")
        except ImportError as e:
            # 导入错误，切换到模拟模式
            logger.warning(f"⚠️ THS交易适配器模块缺失: {e}")
            self.is_mock = True
            self.adapter = None
            self.is_success = True  # 模拟模式下初始化视为成功
            logger.info(f"✅ 已切换到模拟模式，账户: {account_name}")
        except Exception as e:
            logger.warning(f"⚠️ T0 THS交易包装器初始化异常: {e}")
            self.is_mock = True
            self.adapter = None
            self.is_success = True  # 模拟模式下初始化视为成功
            logger.info(f"✅ 已切换到模拟模式，账户: {account_name}")
    
    def is_initialized(self) -> bool:
        """
        检查包装器是否初始化成功
        
        Returns:
            bool: 是否初始化成功
        """
        return self.is_success
    
    def get_account_position(self) -> Optional[Dict[str, Any]]:
        """
        获取账户持仓信息
        
        Returns:
            Dict: 持仓信息字典，如果失败返回None
        """
        try:
            # 检查是否在模拟模式
            if self.is_mock:
                logger.info(f"📊 模拟模式 - 获取账户持仓信息")
                return [
                    {
                        '证券代码': '000001',
                        '证券名称': '平安银行',
                        '持仓数量': 1000,
                        '可用数量': 1000,
                        '摊薄成本价': 11.50,
                        '最新价': 12.34,
                        '浮动盈亏': 840.00
                    }
                ]
            
            if not self.is_initialized() or not self.adapter:
                logger.error("❌ 获取持仓失败：包装器未初始化")
                return None
            
            positions = self.adapter.get_account_position()
            if positions:
                logger.info(f"✅ 成功获取到 {len(positions)} 条持仓信息")
                # 转换为结构化字典返回
                result = []
                for pos in positions:
                    pos_dict = {
                        '证券代码': pos.get('证券代码', ''),
                        '证券名称': pos.get('证券名称', ''),
                        '持仓数量': pos.get('持仓数量', 0),
                        '可用数量': pos.get('可用数量', 0),
                        '摊薄成本价': pos.get('摊薄成本价', 0.0),
                        '最新价': pos.get('最新价', 0.0),
                        '浮动盈亏': pos.get('浮动盈亏', 0.0)
                    }
                    result.append(pos_dict)
                return result
            else:
                logger.info("ℹ️  账户暂无持仓")
                return []
        except Exception as e:
            logger.error(f"❌ 获取持仓信息异常: {e}")
            return None
    
    def get_stock_position(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """
        获取特定股票的持仓信息
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Dict: 股票持仓信息，如果没有持仓或失败返回None
        """
        try:
            # 检查是否在模拟模式
            if self.is_mock:
                logger.info(f"📊 模拟模式 - 获取股票 {stock_code} 持仓信息")
                return {
                    '证券代码': stock_code,
                    '证券名称': f'模拟股票{stock_code}',
                    '持仓数量': 500,
                    '可用数量': 500,
                    '摊薄成本价': 19.80,
                    '最新价': 20.50,
                    '浮动盈亏': 350.00
                }
            
            if not self.is_initialized() or not self.adapter:
                logger.error("❌ 获取股票持仓失败：包装器未初始化")
                return None
            
            positions = self.get_account_position()
            if positions:
                for pos in positions:
                    if pos.get('证券代码') == stock_code:
                        logger.info(f"✅ 成功获取 {stock_code} 的持仓信息")
                        return pos
            
            logger.info(f"ℹ️  未持有 {stock_code} 的股票")
            return None
        except Exception as e:
            logger.error(f"❌ 获取特定股票持仓异常: {e}")
            return None
    
    def get_available_funds(self) -> Optional[Dict[str, Any]]:
        """
        获取账户可用资金信息
        
        Returns:
            Dict: 资金信息字典，如果失败返回None
        """
        try:
            # 检查是否在模拟模式
            if self.is_mock:
                logger.info(f"📊 模拟模式 - 获取可用资金信息")
                return {
                    '可用金额': 50000.00,
                    '总资产': 60000.00,
                    '股票市值': 10000.00,
                    '冻结金额': 0.00
                }
            
            if not self.is_initialized() or not self.adapter:
                logger.error("❌ 获取资金失败：包装器未初始化")
                return None
            
            funds = self.adapter.get_account_funds()
            if funds:
                logger.info("✅ 成功获取账户资金信息")
                # 转换为结构化字典返回
                result = {
                    '可用金额': funds.get('可用金额', 0.0),
                    '总资产': funds.get('总资产', 0.0),
                    '股票市值': funds.get('股票市值', 0.0),
                    '冻结金额': funds.get('冻结金额', 0.0)
                }
                return result
            else:
                logger.error("❌ 获取资金信息失败")
                return None
        except Exception as e:
            logger.error(f"❌ 获取资金信息异常: {e}")
            return None
    
    def buy_stock(self, stock_code: str, stock_name: str, price: float, quantity: int) -> Dict[str, Any]:
        """
        买入股票
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            price: 买入价格
            quantity: 买入数量
            
        Returns:
            Dict: 交易结果字典
        """
        try:
            # 模拟模式处理
            if hasattr(self, 'is_mock') and self.is_mock:
                logger.info(f"🔶 模拟买入: {stock_code} {stock_name} {quantity}股 @ {price}")
                return {
                    'success': True,
                    'message': '模拟买入成功',
                    'order_no': f'mock_buy_{stock_code}_{int(time.time())}'
                }
                
            if not self.is_initialized() or not self.adapter:
                logger.error("❌ 买入失败：包装器未初始化")
                return {'success': False, 'message': '包装器未初始化', 'order_no': ''}
            
            result = self.adapter.buy_stock(
                stock_code=stock_code,
                stock_name=stock_name,
                price=price,
                quantity=quantity
            )
            
            if result.get('success'):
                logger.info(f"✅ 买入成功: {stock_code} {stock_name} {quantity}股 @ {price}")
            else:
                logger.error(f"❌ 买入失败: {stock_code} {stock_name}, 原因: {result.get('message', '未知错误')}")
            
            return result
        except Exception as e:
            logger.error(f"❌ 买入股票异常: {e}")
            return {'success': False, 'message': str(e), 'order_no': ''}
    
    def sell_stock(self, stock_code: str, stock_name: str, price: float, quantity: int, new_ratio: float = None) -> Dict[str, Any]:
        """
        卖出股票
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            price: 卖出价格
            quantity: 卖出数量
            new_ratio: 新比例（可选）
            
        Returns:
            Dict: 交易结果字典
        """
        try:
            # 模拟模式处理
            if hasattr(self, 'is_mock') and self.is_mock:
                logger.info(f"🔶 模拟卖出: {stock_code} {stock_name} {quantity}股 @ {price}")
                return {
                    'success': True,
                    'message': '模拟卖出成功',
                    'order_no': f'mock_sell_{stock_code}_{int(time.time())}'
                }
                
            if not self.is_initialized() or not self.adapter:
                logger.error("❌ 卖出失败：包装器未初始化")
                return {'success': False, 'message': '包装器未初始化', 'order_no': ''}
            
            result = self.adapter.sell_stock(
                stock_code=stock_code,
                stock_name=stock_name,
                price=price,
                quantity=quantity
            )
            
            if result.get('success'):
                logger.info(f"✅ 卖出成功: {stock_code} {stock_name} {quantity}股 @ {price}")
            else:
                logger.error(f"❌ 卖出失败: {stock_code} {stock_name}, 原因: {result.get('message', '未知错误')}")
            
            return result
        except Exception as e:
            logger.error(f"❌ 卖出股票异常: {e}")
            return {'success': False, 'message': str(e), 'order_no': ''}
    
    def do_t0_trade(self, stock_code: str, stock_name: str, buy_price: float, sell_price: float, quantity: int) -> Dict[str, Any]:
        """
        执行T0交易（先买入后卖出或先卖出后买入）
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            buy_price: 买入价格
            sell_price: 卖出价格
            quantity: 交易数量
            
        Returns:
            Dict: 完整T0交易结果
        """
        try:
            # 模拟模式处理
            if hasattr(self, 'is_mock') and self.is_mock:
                logger.info(f"🔶 模拟T0交易: {stock_code} {stock_name} {quantity}股 @ 买{buy_price}/卖{sell_price}")
                
                # 模拟买入和卖出结果
                mock_buy_result = {
                    'success': True,
                    'message': '模拟买入成功',
                    'order_no': f'mock_buy_{stock_code}_{int(time.time())}'
                }
                mock_sell_result = {
                    'success': True,
                    'message': '模拟卖出成功',
                    'order_no': f'mock_sell_{stock_code}_{int(time.time())}'
                }
                
                # 计算模拟利润
                profit = self.calculate_t0_profit(stock_code, quantity, buy_price, sell_price)
                
                # 模拟T0交易步骤
                steps = [
                    {'type': 'buy', 'result': mock_buy_result},
                    {'type': 'sell', 'result': mock_sell_result}
                ]
                
                logger.info(f"✅ 模拟T0交易完成：利润 {profit['net_profit']:.2f} 元")
                return {
                    'success': True,
                    'message': '模拟T0交易成功',
                    'steps': steps,
                    'profit': profit
                }
                
            if not self.is_initialized() or not self.adapter:
                logger.error("❌ T0交易失败：包装器未初始化")
                return {'success': False, 'message': '包装器未初始化', 'steps': []}
            
            # 检查是否持有该股票
            stock_pos = self.get_stock_position(stock_code)
            
            # 计算可用资金
            funds = self.get_available_funds()
            available_funds = funds.get('可用金额', 0) if funds else 0
            
            # 买入金额估算
            buy_amount = buy_price * quantity * 1.001  # 加上手续费估算
            
            steps = []
            
            # 如果持有该股票，先卖出再买入
            if stock_pos and stock_pos.get('可用数量', 0) >= quantity:
                logger.info(f"📤 开始T0交易：先卖出后买入 - {stock_code}")
                
                # 1. 卖出股票
                sell_result = self.sell_stock(stock_code, stock_name, sell_price, quantity)
                steps.append({'type': 'sell', 'result': sell_result})
                
                if sell_result.get('success'):
                    # 2. 买入股票
                    buy_result = self.buy_stock(stock_code, stock_name, buy_price, quantity)
                    steps.append({'type': 'buy', 'result': buy_result})
                    
                    if buy_result.get('success'):
                        # 计算利润
                        profit = self.calculate_t0_profit(stock_code, quantity, buy_price, sell_price)
                        logger.info(f"✅ T0交易完成：利润 {profit['net_profit']:.2f} 元")
                        return {
                            'success': True,
                            'message': 'T0交易成功',
                            'steps': steps,
                            'profit': profit
                        }
                    else:
                        logger.error(f"❌ T0交易失败：卖出成功但买入失败")
                        return {
                            'success': False,
                            'message': '卖出成功但买入失败',
                            'steps': steps
                        }
                else:
                    logger.error(f"❌ T0交易失败：卖出失败")
                    return {
                        'success': False,
                        'message': '卖出失败',
                        'steps': steps
                    }
            # 如果资金充足，先买入再卖出
            elif available_funds >= buy_amount:
                logger.info(f"📥 开始T0交易：先买入后卖出 - {stock_code}")
                
                # 1. 买入股票
                buy_result = self.buy_stock(stock_code, stock_name, buy_price, quantity)
                steps.append({'type': 'buy', 'result': buy_result})
                
                if buy_result.get('success'):
                    # 等待一段时间让买入成交
                    time.sleep(1)
                    
                    # 2. 卖出股票
                    sell_result = self.sell_stock(stock_code, stock_name, sell_price, quantity)
                    steps.append({'type': 'sell', 'result': sell_result})
                    
                    if sell_result.get('success'):
                        # 计算利润
                        profit = self.calculate_t0_profit(stock_code, quantity, buy_price, sell_price)
                        logger.info(f"✅ T0交易完成：利润 {profit['net_profit']:.2f} 元")
                        return {
                            'success': True,
                            'message': 'T0交易成功',
                            'steps': steps,
                            'profit': profit
                        }
                    else:
                        logger.error(f"❌ T0交易失败：买入成功但卖出失败")
                        return {
                            'success': False,
                            'message': '买入成功但卖出失败',
                            'steps': steps
                        }
                else:
                    logger.error(f"❌ T0交易失败：买入失败")
                    return {
                        'success': False,
                        'message': '买入失败',
                        'steps': steps
                    }
            else:
                logger.error(f"❌ T0交易失败：资金不足且无可用持仓")
                return {
                    'success': False,
                    'message': '资金不足且无可用持仓',
                    'steps': []
                }
                
        except Exception as e:
            logger.error(f"❌ T0交易异常: {e}")
            return {'success': False, 'message': str(e), 'steps': []}
    
    def calculate_t0_profit(self, stock_code: str, quantity: int, buy_price: float, sell_price: float) -> Dict[str, float]:
        """
        计算T0交易利润
        
        Args:
            stock_code: 股票代码
            quantity: 交易数量
            buy_price: 买入价格
            sell_price: 卖出价格
            
        Returns:
            Dict: 包含毛利润、手续费和净利润的字典
        """
        try:
            # 计算毛利润
            gross_profit = (sell_price - buy_price) * quantity
            
            # 计算手续费（印花税0.1%，佣金0.03%双边）
            # 买入成本
            buy_commission = buy_price * quantity * 0.0003
            if buy_commission < 5:  # 最低5元
                buy_commission = 5
            
            # 卖出成本
            sell_commission = sell_price * quantity * 0.0003
            if sell_commission < 5:  # 最低5元
                sell_commission = 5
            
            # 印花税（仅卖出收取）
            stamp_tax = sell_price * quantity * 0.001
            
            # 过户费（按股数计算，深市无此项）
            transfer_fee = 0
            if stock_code.startswith('6'):  # 沪市股票
                # 买入过户费
                buy_transfer = quantity * 0.00002
                # 卖出过户费
                sell_transfer = quantity * 0.00002
                transfer_fee = buy_transfer + sell_transfer
            
            # 总手续费
            fee = buy_commission + sell_commission + stamp_tax + transfer_fee
            
            # 净利润
            net_profit = gross_profit - fee
            
            return {
                'gross_profit': gross_profit,
                'fee': fee,
                'net_profit': net_profit,
                'buy_commission': buy_commission,
                'sell_commission': sell_commission,
                'stamp_tax': stamp_tax,
                'transfer_fee': transfer_fee
            }
        except Exception as e:
            logger.error(f"❌ 计算T0利润异常: {e}")
            return {
                'gross_profit': 0.0,
                'fee': 0.0,
                'net_profit': 0.0,
                'buy_commission': 0.0,
                'sell_commission': 0.0,
                'stamp_tax': 0.0,
                'transfer_fee': 0.0
            }
    
    def close(self):
        """
        关闭资源
        """
        try:
            if self.adapter:
                self.adapter.close()
                logger.info("✅ T0 THS交易包装器资源已关闭")
        except Exception as e:
            logger.error(f"❌ 关闭T0 THS交易包装器资源异常: {e}")

# 导入time模块（do_t0_trade方法中使用）
import time