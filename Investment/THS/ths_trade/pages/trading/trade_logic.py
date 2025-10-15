#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
交易逻辑模块
提供买入、卖出等交易逻辑封装
"""

import os
import sys
import time
from typing import Optional, Dict, Any, Tuple, List

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# 使用统一的日志记录器
from utils.logger import setup_logger
from utils.common_utils import retry, get_full_stock_code, is_trading_time
from utils.notification import send_trade_notification
from pages.trading.ths_trade_wrapper import trade_wrapper
from pages.account.account_info import AccountInfo

logger = setup_logger('trade_logic.log')


class TradeLogic:
    """
    交易逻辑类
    实现买入卖出的业务逻辑
    """
    
    def __init__(self, account_name: str = "川财证券"):
        """
        初始化交易逻辑类
        
        Args:
            account_name: 账户名称
        """
        self.account_name = account_name
        self.trade_api = trade_wrapper
        # 初始化AccountInfo实例
        self.account_info = AccountInfo(account_name)
        
        logger.info(f"初始化交易逻辑类 - 账户: {account_name}")
    
    def calculate_buy_volume(self, stock_code: str, price: float, 
                           use_percent: float = 1.0) -> Tuple[int, float]:
        """
        计算买入数量
        
        Args:
            stock_code: 股票代码
            price: 买入价格
            use_percent: 使用资金比例 (0-1)
            
        Returns:
            Tuple[int, float]: (买入数量, 使用资金)
        """
        try:
            # 获取可用资金
            buying_power = self.account_info.get_buying_power()
            
            # 计算可用资金
            available_funds = buying_power * use_percent
            
            # 计算可买数量（取整百）
            volume = int(available_funds / price / 100) * 100
            
            # 确保最小交易量
            if volume < 100:
                volume = 0
            
            # 计算实际使用资金
            actual_amount = volume * price
            
            logger.info(f"计算买入数量: 股票代码={stock_code}, 价格={price}, 可用资金={buying_power}, 买入数量={volume}, 使用资金={actual_amount}")
            
            return volume, actual_amount
        
        except Exception as e:
            logger.error(f"计算买入数量失败: {e}")
            return 0, 0.0
    
    def calculate_sell_volume(self, stock_code: str, sell_percent: float = 1.0) -> int:
        """
        计算卖出数量
        
        Args:
            stock_code: 股票代码
            sell_percent: 卖出比例 (0-1)
            
        Returns:
            int: 卖出数量
        """
        try:
            # 获取可用数量
            available = self.account_info.get_stock_available(stock_code)
            
            # 计算卖出数量（取整百）
            volume = int(available * sell_percent / 100) * 100
            
            # 确保最小交易量
            if volume < 100:
                volume = 0
            
            logger.info(f"计算卖出数量: 股票代码={stock_code}, 可用数量={available}, 卖出比例={sell_percent}, 卖出数量={volume}")
            
            return volume
        
        except Exception as e:
            logger.error(f"计算卖出数量失败: {e}")
            return 0
    
    def buy_stock_with_logic(self, stock_code: str, price: Optional[float] = None,
                           volume: Optional[int] = None, use_percent: float = 1.0,
                           stock_name: Optional[str] = None) -> Dict[str, Any]:
        """
        执行买入逻辑
        
        Args:
            stock_code: 股票代码
            price: 买入价格（可选）
            volume: 买入数量（可选）
            use_percent: 使用资金比例（仅在未指定volume时有效）
            stock_name: 股票名称（可选）
            
        Returns:
            Dict: 交易结果
        """
        try:
            # 检查是否为交易时间
            if not is_trading_time():
                logger.warning(f"当前非交易时间，无法执行买入操作")
                return {
                    'success': False,
                    'message': '当前非交易时间'
                }
            
            # 确保股票名称
            if not stock_name:
                stock_name = f"股票{stock_code}"
            
            # 如果未指定价格，使用当前市价（这里简化处理，实际应该获取实时行情）
            if not price:
                logger.error("未指定买入价格")
                return {
                    'success': False,
                    'message': '未指定买入价格'
                }
            
            # 如果未指定数量，根据可用资金计算
            if not volume:
                calculated_volume, _ = self.calculate_buy_volume(stock_code, price, use_percent)
                if calculated_volume <= 0:
                    logger.warning(f"资金不足，无法买入: {stock_code}")
                    return {
                        'success': False,
                        'message': '资金不足'
                    }
                volume = calculated_volume
            
            # 执行买入操作
            logger.info(f"执行买入操作: {stock_code}，价格: {price}，数量: {volume}")
            result = self.trade_api.buy_stock(stock_code, price, volume)
            
            # 发送通知
            success = result.get('success', False)
            send_trade_notification(stock_name, "买入", volume, price, success)
            
            return result
            
        except Exception as e:
            logger.error(f"买入操作失败: {e}")
            # 发送失败通知
            if stock_name and volume and price:
                send_trade_notification(stock_name, "买入", volume, price, False, str(e))
            
            return {
                'success': False,
                'message': str(e)
            }
    
    def sell_stock_with_logic(self, stock_code: str, price: Optional[float] = None,
                            volume: Optional[int] = None, sell_percent: float = 1.0,
                            stock_name: Optional[str] = None) -> Dict[str, Any]:
        """
        执行卖出逻辑
        
        Args:
            stock_code: 股票代码
            price: 卖出价格（可选）
            volume: 卖出数量（可选）
            sell_percent: 卖出比例（仅在未指定volume时有效）
            stock_name: 股票名称（可选）
            
        Returns:
            Dict: 交易结果
        """
        try:
            # 检查是否为交易时间
            if not is_trading_time():
                logger.warning(f"当前非交易时间，无法执行卖出操作")
                return {
                    'success': False,
                    'message': '当前非交易时间'
                }
            
            # 确保股票名称
            if not stock_name:
                stock_name = f"股票{stock_code}"
            
            # 如果未指定价格，使用当前市价（这里简化处理，实际应该获取实时行情）
            if not price:
                logger.error("未指定卖出价格")
                return {
                    'success': False,
                    'message': '未指定卖出价格'
                }
            
            # 如果未指定数量，根据可用数量计算
            if not volume:
                calculated_volume = self.calculate_sell_volume(stock_code, sell_percent)
                if calculated_volume <= 0:
                    logger.warning(f"持仓不足，无法卖出: {stock_code}")
                    return {
                        'success': False,
                        'message': '持仓不足'
                    }
                volume = calculated_volume
            
            # 执行卖出操作
            logger.info(f"执行卖出操作: {stock_code}，价格: {price}，数量: {volume}")
            result = self.trade_api.sell_stock(stock_code, price, volume)
            
            # 发送通知
            success = result.get('success', False)
            send_trade_notification(stock_name, "卖出", volume, price, success)
            
            return result
            
        except Exception as e:
            logger.error(f"卖出操作失败: {e}")
            # 发送失败通知
            if stock_name and volume and price:
                send_trade_notification(stock_name, "卖出", volume, price, False, str(e))
            
            return {
                'success': False,
                'message': str(e)
            }
    
    def execute_batch_trades(self, trades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行批量交易
        
        Args:
            trades: 交易列表，每个元素包含交易信息
            
        Returns:
            List[Dict]: 交易结果列表
        """
        results = []
        
        for trade in trades:
            try:
                direction = trade.get('direction', '').lower()
                stock_code = trade.get('stock_code', '')
                stock_name = trade.get('stock_name', '')
                price = trade.get('price')
                volume = trade.get('volume')
                percent = trade.get('percent', 1.0)
                
                if direction == 'buy':
                    result = self.buy_stock_with_logic(
                        stock_code=stock_code,
                        price=price,
                        volume=volume,
                        use_percent=percent,
                        stock_name=stock_name
                    )
                elif direction == 'sell':
                    result = self.sell_stock_with_logic(
                        stock_code=stock_code,
                        price=price,
                        volume=volume,
                        sell_percent=percent,
                        stock_name=stock_name
                    )
                else:
                    logger.error(f"未知交易方向: {direction}")
                    result = {
                        'success': False,
                        'message': f'未知交易方向: {direction}'
                    }
                
                # 添加股票代码到结果中
                result['stock_code'] = stock_code
                result['direction'] = direction
                results.append(result)
                
                # 添加间隔，避免频繁操作
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"执行批量交易失败: {e}")
                results.append({
                    'success': False,
                    'message': str(e),
                    'stock_code': trade.get('stock_code', ''),
                    'direction': trade.get('direction', '')
                })
        
        return results
    
    def check_trade_results(self, order_no: str) -> Dict[str, Any]:
        """
        检查交易结果
        
        Args:
            order_no: 订单号
            
        Returns:
            Dict: 订单状态信息
        """
        try:
            # 获取所有未成交订单
            pending_orders = self.trade_api.get_orders('pending')
            
            if not pending_orders.empty:
                # 查找指定订单号
                order = pending_orders[pending_orders['order_no'] == order_no]
                if not order.empty:
                    return {
                        'success': True,
                        'status': order.iloc[0].get('status', 'unknown'),
                        'filled_volume': order.iloc[0].get('filled_volume', 0),
                        'remaining_volume': order.iloc[0].get('remaining_volume', 0)
                    }
            
            # 检查是否已成交
            filled_orders = self.trade_api.get_orders('filled')
            if not filled_orders.empty:
                order = filled_orders[filled_orders['order_no'] == order_no]
                if not order.empty:
                    return {
                        'success': True,
                        'status': 'filled',
                        'filled_volume': order.iloc[0].get('volume', 0),
                        'remaining_volume': 0
                    }
            
            return {
                'success': False,
                'message': '订单不存在'
            }
            
        except Exception as e:
            logger.error(f"检查交易结果失败: {e}")
            return {
                'success': False,
                'message': str(e)
            }


# 测试代码
if __name__ == "__main__":
    # 请替换为实际的账户名称
    test_account = "川财证券"
    
    try:
        trade_logic = TradeLogic(test_account)
        
        # 测试计算买入数量
        stock_code = "000001"
        price = 10.5
        volume, amount = trade_logic.calculate_buy_volume(stock_code, price, 0.5)
        print(f"计算买入数量: {volume}股，使用资金: {amount}元")
        
        # 测试计算卖出数量
        volume = trade_logic.calculate_sell_volume(stock_code, 0.8)
        print(f"计算卖出数量: {volume}股")
        
    except Exception as e:
        print(f"测试失败: {e}")