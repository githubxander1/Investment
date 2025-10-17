# T0交易系统可视化界面
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime, time
import akshare as ak
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Investment.T0.monitor.signal_detector import SignalDetector
from Investment.T0.utils.logger import setup_logger
from Investment.T0.config.settings import DEFAULT_STOCK_POOL

logger = setup_logger('t0_gui')

class T0MonitorGUI:
    """T0监控图形界面"""
    
    def __init__(self, stock_pool=None):
        self.root = tk.Tk()
        self.root.title("T0交易监控系统")
        self.root.geometry("1400x900")
        
        # 初始化变量
        self.stock_pool = stock_pool if stock_pool else DEFAULT_STOCK_POOL
        self.current_stock_index = 0
        self.stock_code = self.stock_pool[self.current_stock_index]
        self.detector = SignalDetector(self.stock_code)
        self.is_monitoring = False
        self.after_id = None
        
        # 创建界面
        self.create_widgets()
        
        # 初始化图表
        self.init_plots()
        
        # 获取初始数据
        self.update_display()
    
    def create_widgets(self):
        """创建界面组件"""
        # 顶部控制面板
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 股票代码选择
        ttk.Label(control_frame, text="股票代码:").pack(side=tk.LEFT)
        
        # 创建股票代码下拉框
        self.stock_var = tk.StringVar(value=self.stock_code)
        self.stock_combo = ttk.Combobox(control_frame, textvariable=self.stock_var, 
                                       values=self.stock_pool, width=10, state="readonly")
        self.stock_combo.pack(side=tk.LEFT, padx=(5, 10))
        self.stock_combo.bind('<<ComboboxSelected>>', self.on_stock_change)
        
        # 上一只/下一只按钮
        ttk.Button(control_frame, text="上一只", command=self.prev_stock).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(control_frame, text="下一只", command=self.next_stock).pack(side=tk.LEFT, padx=(5, 10))
        
        # 开始/停止监控按钮
        self.monitor_btn = ttk.Button(control_frame, text="开始监控", command=self.toggle_monitoring)
        self.monitor_btn.pack(side=tk.LEFT, padx=(5, 10))
        
        # 刷新按钮
        ttk.Button(control_frame, text="刷新", command=self.update_display).pack(side=tk.LEFT, padx=(5, 10))
        
        # 主要内容框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 图表区域
        self.chart_frame = ttk.LabelFrame(main_frame, text="技术指标图表")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # 信号日志区域
        self.log_frame = ttk.LabelFrame(main_frame, text="信号日志")
        self.log_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 5))
        
        # 创建日志文本框和滚动条
        log_frame_inner = ttk.Frame(self.log_frame)
        log_frame_inner.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame_inner, height=8)
        log_scrollbar = ttk.Scrollbar(log_frame_inner, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def on_stock_change(self, event=None):
        """股票代码改变事件"""
        self.stock_code = self.stock_var.get()
        self.detector = SignalDetector(self.stock_code)
        self.update_display()
    
    def prev_stock(self):
        """切换到上一只股票"""
        self.current_stock_index = (self.current_stock_index - 1) % len(self.stock_pool)
        self.stock_code = self.stock_pool[self.current_stock_index]
        self.stock_var.set(self.stock_code)
        self.detector = SignalDetector(self.stock_code)
        self.update_display()
    
    def next_stock(self):
        """切换到下一只股票"""
        self.current_stock_index = (self.current_stock_index + 1) % len(self.stock_pool)
        self.stock_code = self.stock_pool[self.current_stock_index]
        self.stock_var.set(self.stock_code)
        self.detector = SignalDetector(self.stock_code)
        self.update_display()
    
    def init_plots(self):
        """初始化图表"""
        # 创建图表框架
        self.fig, self.axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
        self.fig.subplots_adjust(hspace=0.3)
        
        # 创建画布
        self.canvas = FigureCanvasTkAgg(self.fig, self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 设置图表标题
        self.axes[0].set_title("阻力支撑指标")
        self.axes[1].set_title("扩展指标")
        self.axes[2].set_title("量价指标")
        
        # 设置y轴标签
        self.axes[0].set_ylabel("价格")
        self.axes[1].set_ylabel("指标值")
        self.axes[2].set_ylabel("价格")
        
        for ax in self.axes:
            ax.grid(True, linestyle='--', alpha=0.7)
    
    def toggle_monitoring(self):
        """切换监控状态"""
        if self.is_monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def start_monitoring(self):
        """开始监控"""
        self.is_monitoring = True
        self.monitor_btn.config(text="停止监控")
        self.log_message("开始监控...")
        self.monitor_loop()
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        self.monitor_btn.config(text="开始监控")
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.log_message("停止监控")
    
    def monitor_loop(self):
        """监控循环"""
        if not self.is_monitoring:
            return
            
        try:
            # 检测信号
            signals = self.detector.detect_all_signals()
            if signals:
                for signal in signals:
                    message = f"[{datetime.now().strftime('%H:%M:%S')}] {signal['indicator']} - {signal['type']} - {signal['details']}"
                    self.log_message(message)
            
            # 更新显示
            self.update_display()
            
        except Exception as e:
            self.log_message(f"监控出错: {e}")
        
        # 安排下次监控
        self.after_id = self.root.after(60000, self.monitor_loop)  # 每分钟检测一次
    
    def update_display(self):
        """更新显示"""
        try:
            # 获取数据
            df = self.detector.get_stock_data()
            if df is None or df.empty:
                return
                
            prev_close = self.detector.get_prev_close()
            if prev_close is None:
                prev_close = df['开盘'].dropna().iloc[0] if not df['开盘'].dropna().empty else 0
            
            # 绘制图表
            self.plot_charts(df, prev_close)
            
            # 更新窗口标题
            self.root.title(f"T0交易监控系统 - {self.stock_code}")
            
        except Exception as e:
            self.log_message(f"更新显示出错: {e}")
    
    def plot_charts(self, df, prev_close):
        """绘制图表"""
        # 清除之前的图表
        for ax in self.axes:
            ax.clear()
        
        # 过滤数据
        df_filtered = df.dropna(subset=['收盘'])
        if df_filtered.empty:
            return
        
        x_values = list(range(len(df_filtered)))
        time_labels = [t.strftime('%H:%M') for t in df_filtered.index]
        
        # 1. 阻力支撑指标图
        self.axes[0].plot(x_values, df_filtered['收盘'], color='blue', linewidth=1.5, label='收盘价')
        
        # 计算阻力支撑线
        daily_high = df_filtered['最高'].max()
        daily_low = df_filtered['最低'].min()
        H1 = max(prev_close, daily_high)
        L1 = min(prev_close, daily_low)
        P1 = H1 - L1
        resistance = L1 + P1 * 7 / 8
        support = L1 + P1 * 0.5 / 8
        
        self.axes[0].axhline(y=resistance, color='red', linestyle='--', linewidth=1, label='阻力线')
        self.axes[0].axhline(y=support, color='green', linestyle='--', linewidth=1, label='支撑线')
        self.axes[0].axhline(y=prev_close, color='gray', linestyle='--', linewidth=1, label='昨收价')
        
        self.axes[0].set_title("阻力支撑指标")
        self.axes[0].set_ylabel("价格")
        self.axes[0].legend()
        self.axes[0].grid(True, linestyle='--', alpha=0.7)
        
        # 2. 扩展指标图 (简化为移动平均线)
        if len(df_filtered) > 20:
            df_filtered['MA10'] = df_filtered['收盘'].rolling(window=10).mean()
            df_filtered['MA20'] = df_filtered['收盘'].rolling(window=20).mean()
            
            self.axes[1].plot(x_values, df_filtered['收盘'], color='blue', linewidth=1.5, label='收盘价')
            self.axes[1].plot(x_values, df_filtered['MA10'], color='orange', linewidth=1.5, label='MA10')
            self.axes[1].plot(x_values, df_filtered['MA20'], color='purple', linewidth=1.5, label='MA20')
            
        self.axes[1].set_title("扩展指标")
        self.axes[1].set_ylabel("价格")
        self.axes[1].legend()
        self.axes[1].grid(True, linestyle='--', alpha=0.7)
        
        # 3. 量价指标图
        self.axes[2].plot(x_values, df_filtered['收盘'], color='blue', linewidth=1.5, label='收盘价')
        
        if '成交量' in df_filtered.columns:
            # 创建第二个y轴显示成交量
            ax2 = self.axes[2].twinx()
            ax2.bar(x_values, df_filtered['成交量'], alpha=0.3, color='gray', label='成交量')
            ax2.set_ylabel("成交量")
        
        self.axes[2].set_title("量价指标")
        self.axes[2].set_ylabel("价格")
        self.axes[2].legend()
        self.axes[2].grid(True, linestyle='--', alpha=0.7)
        
        # 设置x轴
        for ax in self.axes:
            ax.set_xticks(x_values[::15])  # 每15个点显示一个标签
            ax.set_xticklabels(time_labels[::15], rotation=45, ha="right")
        
        # 刷新画布
        self.canvas.draw()
    
    def log_message(self, message):
        """记录日志消息"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)  # 自动滚动到末尾
    
    def on_closing(self):
        """关闭窗口时的处理"""
        self.stop_monitoring()
        self.root.destroy()
    
    def run(self):
        """运行GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main(stock_pool=None):
    """主函数"""
    app = T0MonitorGUI(stock_pool)
    app.run()

if __name__ == "__main__":
    # 可以通过命令行参数指定股票代码
    stock_pool = sys.argv[1:] if len(sys.argv) > 1 else None
    main(stock_pool)