# 信号处理器模块
import os
import json
import logging
from datetime import datetime

from Investment.T0.utils.logger import setup_logger

logger = setup_logger('signal_handler')

class SignalHandler:
    """
    信号处理器 - 负责保存和管理交易信号
    """
    
    def __init__(self, signal_dir=None):
        """
        初始化信号处理器
        
        Args:
            signal_dir: 信号存储目录，如果不提供则使用默认路径
        """
        # 设置信号存储目录
        self.signal_dir = signal_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'signals'
        )
        
        # 确保目录存在
        try:
            os.makedirs(self.signal_dir, exist_ok=True)
            logger.info(f"信号存储目录设置为: {self.signal_dir}")
        except Exception as e:
            logger.error(f"创建信号存储目录失败: {e}")
    
    def save_signal(self, signal_data):
        """
        保存交易信号
        
        Args:
            signal_data: 信号数据字典，包含交易相关信息
        
        Returns:
            bool: 是否保存成功
        """
        try:
            # 获取当前日期，用于文件名
            today = datetime.now().strftime("%Y-%m-%d")
            signal_file = os.path.join(self.signal_dir, f"signals_{today}.json")
            
            # 读取现有信号
            signals = []
            if os.path.exists(signal_file):
                try:
                    with open(signal_file, 'r', encoding='utf-8') as f:
                        signals = json.load(f)
                except json.JSONDecodeError:
                    logger.warning(f"信号文件 {signal_file} 格式错误，创建新文件")
                    signals = []
            
            # 添加新信号
            signals.append(signal_data)
            
            # 保存信号到文件
            with open(signal_file, 'w', encoding='utf-8') as f:
                json.dump(signals, f, ensure_ascii=False, indent=2)
            
            logger.info(f"信号已保存到: {signal_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存信号失败: {e}")
            return False
    
    def get_today_signals(self):
        """
        获取今日所有信号
        
        Returns:
            list: 今日信号列表
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            signal_file = os.path.join(self.signal_dir, f"signals_{today}.json")
            
            if os.path.exists(signal_file):
                with open(signal_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return []
            
        except Exception as e:
            logger.error(f"获取今日信号失败: {e}")
            return []
    
    def get_signals_by_stock(self, stock_code, start_date=None, end_date=None):
        """
        根据股票代码获取信号
        
        Args:
            stock_code: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            list: 匹配的信号列表
        """
        try:
            import glob
            
            # 构建文件匹配模式
            pattern = os.path.join(self.signal_dir, "signals_*.json")
            signal_files = glob.glob(pattern)
            
            # 按日期排序
            signal_files.sort()
            
            # 筛选日期范围
            if start_date or end_date:
                filtered_files = []
                for file_path in signal_files:
                    file_name = os.path.basename(file_path)
                    file_date = file_name.replace("signals_", "").replace(".json", "")
                    
                    if start_date and file_date < start_date:
                        continue
                    if end_date and file_date > end_date:
                        continue
                    
                    filtered_files.append(file_path)
                
                signal_files = filtered_files
            
            # 收集匹配的信号
            matched_signals = []
            for file_path in signal_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        signals = json.load(f)
                        
                        for signal in signals:
                            if signal.get("stock_code") == stock_code:
                                matched_signals.append(signal)
                except Exception as e:
                    logger.error(f"读取信号文件 {file_path} 失败: {e}")
            
            return matched_signals
            
        except Exception as e:
            logger.error(f"根据股票代码获取信号失败: {e}")
            return []