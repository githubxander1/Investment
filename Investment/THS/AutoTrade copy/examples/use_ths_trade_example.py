#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用THS交易包装器的示例
展示如何在AutoTrade项目中使用新的交易方式
"""

import os
import sys
import logging
import pandas as pd

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('use_ths_trade_example')

# 导入新的交易包装器
from Investment.THS.AutoTrade.pages.trading.ths_trade_wrapper import THSTradeWrapper


class AutoTradeExample:
    """AutoTrade使用THS交易包装器的示例类"""
    
    def __init__(self):
        """初始化示例类"""
        # 创建交易包装器实例
        self.trade_wrapper = THSTradeWrapper(account_name="我的交易账户")
        
        # 检查初始化是否成功
        if self.trade_wrapper.initialized:
            logger.info("✅ THS交易包装器初始化成功")
        else:
            logger.error("❌ THS交易包装器初始化失败")
    
    def example_get_position(self):
        """示例：获取持仓信息"""
        logger.info("\n=== 获取持仓信息示例 ===")
        
        if not self.trade_wrapper.initialized:
            logger.error("交易包装器未初始化，无法获取持仓")
            return
        
        try:
            # 获取持仓
            position = self.trade_wrapper.get_account_position()
            
            if position is not None and not position.empty:
                logger.info(f"✅ 成功获取持仓，共 {len(position)} 只股票")
                # 显示持仓信息
                print("\n持仓信息:")
                print(position)
                
                # 保存持仓到CSV文件
                csv_file = "position_data.csv"
                position.to_csv(csv_file, index=False, encoding='utf-8-sig')
                logger.info(f"✅ 持仓数据已保存到: {csv_file}")
            else:
                logger.warning("⚠️ 未获取到持仓数据")
                
        except Exception as e:
            logger.error(f"❌ 获取持仓异常: {str(e)}", exc_info=True)
    
    def example_get_balance(self):
        """示例：获取资金信息"""
        logger.info("\n=== 获取资金信息示例 ===")
        
        if not self.trade_wrapper.initialized:
            logger.error("交易包装器未初始化，无法获取资金")
            return
        
        try:
            # 获取资金
            balance = self.trade_wrapper.get_account_balance()
            
            if balance is not None and not balance.empty:
                logger.info("✅ 成功获取资金信息")
                print("\n资金信息:")
                print(balance)
            else:
                logger.warning("⚠️ 未获取到资金数据")
                
        except Exception as e:
            logger.error(f"❌ 获取资金异常: {str(e)}", exc_info=True)
    
    def example_create_trade_dataframe(self):
        """示例：创建交易数据DataFrame"""
        # 创建示例交易数据
        trade_data = {
            '标的名称': ['中国平安', '贵州茅台', '招商银行'],
            '操作': ['买入', '卖出', '买入'],
            '交易数量': [100, 200, 300],
            '最新价': [45.6, 1800.0, 35.8],
            '新比例%': [None, 20.5, None]  # 卖出时使用的新比例
        }
        
        trades_df = pd.DataFrame(trade_data)
        logger.info(f"✅ 创建了 {len(trades_df)} 条交易记录")
        return trades_df
    
    def example_trade_execution(self, trades_df):
        """示例：执行交易（注意：实际环境中请谨慎使用）"""
        logger.info("\n=== 交易执行示例（演示模式）===")
        
        if not self.trade_wrapper.initialized:
            logger.error("交易包装器未初始化，无法执行交易")
            return
        
        # 这里只演示如何准备交易数据，实际交易请谨慎执行
        logger.info("准备执行以下交易:")
        for _, trade in trades_df.iterrows():
            stock_name = trade['标的名称']
            operation = trade['操作']
            volume = trade['交易数量']
            new_ratio = trade.get('新比例%')
            
            logger.info(f"- {operation} {stock_name}, 数量: {volume}, 新比例: {new_ratio}")
            
        # 注意：以下代码在实际测试时可以取消注释，但请谨慎操作
        """
        for _, trade in trades_df.iterrows():
            stock_name = trade['标的名称']
            operation = trade['操作']
            volume = trade['交易数量']
            new_ratio = trade.get('新比例%')
            
            # 提取股票代码（如果需要）
            stock_code = self._extract_stock_code(stock_name)
            
            # 执行交易
            success, info = self.trade_wrapper.operate_stock(
                operation=operation,
                stock_name=stock_name,
                volume=volume,
                new_ratio=new_ratio,
                stock_code=stock_code
            )
            
            if success:
                logger.info(f"✅ {operation} {stock_name} 成功: {info}")
            else:
                logger.error(f"❌ {operation} {stock_name} 失败: {info}")
        """
        
        logger.info("✅ 交易执行示例完成（演示模式）")
    
    def _extract_stock_code(self, stock_name):
        """从股票名称提取代码（示例方法，实际应使用更可靠的方式）"""
        # 这里只是演示，实际项目中应该使用股票名称到代码的映射表
        stock_mapping = {
            '中国平安': '601318',
            '贵州茅台': '600519',
            '招商银行': '600036'
        }
        return stock_mapping.get(stock_name)
    
    def run_all_examples(self):
        """运行所有示例"""
        logger.info("\n=== 开始运行AutoTrade THS交易包装器示例 ===")
        
        # 示例1：获取持仓
        self.example_get_position()
        
        # 示例2：获取资金
        self.example_get_balance()
        
        # 示例3：创建交易数据
        trades_df = self.example_create_trade_dataframe()
        
        # 示例4：执行交易（演示模式）
        self.example_trade_execution(trades_df)
        
        logger.info("\n=== AutoTrade THS交易包装器示例运行完成 ===")


if __name__ == "__main__":
    """运行示例"""
    example = AutoTradeExample()
    example.run_all_examples()