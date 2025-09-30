# T0交易系统信号检测模块
import pandas as pd
import numpy as np
from datetime import datetime, time
import akshare as ak
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Investment.T0.utils.logger import log_signal
from Investment.T0.indicators.resistance_support_indicators import calculate_tdx_indicators as calc_resistance_support, plot_tdx_intraday
from Investment.T0.indicators.extended_indicators import calculate_tdx_indicators as calc_extended
from Investment.T0.indicators.volume_price_indicators import (calculate_volume_price_indicators,
                                               calculate_support_resistance, 
                                               calculate_fund_flow_indicators, 
                                               detect_signals)

class SignalDetector:
    """信号检测器"""
    
    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.prev_signals = {
            'resistance_support': {'buy': False, 'sell': False},
            'extended': {'buy': False, 'sell': False},
            'volume_price': {'buy': False, 'sell': False}
        }
    
    def is_trading_time(self):
        """判断是否为交易时间"""
        now = datetime.now().time()
        # 交易时间段：9:30-11:30 和 13:00-15:00
        morning_session = time(9, 30) <= now <= time(11, 30)
        afternoon_session = time(13, 0) <= now <= time(15, 0)
        return morning_session or afternoon_session
    
    def is_market_closed(self):
        """判断是否已收盘"""
        now = datetime.now().time()
        return now > time(19, 0)
    
    def wait_until_trading_time(self):
        """等待到交易时间开始"""
        import time as time_module
        while not self.is_trading_time() and not self.is_market_closed():
            time_module.sleep(60)  # 每分钟检查一次
    
    def get_stock_data(self, trade_date=None):
        """获取股票分时数据"""
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
            
        try:
            df = ak.stock_zh_a_hist_min_em(
                symbol=self.stock_code,
                period="1",
                start_date=trade_date,
                end_date=trade_date,
                adjust=''
            )
            
            if df.empty:
                return None
                
            # 重命名列以匹配我们的代码
            df = df.rename(columns={
                '时间': '时间',
                '开盘': '开盘',
                '收盘': '收盘',
                '最高': '最高',
                '最低': '最低',
                '成交量': '成交量',
                '成交额': '成交额'
            })
            
            # 转换时间列为datetime类型
            df['时间'] = pd.to_datetime(df['时间'], errors='coerce')
            df = df[df['时间'].notna()]
            
            # 只保留指定日期的数据
            target_date = pd.to_datetime(trade_date, format='%Y%m%d')
            df = df[df['时间'].dt.date == target_date.date()]
            
            # 过滤掉 11:30 到 13:00 之间的数据
            df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
            
            if df.empty:
                return None
            
            # 强制校准时间索引
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
            print(f"获取股票数据时出错: {e}")
            return None
    
    def get_prev_close(self, trade_date=None):
        """获取昨收价"""
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
            
        target_date = pd.to_datetime(trade_date, format='%Y%m%d')
        
        try:
            daily_df = ak.stock_zh_a_hist(
                symbol=self.stock_code,
                period="daily",
                adjust=""
            )
            
            if not daily_df.empty:
                daily_df['日期'] = pd.to_datetime(daily_df['日期'])
                df_before = daily_df[daily_df['日期'] < target_date]
                if not df_before.empty:
                    return df_before.iloc[-1]['收盘']
                    
        except Exception as e:
            print(f"获取昨收价时出错: {e}")
            
        return None
    
    def detect_resistance_support_signals(self, df, prev_close):
        """检测阻力支撑指标信号"""
        if df is None or df.empty or prev_close is None:
            return None
            
        try:
            # 使用完整的指标计算函数
            df_with_indicators = calc_resistance_support(df.copy(), prev_close)
            
            signals = {'buy': False, 'sell': False, 'buy_details': '', 'sell_details': ''}
            
            # 检查是否有买入信号（longcross_support）
            if df_with_indicators['longcross_support'].any():
                signals['buy'] = True
                signals['buy_details'] = f"支撑位买入信号触发"
                
            # 检查是否有卖出信号（longcross_resistance）
            if df_with_indicators['longcross_resistance'].any():
                signals['sell'] = True
                signals['sell_details'] = f"阻力位卖出信号触发"
            
            # 保存图表
            self._save_resistance_support_chart(df_with_indicators, prev_close)
            
            return signals
            
        except Exception as e:
            print(f"检测阻力支撑信号时出错: {e}")
            return None

    def _save_resistance_support_chart(self, df, prev_close):
        """保存阻力支撑指标图表"""
        try:
            import os
            from Investment.T0.indicators.resistance_support_indicators import plot_tdx_intraday
            import pandas as pd
            from datetime import datetime
            
            # 调用阻力支撑指标文件中的完整绘图方法
            stock_code = self.stock_code
            trade_date = datetime.now().strftime('%Y%m%d')
            
            # 直接调用绘图方法
            plot_tdx_intraday(stock_code, trade_date)
                               
        except Exception as e:
            print(f"保存阻力支撑指标图表时出错: {e}")

    def detect_extended_signals(self, df, prev_close):
        """检测扩展指标信号"""
        if df is None or df.empty:
            return None
            
        try:
            # 获取日线数据用于扩展指标计算
            try:
                daily_df = ak.stock_zh_a_hist(
                    symbol=self.stock_code,
                    period="daily",
                    adjust=""
                )
            except:
                daily_df = pd.DataFrame()
            
            # 使用完整的指标计算函数
            df_with_indicators = calc_extended(df.copy(), prev_close, daily_df)
            
            signals = {'buy': False, 'sell': False, 'buy_details': '', 'sell_details': ''}
            
            # 检查买入信号（只包含买入相关的信号）
            buy_conditions = (
                df_with_indicators['longcross_support'].any() or 
                df_with_indicators['主力_拉信号'].any() or 
                df_with_indicators['主力_冲信号'].any()
            )
            
            if buy_conditions:
                signals['buy'] = True
                details = []
                # 仅添加买入相关的详情
                if df_with_indicators['longcross_support'].any():
                    details.append("支撑位买入信号")
                if df_with_indicators['主力_拉信号'].any():
                    details.append("主力拉信号")
                if df_with_indicators['主力_冲信号'].any():
                    details.append("主力冲信号")
                signals['buy_details'] = ", ".join(details)
                
            # 检查卖出信号（只包含卖出相关的信号）
            sell_conditions = (
                df_with_indicators['longcross_resistance'].any() or 
                df_with_indicators['压力信号'].any()
            )
            
            if sell_conditions:
                signals['sell'] = True
                details = []
                # 仅添加卖出相关的详情
                if df_with_indicators['longcross_resistance'].any():
                    details.append("阻力位卖出信号")
                if df_with_indicators['压力信号'].any():
                    details.append("压力信号")
                signals['sell_details'] = ", ".join(details)
            
            # 保存图表
            self._save_extended_chart(df_with_indicators, prev_close)
            
            return signals
            
        except Exception as e:
            print(f"检测扩展指标信号时出错: {e}")
            return None

    def _save_extended_chart(self, df, prev_close):
        """保存扩展指标图表"""
        try:
            import os
            from Investment.T0.indicators.extended_indicators import plot_tdx_intraday
            from datetime import datetime
            
            # 调用扩展指标文件中的完整绘图方法
            stock_code = self.stock_code
            trade_date = datetime.now().strftime('%Y%m%d')
            
            # 直接调用绘图方法
            plot_tdx_intraday(stock_code, trade_date)
                               
        except Exception as e:
            print(f"保存扩展指标图表时出错: {e}")
    
    def detect_volume_price_signals(self, df, prev_close):
        """检测量价指标信号"""
        if df is None or df.empty:
            return None
            
        try:
            # 计算支撑阻力位
            df = calculate_support_resistance(df, prev_close)
            
            # 计算资金流向指标
            df = calculate_fund_flow_indicators(df)
            
            # 检测信号
            df = detect_signals(df)
            
            signals = {'buy': False, 'sell': False, 'buy_details': '', 'sell_details': ''}
            
            # 检查买入信号（只包含买入相关的信号）
            buy_conditions = (
                df['买入信号'].any() or 
                df['主力资金流入'].any()
            )
            
            if buy_conditions:
                signals['buy'] = True
                details = []
                # 仅添加买入相关的详情
                if df['买入信号'].any():
                    details.append("量价买入信号")
                if df['主力资金流入'].any():
                    details.append("主力资金流入")
                signals['buy_details'] = ", ".join(details)
                
            # 检查卖出信号（只包含卖出相关的信号）
            if df['卖出信号'].any():
                signals['sell'] = True
                details = []
                # 仅添加卖出相关的详情
                if df['卖出信号'].any():
                    details.append("量价卖出信号")
                signals['sell_details'] = ", ".join(details)
            
            # 保存图表
            self._save_volume_price_chart(df, prev_close)

            return signals
            
        except Exception as e:
            print(f"检测量价指标信号时出错: {e}")
            return None

    def _save_volume_price_chart(self, df, prev_close):
        """保存量价指标图表"""
        try:
            import os
            from Investment.T0.indicators.volume_price_indicators import analyze_volume_price
            from datetime import datetime
            
            # 调用量价指标文件中的完整分析和绘图方法
            stock_code = self.stock_code
            trade_date = datetime.now().strftime('%Y%m%d')
            
            # 直接调用分析方法，它会自动绘图并保存
            analyze_volume_price(stock_code, trade_date)
                               
        except Exception as e:
            print(f"保存量价指标图表时出错: {e}")
    
    def detect_all_signals(self):
        """检测所有指标的信号"""
        # 获取数据
        df = self.get_stock_data()
        if df is None or df.empty:
            return None
            
        prev_close = self.get_prev_close()
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0] if not df['开盘'].dropna().empty else 0
            
        # 检测各指标信号
        resistance_support_signals = self.detect_resistance_support_signals(df, prev_close)
        extended_signals = self.detect_extended_signals(df, prev_close)
        volume_price_signals = self.detect_volume_price_signals(df, prev_close)
        
        # 检查是否有新信号
        new_signals = []
        
        # 阻力支撑信号
        if resistance_support_signals:
            # 检查是否有新的买入信号
            if resistance_support_signals['buy'] and not self.prev_signals['resistance_support']['buy']:
                new_signals.append({
                    'indicator': '阻力支撑',
                    'type': '买入',
                    'details': resistance_support_signals['buy_details']
                })
                log_signal(self.stock_code, '阻力支撑', '买入', resistance_support_signals['buy_details'])
                
            # 检查是否有新的卖出信号
            if resistance_support_signals['sell'] and not self.prev_signals['resistance_support']['sell']:
                new_signals.append({
                    'indicator': '阻力支撑',
                    'type': '卖出',
                    'details': resistance_support_signals['sell_details']
                })
                log_signal(self.stock_code, '阻力支撑', '卖出', resistance_support_signals['sell_details'])
                
            # 更新之前的信号状态
            self.prev_signals['resistance_support']['buy'] = resistance_support_signals['buy']
            self.prev_signals['resistance_support']['sell'] = resistance_support_signals['sell']
        
        # 扩展指标信号
        if extended_signals:
            # 检查是否有新的买入信号
            if extended_signals['buy'] and not self.prev_signals['extended']['buy']:
                new_signals.append({
                    'indicator': '扩展指标',
                    'type': '买入',
                    'details': extended_signals['buy_details']
                })
                log_signal(self.stock_code, '扩展指标', '买入', extended_signals['buy_details'])
                
            # 检查是否有新的卖出信号
            if extended_signals['sell'] and not self.prev_signals['extended']['sell']:
                new_signals.append({
                    'indicator': '扩展指标',
                    'type': '卖出',
                    'details': extended_signals['sell_details']
                })
                log_signal(self.stock_code, '扩展指标', '卖出', extended_signals['sell_details'])
                
            # 更新之前的信号状态
            self.prev_signals['extended']['buy'] = extended_signals['buy']
            self.prev_signals['extended']['sell'] = extended_signals['sell']
        
        # 量价指标信号
        if volume_price_signals:
            # 检查是否有新的买入信号
            if volume_price_signals['buy'] and not self.prev_signals['volume_price']['buy']:
                new_signals.append({
                    'indicator': '量价指标',
                    'type': '买入',
                    'details': volume_price_signals['buy_details']
                })
                log_signal(self.stock_code, '量价指标', '买入', volume_price_signals['buy_details'])
                
            # 检查是否有新的卖出信号
            if volume_price_signals['sell'] and not self.prev_signals['volume_price']['sell']:
                new_signals.append({
                    'indicator': '量价指标',
                    'type': '卖出',
                    'details': volume_price_signals['sell_details']
                })
                log_signal(self.stock_code, '量价指标', '卖出', volume_price_signals['sell_details'])
                
            # 更新之前的信号状态
            self.prev_signals['volume_price']['buy'] = volume_price_signals['buy']
            self.prev_signals['volume_price']['sell'] = volume_price_signals['sell']
        
        return new_signals