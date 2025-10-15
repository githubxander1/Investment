#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
增强版同花顺交易适配器
为原有适配器添加多账户切换功能
"""

import sys
import os
import logging
import time
import subprocess
from datetime import datetime
from typing import Dict, Optional, List

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('enhanced_ths_trade_adapter')

# 导入ths_trade核心模块
try:
    from applications.adapter.ths_trade_adapter import THSTradeAdapter
    import applications.API_Config as API_Config
    THS_TRADE_AVAILABLE = True
except ImportError as e:
    logging.error(f"导入ths_trade模块失败: {e}")
    THS_TRADE_AVAILABLE = False


class EnhancedTHSTradeAdapter:
    """
    增强版同花顺交易适配器类，在原有功能基础上添加多账户切换支持
    """
    
    def __init__(self, accounts_config: Optional[Dict] = None):
        """
        初始化增强版适配器
        
        Args:
            accounts_config: 账户配置字典，格式如下：
                {
                    "账户1": {"exe_path": "path/to/xiadan.exe", "password": "交易密码"},
                    "账户2": {"exe_path": "path/to/xiadan.exe", "password": "交易密码"},
                    ...
                }
                如不提供，将使用默认配置
        """
        self.accounts = accounts_config or self._get_default_accounts_config()
        self.current_account_name = None
        self.current_adapter = None
        self.current_exe_path = None
        
        logger.info(f"增强版同花顺交易适配器初始化完成，共配置了 {len(self.accounts)} 个账户")
    
    def _get_default_accounts_config(self) -> Dict:
        """
        获取默认账户配置
        用户可以在此方法中硬编码账户信息，或从配置文件读取
        """
        # 默认配置示例，用户需要根据实际情况修改
        return {
            "默认账户": {"exe_path": API_Config.cfg['exe_path'], "password": ""},
            # "长城证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "660493"},
            # "中泰证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "170212"},
            # "川财证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "170212"},
            # "中山证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "660493"},
        }
    
    def _close_ths_process(self, exe_path: str) -> bool:
        """
        关闭同花顺交易软件进程
        
        Args:
            exe_path: 同花顺交易软件路径
            
        Returns:
            bool: 是否成功关闭
        """
        try:
            process_name = os.path.basename(exe_path)
            logger.info(f"正在关闭同花顺交易软件进程: {process_name}")
            
            # 使用taskkill命令关闭进程
            if sys.platform.startswith('win'):
                subprocess.run(['taskkill', '/F', '/IM', process_name], shell=True, check=False)
                # 额外关闭可能的相关进程
                subprocess.run(['taskkill', '/F', '/IM', 'xiadan.exe'], shell=True, check=False)
                subprocess.run(['taskkill', '/F', '/IM', 'xiadan.bin'], shell=True, check=False)
            else:
                logger.error("不支持的操作系统，仅Windows系统支持自动关闭进程")
                return False
            
            # 等待进程完全关闭
            time.sleep(3)
            logger.info(f"同花顺交易软件进程已关闭")
            return True
        except Exception as e:
            logger.error(f"关闭同花顺交易软件进程时发生错误: {e}")
            return False
    
    def _start_ths_process(self, exe_path: str) -> bool:
        """
        启动同花顺交易软件进程
        
        Args:
            exe_path: 同花顺交易软件路径
            
        Returns:
            bool: 是否成功启动
        """
        try:
            if not os.path.exists(exe_path):
                logger.error(f"同花顺交易软件路径不存在: {exe_path}")
                return False
                
            logger.info(f"正在启动同花顺交易软件: {exe_path}")
            # 启动进程，不阻塞当前线程
            subprocess.Popen([exe_path], shell=True)
            
            # 等待软件启动
            logger.info(f"同花顺交易软件正在启动，请稍候...")
            time.sleep(15)  # 给足时间让软件启动并可能需要用户手动登录
            
            logger.info(f"同花顺交易软件启动完成")
            return True
        except Exception as e:
            logger.error(f"启动同花顺交易软件时发生错误: {e}")
            return False
    
    def switch_account(self, account_name: str) -> bool:
        """
        切换到指定账户
        
        Args:
            account_name: 账户名称
            
        Returns:
            bool: 是否成功切换
        """
        try:
            # 检查账户是否在配置中
            if account_name not in self.accounts:
                logger.error(f"账户 {account_name} 未在配置中定义")
                logger.info(f"可用账户列表: {list(self.accounts.keys())}")
                return False
            
            # 如果当前已是目标账户，无需切换
            if self.current_account_name == account_name:
                logger.info(f"当前已是 {account_name} 账户，无需切换")
                return True
            
            account_config = self.accounts[account_name]
            exe_path = account_config['exe_path']
            
            logger.info(f"开始切换到账户: {account_name} (执行文件: {exe_path})")
            
            # 关闭当前的同花顺进程
            if self.current_exe_path:
                self._close_ths_process(self.current_exe_path)
            
            # 启动新的同花顺进程
            if not self._start_ths_process(exe_path):
                logger.error("启动同花顺交易软件失败，切换账户中止")
                return False
            
            # 提示用户可能需要手动登录
            logger.warning("注意: 同花顺交易软件已启动，您可能需要手动完成账户登录操作")
            logger.warning("请确保已在交易软件中成功登录目标账户，然后按任意键继续...")
            
            # 暂停执行，等待用户确认登录完成
            # input("按Enter键继续...")
            logger.info("等待10秒以确保登录完成...")
            time.sleep(10)
            
            # 初始化新的交易适配器
            self.current_adapter = THSTradeAdapter(exe_path=exe_path, account_name=account_name)
            
            if not self.current_adapter.initialized:
                logger.error("交易适配器初始化失败，请检查同花顺交易软件是否已正确启动并登录")
                return False
            
            # 更新当前账户信息
            self.current_account_name = account_name
            self.current_exe_path = exe_path
            
            logger.info(f"✅ 成功切换到账户: {account_name}")
            return True
            
        except Exception as e:
            logger.error(f"切换账户时发生异常: {e}")
            return False
    
    def _check_adapter(self) -> bool:
        """
        检查当前交易适配器是否可用
        
        Returns:
            bool: 是否可用
        """
        if not self.current_adapter or not self.current_adapter.initialized:
            logger.error("交易适配器未初始化或不可用，请先使用switch_account()方法切换到有效账户")
            return False
        return True
    
    def list_available_accounts(self) -> List[str]:
        """
        列出所有可用的账户
        
        Returns:
            List[str]: 账户名称列表
        """
        return list(self.accounts.keys())
    
    def get_current_account(self) -> Optional[str]:
        """
        获取当前使用的账户名称
        
        Returns:
            Optional[str]: 当前账户名称，未初始化时返回None
        """
        return self.current_account_name
    
    # 以下方法代理到当前的THSTradeAdapter实例
    
    def buy_stock(self, stock_code: str, stock_name: str, amount: int, strategy_no: str = "default") -> Dict:
        """
        买入股票
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            amount: 买入数量
            strategy_no: 策略编号
            
        Returns:
            dict: 交易结果
        """
        if not self._check_adapter():
            return {"success": False, "msg": "交易适配器未初始化或不可用"}
        return self.current_adapter.buy_stock(stock_code, stock_name, amount, strategy_no)
    
    def sell_stock(self, stock_code: str, stock_name: str, amount: int, strategy_no: str = "default") -> Dict:
        """
        卖出股票
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            amount: 卖出数量
            strategy_no: 策略编号
            
        Returns:
            dict: 交易结果
        """
        if not self._check_adapter():
            return {"success": False, "msg": "交易适配器未初始化或不可用"}
        return self.current_adapter.sell_stock(stock_code, stock_name, amount, strategy_no)
    
    def get_position(self):
        """
        获取持仓信息
        
        Returns:
            pd.DataFrame or None: 持仓数据
        """
        if not self._check_adapter():
            return None
        return self.current_adapter.get_position()
    
    def get_balance(self):
        """
        获取资金情况
        
        Returns:
            pd.DataFrame or None: 资金数据
        """
        if not self._check_adapter():
            return None
        return self.current_adapter.get_balance()
    
    def get_today_trades(self):
        """
        获取当日成交
        
        Returns:
            pd.DataFrame or None: 当日成交数据
        """
        if not self._check_adapter():
            return None
        return self.current_adapter.get_today_trades()
    
    def get_today_entrusts(self):
        """
        获取当日委托
        
        Returns:
            pd.DataFrame or None: 当日委托数据
        """
        if not self._check_adapter():
            return None
        return self.current_adapter.get_today_entrusts()


# 创建一个全局实例，方便导入使用
try:
    enhanced_adapter = EnhancedTHSTradeAdapter()
except Exception as e:
    logger.error(f"创建增强版适配器全局实例失败: {e}")
    enhanced_adapter = None


if __name__ == "__main__":
    """
    测试增强版适配器功能
    """
    # 初始化增强版适配器
    # 示例：自定义账户配置
    custom_accounts = {
        "默认账户": {"exe_path": API_Config.cfg['exe_path'], "password": ""},
        # 请根据实际情况修改以下配置
        # "长城证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "660493"},
        # "中泰证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "170212"},
    }
    
    adapter = EnhancedTHSTradeAdapter(accounts_config=custom_accounts)
    
    # 列出所有可用账户
    print("\n=== 可用账户列表 ===")
    accounts = adapter.list_available_accounts()
    for i, account in enumerate(accounts):
        print(f"{i+1}. {account}")
    
    # 切换到第一个账户
    if accounts:
        print(f"\n=== 切换到账户: {accounts[0]} ===")
        if adapter.switch_account(accounts[0]):
            print(f"当前账户: {adapter.get_current_account()}")
            
            # 测试获取持仓
            print("\n=== 测试获取持仓 ===")
            position = adapter.get_position()
            if position is not None:
                print(f"持仓股票数量: {len(position)}")
                print(position.head())
            else:
                print("无法获取持仓信息，可能是账户未正确登录或交易软件未完全启动")
        else:
            print("账户切换失败")
    else:
        print("没有配置可用账户")