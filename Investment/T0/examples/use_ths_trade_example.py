#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用THS交易包装器的示例
展示如何在T0项目中使用新的交易方式
"""

import os
import sys
import logging
import time

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('t0_ths_trade_example')

# 导入新的交易包装器
from Investment.T0.trading.ths_trade_wrapper import T0THSTradeWrapper


class T0TradeExample:
    """T0使用THS交易包装器的示例类"""
    
    def __init__(self):
        """初始化示例类"""
        # 创建T0交易包装器实例
        self.trade_wrapper = T0THSTradeWrapper(account_name="T0交易账户")
        
        # 检查初始化是否成功
        if self.trade_wrapper.initialized:
            logger.info("✅ T0 THS交易包装器初始化成功")
        else:
            logger.error("❌ T0 THS交易包装器初始化失败")
    
    def example_get_position(self):
        """示例：获取持仓信息"""
        logger.info("\n=== 获取持仓信息示例 ===")
        
        if not self.trade_wrapper.initialized:
            logger.error("交易包装器未初始化，无法获取持仓")
            return
        
        try:
            # 获取完整持仓
            all_position = self.trade_wrapper.get_account_position()
            
            if all_position is not None and not all_position.empty:
                logger.info(f"✅ 成功获取持仓，共 {len(all_position)} 只股票")
                print("\n完整持仓信息:")
                print(all_position)
            else:
                logger.warning("⚠️ 未获取到持仓数据")
                
        except Exception as e:
            logger.error(f"❌ 获取持仓异常: {str(e)}", exc_info=True)
    
    def example_get_specific_stock_position(self, stock_code="600000"):
        """示例：获取特定股票的持仓信息"""
        logger.info(f"\n=== 获取特定股票持仓示例（代码：{stock_code}）===")
        
        if not self.trade_wrapper.initialized:
            logger.error("交易包装器未初始化，无法获取持仓")
            return
        
        try:
            # 获取特定股票持仓
            stock_position = self.trade_wrapper.get_stock_position(stock_code)
            
            if stock_position:
                logger.info(f"✅ 成功获取股票 {stock_code} 的持仓信息")
                print("\n特定股票持仓信息:")
                for key, value in stock_position.items():
                    print(f"{key}: {value}")
            else:
                logger.warning(f"⚠️ 未找到股票 {stock_code} 的持仓数据")
                
        except Exception as e:
            logger.error(f"❌ 获取特定股票持仓异常: {str(e)}", exc_info=True)
    
    def example_get_available_funds(self):
        """示例：获取可用资金"""
        logger.info("\n=== 获取可用资金示例 ===")
        
        if not self.trade_wrapper.initialized:
            logger.error("交易包装器未初始化，无法获取资金")
            return
        
        try:
            # 获取可用资金
            funds = self.trade_wrapper.get_available_funds()
            logger.info(f"✅ 成功获取可用资金: {funds:.2f} 元")
            
        except Exception as e:
            logger.error(f"❌ 获取可用资金异常: {str(e)}", exc_info=True)
    
    def example_calculate_t0_profit(self):
        """示例：计算T0交易利润"""
        logger.info("\n=== T0交易利润计算示例 ===")
        
        # 示例交易参数
        stock_code = "600000"
        stock_name = "浦发银行"
        sell_price = 8.50
        buy_price = 8.30
        trade_amount = 1000
        
        # 计算利润
        profit_result = self.trade_wrapper.calculate_t0_profit(
            stock_code=stock_code,
            sell_price=sell_price,
            buy_price=buy_price,
            trade_amount=trade_amount
        )
        
        logger.info(f"📊 T0交易利润计算 - 股票: {stock_name}({stock_code})")
        logger.info(f"  卖出价: {sell_price}, 买入价: {buy_price}, 数量: {trade_amount}")
        logger.info(f"  毛利润: {profit_result['gross_profit']:.2f} 元")
        logger.info(f"  交易费用: {profit_result['total_fees']:.2f} 元")
        logger.info(f"  净利润: {profit_result['net_profit']:.2f} 元")
        logger.info(f"  收益率: {profit_result['profit_rate']:.2f}%")
        
        # 详细费用
        logger.info(f"\n详细费用明细:")
        logger.info(f"  买入佣金: {profit_result['buy_commission']:.2f} 元")
        logger.info(f"  卖出佣金: {profit_result['sell_commission']:.2f} 元")
        logger.info(f"  印花税: {profit_result['sell_stamp_tax']:.2f} 元")
    
    def example_t0_trade_process(self):
        """示例：T0交易完整流程（演示模式）"""
        logger.info("\n=== T0交易完整流程示例（演示模式）===")
        
        if not self.trade_wrapper.initialized:
            logger.error("交易包装器未初始化，无法执行交易流程")
            return
        
        # 示例股票信息
        stock_code = "600000"
        stock_name = "浦发银行"
        t0_amount = 1000  # T0交易数量
        
        # 1. 检查可用资金
        available_funds = self.trade_wrapper.get_available_funds()
        logger.info(f"1️⃣ 检查可用资金: {available_funds:.2f} 元")
        
        # 2. 检查股票持仓
        stock_position = self.trade_wrapper.get_stock_position(stock_code)
        if stock_position:
            logger.info(f"2️⃣ 检查持仓: 已持有 {stock_name}({stock_code})")
            # 这里可以添加从持仓中提取可用卖出数量的逻辑
        else:
            logger.warning(f"2️⃣ 检查持仓: 未持有 {stock_name}({stock_code})")
        
        # 3. 模拟T0交易策略（高抛低吸）
        # 假设当前价格是8.30元，预期卖出价格是8.50元
        current_price = 8.30
        target_sell_price = 8.50
        
        logger.info(f"3️⃣ T0策略分析: 当前价={current_price}, 目标卖价={target_sell_price}")
        
        if target_sell_price > current_price:
            # 符合高抛低吸策略
            potential_profit = (target_sell_price - current_price) * t0_amount
            logger.info(f"   潜在毛利润: {potential_profit:.2f} 元")
            
            # 4. 准备执行T0交易
            logger.info(f"4️⃣ 准备执行T0交易: 先卖出 {t0_amount} 股，再买入 {t0_amount} 股")
            
            # 注意：以下代码在实际测试时可以取消注释，但请谨慎操作
            """
            # 执行T0交易
            logger.info("5️⃣ 开始执行T0交易...")
            trade_result = self.trade_wrapper.do_t0_trade(
                stock_code=stock_code,
                stock_name=stock_name,
                sell_amount=t0_amount,
                buy_amount=t0_amount
            )
            
            # 处理交易结果
            if trade_result['success']:
                logger.info(f"✅ T0交易成功完成")
                # 记录交易日志
                self._log_t0_trade(stock_code, stock_name, t0_amount)
            else:
                logger.error(f"❌ T0交易失败: {trade_result.get('msg', '未知错误')}")
            """
            
        else:
            logger.info("   不符合T0交易条件，跳过交易")
        
        logger.info("✅ T0交易流程示例完成（演示模式）")
    
    def _log_t0_trade(self, stock_code, stock_name, trade_amount):
        """记录T0交易日志（示例方法）"""
        # 这里可以实现交易日志记录功能
        trade_time = time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"📝 T0交易记录 - 时间: {trade_time}, 股票: {stock_name}({stock_code}), 数量: {trade_amount}")
    
    def run_all_examples(self):
        """运行所有示例"""
        logger.info("\n=== 开始运行T0 THS交易包装器示例 ===")
        
        # 示例1：获取持仓
        self.example_get_position()
        
        # 示例2：获取特定股票持仓
        self.example_get_specific_stock_position()
        
        # 示例3：获取可用资金
        self.example_get_available_funds()
        
        # 示例4：计算T0交易利润
        self.example_calculate_t0_profit()
        
        # 示例5：T0交易完整流程
        self.example_t0_trade_process()
        
        logger.info("\n=== T0 THS交易包装器示例运行完成 ===")


if __name__ == "__main__":
    """运行示例"""
    example = T0TradeExample()
    example.run_all_examples()