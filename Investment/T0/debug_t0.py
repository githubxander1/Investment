# T0交易系统调试脚本
# 移除时间限制，直接运行检测

import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from monitor.signal_detector import SignalDetector
from config.settings import DEFAULT_STOCK_POOL
from utils.logger import setup_logger, log_signal

# 设置日志
logger = setup_logger('debug_t0')

def debug_signals():
    """调试信号检测"""
    logger.info("开始调试T0交易系统信号检测...")
    print("开始调试T0交易系统信号检测...")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 使用默认股票池中的第一个股票
    stock_code = DEFAULT_STOCK_POOL[0]
    print(f"检测股票: {stock_code}")
    logger.info(f"检测股票: {stock_code}")
    
    # 创建信号检测器
    detector = SignalDetector(stock_code)
    
    # 直接检测信号（不检查时间限制）
    print("正在获取股票数据...")
    logger.info("正在获取股票数据...")
    df = detector.get_stock_data()
    
    if df is None or df.empty:
        print("❌ 无法获取股票数据")
        logger.error("无法获取股票数据")
        return
    
    print(f"✅ 成功获取股票数据，共 {len(df)} 条记录")
    logger.info(f"成功获取股票数据，共 {len(df)} 条记录")
    
    # 获取昨收价
    prev_close = detector.get_prev_close()
    if prev_close is None:
        prev_close = df['开盘'].dropna().iloc[0] if not df['开盘'].dropna().empty else 0
        print(f"⚠️ 无法获取昨收价，使用开盘价替代: {prev_close:.2f}")
        logger.warning(f"无法获取昨收价，使用开盘价替代: {prev_close:.2f}")
    else:
        print(f"昨收价: {prev_close:.2f}")
        logger.info(f"昨收价: {prev_close:.2f}")
    
    # 检测各指标信号
    print("\n=== 检测阻力支撑指标信号 ===")
    logger.info("检测阻力支撑指标信号")
    resistance_support_signals = detector.detect_resistance_support_signals(df, prev_close)
    if resistance_support_signals:
        print(f"买入信号: {resistance_support_signals['buy']}")
        print(f"卖出信号: {resistance_support_signals['sell']}")
        print(f"详情: {resistance_support_signals['details']}")
        logger.info(f"阻力支撑信号 - 买入: {resistance_support_signals['buy']}, 卖出: {resistance_support_signals['sell']}")
        if resistance_support_signals['details']:
            logger.info(f"阻力支撑信号详情: {resistance_support_signals['details']}")
            
        # 记录信号日志
        if resistance_support_signals['buy']:
            log_signal(stock_code, '阻力支撑', '买入', resistance_support_signals['details'])
        if resistance_support_signals['sell']:
            log_signal(stock_code, '阻力支撑', '卖出', resistance_support_signals['details'])
    else:
        print("未生成阻力支撑信号")
        logger.info("未生成阻力支撑信号")
    
    print("\n=== 检测扩展指标信号 ===")
    logger.info("检测扩展指标信号")
    extended_signals = detector.detect_extended_signals(df, prev_close)
    if extended_signals:
        print(f"买入信号: {extended_signals['buy']}")
        print(f"卖出信号: {extended_signals['sell']}")
        print(f"详情: {extended_signals['details']}")
        logger.info(f"扩展指标信号 - 买入: {extended_signals['buy']}, 卖出: {extended_signals['sell']}")
        if extended_signals['details']:
            logger.info(f"扩展指标信号详情: {extended_signals['details']}")
            
        # 记录信号日志
        if extended_signals['buy']:
            log_signal(stock_code, '扩展指标', '买入', extended_signals['details'])
        if extended_signals['sell']:
            log_signal(stock_code, '扩展指标', '卖出', extended_signals['details'])
    else:
        print("未生成扩展指标信号")
        logger.info("未生成扩展指标信号")
    
    print("\n=== 检测量价指标信号 ===")
    logger.info("检测量价指标信号")
    volume_price_signals = detector.detect_volume_price_signals(df, prev_close)
    if volume_price_signals:
        print(f"买入信号: {volume_price_signals['buy']}")
        print(f"卖出信号: {volume_price_signals['sell']}")
        print(f"详情: {volume_price_signals['details']}")
        logger.info(f"量价指标信号 - 买入: {volume_price_signals['buy']}, 卖出: {volume_price_signals['sell']}")
        if volume_price_signals['details']:
            logger.info(f"量价指标信号详情: {volume_price_signals['details']}")
            
        # 记录信号日志
        if volume_price_signals['buy']:
            log_signal(stock_code, '量价指标', '买入', volume_price_signals['details'])
        if volume_price_signals['sell']:
            log_signal(stock_code, '量价指标', '卖出', volume_price_signals['details'])
    else:
        print("未生成量价指标信号")
        logger.info("未生成量价指标信号")
    
    # 检测所有信号
    print("\n=== 检测所有信号 ===")
    logger.info("检测所有信号")
    all_signals = detector.detect_all_signals()
    if all_signals:
        print(f"共检测到 {len(all_signals)} 个信号:")
        logger.info(f"共检测到 {len(all_signals)} 个信号:")
        for signal in all_signals:
            print(f"- 指标: {signal['indicator']}, 类型: {signal['type']}, 详情: {signal['details']}")
            logger.info(f"信号 - 指标: {signal['indicator']}, 类型: {signal['type']}, 详情: {signal['details']}")
    else:
        print("未检测到任何新信号")
        logger.info("未检测到任何新信号")
    
    print("\n调试完成!")
    logger.info("调试完成!")

if __name__ == "__main__":
    debug_signals()