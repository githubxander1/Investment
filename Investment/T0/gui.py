import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 设置matplotlib后端
import matplotlib
matplotlib.use('TkAgg')

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入指标接口模块
try:
    from core.indicator_interface import get_indicator_manager, IndicatorProtocol
    INDICATORS_AVAILABLE = True
except ImportError as e:
    print(f"导入指标接口模块失败: {e}")
    INDICATORS_AVAILABLE = False

class StockAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("股票分析系统")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 当前选择的指标类型
        self.current_indicator = tk.StringVar(value="resistance_support")
        # 当前股票代码和日期
        self.stock_code = tk.StringVar(value="000333")
        # 默认使用昨天的日期
        yesterday = datetime.now() - timedelta(days=1)
        self.trade_date = tk.StringVar(value=yesterday.strftime("%Y-%m-%d"))
        
        # 初始化指标管理器
        self.indicator_manager = None
        self.available_indicators = {}
        if INDICATORS_AVAILABLE:
            self.indicator_manager = get_indicator_manager()
            self.available_indicators = self.indicator_manager.get_available_indicators()
        
        # 创建UI
        self._create_widgets()
        
        # 初始化图表
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # 显示初始图表
        if INDICATORS_AVAILABLE and self.indicator_manager:
            self.indicator_manager.set_indicator(self.current_indicator.get())
            self._update_chart()
        else:
            self._show_error_message("指标模块不可用，请检查相关文件")
    
    def _create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.pack(fill=tk.X, side=tk.TOP, pady=5)
        
        # 股票代码输入
        ttk.Label(control_frame, text="股票代码:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        stock_entry = ttk.Entry(control_frame, textvariable=self.stock_code, width=10)
        stock_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 日期选择
        ttk.Label(control_frame, text="交易日期:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        date_entry = ttk.Entry(control_frame, textvariable=self.trade_date, width=15)
        date_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # 日期选择按钮
        ttk.Button(control_frame, text="选择日期", command=self._select_date).grid(row=0, column=4, padx=5, pady=5)
        
        # 指标选择
        ttk.Label(control_frame, text="指标类型:").grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        
        # 准备指标显示数据
        self.indicator_display_data = {}
        if self.available_indicators:
            # 使用中文名称作为显示值，英文键名作为实际值
            for key, name in self.available_indicators.items():
                self.indicator_display_data[name] = key
            indicator_display_values = list(self.indicator_display_data.keys())
            # 确保默认指标显示正确
            for name, key in self.indicator_display_data.items():
                if key == "resistance_support":
                    self.current_indicator.set(name)
                    break
        else:
            # 默认指标数据
            self.indicator_display_data = {"阻力支撑指标": "resistance_support", "量价指标": "volume_price", "扩展指标": "extended"}
            indicator_display_values = list(self.indicator_display_data.keys())
            self.current_indicator.set("阻力支撑指标")
        
        # 创建下拉框
        indicator_combo = ttk.Combobox(control_frame, textvariable=self.current_indicator, values=indicator_display_values)
        indicator_combo.grid(row=0, column=6, padx=5, pady=5)
        indicator_combo.bind("<<ComboboxSelected>>", lambda event: self._update_chart())
        
        # 刷新按钮
        ttk.Button(control_frame, text="刷新图表", command=self._update_chart).grid(row=0, column=7, padx=5, pady=5)
        
        # 保存按钮
        ttk.Button(control_frame, text="保存图表", command=self._save_chart).grid(row=0, column=8, padx=5, pady=5)
        
        # 调整列权重，使控件合理分布
        control_frame.columnconfigure(9, weight=1)
        
        # 创建图表框架
        self.chart_frame = ttk.LabelFrame(main_frame, text="分析图表", padding="10")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建日志框架
        log_frame = ttk.LabelFrame(main_frame, text="分析日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建日志文本框
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
    
    def _select_date(self):
        # 创建日期选择对话框
        date_window = tk.Toplevel(self.root)
        date_window.title("选择日期")
        date_window.geometry("300x200")
        date_window.transient(self.root)
        date_window.grab_set()
        
        # 获取当前日期
        current_date = datetime.now()
        
        # 年、月、日选择
        year_var = tk.IntVar(value=current_date.year)
        month_var = tk.IntVar(value=current_date.month)
        day_var = tk.IntVar(value=current_date.day)
        
        # 年选择
        ttk.Label(date_window, text="年:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        year_spinbox = ttk.Spinbox(date_window, from_=2000, to=2100, textvariable=year_var, width=10)
        year_spinbox.grid(row=0, column=1, padx=5, pady=5)
        
        # 月选择
        ttk.Label(date_window, text="月:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        month_spinbox = ttk.Spinbox(date_window, from_=1, to=12, textvariable=month_var, width=10)
        month_spinbox.grid(row=1, column=1, padx=5, pady=5)
        
        # 日选择
        ttk.Label(date_window, text="日:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        day_spinbox = ttk.Spinbox(date_window, from_=1, to=31, textvariable=day_var, width=10)
        day_spinbox.grid(row=2, column=1, padx=5, pady=5)
        
        # 确认按钮
        def confirm_date():
            try:
                # 验证日期有效性
                selected_date = datetime(year_var.get(), month_var.get(), day_var.get())
                # 更新日期输入框
                self.trade_date.set(selected_date.strftime("%Y-%m-%d"))
                # 关闭对话框
                date_window.destroy()
                # 更新图表
                self._update_chart()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的日期")
        
        ttk.Button(date_window, text="确认", command=confirm_date).grid(row=3, column=0, columnspan=2, pady=20)
    
    def _update_chart(self):
        """更新图表显示"""
        try:
            # 清除之前的图表
            self.ax.clear()
            self.log_text.delete(1.0, tk.END)
            
            code = self.stock_code.get()
            date = self.trade_date.get()
            indicator_display_name = self.current_indicator.get()
            
            # 获取实际的指标类型键名
            indicator_type = self.indicator_display_data.get(indicator_display_name, indicator_display_name)
            
            # 记录日志
            self._log_message(f"正在分析股票: {code}, 日期: {date}, 指标类型: {indicator_display_name} ({indicator_type})")
            
            if not INDICATORS_AVAILABLE or not self.indicator_manager:
                raise Exception("指标管理器不可用")
            
            # 设置当前指标
            success = self.indicator_manager.set_indicator(indicator_type)
            if not success:
                raise Exception(f"无法设置指标类型: {indicator_type}")
            
            # 使用指标管理器生成图表
            indicator_name = self.indicator_manager.current_indicator.get_name()
            self._log_message(f"当前使用指标: {indicator_name}")
            
            # 分析数据
            df = self.indicator_manager.analyze(code, date)
            if df is None:
                raise Exception("无法获取分析数据")
            
            # 检测信号
            signals = self.indicator_manager.detect_signals(df)
            if signals:
                for signal in signals:
                    self._log_message(f"检测到信号: {signal}")
            
            # 绘制图表
            chart_path = self.indicator_manager.plot(code, date)
            if chart_path:
                self._log_message(f"图表已保存至: {chart_path}")
                
                # 加载并显示图表
                from matplotlib.image import imread
                img = imread(chart_path)
                self.ax.clear()
                self.ax.imshow(img)
                self.ax.axis('off')
                
                # 更新画布
                self.canvas.draw()
            else:
                raise Exception("图表生成失败")
            
        except Exception as e:
            self._log_message(f"错误: {str(e)}")
            self._show_error_message(f"生成图表时出错: {str(e)}")
    
    # 移除了特定的图表生成方法，统一使用指标接口进行处理
    
    def _save_chart(self):
        """保存当前图表"""
        try:
            # 获取指标的显示名称和实际键名
            indicator_display_name = self.current_indicator.get()
            indicator_type = self.indicator_display_data.get(indicator_display_name, indicator_display_name)
            
            # 打开文件对话框
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=f"{self.stock_code.get()}_{self.trade_date.get()}_{indicator_type}.png"
            )
            
            if file_path:
                # 保存图表
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                self._log_message(f"图表已保存至: {file_path}")
                messagebox.showinfo("成功", f"图表已保存至: {file_path}")
        except Exception as e:
            self._log_message(f"保存图表失败: {str(e)}")
            self._show_error_message(f"保存图表失败: {str(e)}")
    
    def _log_message(self, message):
        """记录消息到日志文本框"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def _show_error_message(self, message):
        """显示错误消息框"""
        messagebox.showerror("错误", message)

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    # 创建应用实例
    app = StockAnalysisGUI(root)
    # 运行主循环
    root.mainloop()