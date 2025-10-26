#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图表管理模块 - 负责主分时图和指标图的绘制
"""

import pandas as pd
import numpy as np
import logging
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .config import MAIN_CHART_SIZE, INDICATOR_CHART_SIZE, DPI, STOCKS

logger = logging.getLogger(__name__)


class ChartManager:
    """图表管理器"""
    
    def __init__(self):
        self.full_data_min_change = 0
        self.full_data_max_change = 0
        self._plot_data = None
    
    def calculate_avg_price(self, df):
        """计算均价线"""
        try:
            if '成交额' not in df.columns:
                if '收盘' in df.columns and '成交量' in df.columns:
                    df['成交额'] = df['收盘'] * df['成交量']
                else:
                    df['成交额'] = np.ones(len(df)) * 100000

            if '成交量' not in df.columns:
                df['成交量'] = np.ones(len(df)) * 1000

            if df['成交量'].sum() > 0:
                cum_amount = df['成交额'].cumsum()
                cum_volume = df['成交量'].cumsum()
                avg_price = cum_amount / cum_volume.replace(0, np.nan)
                avg_price = avg_price.ffill().fillna(0)

                base_price = df['开盘'].iloc[0] if '开盘' in df.columns else df['收盘'].iloc[0]
                df['avg_change'] = (avg_price / base_price - 1) * 100
                df['均价'] = avg_price
            else:
                df['avg_change'] = df['涨跌幅'] * 0.8

        except Exception as e:
            logger.error(f"计算均价线失败: {e}")
            df['avg_change'] = df['涨跌幅'] * 0.8 if '涨跌幅' in df.columns else np.zeros(len(df))
    
    def plot_main_chart(self, ax, df, stock_code):
        """绘制主分时图（不带指标）"""
        try:
            # 确保数据有必要的列
            if '时间' not in df.columns or '涨跌幅' not in df.columns:
                logger.error("数据格式错误")
                return False

            # 保存完整数据范围
            self.full_data_min_change = df['涨跌幅'].min()
            self.full_data_max_change = df['涨跌幅'].max()

            # 计算均价线
            self.calculate_avg_price(df)

            # 清空并重绘
            ax.clear()

            # 使用连续索引绘制
            x_indices = list(range(len(df)))
            self._plot_data = df.copy()

            # 绘制分时线和均价线
            ax.plot(x_indices, df['涨跌幅'], 'b-', linewidth=1.5, label='分时线')
            ax.plot(x_indices, df['avg_change'], 'r-', linewidth=1.2, label='均价线', alpha=0.8)

            # 绘制零轴线
            ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3)

            # 设置x轴为时间标签
            num_points = len(df)
            if num_points > 0:
                step = max(1, num_points // 8)
                tick_indices = list(range(0, num_points, step))
                if tick_indices and tick_indices[-1] != num_points - 1:
                    tick_indices.append(num_points - 1)

                tick_labels = [df.iloc[i]['时间'].strftime('%H:%M') for i in tick_indices]
                ax.set_xticks(tick_indices)
                ax.set_xticklabels(tick_labels, rotation=45)

            # 设置标题和标签
            ax.set_title(f"{STOCKS[stock_code]}({stock_code}) 分时图", fontsize=14)
            ax.set_ylabel('涨跌幅 (%)', fontsize=10)

            # 设置坐标轴范围
            ax.set_xlim(-0.5, len(df) - 0.5)
            padding = (self.full_data_max_change - self.full_data_min_change) * 0.1 if self.full_data_max_change > self.full_data_min_change else 0.5
            ax.set_ylim(self.full_data_min_change - padding, self.full_data_max_change + padding)

            # 添加网格和图例
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper right')

            logger.info("主分时图绘制完成")
            return True

        except Exception as e:
            logger.error(f"绘制主分时图失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def plot_indicator_with_signals(self, ax, df, indicator_data, title):
        """绘制带信号的指标分时图"""
        try:
            x_indices = list(range(len(df)))
            
            # 绘制分时线
            ax.plot(x_indices, df['涨跌幅'], 'b-', linewidth=1.0, label='分时线', alpha=0.7)
            
            # 标记买卖信号
            if 'Buy_Signal' in indicator_data.columns:
                buy_signals = indicator_data[indicator_data['Buy_Signal']]
                for idx in buy_signals.index:
                    x_pos = indicator_data.index.get_loc(idx)
                    ax.scatter(x_pos, df.iloc[x_pos]['涨跌幅'], 
                             color='red', marker='^', s=80, zorder=5)
            
            if 'Sell_Signal' in indicator_data.columns:
                sell_signals = indicator_data[indicator_data['Sell_Signal']]
                for idx in sell_signals.index:
                    x_pos = indicator_data.index.get_loc(idx)
                    ax.scatter(x_pos, df.iloc[x_pos]['涨跌幅'], 
                             color='green', marker='v', s=80, zorder=5)
            
            # 设置标题和标签
            ax.set_title(title, fontsize=10)
            ax.set_ylabel('涨跌幅 (%)', fontsize=9)
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper right', fontsize=8)
            ax.set_xlim(-0.5, len(df) - 0.5)
            
        except Exception as e:
            logger.error(f"绘制带信号的分时图失败: {e}")
