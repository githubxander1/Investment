#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票实时监控脚本 (monitor_stocks.py)

功能：
1. 定时监控多个股票的实时数据
2. 运行综合T0策略分析
3. 当检测到交易信号时发送系统通知
4. 智能判断交易时间，只在交易时段运行

使用方法：
python monitor_stocks.py [监控间隔分钟数]
"""

import os
import sys
import time
import datetime
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(project_root, 'monitor.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 导入策略模块
try:
    from indicators.comprehensive_t0_strategy import analyze_comprehensive_t0
    logger.info("✅ 成功导入综合T0策略模块")
except ImportError as e:
    logger.error(f"❌ 导入策略模块失败: {e}")
    sys.exit(1)


class StockMonitor:
    """股票监控类"""
    
    def __init__(self, stocks: List[str], interval_minutes: int = 5):
        """
        初始化监控器
        
        Args:
            stocks: 要监控的股票代码列表
            interval_minutes: 监控间隔（分钟）
        """
        self.stocks = stocks
        self.interval_minutes = interval_minutes
        self.last_signals: Dict[str, Dict[str, Any]] = {}
        self.running = False
        
        # 初始化上次信号记录
        for stock in stocks:
            self.last_signals[stock] = {
                'buy_signal': None,
                'sell_signal': None,
                'has_open_position': False
            }
    
    def is_trading_time(self) -> bool:
        """
        判断当前是否为交易时间
        
        Returns:
            bool: 是否为交易时间
        """
        now = datetime.datetime.now()
        
        # 判断是否为工作日（周一到周五）
        if now.weekday() >= 5:
            return False
        
        # 判断是否在交易时间段内
        current_time = now.time()
        morning_trading = datetime.time(9, 30) <= current_time <= datetime.time(11, 30)
        afternoon_trading = datetime.time(13, 0) <= current_time <= datetime.time(15, 0)
        
        return morning_trading or afternoon_trading
    
    def _send_notification(self, message: str):
        """
        发送系统通知
        
        Args:
            message: 通知内容
        """
        try:
            # 首先打印到控制台
            print("=" * 50)
            print("🔔 交易信号通知")
            print("=" * 50)
            print(message)
            print("=" * 50)
            
            # 记录到日志
            logger.info(f"发送通知: {message}")
            
            # 尝试发送Windows系统通知
            try:
                # 尝试导入win10toast库
                try:
                    from win10toast import ToastNotifier
                    
                    # 创建通知器
                    toaster = ToastNotifier()
                    
                    # 解析消息，提取股票代码和信号类型作为标题
                    lines = message.strip().split('\n')
                    title = "T0交易信号"
                    
                    # 尝试提取股票代码和信号类型
                    stock_code = None
                    signal_type = None
                    
                    for line in lines:
                        if line.startswith("股票代码:"):
                            stock_code = line.split(":")[1].strip()
                        elif line.startswith("信号类型:"):
                            signal_type = line.split(":")[1].strip()
                    
                    # 如果找到股票代码和信号类型，构建更具体的标题
                    if stock_code and signal_type:
                        title = f"{stock_code} - {signal_type}"
                    elif stock_code:
                        title = f"{stock_code} 信号"
                    
                    # 发送通知
                    toaster.show_toast(
                        title=title,
                        msg="点击查看详情",
                        icon_path=None,
                        duration=10,
                        threaded=True
                    )
                    logger.info("✅ Windows系统通知已发送")
                    
                except ImportError:
                    logger.warning("❌ win10toast库未安装，尝试使用其他方式发送通知")
                    
                    # 尝试使用Windows内置的通知功能（通过powershell）
                    try:
                        import subprocess
                        
                        # 清理消息内容，使其适合PowerShell
                        clean_message = message.replace('"', '\"').replace('`', '``')
                        
                        # 构建PowerShell命令
                        ps_command = f'Add-Type -AssemblyName System.Windows.Forms; $global:balloon = New-Object System.Windows.Forms.NotifyIcon; $path = (Get-Process -id $pid).Path; $balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path); $balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info; $balloon.BalloonTipText = "{clean_message}"; $balloon.BalloonTipTitle = "T0交易信号"; $balloon.Visible = $true; $balloon.ShowBalloonTip(10000);'
                        
                        # 执行PowerShell命令
                        subprocess.Popen(["powershell", "-Command", ps_command], shell=True)
                        logger.info("✅ 通过PowerShell发送Windows通知")
                    except Exception as ps_e:
                        logger.warning(f"❌ 通过PowerShell发送通知失败: {ps_e}")
                        
            except Exception as notify_e:
                logger.error(f"发送系统通知时出错: {notify_e}")
                
        except Exception as e:
            logger.error(f"发送通知时出错: {e}")
    
    def monitor_stock(self, stock_code: str):
        """
        监控单个股票
        
        Args:
            stock_code: 股票代码
        """
        try:
            logger.info(f"🔍 正在监控股票: {stock_code}")
            
            # 获取当前日期
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            
            # 获取是否有未完成的T操作
            has_open_position = self.last_signals[stock_code]['has_open_position']
            
            # 运行综合T0策略分析
            result = analyze_comprehensive_t0(
                stock_code=stock_code,
                trade_date=today,
                has_open_position=has_open_position
            )
            
            if result is None:
                logger.warning(f"❌ 无法获取 {stock_code} 的数据")
                return
            
            df, trades = result
            
            # 获取最新的买入和卖出信号
            buy_signals = df[df['Buy_Signal']]
            sell_signals = df[df['Sell_Signal']]
            
            # 处理最新的买入信号
            if not buy_signals.empty:
                latest_buy = buy_signals.index[-1]
                last_buy = self.last_signals[stock_code]['buy_signal']
                
                # 检查是否是新的买入信号
                if last_buy is None or latest_buy > last_buy:
                    self.last_signals[stock_code]['buy_signal'] = latest_buy
                    self.last_signals[stock_code]['has_open_position'] = True
                    
                    # 构建通知消息
                    message = f"股票代码: {stock_code}\n"
                    message += f"信号类型: 买入信号\n"
                    message += f"信号时间: {latest_buy.strftime('%H:%M:%S')}\n"
                    message += f"信号评分: {buy_signals.loc[latest_buy, 'buy_score']:.1f}\n"
                    message += f"当前价格: {buy_signals.loc[latest_buy, '收盘']:.2f}\n"
                    message += f"是否持有: {self.last_signals[stock_code]['has_open_position']}"
                    
                    # 发送通知
                    self._send_notification(message)
                    logger.info(f"✅ 检测到买入信号: {stock_code} at {latest_buy}")
            
            # 处理最新的卖出信号
            if not sell_signals.empty:
                latest_sell = sell_signals.index[-1]
                last_sell = self.last_signals[stock_code]['sell_signal']
                
                # 检查是否是新的卖出信号
                if last_sell is None or latest_sell > last_sell:
                    self.last_signals[stock_code]['sell_signal'] = latest_sell
                    self.last_signals[stock_code]['has_open_position'] = False
                    
                    # 构建通知消息
                    message = f"股票代码: {stock_code}\n"
                    message += f"信号类型: 卖出信号\n"
                    message += f"信号时间: {latest_sell.strftime('%H:%M:%S')}\n"
                    message += f"信号评分: {sell_signals.loc[latest_sell, 'sell_score']:.1f}\n"
                    message += f"当前价格: {sell_signals.loc[latest_sell, '收盘']:.2f}\n"
                    message += f"是否持有: {self.last_signals[stock_code]['has_open_position']}"
                    
                    # 发送通知
                    self._send_notification(message)
                    logger.info(f"✅ 检测到卖出信号: {stock_code} at {latest_sell}")
            
            # 记录交易对信息
            if trades:
                latest_trade = trades[-1]
                logger.info(f"📊 {stock_code} 最新交易对: 买入价 {latest_trade['buy_price']:.2f}, 卖出价 {latest_trade['sell_price']:.2f}, 收益 {latest_trade['profit_pct']:+.2f}%")
            
        except Exception as e:
            logger.error(f"监控 {stock_code} 时出错: {e}")
            import traceback
            traceback.print_exc()
    
    def run(self):
        """
        启动监控器
        """
        logger.info(f"🚀 股票监控系统启动")
        logger.info(f"📊 监控股票: {', '.join(self.stocks)}")
        logger.info(f"⏰ 监控间隔: {self.interval_minutes}分钟")
        
        self.running = True
        
        try:
            while self.running:
                # 检查是否为交易时间
                if self.is_trading_time():
                    logger.info(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (交易时间)")
                    
                    # 监控所有股票
                    for stock in self.stocks:
                        self.monitor_stock(stock)
                        time.sleep(1)  # 避免请求过于频繁
                    
                    # 等待下一个监控周期
                    wait_time = self.interval_minutes * 60
                    logger.info(f"等待 {self.interval_minutes} 分钟后再次监控")
                    
                    # 等待期间检查是否到达非交易时间
                    for _ in range(wait_time):
                        if not self.is_trading_time():
                            logger.info("💤 非交易时间，暂停监控")
                            break
                        time.sleep(1)
                else:
                    # 非交易时间，每30秒检查一次
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    logger.info(f"当前时间: {current_time} (非交易时间)")
                    
                    # 计算下次交易时间
                    now = datetime.datetime.now()
                    
                    if now.weekday() >= 5 or (now.hour >= 15 and now.minute > 0):
                        # 周末或收盘后，等待到下个交易日9:29
                        next_trading_day = now + datetime.timedelta(days=1)
                        while next_trading_day.weekday() >= 5:
                            next_trading_day += datetime.timedelta(days=1)
                        next_start = next_trading_day.replace(hour=9, minute=29, second=0, microsecond=0)
                    elif now.hour < 9 or (now.hour == 9 and now.minute < 29):
                        # 开盘前，等待到9:29
                        next_start = now.replace(hour=9, minute=29, second=0, microsecond=0)
                    elif now.hour >= 11 and now.minute >= 30 and now.hour < 13:
                        # 午休，等待到12:59
                        next_start = now.replace(hour=12, minute=59, second=0, microsecond=0)
                    else:
                        next_start = now + datetime.timedelta(minutes=30)
                    
                    wait_seconds = (next_start - now).total_seconds()
                    logger.info(f"等待到 {next_start.strftime('%Y-%m-%d %H:%M:%S')} ({wait_seconds:.0f}秒)")
                    time.sleep(min(wait_seconds, 30))  # 最多等待30秒就再次检查
                
        except KeyboardInterrupt:
            logger.info("👋 用户中断监控")
        finally:
            self.running = False
            logger.info("✅ 监控系统已停止")
    
    def stop(self):
        """
        停止监控器
        """
        self.running = False


def parse_arguments():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='股票实时监控脚本')
    parser.add_argument('interval', type=int, nargs='?', default=5, 
                       help='监控间隔（分钟），默认5分钟')
    parser.add_argument('--stocks', type=str, nargs='+', 
                       default=['600030', '000333', '002415'],  # 默认监控中信证券、美的集团、海康威视
                       help='要监控的股票代码列表')
    return parser.parse_args()


def main():
    """
    主函数
    """
    args = parse_arguments()
    
    # 创建监控器
    monitor = StockMonitor(
        stocks=args.stocks,
        interval_minutes=args.interval
    )
    
    # 启动监控
    monitor.run()


if __name__ == "__main__":
    main()