#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图表生成器模块
提供高级图表生成和报告功能
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class ChartGenerator:
    """
    图表生成器类
    负责生成各种复杂图表和报告
    """
    
    def __init__(self, output_dir=None):
        """
        初始化图表生成器
        
        参数:
        output_dir: 图表输出目录，如果为None则使用默认目录
        """
        # 设置输出目录
        if output_dir is None:
            # 使用项目中的output目录
            self.output_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                'output'
            )
        else:
            self.output_dir = output_dir
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 设置默认样式
        self._set_default_style()
    
    def _set_default_style(self):
        """
        设置默认的图表样式
        """
        plt.style.use('seaborn-v0_8-darkgrid')
        # 设置图表大小和DPI
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['figure.dpi'] = 100
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
    
    def generate_stock_analysis_chart(self, stock_code, df, signals, 
                                     save_path=None, show=False):
        """
        生成股票分析图表，包含价格、交易量、技术指标和交易信号
        
        参数:
        stock_code: 股票代码
        df: 包含股票数据的DataFrame
        signals: 交易信号字典，包含buy_signals和sell_signals
        save_path: 保存路径，如果为None则使用默认路径
        show: 是否显示图表
        
        返回:
        str: 保存的图表路径
        """
        try:
            # 创建图表和子图
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 16), 
                                              gridspec_kw={'height_ratios': [3, 1, 2]})
            fig.suptitle(f'{stock_code} 股票分析图', fontsize=16, fontweight='bold')
            
            # 确保时间列是datetime类型
            if not pd.api.types.is_datetime64_any_dtype(df.index):
                if 'time' in df.columns:
                    df = df.set_index('time')
                elif '时间' in df.columns:
                    df = df.set_index('时间')
                
                df.index = pd.to_datetime(df.index)
            
            # 图表1: 价格和均线
            ax1.plot(df.index, df['close'] if 'close' in df.columns else df['收盘'], 
                    label='价格', linewidth=2, color='blue')
            
            # 添加均线（如果存在）
            for ma_period in [5, 10, 20]:
                ma_col = f'ma{ma_period}'
                if ma_col in df.columns:
                    ax1.plot(df.index, df[ma_col], label=f'MA{ma_period}', linewidth=1.5)
            
            # 添加布林带（如果存在）
            if 'upper_band' in df.columns and 'lower_band' in df.columns:
                ax1.fill_between(df.index, df['upper_band'], df['lower_band'], 
                                alpha=0.2, color='gray', label='布林带')
            
            # 添加买入信号
            if 'buy_signals' in signals and signals['buy_signals']:
                buy_times = [pd.to_datetime(sig['time']) for sig in signals['buy_signals']]
                buy_prices = [sig['price'] for sig in signals['buy_signals']]
                ax1.scatter(buy_times, buy_prices, marker='^', color='green', 
                           s=150, label='买入信号')
            
            # 添加卖出信号
            if 'sell_signals' in signals and signals['sell_signals']:
                sell_times = [pd.to_datetime(sig['time']) for sig in signals['sell_signals']]
                sell_prices = [sig['price'] for sig in signals['sell_signals']]
                ax1.scatter(sell_times, sell_prices, marker='v', color='red', 
                           s=150, label='卖出信号')
            
            # 设置图表1属性
            ax1.set_title('价格趋势和交易信号', fontsize=14)
            ax1.set_ylabel('价格', fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.legend(loc='best')
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            
            # 图表2: 成交量
            volume_col = 'volume' if 'volume' in df.columns else '成交量'
            if volume_col in df.columns:
                ax2.bar(df.index, df[volume_col], label='成交量', color='orange', alpha=0.6)
                ax2.set_title('成交量', fontsize=14)
                ax2.set_ylabel('成交量', fontsize=12)
                ax2.grid(True, alpha=0.3)
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            
            # 图表3: 技术指标
            # RSI (如果存在)
            if 'rsi' in df.columns:
                ax3.plot(df.index, df['rsi'], label='RSI', color='purple', linewidth=2)
                ax3.axhline(y=70, color='red', linestyle='--', alpha=0.5)
                ax3.axhline(y=30, color='green', linestyle='--', alpha=0.5)
            
            # MACD (如果存在)
            if 'macd' in df.columns and 'signal_line' in df.columns:
                ax3_twin = ax3.twinx()
                ax3_twin.plot(df.index, df['macd'], label='MACD', color='blue', linewidth=1.5)
                ax3_twin.plot(df.index, df['signal_line'], label='Signal Line', 
                            color='red', linewidth=1.5)
                ax3_twin.set_ylabel('MACD', fontsize=12)
            
            # 设置图表3属性
            ax3.set_title('技术指标', fontsize=14)
            ax3.set_xlabel('时间', fontsize=12)
            ax3.set_ylabel('RSI', fontsize=12)
            ax3.grid(True, alpha=0.3)
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            
            # 调整子图间距
            plt.tight_layout(rect=[0, 0, 1, 0.97])
            
            # 保存图表
            if save_path is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                save_path = os.path.join(
                    self.output_dir, 
                    f'{stock_code}_analysis_{timestamp}.png'
                )
            
            plt.savefig(save_path, dpi=200, bbox_inches='tight')
            
            # 显示图表
            if show:
                plt.show()
            else:
                plt.close()
            
            return save_path
            
        except Exception as e:
            print(f"生成股票分析图表失败: {e}")
            return None
    
    def generate_performance_report(self, stock_codes, results, save_path=None, show=False):
        """
        生成策略性能报告图表
        
        参数:
        stock_codes: 股票代码列表
        results: 策略运行结果字典
        save_path: 保存路径，如果为None则使用默认路径
        show: 是否显示图表
        
        返回:
        str: 保存的图表路径
        """
        try:
            # 创建图表
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('策略性能报告', fontsize=16, fontweight='bold')
            
            # 1. 每个股票的信号数量比较
            ax1 = axes[0, 0]
            buy_counts = []
            sell_counts = []
            
            for stock_code in stock_codes:
                if stock_code in results and 'signals' in results[stock_code]:
                    signals = results[stock_code]['signals']
                    buy_counts.append(len(signals.get('buy_signals', [])))
                    sell_counts.append(len(signals.get('sell_signals', [])))
                else:
                    buy_counts.append(0)
                    sell_counts.append(0)
            
            x = np.arange(len(stock_codes))
            width = 0.35
            
            ax1.bar(x - width/2, buy_counts, width, label='买入信号', color='green')
            ax1.bar(x + width/2, sell_counts, width, label='卖出信号', color='red')
            
            ax1.set_title('各股票交易信号数量', fontsize=14)
            ax1.set_ylabel('信号数量', fontsize=12)
            ax1.set_xticks(x)
            ax1.set_xticklabels(stock_codes, rotation=45)
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis='y')
            
            # 2. 策略胜率（如果有回测结果）
            ax2 = axes[0, 1]
            # 这里可以添加胜率计算和展示
            ax2.text(0.5, 0.5, '策略胜率图表\n(需要回测数据)', 
                    ha='center', va='center', fontsize=14)
            ax2.set_title('策略胜率分析', fontsize=14)
            ax2.axis('off')
            
            # 3. 信号强度分布图
            ax3 = axes[1, 0]
            signal_strengths = []
            signal_types = []  # 'buy' 或 'sell'
            
            for stock_code in stock_codes:
                if stock_code in results and 'signals' in results[stock_code]:
                    signals = results[stock_code]['signals']
                    # 添加买入信号强度
                    for sig in signals.get('buy_signals', []):
                        if 'strength' in sig:
                            signal_strengths.append(sig['strength'])
                            signal_types.append('buy')
                    # 添加卖出信号强度
                    for sig in signals.get('sell_signals', []):
                        if 'strength' in sig:
                            signal_strengths.append(sig['strength'])
                            signal_types.append('sell')
            
            if signal_strengths:
                colors = ['green' if st == 'buy' else 'red' for st in signal_types]
                ax3.scatter(range(len(signal_strengths)), signal_strengths, 
                           c=colors, alpha=0.6)
                ax3.set_title('信号强度分布', fontsize=14)
                ax3.set_xlabel('信号索引', fontsize=12)
                ax3.set_ylabel('信号强度', fontsize=12)
                ax3.grid(True, alpha=0.3)
            else:
                ax3.text(0.5, 0.5, '暂无信号强度数据', 
                        ha='center', va='center', fontsize=14)
                ax3.axis('off')
            
            # 4. 时间分布图
            ax4 = axes[1, 1]
            signal_hours = []
            signal_minutes = []
            
            for stock_code in stock_codes:
                if stock_code in results and 'signals' in results[stock_code]:
                    signals = results[stock_code]['signals']
                    # 收集所有信号的时间
                    all_signals = signals.get('buy_signals', []) + signals.get('sell_signals', [])
                    for sig in all_signals:
                        signal_time = pd.to_datetime(sig['time'])
                        signal_hours.append(signal_time.hour)
                        signal_minutes.append(signal_time.minute)
            
            if signal_hours:
                # 转换为分钟数
                minutes_from_open = [h*60 + m for h, m in zip(signal_hours, signal_minutes)]
                ax4.hist(minutes_from_open, bins=20, alpha=0.7, color='purple')
                ax4.set_title('信号时间分布', fontsize=14)
                ax4.set_xlabel('开盘后分钟数', fontsize=12)
                ax4.set_ylabel('信号数量', fontsize=12)
                ax4.grid(True, alpha=0.3, axis='y')
            else:
                ax4.text(0.5, 0.5, '暂无信号时间数据', 
                        ha='center', va='center', fontsize=14)
                ax4.axis('off')
            
            # 调整布局
            plt.tight_layout(rect=[0, 0, 1, 0.97])
            
            # 保存图表
            if save_path is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                save_path = os.path.join(
                    self.output_dir, 
                    f'performance_report_{timestamp}.png'
                )
            
            plt.savefig(save_path, dpi=200, bbox_inches='tight')
            
            # 显示图表
            if show:
                plt.show()
            else:
                plt.close()
            
            return save_path
            
        except Exception as e:
            print(f"生成性能报告图表失败: {e}")
            return None
    
    def generate_backtest_report(self, backtest_results, save_path=None, show=False):
        """
        生成回测报告图表
        
        参数:
        backtest_results: 回测结果字典
        save_path: 保存路径，如果为None则使用默认路径
        show: 是否显示图表
        
        返回:
        str: 保存的图表路径
        """
        try:
            # 创建图表
            fig, axes = plt.subplots(3, 2, figsize=(18, 16))
            fig.suptitle('回测报告', fontsize=16, fontweight='bold')
            
            # 1. 累计收益率曲线
            ax1 = axes[0, 0]
            if 'equity_curve' in backtest_results:
                equity_curve = backtest_results['equity_curve']
                ax1.plot(equity_curve.index, equity_curve['cumulative_return'], 
                        label='策略收益', linewidth=2, color='blue')
                ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                ax1.set_title('累计收益率曲线', fontsize=14)
                ax1.set_ylabel('累计收益率(%)', fontsize=12)
                ax1.grid(True, alpha=0.3)
                ax1.legend()
            else:
                ax1.text(0.5, 0.5, '暂无回测数据', 
                        ha='center', va='center', fontsize=14)
                ax1.axis('off')
            
            # 2. 每日收益率分布
            ax2 = axes[0, 1]
            if 'daily_returns' in backtest_results:
                daily_returns = backtest_results['daily_returns']
                ax2.hist(daily_returns, bins=30, alpha=0.7, color='green')
                ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)
                ax2.set_title('每日收益率分布', fontsize=14)
                ax2.set_xlabel('日收益率(%)', fontsize=12)
                ax2.set_ylabel('频次', fontsize=12)
                ax2.grid(True, alpha=0.3, axis='y')
            else:
                ax2.text(0.5, 0.5, '暂无回测数据', 
                        ha='center', va='center', fontsize=14)
                ax2.axis('off')
            
            # 3. 最大回撤
            ax3 = axes[1, 0]
            if 'drawdown' in backtest_results:
                drawdown = backtest_results['drawdown']
                ax3.fill_between(drawdown.index, drawdown, 0, alpha=0.7, color='red')
                ax3.set_title('最大回撤', fontsize=14)
                ax3.set_ylabel('回撤(%)', fontsize=12)
                ax3.grid(True, alpha=0.3)
            else:
                ax3.text(0.5, 0.5, '暂无回测数据', 
                        ha='center', va='center', fontsize=14)
                ax3.axis('off')
            
            # 4. 胜率和盈亏比
            ax4 = axes[1, 1]
            metrics = ['胜率', '盈亏比']
            values = []
            
            if 'win_rate' in backtest_results:
                values.append(backtest_results['win_rate'] * 100)  # 转换为百分比
            else:
                values.append(0)
                
            if 'profit_loss_ratio' in backtest_results:
                values.append(backtest_results['profit_loss_ratio'])
            else:
                values.append(0)
            
            bars = ax4.bar(metrics, values, color=['blue', 'green'])
            ax4.set_title('关键绩效指标', fontsize=14)
            ax4.grid(True, alpha=0.3, axis='y')
            
            # 在柱状图上添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                        f'{height:.2f}', ha='center', va='bottom')
            
            # 5. 月度收益率热力图
            ax5 = axes[2, 0]
            ax5.text(0.5, 0.5, '月度收益率热力图\n(需要实现)', 
                    ha='center', va='center', fontsize=14)
            ax5.axis('off')
            
            # 6. 绩效摘要
            ax6 = axes[2, 1]
            performance_metrics = []
            
            if 'total_return' in backtest_results:
                performance_metrics.append(f"总收益率: {backtest_results['total_return']*100:.2f}%")
            if 'annual_return' in backtest_results:
                performance_metrics.append(f"年化收益率: {backtest_results['annual_return']*100:.2f}%")
            if 'sharpe_ratio' in backtest_results:
                performance_metrics.append(f"夏普比率: {backtest_results['sharpe_ratio']:.2f}")
            if 'max_drawdown' in backtest_results:
                performance_metrics.append(f"最大回撤: {backtest_results['max_drawdown']*100:.2f}%")
            if 'trades_count' in backtest_results:
                performance_metrics.append(f"交易次数: {backtest_results['trades_count']}")
            
            if performance_metrics:
                ax6.text(0.1, 0.9, '绩效摘要', fontsize=14, fontweight='bold')
                for i, metric in enumerate(performance_metrics):
                    ax6.text(0.1, 0.8 - i*0.1, metric, fontsize=12)
                ax6.axis('off')
            else:
                ax6.text(0.5, 0.5, '暂无回测数据', 
                        ha='center', va='center', fontsize=14)
                ax6.axis('off')
            
            # 调整布局
            plt.tight_layout(rect=[0, 0, 1, 0.97])
            
            # 保存图表
            if save_path is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                save_path = os.path.join(
                    self.output_dir, 
                    f'backtest_report_{timestamp}.png'
                )
            
            plt.savefig(save_path, dpi=200, bbox_inches='tight')
            
            # 显示图表
            if show:
                plt.show()
            else:
                plt.close()
            
            return save_path
            
        except Exception as e:
            print(f"生成回测报告图表失败: {e}")
            return None


# 示例用法
if __name__ == "__main__":
    # 创建图表生成器实例
    chart_gen = ChartGenerator()
    print("图表生成器已初始化")
    
    # 这里可以添加测试代码
    print("请在实际使用时传入数据进行图表生成")