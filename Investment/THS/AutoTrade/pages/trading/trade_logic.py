import pandas as pd
import uiautomator2 as u2
import os

from Investment.THS.AutoTrade.pages.trading.page_trading import TradingPage
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.pages.base.page_common import CommonPage

logger = setup_logger('trade.log')

class TradeLogic:
    """
    交易逻辑类，处理交易相关的业务逻辑
    """
    
    def __init__(self):
        self.d = u2.connect()
        self.account_name = None
        self.trading_page = TradingPage(self.d)
        self.common_page = CommonPage(self.d)
        self._current_stock_name = None
        self.VOLUME_MAX_BUY = 5000

    def calculate_buy_volume(self, account_asset, stock_price, new_ratio=None):
        """
        根据可用资金和价格计算买入数量
        
        Args:
            account_asset: 账户总资产
            stock_price: 股票价格
            new_ratio: 新仓位比例（可选）
            
        Returns:
            int: 计算出的股数，或 None 表示失败
        """
        try:
            # 检查必要参数
            if account_asset is None or stock_price is None or stock_price <= 0:
                logger.warning(f"计算买入数量失败：account_asset={account_asset}, stock_price={stock_price}")
                return None

            # 如果提供了新比例，则按比例计算买入金额
            if new_ratio is not None:
                # 确保new_ratio是数值类型
                try:
                    new_ratio = float(new_ratio)
                except (ValueError, TypeError):
                    logger.warning(f"new_ratio转换为数值失败: {new_ratio}")
                    new_ratio = None
            
            if new_ratio is not None and new_ratio > 0:
                # 计算目标金额 = 账户总资产 * 新比例% / 100 （因为new_ratio是百分比）
                target_amount = account_asset * float(new_ratio) / 100
                logger.info(f"目标投资金额: {account_asset} * {new_ratio}% = {target_amount}")

                # 计算股数 = 目标金额 / 价格
                volume = int(target_amount / stock_price)
                logger.info(f"计算股数: {target_amount} / {stock_price} = {volume}")

                # 转换为100的倍数
                volume = (volume // 100) * 100
                if volume < 100:
                    logger.warning("计算出的买入股数不足100股")
                    # 修改：即使不足100股也返回计算结果，让调用者决定是否执行
                    return volume if volume > 0 else None

                logger.info(f"计算买入股数: {volume}")
                return volume
            else:
                # 原有逻辑：使用最大可用资金或VOLUME_MAX_BUY中的较小值
                volume = int((account_asset if account_asset < self.VOLUME_MAX_BUY else self.VOLUME_MAX_BUY) / stock_price)
                logger.info(f"使用默认计算方式: 可用资金{account_asset}, 最大买入金额{self.VOLUME_MAX_BUY}, 实时价格{stock_price}, 计算股数{volume}")

            volume = (volume // 100) * 100  # 对齐100股整数倍
            if volume < 100:
                logger.warning("买入数量不足100股")
                # 修改：即使不足100股也返回计算结果，让调用者决定是否执行
                return volume if volume > 0 else None
            return volume
        except Exception as e:
            error_msg = f"买入数量计算失败: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return None

    def calculate_sell_volume(self, account_asset, available_shares, stock_price, new_ratio=None):
        """
        根据可用数量和策略比例计算卖出数量
        
        Args:
            account_asset: 账户总资产
            available_shares: 可卖数量
            stock_price: 股票当前价格
            new_ratio: 新仓位比例（可选）
            
        Returns:
            int: 卖出数量，或 None 表示失败
        """
        try:
            if available_shares is None or available_shares <= 0:
                logger.warning(f"无可用数量: available_shares={available_shares}")
                return None

            # 确保new_ratio是数值类型
            if new_ratio is not None:
                try:
                    new_ratio = float(new_ratio)
                except (ValueError, TypeError):
                    logger.warning(f"new_ratio转换为数值失败: {new_ratio}")
                    new_ratio = None

            # 当new_ratio为0或None时，全仓卖出
            if new_ratio is None or new_ratio <= 0:
                volume = available_shares  # 全部卖出
                logger.info("全部卖出")
            else:
                # 按比例计算应该保留的数量，然后计算卖出数量
                # 计算目标金额 = 账户总资产 * 新比例% / 100 （因为new_ratio是百分比）
                target_amount = account_asset * float(new_ratio) / 100
                logger.info(f"目标投资金额: {account_asset} * {new_ratio}% = {target_amount}")

                # 计算股数 = 目标金额 / 价格
                target_volume = int(target_amount / stock_price)
                logger.info(f"计算目标股数: {target_amount} / {stock_price} = {target_volume}")

                # 转换为100的倍数
                target_volume = (target_volume // 100) * 100
                if target_volume < 100:
                    logger.warning("计算出的目标股数不足100股")
                    target_volume = 0

                logger.info(f"计算卖出时，需要持仓股数: {target_volume}")
                
                # 计算需要卖出的数量
                volume = available_shares - target_volume
                if volume < 0:
                    volume = 0  # 不应该出现负数，如果出现则设为0
                    
                logger.info(f"按比例计算卖出: 当前持有{available_shares}股, 新比例{new_ratio}%, 目标持仓{target_volume}股, 卖出{volume}股")

            volume = (volume // 100) * 100
            # 修改：即使不足100股也返回计算结果，让调用者决定是否执行
            if volume <= 0:
                logger.info("计算出的卖出数量为0或负数，将返回0表示不卖出")
                return 0

            if volume < 100 and volume > 0:
                logger.warning(f"卖出数量不足100股: 计算结果={volume}")
                # 在这种情况下，我们仍然返回计算出的数量，让调用者决定是否继续
                return volume

            return volume
        except Exception as e:
            error_msg = f"卖出数量计算失败: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return None

    def calculate_batch_buy_volumes(self, stocks_info, total_buying_power):
        """
        根据总资金和各股票的目标比例，批量计算买入数量
        
        Args:
            stocks_info: 股票信息列表，每个元素包含 {'stock_name', 'real_price', 'target_ratio'}
            total_buying_power: 总可用资金
            
        Returns:
            dict: 每只股票的买入数量字典
        """
        try:
            if not stocks_info or total_buying_power <= 0:
                logger.warning("无效的输入参数")
                return {}

            # 首先计算各股票的目标资金
            target_amounts = {}
            total_target_ratio = sum([stock['新比例%'] for stock in stocks_info])
            
            # 如果总比例超过100%，则按比例缩放
            scale_factor = 1.0
            if total_target_ratio > 100:
                scale_factor = 100.0 / total_target_ratio
                logger.info(f"目标比例总和超过100% ({total_target_ratio}%)，按比例缩放: {scale_factor}")

            # 计算每只股票的目标资金和数量
            buy_volumes = {}
            for stock in stocks_info:
                stock_name = stock['stock_name']
                real_price = stock['real_price']
                target_ratio = stock['target_ratio'] * scale_factor
                
                # 计算目标资金
                target_amount = total_buying_power * (target_ratio / 100)
                
                # 计算股数
                volume = int(target_amount / real_price)
                volume = (volume // 100) * 100  # 对齐100股整数倍
                
                buy_volumes[stock_name] = volume
                logger.info(f"{stock_name}: 比例{target_ratio:.2f}%，目标资金{target_amount:.2f}，价格{real_price}，计算股数{volume}")

            return buy_volumes
        except Exception as e:
            error_msg = f"批量买入数量计算失败: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return {}

    def get_account_info(self, account_file, account_name, stock_name):
        """
        获取相应账户里某股票的'持有数量'的值
        
        Args:
            account_file: 账户文件路径
            account_name: 账户名称
            stock_name: 股票名称
            
        Returns:
            tuple: (账户总资产, 账户余额, 股票可用数量, 股票持仓比例, 股票价格)
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(account_file):
                error_msg = f"账户文件不存在: {account_file}"
                logger.error(error_msg)
                send_notification(error_msg)
                return 0.0, 0.0, 0, 0, 0
                
            # 初始化返回值
            account_asset = 0.0
            account_balance = 0.0
            stock_available = 0
            stock_ratio = 0
            stock_price = 0
            
            # 读取工作表
            with pd.ExcelFile(account_file, engine='openpyxl') as xls:
                sheets = xls.sheet_names
                logger.info(f"账户文件中的工作表列表: {sheets}")
                
                # 尝试读取账户汇总数据
                if '账户汇总' in sheets:
                    try:
                        account_balance_data = pd.read_excel(xls, sheet_name='账户汇总')
                        logger.info(f"账户汇总数据形状: {account_balance_data.shape}")
                        logger.info(f"账户汇总列名: {account_balance_data.columns.tolist()}")
                        
                        # 尝试查找账户名
                        # 检查可能的列名变体
                        account_col = None
                        for col in ['账户名', '账户名称']:
                            if col in account_balance_data.columns:
                                account_col = col
                                break
                        
                        if account_col:
                            # 查找匹配的账户行
                            matching_rows = account_balance_data[account_balance_data[account_col].str.contains(account_name, na=False)]
                            if not matching_rows.empty:
                                account_row = matching_rows.iloc[0]
                                logger.info(f"找到匹配的账户行: {account_row.to_dict()}")
                                
                                # 尝试获取总资产
                                for asset_col in ['总资产', '资产', '资产总值']:
                                    if asset_col in account_row:
                                        try:
                                            account_asset = float(str(account_row[asset_col]).replace(',', ''))
                                            logger.info(f"从'{asset_col}'列获取总资产: {account_asset}")
                                            break
                                        except (ValueError, TypeError):
                                            logger.warning(f"无法转换'{asset_col}'的值为数字: {account_row[asset_col]}")
                                
                                # 尝试获取可用资金
                                for balance_col in ['可用', '可用资金', '余额']:
                                    if balance_col in account_row:
                                        try:
                                            account_balance = float(str(account_row[balance_col]).replace(',', ''))
                                            logger.info(f"从'{balance_col}'列获取可用资金: {account_balance}")
                                            break
                                        except (ValueError, TypeError):
                                            logger.warning(f"无法转换'{balance_col}'的值为数字: {account_row[balance_col]}")
                            else:
                                logger.warning(f"未在汇总表中找到账户 '{account_name}'")
                        else:
                            logger.warning("账户汇总表中没有找到有效的账户名列")
                    except Exception as e:
                        error_msg = f"读取账户汇总数据时出错: {e}"
                        logger.error(error_msg)
                        send_notification(error_msg)
                else:
                    logger.warning("账户文件中没有'账户汇总'工作表")
                
                # 尝试直接从账户工作表获取资产信息（备用方案）
                if account_asset <= 0 and account_name in sheets:
                    try:
                        account_sheet_data = pd.read_excel(xls, sheet_name=account_name)
                        logger.info(f"直接读取账户工作表 {account_name} 的数据形状: {account_sheet_data.shape}")
                        logger.info(f"账户工作表列名: {account_sheet_data.columns.tolist()}")
                        
                        # 如果工作表有表头行，尝试从中获取资产信息
                        if not account_sheet_data.empty:
                            # 检查第一行是否包含总资产信息
                            first_row = account_sheet_data.iloc[0].dropna()
                            logger.info(f"账户工作表第一行数据: {first_row.to_dict()}")
                            
                            # 尝试识别并提取总资产
                            for idx, value in first_row.items():
                                if '总资产' in str(idx) or '资产' in str(idx):
                                    try:
                                        # 从字符串中提取数字
                                        import re
                                        numbers = re.findall(r'\d+(?:\.\d+)?', str(value))
                                        if numbers:
                                            account_asset = float(numbers[0])
                                            logger.info(f"从账户工作表中提取总资产: {account_asset}")
                                            break
                                    except (ValueError, TypeError):
                                        logger.warning(f"无法从值 '{value}' 中提取数字")
                    except Exception as e:
                        error_msg = f"从账户工作表获取资产信息时出错: {e}"
                        logger.error(error_msg)
                        send_notification(error_msg)
                
                # 读取股票持仓信息
                if account_name in sheets:
                    try:
                        account_holding_data = pd.read_excel(xls, sheet_name=account_name)
                        logger.info(f"持仓数据形状: {account_holding_data.shape}")
                        logger.info(f"持仓数据列名: {account_holding_data.columns.tolist()}")
                        
                        # 查找股票名称列
                        name_column = None
                        for col in ['股票名称', '标的名称']:
                            if col in account_holding_data.columns:
                                name_column = col
                                break
                        
                        if name_column:
                            # 查找匹配的股票
                            matching_stocks = account_holding_data[account_holding_data[name_column].str.contains(stock_name, na=False)]
                            if not matching_stocks.empty:
                                stock_data = matching_stocks.iloc[0]
                                logger.info(f"找到匹配的股票数据: {stock_data.to_dict()}")
                                
                                # 提取股票信息
                                for avail_col in ['可用', '可用数量']:
                                    if avail_col in stock_data:
                                        try:
                                            stock_available = int(stock_data[avail_col])
                                            break
                                        except (ValueError, TypeError):
                                            logger.warning(f"无法转换可用数量: {stock_data[avail_col]}")
                                
                                for ratio_col in ['持仓占比', '占比']:
                                    if ratio_col in stock_data:
                                        try:
                                            stock_ratio = float(stock_data[ratio_col])
                                            break
                                        except (ValueError, TypeError):
                                            logger.warning(f"无法转换持仓占比: {stock_data[ratio_col]}")
                                
                                for price_col in ['当前价', '价格']:
                                    if price_col in stock_data:
                                        try:
                                            stock_price = float(str(stock_data[price_col]).replace(',', ''))
                                            break
                                        except (ValueError, TypeError):
                                            logger.warning(f"无法转换价格: {stock_data[price_col]}")
                            else:
                                logger.warning(f"未在账户 {account_name} 中找到股票 {stock_name}")
                        else:
                            logger.warning("持仓数据中没有找到有效的股票名称列")
                    except Exception as e:
                        error_msg = f"读取持仓数据时出错: {e}"
                        logger.error(error_msg)
                        send_notification(error_msg)
                else:
                    logger.warning(f"账户文件中没有 {account_name} 工作表")
        
        except Exception as e:
            error_msg = f"获取账户信息时发生异常: {e}"
            logger.error(error_msg, exc_info=True)
            send_notification(error_msg)
            account_asset = 0.0
            account_balance = 0.0
            stock_available = 0
            stock_ratio = 0
            stock_price = 0
            
        logger.info(f"获取到 {account_name} 总资产: {account_asset} 余额: {account_balance}, {stock_name} 当前价 {stock_price} 可用 {stock_available} 持仓占比 {stock_ratio}")
        return account_asset, account_balance, stock_available, stock_ratio, stock_price

    def operate_stock(self, operation, stock_name, volume=None):
        """
        执行股票交易操作
        
        Args:
            operation: 操作类型("买入"或"卖出")
            stock_name: 股票名称
            volume: 交易数量
            
        Returns:
            tuple: (是否成功, 消息)
        """
        # 进入到 账户 页面
        self.common_page.goto_account_page()
        try:
            # 点击按钮 买/卖 操作按钮（tab)
            self.trading_page.click_operate_button(operation)
            # 搜索股票
            self.trading_page.search_stock(stock_name)

            # 检查交易数量是否有效
            # 修改：允许volume为0的情况
            if volume is None:
                error_msg = f"{operation} {stock_name} 交易数量为 None，跳过交易"
                logger.warning(error_msg)
                send_notification(error_msg)
                return False, error_msg

            # 输入交易数量
            self.trading_page.input_volume(int(volume))
            # 点击提交按钮
            self.trading_page.click_submit_button(operation)
            # 处理弹窗
            success, info = self.trading_page.dialog_handle()
            # 发送交易结果通知
            send_notification(f"{operation} {stock_name} {volume}股 {success} {info}")
            logger.info(f"{operation} {stock_name} {volume}股 {success} {info}")
            return success, info
        except Exception as e:
            calculate_volume = volume if volume is not None else "未知"
            error_msg = f"{operation} {stock_name} {calculate_volume} 股失败: {e}"
            logger.error(error_msg, exc_info=True)
            send_notification(error_msg)
            return False, error_msg

if __name__ == '__main__':
    trade = TradeLogic()
    trade.operate_stock("卖出", "中国电信", 10000)