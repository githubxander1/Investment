import pandas as pd
import datetime
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import THS_AUTO_TRADE_LOG_FILE_MAIN

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_MAIN)

class TradeExecutor:
    """
    交易执行器，用于按价格从低到高排序并确保先卖后买
    """
    
    @staticmethod
    def sort_and_execute_trades(trades_df, trader, account_name, common_page):
        """
        对交易按价格排序并执行，确保先卖后买
        
        Args:
            trades_df: 包含交易信息的DataFrame，需包含标的名称、操作、最新价等列
            trader: 交易执行对象
            account_name: 账户名称
            common_page: 页面操作对象
            
        Returns:
            bool: 执行是否成功
        """
        if trades_df.empty:
            logger.info("⚠️ 无交易数据需要执行")
            return True
            
        # 确保必要的列存在
        required_columns = ['标的名称', '操作']
        for col in required_columns:
            if col not in trades_df.columns:
                logger.error(f"❌ 缺少必要列: {col}")
                return False
                
        # 分离买入和卖出操作
        sell_trades = trades_df[trades_df['操作'] == '卖出'].copy()
        buy_trades = trades_df[trades_df['操作'] == '买入'].copy()
        
        # 按价格从低到高排序买入操作
        if not buy_trades.empty and '最新价' in buy_trades.columns:
            buy_trades = buy_trades.sort_values('最新价', ascending=True)
            logger.info(f"📈 买入顺序（按价格从低到高）: \n{buy_trades[['标的名称', '最新价']].to_string(index=False)}")
        elif not buy_trades.empty:
            logger.info(f"📈 买入顺序: \n{buy_trades[['标的名称']].to_string(index=False)}")
            
        # 按价格从低到高排序卖出操作（可选，一般按持有量或其他逻辑排序更合理）
        if not sell_trades.empty and '最新价' in sell_trades.columns:
            sell_trades = sell_trades.sort_values('最新价', ascending=True)
            logger.info(f"📉 卖出顺序（按价格从低到高）: \n{sell_trades[['标的名称', '最新价']].to_string(index=False)}")
        elif not sell_trades.empty:
            logger.info(f"📉 卖出顺序: \n{sell_trades[['标的名称']].to_string(index=False)}")
            
        # 合并操作，确保先执行卖出再执行买入
        all_trades = pd.concat([sell_trades, buy_trades], ignore_index=True)
        
        if all_trades.empty:
            logger.info("⚠️ 无有效交易需要执行")
            return True
            
        logger.info(f"📋 总共 {len(all_trades)} 个操作需要执行")
        
        # 执行交易
        success_count = 0
        fail_count = 0
        
        for _, trade in all_trades.iterrows():
            stock_name = trade['标的名称']
            operation = trade['操作']
            
            try:
                # 切换到对应账户
                common_page.change_account(account_name)
                logger.info(f"✅ 已切换到账户: {account_name}")
                
                # 获取其他可能需要的参数
                volume = trade.get('交易数量', None)
                new_ratio = trade.get('新比例%', None) if operation == '卖出' else None
                
                # 执行交易
                status, info = trader.operate_stock(
                    operation=operation,
                    stock_name=stock_name,
                    volume=volume,
                    new_ratio=new_ratio
                )
                
                if status:
                    logger.info(f"✅ {operation} {stock_name} 执行成功: {info}")
                    success_count += 1
                else:
                    logger.error(f"❌ {operation} {stock_name} 执行失败: {info}")
                    fail_count += 1
                    
            except Exception as e:
                logger.error(f"❌ {operation} {stock_name} 执行异常: {str(e)}")
                fail_count += 1
                
        logger.info(f"📊 交易执行完成 - 成功: {success_count}, 失败: {fail_count}")
        return fail_count == 0

    @staticmethod
    def sort_position_files_by_price(file_path, sheet_name=None):
        """
        对持仓文件按价格排序
        
        Args:
            file_path: Excel文件路径
            sheet_name: 工作表名称，如果为None则处理所有工作表
            
        Returns:
            bool: 排序是否成功
        """
        try:
            # 读取Excel文件
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheet_names = [sheet_name]
            else:
                excel_file = pd.ExcelFile(file_path)
                sheet_names = excel_file.sheet_names
                df = None
                
            processed_sheets = {}
            
            # 处理每个工作表
            for name in sheet_names:
                if not df or name != sheet_name:
                    temp_df = pd.read_excel(file_path, sheet_name=name)
                else:
                    temp_df = df
                    
                # 按最新价排序（如果存在该列）
                if '最新价' in temp_df.columns:
                    temp_df = temp_df.sort_values('最新价', ascending=True)
                    logger.info(f"📊 工作表 '{name}' 已按最新价排序")
                else:
                    logger.warning(f"⚠️ 工作表 '{name}' 中未找到 '最新价' 列")
                    
                processed_sheets[name] = temp_df
                
            # 保存回Excel文件
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                for name, data in processed_sheets.items():
                    data.to_excel(writer, sheet_name=name, index=False)
                    
            logger.info(f"✅ 文件 {file_path} 排序完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 排序文件时出错: {str(e)}")
            return False