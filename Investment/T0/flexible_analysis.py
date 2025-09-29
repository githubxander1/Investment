import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import akshare as ak

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from indicators import tdx_indicators, liang, liangjia
from utils import data_handler
from visualization import plotting


class FlexibleStockAnalyzer:
    """
    灵活的股票分析器 - 支持为不同股票使用不同指标或指标组合
    """

    def __init__(self):
        """初始化分析器"""
        self.results = {}
        # 设置中文字体
        plotting.set_chinese_font()
        print("灵活股票分析器初始化完成")

    def get_stock_data(self, stock_code, trade_date=None):
        """
        获取股票数据
        
        参数:
        stock_code: 股票代码
        trade_date: 交易日期，格式'YYYYMMDD'
        
        返回:
        df: 股票数据DataFrame
        """
        try:
            # 如果没有指定日期，则使用今天
            if trade_date is None:
                trade_date = datetime.now().strftime('%Y%m%d')
            
            # 尝试从缓存获取数据
            df = data_handler.get_cached_data(stock_code, trade_date)
            
            # 如果缓存中没有数据，则从网络获取
            if df is None:
                print(f"缓存中无数据，从网络获取 {stock_code} 的数据...")
                df = ak.stock_zh_a_hist_min_em(
                    symbol=stock_code,
                    period="1",
                    start_date=trade_date,
                    end_date=trade_date,
                    adjust=''
                )
                
                if df.empty:
                    print(f"❌ 无分时数据: {stock_code}")
                    return None
                
                # 保存到缓存
                data_handler.save_data_to_cache(df.copy(), stock_code, trade_date)
            else:
                print(f"使用缓存数据: {stock_code}")
            
            # 数据预处理
            df['时间'] = pd.to_datetime(df['时间'], errors='coerce')
            df = df[df['时间'].notna()]
            
            # 只保留指定日期的数据
            target_date = pd.to_datetime(trade_date, format='%Y%m%d')
            df = df[df['时间'].dt.date == target_date.date()]
            
            # 过滤掉 11:30 到 13:00 之间的数据
            df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
            
            if df.empty:
                print("❌ 所有时间数据均无效")
                return None
            
            # 校准时间索引
            morning_index = pd.date_range(
                start=f"{trade_date} 09:30:00",
                end=f"{trade_date} 11:30:00",
                freq='1min'
            )
            afternoon_index = pd.date_range(
                start=f"{trade_date} 13:00:00",
                end=f"{trade_date} 15:00:00",
                freq='1min'
            )
            
            # 合并索引
            full_index = morning_index.union(afternoon_index)
            df = df.set_index('时间').reindex(full_index)
            df.index.name = '时间'
            
            # 填充缺失值
            df = df.ffill().bfill()
            
            return df
            
        except Exception as e:
            print(f"获取股票数据失败: {e}")
            return None

    def get_previous_close(self, stock_code, trade_date):
        """
        获取前一日收盘价
        
        参数:
        stock_code: 股票代码
        trade_date: 交易日期
        
        返回:
        float: 前一日收盘价
        """
        try:
            daily_df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                adjust=""
            )
            
            if not daily_df.empty:
                daily_df['日期'] = pd.to_datetime(daily_df['日期'])
                target_date = pd.to_datetime(trade_date, format='%Y%m%d')
                df_before = daily_df[daily_df['日期'] < target_date]
                
                if not df_before.empty:
                    return df_before.iloc[-1]['收盘']
            
            # 如果无法获取前一日收盘价，使用当日开盘价替代
            return None
            
        except Exception as e:
            print(f"获取前一日收盘价失败: {e}")
            return None

    def apply_indicator_tdx(self, df, prev_close):
        """
        应用TDX指标
        
        参数:
        df: 股票数据
        prev_close: 前一日收盘价
        
        返回:
        df: 添加了TDX指标的DataFrame
        """
        try:
            df = tdx_indicators.calculate_tdx_indicators(df, prev_close)
            # 计算均价
            df['均价'] = df['收盘'].expanding().mean()
            return df
        except Exception as e:
            print(f"应用TDX指标失败: {e}")
            return df

    def apply_indicator_liang(self, df, prev_close):
        """
        应用liang指标
        
        参数:
        df: 股票数据
        prev_close: 前一日收盘价
        
        返回:
        df: 添加了liang指标的DataFrame
        """
        try:
            # 获取日线数据用于liang指标计算
            daily_df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                adjust=""
            )
            df = liang.calculate_tdx_indicators(df, prev_close, daily_df)
            return df
        except Exception as e:
            print(f"应用liang指标失败: {e}")
            return df

    def apply_indicator_liangjia(self, df, prev_close):
        """
        应用liangjia指标
        
        参数:
        df: 股票数据
        prev_close: 前一日收盘价
        
        返回:
        tuple: (df, buy_ratio, sell_ratio, diff_ratio)
        """
        try:
            df, buy_ratio, sell_ratio, diff_ratio = liangjia.calculate_volume_price_indicators(df, prev_close)
            df = liangjia.calculate_support_resistance(df, prev_close)
            df = liangjia.calculate_fund_flow_indicators(df)
            df = liangjia.calculate_precise_lines(df)
            df = liangjia.detect_signals(df)
            return df, buy_ratio, sell_ratio, diff_ratio
        except Exception as e:
            print(f"应用liangjia指标失败: {e}")
            return df, 0, 0, 0

    def plot_tdx_chart(self, df, stock_code, trade_date, prev_close):
        """
        绘制TDX指标图表
        
        参数:
        df: 包含TDX指标的股票数据
        stock_code: 股票代码
        trade_date: 交易日期
        prev_close: 前一日收盘价
        """
        try:
            fig = plotting.create_intraday_plot(
                df, stock_code, trade_date, prev_close, 
                lambda signal_type, code, price, time_str: None  # 空的通知函数
            )
            if fig:
                plt.show(block=False)
                return fig
        except Exception as e:
            print(f"绘制TDX图表失败: {e}")
        return None

    def plot_liangjia_chart(self, df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio):
        """
        绘制liangjia指标图表
        
        参数:
        df: 包含liangjia指标的股票数据
        stock_code: 股票代码
        trade_date: 交易日期
        buy_ratio: 买入比例
        sell_ratio: 卖出比例
        diff_ratio: 差异比例
        """
        try:
            fig = liangjia.plot_indicators(df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio)
            if fig:
                plt.show(block=False)
                return fig
        except Exception as e:
            print(f"绘制liangjia图表失败: {e}")
        return None

    def analyze_stock_with_indicator(self, stock_code, indicator_type, trade_date=None):
        """
        使用指定指标分析股票
        
        参数:
        stock_code: 股票代码
        indicator_type: 指标类型 ('tdx', 'liang', 'liangjia')
        trade_date: 交易日期
        
        返回:
        dict: 分析结果
        """
        print(f"使用 {indicator_type} 指标分析股票 {stock_code}")
        
        # 获取数据
        df = self.get_stock_data(stock_code, trade_date)
        if df is None:
            return None
        
        # 获取前一日收盘价
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
        
        prev_close = self.get_previous_close(stock_code, trade_date)
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0] if '开盘' in df.columns else df['收盘'].iloc[0]
            print(f"⚠️ 使用开盘价替代昨收: {prev_close:.2f}")
        
        # 根据指标类型应用相应指标
        if indicator_type == 'tdx':
            df = self.apply_indicator_tdx(df, prev_close)
            fig = self.plot_tdx_chart(df, stock_code, trade_date, prev_close)
            result = {
                'stock_code': stock_code,
                'indicator_type': indicator_type,
                'data': df,
                'prev_close': prev_close,
                'figure': fig
            }
            
        elif indicator_type == 'liang':
            df = self.apply_indicator_liang(df, prev_close)
            # 使用liang的绘图函数
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df.index, df['收盘'], label='收盘价')
            ax.set_title(f'{stock_code} - Liang指标分析')
            ax.legend()
            plt.show(block=False)
            result = {
                'stock_code': stock_code,
                'indicator_type': indicator_type,
                'data': df,
                'prev_close': prev_close,
                'figure': fig
            }
            
        elif indicator_type == 'liangjia':
            df, buy_ratio, sell_ratio, diff_ratio = self.apply_indicator_liangjia(df, prev_close)
            fig = self.plot_liangjia_chart(df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio)
            result = {
                'stock_code': stock_code,
                'indicator_type': indicator_type,
                'data': df,
                'prev_close': prev_close,
                'buy_ratio': buy_ratio,
                'sell_ratio': sell_ratio,
                'diff_ratio': diff_ratio,
                'figure': fig
            }
            
        else:
            print(f"未知指标类型: {indicator_type}")
            return None
        
        # 保存结果
        self.results[f"{stock_code}_{indicator_type}"] = result
        return result

    def analyze_multiple_stocks(self, stock_indicator_mapping, trade_date=None):
        """
        分析多个股票，每个股票可使用不同指标
        
        参数:
        stock_indicator_mapping: 股票与指标的映射字典，例如:
            {
                '600900': 'tdx',
                '601088': 'liangjia',
                '601398': ['tdx', 'liangjia']  # 同时使用多个指标
            }
        trade_date: 交易日期
        """
        print("开始分析多个股票...")
        
        for stock_code, indicators in stock_indicator_mapping.items():
            # 如果是单个指标
            if isinstance(indicators, str):
                self.analyze_stock_with_indicator(stock_code, indicators, trade_date)
            # 如果是多个指标
            elif isinstance(indicators, (list, tuple)):
                for indicator in indicators:
                    self.analyze_stock_with_indicator(stock_code, indicator, trade_date)
            else:
                print(f"无效的指标配置: {stock_code} -> {indicators}")

    def close_all_plots(self):
        """关闭所有图表"""
        plt.close('all')


def main():
    """
    主函数 - 演示如何使用灵活分析器
    """
    # 创建分析器实例
    analyzer = FlexibleStockAnalyzer()
    
    # 示例1: 不同股票使用不同指标
    # print("=== 示例1: 不同股票使用不同指标 ===")
    # stock_indicator_mapping = {
    #     '600900': 'tdx',      # 长江电力使用TDX指标
    #     '601088': 'liangjia', # 中国神华使用liangjia指标
    #     '601398': 'tdx'       # 工商银行使用TDX指标
    # }
    
    # analyzer.analyze_multiple_stocks(stock_indicator_mapping)
    
    # 示例2: 同一股票使用多个指标
    print("\n=== 示例2: 同一股票使用多个指标 ===")
    stock_indicator_mapping_multi = {
        '600900': ['tdx', 'liangjia']  # 长江电力同时使用TDX和liangjia指标
    }

    analyzer.analyze_multiple_stocks(stock_indicator_mapping_multi)
    #
    # print("\n分析完成，请查看图表")
    # input("按回车键关闭所有图表并退出...")
    # analyzer.close_all_plots()


if __name__ == "__main__":
    main()