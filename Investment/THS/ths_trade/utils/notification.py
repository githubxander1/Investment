#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通知工具模块
提供系统通知、邮件通知等功能
"""

import os
import logging
from typing import Optional, Dict, Any

# 使用统一的日志记录器
from Investment.THS.ths_trade.utils.logger import setup_logger

logger = setup_logger('notification.log')


def send_notification(message: str, title: Optional[str] = "交易通知", 
                      notification_type: str = "system") -> bool:
    """
    发送通知
    
    Args:
        message: 通知消息内容
        title: 通知标题
        notification_type: 通知类型，目前仅支持"system"
        
    Returns:
        bool: 是否发送成功
    """
    try:
        logger.info(f"发送通知: [{title}] {message}")
        
        # Windows系统通知
        if os.name == 'nt':
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=10)
                return True
            except ImportError:
                logger.warning("未安装win10toast，无法发送系统通知")
                # 回退到简单的日志记录
                return True
        
        # 其他系统暂不支持，仅记录日志
        return True
        
    except Exception as e:
        logger.error(f"发送通知失败: {e}")
        return False


def send_trade_notification(stock_name: str, operation: str, volume: int,
                           price: Optional[float] = None, success: bool = True,
                           message: Optional[str] = None) -> bool:
    """
    发送交易通知
    
    Args:
        stock_name: 股票名称
        operation: 操作类型（买入/卖出）
        volume: 交易数量
        price: 交易价格（可选）
        success: 是否成功
        message: 附加消息（可选）
        
    Returns:
        bool: 是否发送成功
    """
    status_text = "✅ 成功" if success else "❌ 失败"
    title = f"交易{operation}通知 {status_text}"
    
    content = f"股票: {stock_name}\n操作: {operation}\n数量: {volume}"
    if price:
        content += f"\n价格: {price:.2f}"
    if message:
        content += f"\n{message}"
    
    return send_notification(content, title)