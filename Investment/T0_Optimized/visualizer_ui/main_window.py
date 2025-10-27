#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
主窗口模块 - T0数据可视化工具主界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import logging
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .config import *
from .data_loader import DataLoader
from .chart_manager import ChartManager
from .indicator_plotters import IndicatorPlotters

logger = logging.getLogger(__name__)


class T0DataVisualizer:
    """T0交易系统分时数据可视化工具"""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.minsize(*WINDOW_MIN_SIZE)

        # 当前选中的股票
        self.current_stock = tk.StringVar(value='600030')
        
        # 获取当前日期
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        # 当前选择的日期
        self.current_date = tk.StringVar(value=today)

        # 数据加载器
        self.data_loader = DataLoader()
        
        # 图表管理器
        self.chart_manager = ChartManager()

        # 播放控制变量
        self.is_playing = False
        self.play_thread = None
        self.play_stop_event = threading.Event()
        self.play_speed = tk.DoubleVar(value=DEFAULT_PLAY_SPEED)
        self.current_play_index = 0

        # 指标显示控制
        self.show_comprehensive_t0 = tk.BooleanVar(value=True)
        self.show_price_ma_deviation = tk.BooleanVar(value=True)
        self.show_price_ma_deviation_optimized = tk.BooleanVar(value=True)

        # 指标数据缓存
        self.indicator_data = {}

        # 创建UI
        self._create_ui()

        # 初始化数据
        self._init_data()

    def _create_ui(self):
        """创建用户界面 - 重构为上下两部分"""
        # ========== 上部: 控制栏（股票选择 + 指标选择 + 播放控制）==========
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X, side=tk.TOP)

        # 股票选择
        ttk.Label(control_frame, text="股票选择:").pack(side=tk.LEFT, padx=5)
        stock_combo = ttk.Combobox(
            control_frame,
            textvariable=self.current_stock,
            values=list(STOCKS.keys()),
            width=10
        )
        stock_combo.pack(side=tk.LEFT, padx=5)
        stock_combo.bind("<<ComboboxSelected>>", lambda event: self._on_stock_change())

        # 股票名称显示
        self.stock_name_label = ttk.Label(control_frame, text=STOCKS[self.current_stock.get()], font=('SimHei', 12))
        self.stock_name_label.pack(side=tk.LEFT, padx=5)

        # 分隔符
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        # 日期选择
        ttk.Label(control_frame, text="日期:").pack(side=tk.LEFT, padx=5)
        # 生成包含今天和最近几天的日期列表
        from datetime import datetime, timedelta
        today = datetime.now()
        dates = [today.strftime('%Y-%m-%d')]
        # 添加最近4天的日期
        for i in range(1, 5):
            past_date = today - timedelta(days=i)
            dates.append(past_date.strftime('%Y-%m-%d'))
        
        date_combo = ttk.Combobox(
            control_frame,
            textvariable=self.current_date,
            values=dates,
            width=12
        )
        date_combo.pack(side=tk.LEFT, padx=5)
        date_combo.bind("<<ComboboxSelected>>", lambda event: self._on_date_change())

        # 分隔符
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)

        # 指标选择（移到控制栏）
        ttk.Label(control_frame, text="指标选择:").pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(control_frame, text="综合T0策略", variable=self.show_comprehensive_t0,
                       command=lambda: self._update_indicator_charts()).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(control_frame, text="价格均线偏离(基础)", variable=self.show_price_ma_deviation,
                       command=lambda: self._update_indicator_charts()).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(control_frame, text="价格均线偏离(优化)", variable=self.show_price_ma_deviation_optimized,
                       command=lambda: self._update_indicator_charts()).pack(side=tk.LEFT, padx=5)

        # 分隔符
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)

        # 数据加载按钮
        ttk.Button(control_frame, text="重新加载", command=self._load_data).pack(side=tk.LEFT, padx=5)

        # 播放控制
        self.play_button = ttk.Button(control_frame, text="播放", command=self._start_play, width=6)
        self.play_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="暂停", command=self._pause_play, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="重置", command=self._reset_play, width=6).pack(side=tk.LEFT, padx=2)

        # 播放速度
        ttk.Label(control_frame, text="速度:").pack(side=tk.LEFT, padx=5)
        speed_scale = ttk.Scale(control_frame, from_=MIN_PLAY_SPEED, to=MAX_PLAY_SPEED,
                               orient=tk.HORIZONTAL, length=80, variable=self.play_speed)
        speed_scale.pack(side=tk.LEFT, padx=2)
        self.speed_label = ttk.Label(control_frame, text=f"{self.play_speed.get():.1f}x", width=4)
        self.speed_label.pack(side=tk.LEFT, padx=2)

        def update_speed_label(event):
            self.speed_label.config(text=f"{self.play_speed.get():.1f}x")
        speed_scale.bind("<Motion>", update_speed_label)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # ========== 下部: 指标图表展示区域（横向滚动）==========
        self.indicator_chart_frame = ttk.LabelFrame(self.root, text="指标分析图表", padding="5")
        self.indicator_chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # 创建横向+纵向双滚动的容器
        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(self.indicator_chart_frame, orient="horizontal")
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(self.indicator_chart_frame, orient="vertical")
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas容器
        self.indicator_canvas_widget = tk.Canvas(
            self.indicator_chart_frame, 
            bg='white', 
            highlightthickness=0,
            xscrollcommand=h_scrollbar.set,
            yscrollcommand=v_scrollbar.set
        )
        self.indicator_canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        h_scrollbar.config(command=self.indicator_canvas_widget.xview)
        v_scrollbar.config(command=self.indicator_canvas_widget.yview)

        # 可滚动框架（横向布局）
        self.indicator_scrollable_frame = ttk.Frame(self.indicator_canvas_widget)
        self.indicator_canvas_widget.create_window((0, 0), window=self.indicator_scrollable_frame, anchor="nw")

        # 绑定配置更新
        self.indicator_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.indicator_canvas_widget.configure(scrollregion=self.indicator_canvas_widget.bbox("all"))
        )

        # 鼠标滚轮支持（纵向滚动）
        def _on_mousewheel(event):
            self.indicator_canvas_widget.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Shift+滚轮支持（横向滚动）
        def _on_shift_mousewheel(event):
            self.indicator_canvas_widget.xview_scroll(int(-1*(event.delta/120)), "units")
        
        self.indicator_canvas_widget.bind_all("<MouseWheel>", _on_mousewheel)
        self.indicator_canvas_widget.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

        # 存储指标图表对象
        self.indicator_figures = {}
        self.indicator_canvases = {}

    def _init_data(self):
        """初始化数据"""
        try:
            target_date = self.current_date.get()
            logger.info(f"正在初始化数据，目标日期：{target_date}")

            for stock_code in STOCKS.keys():
                cached_data = self.data_loader.load_from_cache(stock_code, target_date)
                if cached_data is not None and not cached_data.empty:
                    logger.info(f"已从缓存加载股票 {STOCKS[stock_code]} 的数据，行数：{len(cached_data)}")
                    self.data_loader.data_cache[stock_code] = cached_data
                    self.status_var.set(f"已加载股票 {STOCKS[stock_code]} 的缓存数据")
                else:
                    try:
                        self.data_loader.load_stock_data(stock_code, target_date)
                    except Exception as e:
                        logger.error(f"加载股票 {STOCKS[stock_code]} 数据失败: {e}")

            self._update_chart()

        except Exception as e:
            logger.error(f"初始化数据失败: {str(e)}")
            messagebox.showerror("错误", f"初始化数据失败: {str(e)}")

    def _load_data(self):
        """加载数据"""
        try:
            target_date = self.current_date.get()
            stock_code = self.current_stock.get()
            self.data_loader.load_stock_data(stock_code, target_date)
            
            if stock_code in self.data_loader.data_cache and not self.data_loader.data_cache[stock_code].empty:
                self._update_chart()

        except Exception as e:
            logger.error(f"加载数据失败: {str(e)}")
            messagebox.showerror("错误", f"加载数据失败: {str(e)}")

    def _on_stock_change(self):
        """股票选择变更处理"""
        stock_code = self.current_stock.get()
        self.stock_name_label.config(text=STOCKS.get(stock_code, "未知股票"))
        self.indicator_data = {}
        self.current_play_index = 0
        self._update_chart()
        self._pause_play()
    
    def _on_date_change(self):
        """日期改变处理"""
        logger.info(f"日期改变为: {self.current_date.get()}")
        # 重新加载数据
        self._init_data()

    def _update_chart(self):
        """更新图表显示（仅更新指标图表）"""
        try:
            stock_code = self.current_stock.get()

            if stock_code not in self.data_loader.data_cache or self.data_loader.data_cache[stock_code].empty:
                logger.warning(f"未找到股票 {STOCKS[stock_code]} 的数据")
                self.status_var.set(f"未找到股票 {STOCKS[stock_code]} 的数据")
                return

            df = self.data_loader.data_cache[stock_code].copy()
            logger.info(f"更新指标图表，使用 {len(df)} 条数据")

            # 直接更新指标图
            self._update_indicator_charts()
            
            logger.info("指标图表更新完成")
            self.status_var.set(f"已显示股票 {STOCKS[stock_code]} 的指标分析")

        except Exception as e:
            logger.error(f"更新图表失败: {str(e)}")
            import traceback
            traceback.print_exc()

    def _update_indicator_charts(self):
        """更新指标图表区域"""
        try:
            stock_code = self.current_stock.get()
            
            if stock_code not in self.data_loader.data_cache or self.data_loader.data_cache[stock_code].empty:
                return

            df = self.data_loader.data_cache[stock_code].copy()
            
            # 清空指标显示区域
            for widget in self.indicator_scrollable_frame.winfo_children():
                widget.destroy()
            
            self.indicator_figures = {}
            self.indicator_canvases = {}
            
            # 绘制选中的指标
            if self.show_comprehensive_t0.get():
                self._create_indicator_chart("综合T0策略", df, stock_code, 
                                            IndicatorPlotters.plot_comprehensive_t0)
            
            if self.show_price_ma_deviation.get():
                self._create_indicator_chart("价格均线偏离(基础)", df, stock_code,
                                            IndicatorPlotters.plot_price_ma_deviation)
            
            if self.show_price_ma_deviation_optimized.get():
                self._create_indicator_chart("价格均线偏离(优化)", df, stock_code,
                                            IndicatorPlotters.plot_price_ma_deviation_optimized)
            
            logger.info("指标图表绘制完成")
            
        except Exception as e:
            logger.error(f"更新指标图表失败: {e}")
            import traceback
            traceback.print_exc()

    def _create_indicator_chart(self, title, df, stock_code, plot_func):
        """创建单个指标图表（智能布局）"""
        try:
            # 统计当前勾选的指标数量
            checked_count = sum([
                self.show_comprehensive_t0.get(),
                self.show_price_ma_deviation.get(),
                self.show_price_ma_deviation_optimized.get()
            ])
            
            # 根据指标数量调整布局
            if checked_count == 1:
                # 单个指标：充满整个区域
                frame = ttk.LabelFrame(self.indicator_scrollable_frame, text=title, padding="5")
                frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                # 使用更大的尺寸
                fig = Figure(figsize=(14, 8), dpi=DPI)
            else:
                # 多个指标：横向排列
                frame = ttk.LabelFrame(self.indicator_scrollable_frame, text=title, padding="5")
                frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
                
                # 使用配置的图表尺寸
                fig = Figure(figsize=INDICATOR_CHART_SIZE, dpi=DPI)
            
            # 调用绘图函数
            if plot_func(fig, df, stock_code):
                # 使用tight_layout避免图表元素重叠
                fig.tight_layout(pad=1.5)
                
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                self.indicator_figures[title] = fig
                self.indicator_canvases[title] = canvas
                logger.info(f"成功绘制指标: {title}")
            else:
                logger.warning(f"绘制指标失败: {title}")
                
        except Exception as e:
            logger.error(f"创建指标图表失败 ({title}): {e}")

    def _start_play(self):
        """开始播放"""
        if not self.is_playing:
            self.is_playing = True
            self.play_stop_event.clear()
            self.play_button.config(state=tk.DISABLED)
            self.play_thread = threading.Thread(target=self._play_simulation)
            self.play_thread.daemon = True
            self.play_thread.start()

    def _pause_play(self):
        """暂停播放"""
        self.is_playing = False
        self.play_stop_event.set()
        if hasattr(self, 'play_button'):
            self.root.after(100, lambda: self.play_button.config(state=tk.NORMAL))

    def _reset_play(self):
        """重置播放"""
        self._pause_play()
        self.current_play_index = 0
        self._update_chart()

    def _play_simulation(self):
        """播放模拟 - 回放勾选的指标图表"""
        try:
            stock_code = self.current_stock.get()
            
            if stock_code not in self.data_loader.data_cache or self.data_loader.data_cache[stock_code].empty:
                logger.warning("没有可用的数据进行回放")
                return
            
            df = self.data_loader.data_cache[stock_code].copy()
            total_rows = len(df)
            
            logger.info(f"开始回放，总数据点: {total_rows}")
            
            while self.is_playing and self.current_play_index < total_rows:
                if self.play_stop_event.is_set():
                    break
                
                # 获取当前时间点的数据
                current_data = df.iloc[:self.current_play_index + 1]
                
                # 更新勾选的指标图表
                self.root.after(0, lambda: self._update_play_charts(current_data))
                
                # 根据速度控制延迟
                speed = self.play_speed.get()
                delay = 0.1 / speed  # 基础延迟100ms
                time.sleep(delay)
                
                self.current_play_index += 1
            
            # 播放完成
            if self.current_play_index >= total_rows:
                logger.info("回放完成")
                self.root.after(0, self._pause_play)
                self.root.after(0, lambda: self.status_var.set("回放完成"))
                
        except Exception as e:
            logger.error(f"回放过程中出错: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(0, self._pause_play)
    
    def _update_play_charts(self, current_data):
        """更新播放过程中的图表"""
        try:
            stock_code = self.current_stock.get()
            
            # 清空指标显示区域
            for widget in self.indicator_scrollable_frame.winfo_children():
                widget.destroy()
            
            self.indicator_figures = {}
            self.indicator_canvases = {}
            
            # 绘制选中的指标
            if self.show_comprehensive_t0.get():
                self._create_indicator_chart("综合T0策略", current_data, stock_code, 
                                            IndicatorPlotters.plot_comprehensive_t0)
            
            if self.show_price_ma_deviation.get():
                self._create_indicator_chart("价格均线偏离(基础)", current_data, stock_code,
                                            IndicatorPlotters.plot_price_ma_deviation)
            
            if self.show_price_ma_deviation_optimized.get():
                self._create_indicator_chart("价格均线偏离(优化)", current_data, stock_code,
                                            IndicatorPlotters.plot_price_ma_deviation_optimized)
            
            # 更新状态栏
            current_time = current_data['\u65f6\u95f4'].iloc[-1] if '\u65f6\u95f4' in current_data.columns else ""
            progress = int((self.current_play_index / len(self.data_loader.data_cache[stock_code])) * 100)
            self.status_var.set(f"回放中: {current_time} ({progress}%)")
            
        except Exception as e:
            logger.error(f"更新回放图表失败: {e}")
