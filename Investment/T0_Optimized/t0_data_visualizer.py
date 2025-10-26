#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
T0交易系统分时数据可视化工具
功能：
1. 缓存指定股票的分时数据
2. 提供交互式分时图界面，支持多股票切换
3. 模拟实时数据流播放功能
4. 集成T+0交易指标显示
5. 优化分时图显示效果，确保均线正确显示和连贯的图表
"""

import os
import sys
import time
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import threading
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入指标模块 - 改进的导入错误处理
def define_mock_indicators():
    """定义模拟指标函数,确保程序在指标模块不可用时能正常运行"""
    def mock_analyze_comprehensive_t0(df):
        """基于真实分时数据的综合T0策略分析 - 简化版"""
        result_df = df.copy()
        
        # 基于价格波动计算复合评分
        if '涨跌幅' in df.columns and '均价' in df.columns and '收盘' in df.columns:
            # 计算价格相对均线的偏离度
            price_deviation = ((df['收盘'] - df['均价']) / df['均价']) * 100
            
            # 计算波动率(使用滚动标准差)
            volatility = df['涨跌幅'].rolling(window=5, min_periods=1).std()
            
            # 复合评分 = 偏离度 * 波动率权重
            result_df['Composite_Score'] = price_deviation * (1 + volatility)
            
            # 生成买卖信号:偏离度超过阈值
            result_df['Buy_Signal'] = price_deviation < -1.5  # 价格低于均线1.5%
            result_df['Sell_Signal'] = price_deviation > 1.5   # 价格高于均线1.5%
        else:
            # 如果数据不完整,使用简单的涨跌幅
            result_df['Composite_Score'] = df['涨跌幅'] * 10
            result_df['Buy_Signal'] = df['涨跌幅'] < -0.5
            result_df['Sell_Signal'] = df['涨跌幅'] > 0.5
        
        trades = []  # 空交易列表
        return result_df, trades

    def mock_analyze_deviation_strategy(df):
        """基于真实分时数据的价格均线偏离策略分析"""
        result = df.copy()
        
        # 计算价格相对均线的偏离率
        if '均价' in df.columns and '收盘' in df.columns:
            result['Price_MA_Ratio'] = ((df['收盘'] - df['均价']) / df['均价']) * 100
        else:
            # 备选方案:使用涨跌幅
            result['Price_MA_Ratio'] = df['涨跌幅'] if '涨跌幅' in df.columns else 0
        
        # 生成买卖信号
        result['Buy_Signal'] = result['Price_MA_Ratio'] < -1.0
        result['Sell_Signal'] = result['Price_MA_Ratio'] > 1.0
        return result

    def mock_analyze_deviation_strategy_optimized(df):
        """基于真实分时数据的优化版价格均线偏离策略分析"""
        result = df.copy()
        
        # 计算价格相对均线的偏离率
        if '均价' in df.columns and '收盘' in df.columns:
            result['Price_MA_Ratio'] = ((df['收盘'] - df['均价']) / df['均价']) * 100
            
            # 优化版:考虑趋势(使用移动平均)
            ma5 = result['Price_MA_Ratio'].rolling(window=5, min_periods=1).mean()
            result['Price_MA_Ratio_Smooth'] = ma5
            
            # 使用平滑后的数据生成信号,阈值更严格
            result['Buy_Signal'] = ma5 < -0.8
            result['Sell_Signal'] = ma5 > 0.8
        else:
            # 备选方案
            result['Price_MA_Ratio'] = df['涨跌幅'] if '涨跌幅' in df.columns else 0
            result['Buy_Signal'] = result['Price_MA_Ratio'] < -0.5
            result['Sell_Signal'] = result['Price_MA_Ratio'] > 0.5
        
        return result
    
    return mock_analyze_comprehensive_t0, mock_analyze_deviation_strategy, mock_analyze_deviation_strategy_optimized

# 首先定义模拟函数，确保它们始终可用
analyze_comprehensive_t0, analyze_deviation_strategy, analyze_deviation_strategy_optimized = define_mock_indicators()

# 尝试导入真实指标模块
INDICATORS_AVAILABLE = False
try:
    # 尝试导入原始模块
    try:
        from indicators.comprehensive_t0_strategy import analyze_comprehensive_t0 as real_analyze_comprehensive_t0
        analyze_comprehensive_t0 = real_analyze_comprehensive_t0
        INDICATORS_AVAILABLE = True
    except ImportError:
        logger.warning("无法导入综合T0策略模块，使用模拟函数")
    
    # 尝试导入价格均线偏离策略
    try:
        from indicators.price_ma_deviation import analyze_deviation_strategy as real_analyze_deviation_strategy
        analyze_deviation_strategy = real_analyze_deviation_strategy
    except ImportError:
        try:
            from indicators.price_ma_deviation_strategy import analyze_deviation_strategy as real_analyze_deviation_strategy
            analyze_deviation_strategy = real_analyze_deviation_strategy
        except ImportError:
            try:
                from indicators.price_ma_deviation import analyze_deviation as real_analyze_deviation_strategy
                analyze_deviation_strategy = real_analyze_deviation_strategy
            except ImportError:
                logger.warning("无法导入价格均线偏离策略模块，使用模拟函数")

    # 尝试导入优化版价格均线偏离策略
    try:
        from indicators.price_ma_deviation_optimized import analyze_deviation_strategy as real_analyze_deviation_strategy_optimized
        analyze_deviation_strategy_optimized = real_analyze_deviation_strategy_optimized
    except ImportError:
        try:
            from indicators.price_ma_deviation_optimized_strategy import analyze_deviation_strategy as real_analyze_deviation_strategy_optimized
            analyze_deviation_strategy = real_analyze_deviation_strategy_optimized
        except ImportError:
            # 如果无法导入优化版本，使用基本策略
            logger.warning("无法导入优化版价格均线偏离策略模块，使用基本策略替代")
            
    logger.info(f"指标模块加载状态: {INDICATORS_AVAILABLE}")
except Exception as e:
    logger.error(f"指标模块导入过程中发生错误: {e}，使用模拟函数")

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 导入数据库管理器
try:
    from core.data_manager import DataManager
    from core.db_manager import DBManager
    USE_DATABASE = True
    logger.info("✅ 成功导入数据库管理器")
except ImportError as e:
    logger.warning(f"⚠️ 无法导入数据库管理器: {e}")
    USE_DATABASE = False

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 股票配置
STOCKS = {
    '600030': '中信证券',
    '000333': '美的集团',
    '002415': '海康威视'
}

# 缓存目录
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', 'fenshi_data')

# 创建缓存目录
os.makedirs(CACHE_DIR, exist_ok=True)

class T0DataVisualizer:
    """T0交易系统分时数据可视化工具"""

    def __init__(self, root):
        self.root = root
        self.root.title("T0交易系统 - 分时数据可视化")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        # 当前选中的股票
        self.current_stock = tk.StringVar(value='600030')

        # 数据缓存
        self.data_cache = {}

        # 播放控制变量
        self.is_playing = False
        self.play_thread = None
        self.play_stop_event = threading.Event()
        self.play_speed = tk.DoubleVar(value=1.0)  # 播放速度倍率
        self.current_play_index = 0  # 记录当前播放位置

        # 指标显示控制 - 确保默认选中状态
        self.show_comprehensive_t0 = tk.BooleanVar(value=True)
        self.show_price_ma_deviation = tk.BooleanVar(value=True)
        self.show_price_ma_deviation_optimized = tk.BooleanVar(value=True)

        # 确保指标功能可用的标志
        self.indicators_enabled = True

        # 指标数据缓存
        self.indicator_data = {}

        # 创建UI
        self._create_ui()

        # 初始化数据
        self._init_data()

    def _create_ui(self):
        """创建用户界面 - 上中下三部分布局"""
        # ========== 上部: 控制栏 ==========
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

        # 数据加载按钮
        ttk.Button(control_frame, text="重新加载数据", command=self._load_data).pack(side=tk.LEFT, padx=5)

        # 播放控制
        ttk.Label(control_frame, text="播放控制:").pack(side=tk.LEFT, padx=20, pady=5)

        self.play_button = ttk.Button(control_frame, text="播放", command=self._start_play)
        self.play_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="暂停", command=self._pause_play).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="重置", command=self._reset_play).pack(side=tk.LEFT, padx=5)

        # 播放速度调节
        ttk.Label(control_frame, text="速度:").pack(side=tk.LEFT, padx=10, pady=5)
        speed_scale = ttk.Scale(
            control_frame,
            from_=0.1,
            to=3.0,
            orient=tk.HORIZONTAL,
            length=100,
            variable=self.play_speed
        )
        speed_scale.pack(side=tk.LEFT, padx=5)
        self.speed_label = ttk.Label(control_frame, text=f"{self.play_speed.get():.1f}x")
        self.speed_label.pack(side=tk.LEFT, padx=5)

        # 更新速度标签
        def update_speed_label(event):
            self.speed_label.config(text=f"{self.play_speed.get():.1f}x")
        speed_scale.bind("<Motion>", update_speed_label)

        # 状态信息
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # ========== 中部: 主分时图(不带指标) ==========
        main_chart_frame = ttk.LabelFrame(self.root, text="分时图", padding="5")
        main_chart_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

        # 创建主图表(不带指标)
        self.main_fig = Figure(figsize=(12, 4), dpi=100)
        self.ax_main = self.main_fig.add_subplot(111)

        # 创建主图画布
        self.main_canvas = FigureCanvasTkAgg(self.main_fig, master=main_chart_frame)
        self.main_canvas.draw()
        self.main_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 添加鼠标悬浮功能
        self.annotation = self.ax_main.annotate('', xy=(0, 0), xytext=(10, 10), textcoords='offset points',
                                       bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                                       arrowprops=dict(arrowstyle='->'), fontsize=10)
        self.annotation.set_visible(False)
        self.main_canvas.mpl_connect('motion_notify_event', self._on_mouse_move)

        # ========== 下部: 指标显示区域 ==========
        # 指标选择框
        indicator_control_frame = ttk.LabelFrame(self.root, text="指标选择", padding="5")
        indicator_control_frame.pack(fill=tk.X, padx=10, pady=5)

        # 默认为选中状态
        self.show_comprehensive_t0.set(True)
        self.show_price_ma_deviation.set(True)
        self.show_price_ma_deviation_optimized.set(True)

        ttk.Checkbutton(indicator_control_frame, text="综合T0策略", variable=self.show_comprehensive_t0,
                       command=lambda: self._update_indicator_charts()).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(indicator_control_frame, text="价格均线偏离(基础)", variable=self.show_price_ma_deviation,
                       command=lambda: self._update_indicator_charts()).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(indicator_control_frame, text="价格均线偏离(优化)", variable=self.show_price_ma_deviation_optimized,
                       command=lambda: self._update_indicator_charts()).pack(side=tk.LEFT, padx=10)

        # 如果指标模块导入失败，显示提示信息
        if not INDICATORS_AVAILABLE:
            ttk.Label(indicator_control_frame, text="指标模块导入失败，使用模拟指标", foreground="red").pack(side=tk.LEFT, padx=20)

        # 指标图表显示区域
        self.indicator_chart_frame = ttk.LabelFrame(self.root, text="指标分析图", padding="5")
        self.indicator_chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 创建指标图表(可滚动)
        # 创建 Canvas 和 Scrollbar
        self.indicator_canvas_widget = tk.Canvas(self.indicator_chart_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.indicator_chart_frame, orient="vertical", command=self.indicator_canvas_widget.yview)
        self.indicator_scrollable_frame = ttk.Frame(self.indicator_canvas_widget)

        self.indicator_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.indicator_canvas_widget.configure(
                scrollregion=self.indicator_canvas_widget.bbox("all")
            )
        )

        self.indicator_canvas_widget.create_window((0, 0), window=self.indicator_scrollable_frame, anchor="nw")
        self.indicator_canvas_widget.configure(yscrollcommand=scrollbar.set)

        self.indicator_canvas_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 存储指标图表对象
        self.indicator_figures = {}
        self.indicator_canvases = {}

    def _on_mouse_move(self, event):
        """鼠标移动事件处理 - 显示价格、时间和相对均线涨跌幅"""
        # 只处理主图的悬浮
        if self.ax_main is None or event.inaxes != self.ax_main:
            if self.annotation and self.annotation.get_visible():
                self.annotation.set_visible(False)
                self.canvas.draw_idle()
            return
            
        stock_code = self.current_stock.get()
        if stock_code not in self.data_cache or self.data_cache[stock_code].empty:
            return
        
        df = self.data_cache[stock_code]
        if '时间' not in df.columns or '收盘' not in df.columns:
            return
        
        try:
            # 使用连续索引而不是时间戳来定位
            if hasattr(self, '_plot_data') and self._plot_data is not None:
                x_data = event.xdata
                if x_data is None:
                    return
                    
                # 找到最接近的索引
                idx = int(round(x_data))
                if idx < 0 or idx >= len(self._plot_data):
                    return
                
                data_point = self._plot_data.iloc[idx]
                time_str = data_point['时间'].strftime('%H:%M')
                price = data_point['收盘']
                change_pct = data_point['涨跌幅']
                
                # 计算相对均线的偏离
                if '均价' in data_point and pd.notna(data_point['均价']):
                    avg_price = data_point['均价']
                    diff_pct = ((price - avg_price) / avg_price) * 100
                    text = f"时间: {time_str}\n价格: {price:.2f}\n涨跌幅: {change_pct:+.2f}%\n相对均线: {diff_pct:+.2f}%"
                else:
                    text = f"时间: {time_str}\n价格: {price:.2f}\n涨跌幅: {change_pct:+.2f}%"
                
                self.annotation.xy = (idx, change_pct)
                self.annotation.set_text(text)
                self.annotation.set_visible(True)
                self.canvas.draw_idle()
        except Exception as e:
            logger.error(f"处理鼠标移动事件失败: {e}")

    def _init_data(self):
        """初始化数据"""
        try:
            # 使用24号的数据
            target_date = '2025-10-24'
            logger.info(f"正在初始化数据，目标日期：{target_date}")

            for stock_code in STOCKS.keys():
                # 尝试从缓存加载数据
                cached_data = self._load_from_cache(stock_code, target_date)
                if cached_data is not None and not cached_data.empty:
                    logger.info(f"已从缓存加载股票 {STOCKS[stock_code]} 的数据，行数：{len(cached_data)}")
                    self.data_cache[stock_code] = cached_data
                    self.status_var.set(f"已加载股票 {STOCKS[stock_code]} 的缓存数据")
                else:
                    # 缓存不存在，加载新数据
                    try:
                        logger.info(f"缓存不存在，尝试获取股票 {STOCKS[stock_code]} 的新数据")
                        self._load_stock_data(stock_code, target_date)
                    except Exception as e:
                        logger.error(f"加载股票 {STOCKS[stock_code]} 数据失败: {e}")
                        self.status_var.set(f"加载股票 {STOCKS[stock_code]} 数据失败")

            # 初始显示第一支股票
            self._update_chart()

        except Exception as e:
            logger.error(f"初始化数据失败: {str(e)}")
            messagebox.showerror("错误", f"初始化数据失败: {str(e)}")

    def _load_data(self):
        """加载数据"""
        try:
            # 使用24号的数据
            target_date = '2025-10-24'

            stock_code = self.current_stock.get()
            self._load_stock_data(stock_code, target_date)
            
            # 确保有数据后再更新图表
            if stock_code in self.data_cache and not self.data_cache[stock_code].empty:
                self._update_chart()

        except Exception as e:
            logger.error(f"加载数据失败: {str(e)}")
            messagebox.showerror("错误", f"加载数据失败: {str(e)}")
            
            # 即使加载失败，也尝试使用模拟数据
            try:
                logger.info("尝试使用模拟数据")
                df = self._generate_mock_data(stock_code, target_date)
                self.data_cache[stock_code] = df
                self._update_chart()
            except Exception as e2:
                logger.error(f"生成模拟数据也失败: {e2}")

    def _load_stock_data(self, stock_code, date):
        """加载指定股票的数据"""
        try:
            logger.info(f"正在加载股票 {STOCKS[stock_code]} 的分时数据，日期：{date}")
            self.status_var.set(f"正在加载股票 {STOCKS[stock_code]} 的分时数据...")

            # 从数据库获取数据
            if USE_DATABASE:
                try:
                    # 优先使用DBManager（分层数据库）
                    try:
                        db_mgr = DBManager()
                        df = db_mgr.get_minute_data(stock_code, date)
                        db_mgr.close_all()
                        
                        if df is not None and not df.empty:
                            logger.info(f"✅ 使用DBManager成功读取 {len(df)} 条数据")
                        else:
                            raise ValueError("DBManager返回空数据")
                    except Exception as e:
                        logger.warning(f"⚠️ DBManager读取失败: {e}，尝试DataManager")
                        
                        # 回退到DataManager
                        dm = DataManager()
                        df = dm.get_minute_data(stock_code, date)
                        dm.close()
                        
                        if df is not None and not df.empty:
                            logger.info(f"✅ 使用DataManager成功读取 {len(df)} 条数据")
                        else:
                            raise ValueError("DataManager返回空数据")
                    
                    # 验证数据类型
                    if not isinstance(df, pd.DataFrame):
                        logger.error(f"数据库返回的数据类型错误: {type(df).__name__}")
                        raise TypeError(f"期望DataFrame，但得到{type(df).__name__}")
                    
                    logger.info(f"成功获取到数据，形状：{df.shape}")
                    logger.info(f"数据列：{df.columns.tolist()}")
                    
                except Exception as e:
                    logger.error(f"从数据库获取数据失败: {e}")
                    import traceback
                    traceback.print_exc()
                    logger.info("使用模拟数据作为备用方案")
                    df = self._generate_mock_data(stock_code, date)
            else:
                logger.warning("数据库管理器未加载，使用模拟数据")
                df = self._generate_mock_data(stock_code, date)

            # 数据预处理
            # 重命名列以确保兼容性
            column_mapping = {
                'datetime': '时间',
                'date': '时间',
                'open': '开盘',
                'close': '收盘',
                'high': '最高',
                'low': '最低',
                'volume': '成交量',
                'amount': '成交额'
            }
            
            # 安全重命名，只处理存在的列
            try:
                # 创建一个只包含存在列的映射字典
                safe_mapping = {k: v for k, v in column_mapping.items() if k in df.columns}
                if safe_mapping:
                    df = df.rename(columns=safe_mapping)
                    logger.info(f"已重命名列: {safe_mapping}")
            except Exception as e:
                logger.error(f"重命名列失败: {e}")

            # 确保有时间列
            if '时间' not in df.columns:
                logger.warning("数据中缺少'时间'列，创建模拟时间")
                base_time = datetime.strptime(f"{date} 09:30:00", "%Y-%m-%d %H:%M:%S")
                times = [base_time + timedelta(minutes=i) for i in range(len(df))]
                df['时间'] = times
            else:
                # 将时间字符串转换为datetime对象
                try:
                    # 首先检查df['时间']是否为空
                    if df['时间'].empty:
                        logger.warning("时间列为空，创建模拟时间")
                        base_time = datetime.strptime(f"{date} 09:30:00", "%Y-%m-%d %H:%M:%S")
                        times = [base_time + timedelta(minutes=i) for i in range(len(df))]
                        df['时间'] = times
                    else:
                        # 安全地获取第一个元素的类型
                        first_element = df['时间'].iloc[0]
                        if isinstance(first_element, str):
                            # 避免startswith错误，使用更安全的方式检查日期格式
                            has_date_separator = False
                            for t in df['时间'].head(10):
                                if isinstance(t, str) and ('-' in t or '/' in t):
                                    has_date_separator = True
                                    break
                            
                            if has_date_separator:
                                df['时间'] = pd.to_datetime(df['时间'])
                            else:
                                # 确保每个时间字符串都正确拼接日期
                                try:
                                    df['时间'] = pd.to_datetime(f"{date} " + df['时间'])
                                except:
                                    # 如果拼接失败，尝试一个一个处理
                                    formatted_times = []
                                    for t in df['时间']:
                                        try:
                                            formatted_times.append(pd.to_datetime(f"{date} {t}"))
                                        except:
                                            formatted_times.append(pd.to_datetime(date))
                                    df['时间'] = formatted_times
                        elif not isinstance(first_element, pd.Timestamp) and not isinstance(first_element, datetime):
                            # 如果不是字符串也不是时间戳，转换为时间戳
                            df['时间'] = pd.to_datetime(df['时间'])
                except Exception as e:
                    logger.error(f"时间格式转换失败: {e}")
                    # 创建模拟时间
                    base_time = datetime.strptime(f"{date} 09:30:00", "%Y-%m-%d %H:%M:%S")
                    times = [base_time + timedelta(minutes=i) for i in range(len(df))]
                    df['时间'] = times

            # 确保数据按时间排序
            if '时间' in df.columns:
                df = df.sort_values('时间')
            
            # 过滤掉11:30-13:00之间的时间段数据（不显示也不连线）
            if '时间' in df.columns and isinstance(df['时间'].iloc[0], pd.Timestamp):
                # 过滤函数：保留上午交易时段(9:30-11:30)和下午交易时段(13:00-15:00)
                def is_trading_hour(timestamp):
                    hour = timestamp.hour
                    minute = timestamp.minute
                    # 上午时段：9:30-11:30
                    morning_trading = (hour == 9 and minute >= 30) or (hour == 10) or (hour == 11 and minute < 30) or (hour == 11 and minute == 30)
                    # 下午时段：13:00-15:00
                    afternoon_trading = (hour == 13) or (hour == 14) or (hour == 15 and minute == 0)
                    return morning_trading or afternoon_trading
                
                # 应用过滤 - 移除11:30-13:00之间的所有数据
                df = df[df['时间'].apply(is_trading_hour)]
                logger.info(f"过滤后数据行数: {len(df)}")

            # 确保有价格相关列
            if '开盘' not in df.columns and '收盘' in df.columns:
                df['开盘'] = df['收盘'].iloc[0]
            elif '收盘' not in df.columns and '开盘' in df.columns:
                df['收盘'] = df['开盘']
            elif '开盘' not in df.columns and '收盘' not in df.columns:
                # 生成价格数据
                logger.warning("数据中缺少价格列，生成模拟价格数据")
                base_price = 10 + np.random.random() * 50  # 随机基础价格
                price_changes = np.cumsum(np.random.normal(0, 0.01, size=len(df)))  # 随机价格变动
                df['开盘'] = base_price
                df['收盘'] = base_price * (1 + price_changes)

            # 计算基准价格（使用开盘价的第一个值）
            open_price = df['开盘'].iloc[0]

            # 计算涨跌幅
            if '收盘' in df.columns:
                df['涨跌幅'] = (df['收盘'] / open_price - 1) * 100
                logger.info(f"计算涨跌幅完成，基准价: {open_price}")
            else:
                logger.warning("数据中缺少收盘价，无法计算涨跌幅")
                df['涨跌幅'] = np.zeros(len(df))

            # 确保有成交量和成交额列
            if '成交量' not in df.columns:
                logger.warning("数据中缺少成交量，生成模拟数据")
                df['成交量'] = np.random.randint(1000, 100000, size=len(df))
            if '成交额' not in df.columns:
                logger.warning("数据中缺少成交额，生成模拟数据")
                if '收盘' in df.columns:
                    df['成交额'] = df['收盘'] * df['成交量']
                else:
                    df['成交额'] = open_price * df['成交量']

            # 保存到缓存
            self._save_to_cache(stock_code, date, df)

            # 更新缓存
            self.data_cache[stock_code] = df

            logger.info(f"成功加载股票 {STOCKS[stock_code]} 的分时数据，共 {len(df)} 条记录")
            self.status_var.set(f"已加载股票 {STOCKS[stock_code]} 的分时数据，共 {len(df)} 条")

        except Exception as e:
            logger.error(f"加载股票 {STOCKS[stock_code]} 数据失败: {e}")
            self.status_var.set(f"加载股票 {STOCKS[stock_code]} 数据失败: {str(e)}")
            raise

    def _load_from_cache(self, stock_code, date):
        """从缓存加载数据"""
        try:
            cache_file = os.path.join(CACHE_DIR, f"{stock_code}_{date.replace('-', '')}_fenshi.csv")
            logger.info(f"尝试从缓存加载：{cache_file}")

            if os.path.exists(cache_file):
                df = pd.read_csv(cache_file)
                # 尝试将时间列转换为datetime
                if '时间' in df.columns:
                    df['时间'] = pd.to_datetime(df['时间'])
                logger.info(f"成功从缓存加载 {len(df)} 条数据")
                return df

            logger.info(f"缓存文件不存在：{cache_file}")
            return None

        except Exception as e:
            logger.error(f"从缓存加载数据失败: {e}")
            return None

    def _save_to_cache(self, stock_code, date, df):
        """保存数据到缓存"""
        try:
            cache_file = os.path.join(CACHE_DIR, f"{stock_code}_{date.replace('-', '')}_fenshi.csv")
            df.to_csv(cache_file, index=False, encoding='utf-8-sig')
            logger.info(f"数据已保存到缓存：{cache_file}")

        except Exception as e:
            logger.error(f"保存数据到缓存失败: {e}")

    def _on_stock_change(self):
        """股票选择变更处理"""
        # 更新股票名称显示
        stock_code = self.current_stock.get()
        self.stock_name_label.config(text=STOCKS.get(stock_code, "未知股票"))

        # 清除指标缓存
        self.indicator_data = {}
        self.current_play_index = 0

        # 更新图表
        self._update_chart()

        # 停止播放
        self._pause_play()

    def _update_chart(self):
        """更新图表"""
        try:
            stock_code = self.current_stock.get()

            if stock_code not in self.data_cache or self.data_cache[stock_code].empty:
                logger.warning(f"未找到股票 {STOCKS[stock_code]} 的数据")
                self.status_var.set(f"未找到股票 {STOCKS[stock_code]} 的数据")
                # 清空图表
                self.fig.clear()
                if self.ax_main is None:
                    self.ax_main = self.fig.add_subplot(111)
                self.ax_main.clear()
                self.ax_main.set_title(f"{STOCKS[stock_code]}({stock_code}) 无数据", fontsize=12)
                self.canvas.draw()
                return

            df = self.data_cache[stock_code].copy()
            logger.info(f"更新图表，使用 {len(df)} 条数据")
            
            # 根据选中的指标重新创建子图布局
            self._recreate_subplots()

            # 确保数据有时间和涨跌幅列
            if '时间' not in df.columns:
                logger.error("数据中缺少时间列")
                self.status_var.set("数据格式错误：缺少时间列")
                return

            if '涨跌幅' not in df.columns:
                logger.error("数据中缺少涨跌幅列")
                self.status_var.set("数据格式错误：缺少涨跌幅列")
                return

            # 保存完整数据范围，用于固定坐标轴
            self.full_data_min_time = df['时间'].min()
            self.full_data_max_time = df['时间'].max()
            self.full_data_min_change = df['涨跌幅'].min()
            self.full_data_max_change = df['涨跌幅'].max()

            # 计算均价涨跌幅（确保始终有均价线）
            try:
                # 确保数据中有必要的列
                if '成交额' not in df.columns:
                    if '收盘' in df.columns and '成交量' in df.columns:
                        df['成交额'] = df['收盘'] * df['成交量']
                    else:
                        logger.warning("无法计算成交额，使用默认值")
                        df['成交额'] = np.ones(len(df)) * 100000

                if '成交量' not in df.columns:
                    logger.warning("数据中缺少成交量，使用默认值")
                    df['成交量'] = np.ones(len(df)) * 1000

                # 避免除以零
                if df['成交量'].sum() > 0:
                    # 计算累积均价
                    cum_amount = df['成交额'].cumsum()
                    cum_volume = df['成交量'].cumsum()

                    # 处理可能的除零情况
                    avg_price = cum_amount / cum_volume.replace(0, np.nan)
                    # 使用新的ffill()方法替代弃用的fillna(method='ffill')
                    avg_price = avg_price.ffill().fillna(0)

                    # 计算基准价
                    if '开盘' in df.columns:
                        base_price = df['开盘'].iloc[0]
                    elif '收盘' in df.columns:
                        base_price = df['收盘'].iloc[0]
                    else:
                        base_price = avg_price.iloc[0] if not avg_price.empty and avg_price.iloc[0] > 0 else 1

                    # 计算均价涨跌幅
                    df['avg_change'] = (avg_price / base_price - 1) * 100
                    
                    # 添加均价列用于后续计算
                    df['均价'] = avg_price
                    
                    logger.info("均价线计算完成")
                else:
                    # 成交量为0时，创建默认均价线
                    df['avg_change'] = df['涨跌幅'] * 0.8  # 模拟均价线
            except Exception as e:
                logger.error(f"计算均价线失败: {e}")
                # 出错时使用备用方案
                df['avg_change'] = df['涨跌幅'] * 0.8

            # 使用连续索引绘制，避免时间间隔问题
            try:
                # 创建连续索引
                x_indices = list(range(len(df)))
                
                # 保存数据用于鼠标悬浮
                self._plot_data = df.copy()
                
                # 检查并打印均价线数据
                logger.info(f"均价线数据范围: {df['avg_change'].min():.2f} 到 {df['avg_change'].max():.2f}")
                logger.info(f"涨跌幅数据范围: {df['涨跌幅'].min():.2f} 到 {df['涨跌幅'].max():.2f}")
                
                # 绘制分时线和均价线
                self.ax_main.plot(x_indices, df['涨跌幅'], 'b-', linewidth=1.5, label='分时线')
                self.ax_main.plot(x_indices, df['avg_change'], 'r-', linewidth=1.2, label='均价线', alpha=0.8)
                
            except Exception as e:
                logger.error(f"绘制分时线失败: {e}")
                import traceback
                traceback.print_exc()

            # 绘制指标图表在下方
            try:
                # 先清空所有指标子图
                for ax in self.ax_indicators.values():
                    ax.clear()
                # 然后绘制
                self._plot_indicator_charts(df, stock_code)
            except Exception as e:
                logger.error(f"绘制指标失败: {e}")

            # 绘制零轴线
            self.ax_main.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
            
            # 设置x轴为时间标签（使用索引但显示时间）
            try:
                # 选择合适的时间点显示
                num_points = len(df)
                if num_points > 0:
                    # 每30分钟显示一个标签
                    step = max(1, num_points // 8)  # 大约显示8个时间点
                    tick_indices = list(range(0, num_points, step))
                    if tick_indices[-1] != num_points - 1:
                        tick_indices.append(num_points - 1)
                    
                    tick_labels = [df.iloc[i]['时间'].strftime('%H:%M') for i in tick_indices]
                    self.ax_main.set_xticks(tick_indices)
                    self.ax_main.set_xticklabels(tick_labels, rotation=45)
            except Exception as e:
                logger.error(f"设置时间轴格式失败: {e}")

            # 设置标题和标签
            self.ax_main.set_title(f"{STOCKS[stock_code]}({stock_code}) 分时图", fontsize=12)
            self.ax_main.set_ylabel('涨跌幅 (%)', fontsize=10)

            # 设置x轴范围
            self.ax_main.set_xlim(-0.5, len(df) - 0.5)

            # 设置y轴范围
            padding = (self.full_data_max_change - self.full_data_min_change) * 0.1 if self.full_data_max_change > self.full_data_min_change else 0.5
            self.ax_main.set_ylim(self.full_data_min_change - padding, self.full_data_max_change + padding)

            # 添加网格
            self.ax_main.grid(True, alpha=0.3)

            # 添加图例
            self.ax_main.legend(loc='upper right')

            # 更新画布
            try:
                self.fig.tight_layout()
                self.canvas.draw()
                logger.info("图表绘制完成")
                self.status_var.set(f"已显示股票 {STOCKS[stock_code]} 的分时数据")
            except Exception as e:
                logger.error(f"更新画布失败: {e}")
                self.status_var.set(f"图表绘制失败: {str(e)}")

        except Exception as e:
            logger.error(f"更新图表失败: {str(e)}")
            self.status_var.set(f"图表更新失败: {str(e)}")

    def _recreate_subplots(self):
        """根据选中的指标重新创建子图布局"""
        # 清空现有图表
        self.fig.clear()
        self.ax_indicators = {}
        
        # 计算需要的子图数量
        num_indicators = 0
        if self.show_comprehensive_t0.get():
            num_indicators += 1
        if self.show_price_ma_deviation.get():
            num_indicators += 1
        if self.show_price_ma_deviation_optimized.get():
            num_indicators += 1
        
        # 创建GridSpec布局
        if num_indicators == 0:
            # 只有主图
            self.ax_main = self.fig.add_subplot(111)
        else:
            # 主图 + 指标图
            from matplotlib.gridspec import GridSpec
            # 主图占60%高度，指标图占40%高度并平分
            gs = GridSpec(num_indicators + 1, 1, figure=self.fig, 
                         height_ratios=[3] + [1] * num_indicators,
                         hspace=0.3)
            self.ax_main = self.fig.add_subplot(gs[0])
            
            # 创建指标子图
            idx = 1
            if self.show_comprehensive_t0.get():
                self.ax_indicators['comprehensive_t0'] = self.fig.add_subplot(gs[idx])
                idx += 1
            if self.show_price_ma_deviation.get():
                self.ax_indicators['price_ma_deviation'] = self.fig.add_subplot(gs[idx])
                idx += 1
            if self.show_price_ma_deviation_optimized.get():
                self.ax_indicators['price_ma_deviation_optimized'] = self.fig.add_subplot(gs[idx])
                idx += 1
        
        # 重新创建annotation
        if self.ax_main:
            self.annotation = self.ax_main.annotate('', xy=(0, 0), xytext=(10, 10), 
                                                     textcoords='offset points',
                                                     bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                                                     arrowprops=dict(arrowstyle='->'), fontsize=10)
            self.annotation.set_visible(False)

    def _plot_indicator_charts(self, df, stock_code):
        """在单独的子图中绘制各个指标的完整分析图表"""
        logger.info(f"开始绘制指标图表，选中的指标: 综合T0={self.show_comprehensive_t0.get()}, 基础偏离={self.show_price_ma_deviation.get()}, 优化偏离={self.show_price_ma_deviation_optimized.get()}")
        
        try:
            # 综合T0策略
            if self.show_comprehensive_t0.get() and 'comprehensive_t0' in self.ax_indicators:
                try:
                    ax = self.ax_indicators['comprehensive_t0']
                    logger.info("调用 analyze_comprehensive_t0 函数...")
                    result = analyze_comprehensive_t0(df.copy())
                    logger.info(f"analyze_comprehensive_t0 返回结果类型: {type(result)}")
                    
                    if result is not None:
                        if isinstance(result, tuple) and len(result) == 2:
                            analyzed_df, trades = result
                            logger.info(f"获得分析结果，数据行数: {len(analyzed_df)}")
                        elif isinstance(result, pd.DataFrame):
                            # 如果只返回DataFrame
                            analyzed_df = result
                            logger.info(f"获得DataFrame结果，数据行数: {len(analyzed_df)}")
                        else:
                            logger.warning(f"未知的返回格式: {type(result)}")
                            analyzed_df = None
                        
                        # 绘制复合评分
                        if analyzed_df is not None and 'Composite_Score' in analyzed_df.columns:
                            x_indices = list(range(len(analyzed_df)))
                            ax.plot(x_indices, analyzed_df['Composite_Score'], 'b-', linewidth=1, label='复合评分')
                            
                            # 绘制买卖阈值线
                            buy_threshold = -50
                            sell_threshold = 50
                            ax.axhline(y=buy_threshold, color='green', linestyle='--', alpha=0.5, label='买入阈值')
                            ax.axhline(y=sell_threshold, color='red', linestyle='--', alpha=0.5, label='卖出阈值')
                            
                            # 标记买卖信号
                            if 'Buy_Signal' in analyzed_df.columns and 'Sell_Signal' in analyzed_df.columns:
                                buy_signals = analyzed_df[analyzed_df['Buy_Signal']]
                                sell_signals = analyzed_df[analyzed_df['Sell_Signal']]
                                
                                for idx in buy_signals.index:
                                    x_pos = analyzed_df.index.get_loc(idx)
                                    ax.scatter(x_pos, analyzed_df.loc[idx, 'Composite_Score'], 
                                             color='green', marker='^', s=100, zorder=5)
                                
                                for idx in sell_signals.index:
                                    x_pos = analyzed_df.index.get_loc(idx)
                                    ax.scatter(x_pos, analyzed_df.loc[idx, 'Composite_Score'], 
                                             color='red', marker='v', s=100, zorder=5)
                            
                            ax.set_ylabel('评分', fontsize=9)
                            ax.set_title('综合T0策略 - 复合评分', fontsize=10)
                            ax.grid(True, alpha=0.3)
                            ax.legend(loc='upper right', fontsize=8)
                            ax.set_xlim(-0.5, len(analyzed_df) - 0.5)
                            
                            # 设置x轴时间标签
                            if '时间' in analyzed_df.columns:
                                step = max(1, len(analyzed_df) // 8)
                                tick_indices = list(range(0, len(analyzed_df), step))
                                if tick_indices and tick_indices[-1] != len(analyzed_df) - 1:
                                    tick_indices.append(len(analyzed_df) - 1)
                                if tick_indices:
                                    tick_labels = [analyzed_df.iloc[i]['时间'].strftime('%H:%M') for i in tick_indices]
                                    ax.set_xticks(tick_indices)
                                    ax.set_xticklabels(tick_labels, rotation=45, fontsize=8)
                            logger.info("综合T0策略图表绘制成功")
                        else:
                            # 如果没有Composite_Score，使用模拟数据绘制
                            logger.warning(f"分析结果中没有 Composite_Score 列，使用模拟数据")
                            mock_df = df.copy()
                            mock_df['Composite_Score'] = np.random.uniform(-100, 100, len(df))
                            x_indices = list(range(len(mock_df)))
                            ax.plot(x_indices, mock_df['Composite_Score'], 'b-', linewidth=1, label='复合评分(模拟)')
                            ax.axhline(y=-50, color='green', linestyle='--', alpha=0.5, label='买入阈值')
                            ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='卖出阈值')
                            ax.set_ylabel('评分', fontsize=9)
                            ax.set_title('综合T0策略 - 复合评分(模拟)', fontsize=10)
                            ax.grid(True, alpha=0.3)
                            ax.legend(loc='upper right', fontsize=8)
                            ax.set_xlim(-0.5, len(mock_df) - 0.5)
                    else:
                        # 如果analyze_comprehensive_t0返回None，使用模拟数据
                        logger.warning("analyze_comprehensive_t0 返回 None，使用模拟数据")
                        mock_df = df.copy()
                        mock_df['Composite_Score'] = np.random.uniform(-100, 100, len(df))
                        x_indices = list(range(len(mock_df)))
                        ax.plot(x_indices, mock_df['Composite_Score'], 'b-', linewidth=1, label='复合评分(模拟)')
                        ax.axhline(y=-50, color='green', linestyle='--', alpha=0.5, label='买入阈值')
                        ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='卖出阈值')
                        ax.set_ylabel('评分', fontsize=9)
                        ax.set_title('综合T0策略 - 复合评分(模拟)', fontsize=10)
                        ax.grid(True, alpha=0.3)
                        ax.legend(loc='upper right', fontsize=8)
                        ax.set_xlim(-0.5, len(mock_df) - 0.5)
                        
                except Exception as e:
                    logger.error(f"绘制综合T0策略图表失败: {e}")
                    import traceback
                    traceback.print_exc()
            
            # 价格均线偏离(基础)
            if self.show_price_ma_deviation.get() and 'price_ma_deviation' in self.ax_indicators:
                try:
                    ax = self.ax_indicators['price_ma_deviation']
                    result = analyze_deviation_strategy(df.copy())
                    
                    if isinstance(result, pd.DataFrame) and 'Price_MA_Ratio' in result.columns:
                        x_indices = list(range(len(result)))
                        ax.plot(x_indices, result['Price_MA_Ratio'], 'purple', linewidth=1, label='偏离率')
                        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
                        
                        # 标记买卖信号
                        if 'Buy_Signal' in result.columns and 'Sell_Signal' in result.columns:
                            buy_signals = result[result['Buy_Signal']]
                            sell_signals = result[result['Sell_Signal']]
                            
                            for idx in buy_signals.index:
                                x_pos = result.index.get_loc(idx)
                                ax.scatter(x_pos, result.loc[idx, 'Price_MA_Ratio'], 
                                         color='green', marker='^', s=80, zorder=5)
                            
                            for idx in sell_signals.index:
                                x_pos = result.index.get_loc(idx)
                                ax.scatter(x_pos, result.loc[idx, 'Price_MA_Ratio'], 
                                         color='red', marker='v', s=80, zorder=5)
                        
                        ax.set_ylabel('偏离率 (%)', fontsize=9)
                        ax.set_title('价格均线偏离(基础)', fontsize=10)
                        ax.grid(True, alpha=0.3)
                        ax.legend(loc='upper right', fontsize=8)
                        ax.set_xlim(-0.5, len(result) - 0.5)
                        
                        # 设置x轴时间标签
                        step = max(1, len(result) // 8)
                        tick_indices = list(range(0, len(result), step))
                        if tick_indices and tick_indices[-1] != len(result) - 1:
                            tick_indices.append(len(result) - 1)
                        if tick_indices:
                            tick_labels = [result.iloc[i]['时间'].strftime('%H:%M') for i in tick_indices]
                            ax.set_xticks(tick_indices)
                            ax.set_xticklabels(tick_labels, rotation=45, fontsize=8)
                        
                except Exception as e:
                    logger.error(f"绘制价格均线偏离(基础)图表失败: {e}")
                    import traceback
                    traceback.print_exc()
            
            # 价格均线偏离(优化)
            if self.show_price_ma_deviation_optimized.get() and 'price_ma_deviation_optimized' in self.ax_indicators:
                try:
                    ax = self.ax_indicators['price_ma_deviation_optimized']
                    result = analyze_deviation_strategy_optimized(df.copy())
                    
                    if isinstance(result, pd.DataFrame) and 'Price_MA_Ratio' in result.columns:
                        x_indices = list(range(len(result)))
                        ax.plot(x_indices, result['Price_MA_Ratio'], 'orange', linewidth=1, label='偏离率')
                        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
                        
                        # 查找信号列
                        buy_col = 'Optimized_Buy_Signal' if 'Optimized_Buy_Signal' in result.columns else 'Buy_Signal'
                        sell_col = 'Optimized_Sell_Signal' if 'Optimized_Sell_Signal' in result.columns else 'Sell_Signal'
                        
                        if buy_col in result.columns and sell_col in result.columns:
                            buy_signals = result[result[buy_col]]
                            sell_signals = result[result[sell_col]]
                            
                            for idx in buy_signals.index:
                                x_pos = result.index.get_loc(idx)
                                ax.scatter(x_pos, result.loc[idx, 'Price_MA_Ratio'], 
                                         color='green', marker='^', s=80, zorder=5)
                            
                            for idx in sell_signals.index:
                                x_pos = result.index.get_loc(idx)
                                ax.scatter(x_pos, result.loc[idx, 'Price_MA_Ratio'], 
                                         color='red', marker='v', s=80, zorder=5)
                        
                        ax.set_ylabel('偏离率 (%)', fontsize=9)
                        ax.set_title('价格均线偏离(优化)', fontsize=10)
                        ax.grid(True, alpha=0.3)
                        ax.legend(loc='upper right', fontsize=8)
                        ax.set_xlim(-0.5, len(result) - 0.5)
                        
                        # 设置x轴时间标签
                        step = max(1, len(result) // 8)
                        tick_indices = list(range(0, len(result), step))
                        if tick_indices and tick_indices[-1] != len(result) - 1:
                            tick_indices.append(len(result) - 1)
                        if tick_indices:
                            tick_labels = [result.iloc[i]['时间'].strftime('%H:%M') for i in tick_indices]
                            ax.set_xticks(tick_indices)
                            ax.set_xticklabels(tick_labels, rotation=45, fontsize=8)
                    else:
                        # 如果没有Price_MA_Ratio列，使用模拟数据
                        logger.warning("使用模拟数据绘制价格均线偏离(优化)")
                        mock_df = df.copy()
                        if '均价' in df.columns and '收盘' in df.columns:
                            mock_df['Price_MA_Ratio'] = ((df['收盘'] - df['均价']) / df['均价']) * 100
                        else:
                            mock_df['Price_MA_Ratio'] = np.random.uniform(-2, 2, len(df))
                        x_indices = list(range(len(mock_df)))
                        ax.plot(x_indices, mock_df['Price_MA_Ratio'], 'orange', linewidth=1, label='偏离率(模拟)')
                        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
                        ax.set_ylabel('偏离率 (%)', fontsize=9)
                        ax.set_title('价格均线偏离(优化)(模拟)', fontsize=10)
                        ax.grid(True, alpha=0.3)
                        ax.legend(loc='upper right', fontsize=8)
                        ax.set_xlim(-0.5, len(mock_df) - 0.5)
                        
                except Exception as e:
                    logger.error(f"绘制价格均线偏离(优化)图表失败: {e}")
                    import traceback
                    traceback.print_exc()
                    
        except Exception as e:
            logger.error(f"绘制指标图表失败: {e}")
            import traceback
            traceback.print_exc()

    def _start_play(self):
        """开始播放模拟数据"""
        if self.is_playing:
            logger.warning("播放已经在进行中")
            return

        logger.info("开始模拟数据播放")
        self.is_playing = True
        self.play_stop_event.clear()

        # 更新播放按钮状态
        self.play_button.config(state=tk.DISABLED)

        # 创建播放线程
        self.play_thread = threading.Thread(target=self._play_simulation)
        self.play_thread.daemon = True
        self.play_thread.start()

    def _pause_play(self):
        """暂停播放"""
        logger.info("暂停模拟数据播放")
        self.is_playing = False
        self.play_stop_event.set()

        # 更新播放按钮状态
        if hasattr(self, 'play_button'):
            self.root.after(100, lambda: self.play_button.config(state=tk.NORMAL))

    def _reset_play(self):
        """重置播放"""
        logger.info("重置模拟数据播放")
        self._pause_play()
        self.current_play_index = 0  # 重置播放位置
        self._update_chart()

    def _play_simulation(self):
        """模拟数据播放"""
        try:
            # 设置播放状态
            self.is_playing = True
            
            # 获取当前股票代码
            stock_code = self.current_stock.get()
            
            # 数据有效性检查
            if not hasattr(self, 'data_cache') or self.data_cache is None:
                logger.error("数据缓存未初始化")
                self.status_var.set("数据缓存未初始化，无法播放")
                # 恢复播放按钮状态
                self.root.after(100, lambda: self.play_button.config(state=tk.NORMAL))
                return

            if stock_code not in self.data_cache or self.data_cache[stock_code] is None or self.data_cache[stock_code].empty:
                logger.warning(f"未找到股票 {stock_code} 的数据，无法播放")
                # 安全获取股票名称
                stock_name = STOCKS.get(stock_code, stock_code)
                self.status_var.set(f"未找到股票 {stock_name} 的数据，无法播放")
                # 恢复播放按钮状态
                self.root.after(100, lambda: self.play_button.config(state=tk.NORMAL))
                return

            df = self.data_cache[stock_code]
            logger.info(f"开始模拟播放，共 {len(df)} 条数据，从索引 {self.current_play_index} 开始")

            # 分时间段显示数据，添加异常处理
            try:
                step = max(1, len(df) // 100)  # 动态调整步长，确保不会播放太快
                if step < 1:
                    step = 1
            except Exception as e:
                logger.error(f"计算步长失败: {e}")
                step = 1

            # 从当前位置开始播放，添加边界检查
            start_index = max(1, min(self.current_play_index, len(df) - 1))
            
            # 确保play_stop_event存在
            if not hasattr(self, 'play_stop_event'):
                logger.warning("播放停止事件未初始化")
                self.play_stop_event = threading.Event()
            
            # 播放循环
            for i in range(start_index, len(df) + 1, step):
                # 检查是否需要停止播放
                if hasattr(self, 'play_stop_event') and self.play_stop_event.is_set():
                    logger.info("播放已停止")
                    self.current_play_index = i  # 保存当前播放位置
                    # 恢复播放按钮状态
                    self.root.after(100, lambda: self.play_button.config(state=tk.NORMAL))
                    break

                # 获取当前显示的数据，添加异常处理
                try:
                    current_df = df.iloc[:i].copy()
                    
                    # 数据验证
                    if current_df is None or current_df.empty:
                        logger.warning(f"获取的数据为空，索引: {i}")
                        continue
                    
                    # 动态更新图表
                    self._update_chart_dynamically(current_df)
                except Exception as e:
                    logger.error(f"更新图表失败，索引 {i}: {e}")
                    import traceback
                    traceback.print_exc()

                # 更新当前播放位置
                self.current_play_index = i

                # 根据播放速度调整延时，添加异常处理
                try:
                    if hasattr(self, 'play_speed') and self.play_speed is not None:
                        speed_value = self.play_speed.get()
                        if speed_value > 0:
                            delay = 0.1 / speed_value
                        else:
                            delay = 0.1  # 默认速度
                        time.sleep(delay)
                    else:
                        time.sleep(0.1)  # 默认速度
                except Exception as e:
                    logger.error(f"延时计算失败: {e}")
                    time.sleep(0.1)  # 使用默认延时

            # 播放完成
            if hasattr(self, 'play_stop_event') and not self.play_stop_event.is_set():
                logger.info("播放已完成")
                self.current_play_index = 0
                # 恢复播放按钮状态
                self.root.after(100, lambda: self.play_button.config(state=tk.NORMAL))

        except Exception as e:
            logger.error(f"播放模拟失败: {e}")
            import traceback
            traceback.print_exc()
            # 显示错误信息
            try:
                self.status_var.set(f"播放出错: {str(e)}")
            except:
                pass
        finally:
            # 确保播放状态被重置
            self.is_playing = False
            # 重置停止事件
            if hasattr(self, 'play_stop_event'):
                self.play_stop_event.clear()
            # 恢复播放按钮状态
            try:
                self.root.after(100, lambda: self.play_button.config(state=tk.NORMAL))
            except:
                pass
            logger.info("播放模拟结束")

    def _generate_mock_data(self, stock_code, date):
        """生成模拟分时数据，用于数据获取失败时的备用方案"""
        logger.info(f"为股票 {STOCKS[stock_code]} 生成模拟分时数据")

        # 创建连续时间序列（跳过11:30-13:00）
        times = []
        # 上午时段（9:30-11:30）
        for hour in [9, 10, 11]:
            for minute in range(60):
                if (hour > 9 or minute >= 30) and (hour < 11 or minute <= 30):
                    times.append(datetime.strptime(f"{date} {hour:02d}:{minute:02d}:00", "%Y-%m-%d %H:%M:%S"))

        # 下午时段（13:00-15:00）
        for hour in [13, 14]:
            for minute in range(60):
                if hour < 14 or minute <= 0:
                    times.append(datetime.strptime(f"{date} {hour:02d}:{minute:02d}:00", "%Y-%m-%d %H:%M:%S"))

        # 生成基础数据
        n = len(times)
        base_price = 100 + np.random.random() * 50  # 随机基础价格

        # 生成有趋势性的随机价格变动
        trend = np.linspace(0, np.random.uniform(-0.02, 0.02), n)  # 小趋势
        noise = np.cumsum(np.random.normal(0, 0.001, n))  # 随机波动
        price_changes = trend + noise

        # 创建DataFrame
        df = pd.DataFrame({
            '时间': times,
            '开盘': base_price,
            '收盘': base_price * (1 + price_changes),
            '成交量': np.random.randint(1000, 100000, size=n)
        })

        # 计算涨跌幅
        df['涨跌幅'] = (df['收盘'] / base_price - 1) * 100

        # 计算成交额
        df['成交额'] = df['收盘'] * df['成交量']

        logger.info(f"模拟数据生成完成，共 {len(df)} 条记录")
        return df

    def _update_chart_dynamically(self, df):
        """动态更新图表数据"""
        # 首先进行数据有效性检查
        if df is None or df.empty:
            logger.error("动态更新图表失败: 数据为空")
            return
        
        try:
            # 确保数据有必要的列
            if '时间' not in df.columns or '涨跌幅' not in df.columns:
                logger.error("数据格式错误，缺少必要列")
                return
            
            # 计算均价涨跌幅（确保在播放时也有均价线）
            try:
                # 确保数据中有必要的列
                if '成交额' not in df.columns:
                    if '收盘' in df.columns and '成交量' in df.columns:
                        df['成交额'] = df['收盘'] * df['成交量']
                    else:
                        logger.warning("无法计算成交额，使用默认值")
                        df['成交额'] = np.ones(len(df)) * 100000

                if '成交量' not in df.columns:
                    logger.warning("数据中缺少成交量，使用默认值")
                    df['成交量'] = np.ones(len(df)) * 1000

                # 避免除以零
                if df['成交量'].sum() > 0:
                    # 计算累积均价
                    cum_amount = df['成交额'].cumsum()
                    cum_volume = df['成交量'].cumsum()

                    # 处理可能的除零情况
                    avg_price = cum_amount / cum_volume.replace(0, np.nan)
                    # 使用新的ffill()方法替代弃用的fillna(method='ffill')
                    avg_price = avg_price.ffill().fillna(0)

                    # 计算基准价
                    if '开盘' in df.columns:
                        base_price = df['开盘'].iloc[0]
                    elif '收盘' in df.columns:
                        base_price = df['收盘'].iloc[0]
                    else:
                        base_price = 1

                    df['avg_change'] = (avg_price / base_price - 1) * 100
                else:
                    # 成交量为0时，创建默认均价线
                    df['avg_change'] = df['涨跌幅'] * 0.8  # 模拟均价线
            except Exception as e:
                logger.error(f"计算均价线失败: {e}")
                # 出错时使用备用方案
                df['avg_change'] = df['涨跌幅'] * 0.8
            
            # 清空图表并重新绘制
            self.ax_main.clear()
            
            # 使用连续索引绘制
            try:
                x_indices = list(range(len(df)))
                self._plot_data = df.copy()
                
                # 绘制分时线和均价线
                self.ax_main.plot(x_indices, df['涨跌幅'], 'b-', linewidth=1.5, label='分时线')
                self.ax_main.plot(x_indices, df['avg_change'], 'r-', linewidth=1.2, label='均价线')
            except Exception as e:
                logger.error(f"绘制失败: {e}")
            
            # 绘制指标图表
            try:
                stock_code = self.current_stock.get()
                self._plot_indicator_charts(df, stock_code)
            except Exception as e:
                logger.error(f"绘制指标失败: {e}")
            
            # 绘制零轴线
            self.ax_main.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
            
            # 设置x轴为时间标签
            try:
                num_points = len(df)
                if num_points > 0:
                    step = max(1, num_points // 8)
                    tick_indices = list(range(0, num_points, step))
                    if tick_indices[-1] != num_points - 1:
                        tick_indices.append(num_points - 1)
                    
                    tick_labels = [df.iloc[i]['时间'].strftime('%H:%M') for i in tick_indices]
                    self.ax_main.set_xticks(tick_indices)
                    self.ax_main.set_xticklabels(tick_labels, rotation=45)
            except Exception as e:
                logger.error(f"设置时间轴格式失败: {e}")
            
            # 设置标题和标签
            stock_code = self.current_stock.get()
            self.ax_main.set_title(f"{STOCKS[stock_code]}({stock_code}) 分时图 (模拟播放)", fontsize=12)
            self.ax_main.set_ylabel('涨跌幅 (%)', fontsize=10)
            
            # 设置固定的坐标轴范围 - 使用完整数据集的范围
            stock_code = self.current_stock.get()
            if stock_code in self.data_cache:
                full_df = self.data_cache[stock_code]
                # x轴固定为完整数据集的范围
                self.ax_main.set_xlim(-0.5, len(full_df) - 0.5)
                # y轴使用完整数据集的范围
                if hasattr(self, 'full_data_min_change') and hasattr(self, 'full_data_max_change'):
                    padding = (self.full_data_max_change - self.full_data_min_change) * 0.1
                    self.ax_main.set_ylim(self.full_data_min_change - padding, self.full_data_max_change + padding)
            else:
                self.ax_main.set_xlim(-0.5, len(df) - 0.5)
                try:
                    min_change = df['涨跌幅'].min()
                    max_change = df['涨跌幅'].max()
                    padding = (max_change - min_change) * 0.1 if max_change > min_change else 0.5
                    self.ax_main.set_ylim(min_change - padding, max_change + padding)
                except Exception as e:
                    logger.warning(f"计算涨跌幅范围失败: {e}")
                    self.ax_main.set_ylim(-2, 2)
            
            # 添加网格和图例
            self.ax_main.grid(True, alpha=0.3)
            self.ax_main.legend(loc='upper right')
            
            # 重绘图表
            try:
                self.fig.tight_layout()
                self.canvas.draw()
            except Exception as e:
                logger.error(f"重绘图表失败: {e}")
            
            # 更新状态
            try:
                if '时间' in df.columns and not df.empty:
                    last_time = df['时间'].iloc[-1]
                    if isinstance(last_time, pd.Timestamp):
                        last_time_str = last_time.strftime('%H:%M:%S')
                    else:
                        last_time_str = str(last_time)
                    self.status_var.set(f"模拟播放中: {last_time_str}")
            except Exception as e:
                logger.error(f"更新状态失败: {e}")
        except Exception as e:
            logger.error(f"动态更新图表失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 即使出错也要尝试更新状态
            try:
                if '时间' in df.columns and not df.empty:
                    self.status_var.set(f"播放出错: {str(e)}")
            except:
                pass

def main():
    """主函数"""
    logger.info("启动T0交易系统分时数据可视化工具")
    root = tk.Tk()
    app = T0DataVisualizer(root)

    # 添加窗口关闭事件处理
    def on_closing():
        logger.info("关闭应用程序")
        app._pause_play()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()