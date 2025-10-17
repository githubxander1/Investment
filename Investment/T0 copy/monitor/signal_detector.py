# T0交易系统信号检测模块
import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
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

# 尝试导入tushare
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False
    print("警告: 未安装tushare库，将无法使用tushare数据源")

class SignalDetector:
    """信号检测器"""
    
    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.prev_signals = {
            'resistance_support': {'buy': False, 'sell': False},
            'extended': {'buy': False, 'sell': False},
            'volume_price': {'buy': False, 'sell': False}
        }
        # 如果tushare可用，设置token（如果用户有token的话）
        if TUSHARE_AVAILABLE:
            # 可以在这里设置tushare token，如果用户有的话
            # ts.set_token('your_token_here')
            pass
    
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
            # 添加重试机制
            try:
                print("正在重试获取股票数据...")
                import time
                time.sleep(2)  # 等待2秒后重试
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
            except Exception as retry_e:
                print(f"重试获取股票数据失败: {retry_e}")
            return None
    
    def get_prev_close(self, trade_date=None):
        """获取昨收价"""
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
            
        target_date = pd.to_datetime(trade_date, format='%Y%m%d')
        
        # 尝试多个数据源获取昨收价
        data_sources = [
            # 主要数据源
            lambda: self._get_prev_close_from_akshare_daily(self.stock_code, target_date),
            # 备用数据源1: 从 akshare 实时行情获取
            lambda: self._get_prev_close_from_akshare_spot(self.stock_code),
            # 备用数据源2: 从分时数据获取
            lambda: self._get_prev_close_from_intraday(self.stock_code, target_date),
            # 备用数据源3: 从历史数据获取
            lambda: self._get_prev_close_from_hist(self.stock_code, target_date),
            # 备用数据源4: 从 tushare 获取（如果可用）
            lambda: self._get_prev_close_from_tushare(self.stock_code, target_date) if TUSHARE_AVAILABLE else None,
            # 备用数据源5: 从腾讯接口获取
            lambda: self._get_prev_close_from_tencent(self.stock_code)
        ]
        
        for i, data_source in enumerate(data_sources):
            # 跳过不可用的数据源
            if data_source is None:
                continue
                
            try:
                prev_close = data_source()
                if prev_close is not None:
                    print(f"✅ 成功从数据源 {i+1} 获取昨收价: {prev_close:.2f}")
                    return prev_close
            except Exception as e:
                print(f"数据源 {i+1} 获取昨收价失败: {e}")
                continue
                
        print("❌ 所有数据源均无法获取昨收价")
        return None
    
    def _get_prev_close_from_akshare_daily(self, stock_code, target_date):
        """从akshare日线数据获取昨收价"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                daily_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    adjust=""
                )
                
                if not daily_df.empty:
                    # 检查是否存在日期列
                    if '日期' not in daily_df.columns:
                        print(f"日线数据中缺少'日期'列，列名包括: {list(daily_df.columns)}")
                        return None
                        
                    daily_df['日期'] = pd.to_datetime(daily_df['日期'])
                    df_before = daily_df[daily_df['日期'] < target_date]
                    if not df_before.empty:
                        # 检查是否存在收盘列
                        if '收盘' not in df_before.columns:
                            print(f"日线数据中缺少'收盘'列，列名包括: {list(df_before.columns)}")
                            return None
                        return df_before.iloc[-1]['收盘']
                        
            except KeyError as e:
                if attempt < max_retries - 1:  # 不是最后一次尝试
                    print(f"从日线数据获取昨收价缺少关键列: {e}，正在重试... (第{attempt+1}次)")
                    import time
                    time.sleep(3)  # 等待3秒后重试
                else:
                    print(f"从日线数据获取昨收价缺少关键列，最后一次尝试出错: {e}")
            except Exception as e:
                if attempt < max_retries - 1:  # 不是最后一次尝试
                    print(f"从日线数据获取昨收价出错: {e}，正在重试... (第{attempt+1}次)")
                    import time
                    time.sleep(3)  # 等待3秒后重试
                else:
                    print(f"从日线数据获取昨收价失败，最后一次尝试出错: {e}")
        return None
    
    def _get_prev_close_from_akshare_spot(self, stock_code):
        """从akshare实时行情数据获取昨收价"""
        try:
            # 获取所有股票的实时行情数据
            spot_df = ak.stock_zh_a_spot()
            if not spot_df.empty:
                # 检查是否存在代码列
                if '代码' not in spot_df.columns:
                    print(f"实时行情数据中缺少'代码'列，列名包括: {list(spot_df.columns)}")
                    return None
                    
                # 查找目标股票
                target_stock = spot_df[spot_df['代码'] == stock_code]
                if not target_stock.empty:
                    # 检查是否存在昨收列
                    if '昨收' not in target_stock.columns:
                        print(f"实时行情数据中缺少'昨收'列，列名包括: {list(target_stock.columns)}")
                        return None
                    # 返回昨收价
                    return target_stock.iloc[0]['昨收']
        except KeyError as e:
            print(f"从实时行情数据获取昨收价时缺少关键列: {e}")
        except Exception as e:
            print(f"从实时行情数据获取昨收价失败: {e}")
        return None
    
    def _get_prev_close_from_intraday(self, stock_code, target_date):
        """从分时数据获取昨收价"""
        try:
            # 获取前一天的日期
            prev_date = target_date - timedelta(days=1)
            prev_date_str = prev_date.strftime('%Y%m%d')
            
            # 获取前一天的分时数据
            intraday_df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period="1",
                start_date=prev_date_str,
                end_date=prev_date_str,
                adjust=""
            )
            
            if not intraday_df.empty:
                # 检查是否存在时间列
                time_col = None
                for col in ['时间', 'date', 'datetime', 'timestamp']:
                    if col in intraday_df.columns:
                        time_col = col
                        break
                        
                if time_col is None:
                    print(f"分时数据中缺少时间列，列名包括: {list(intraday_df.columns)}")
                    return None
                    
                # 获取前一天的收盘价
                intraday_df[time_col] = pd.to_datetime(intraday_df[time_col])
                # 过滤掉午休时间的数据
                intraday_df = intraday_df[
                    ~((intraday_df[time_col].dt.hour == 11) & (intraday_df[time_col].dt.minute >= 30)) & 
                    ~(intraday_df[time_col].dt.hour == 12)
                ]
                
                if not intraday_df.empty:
                    # 检查是否存在收盘列
                    if '收盘' not in intraday_df.columns:
                        print(f"分时数据中缺少'收盘'列，列名包括: {list(intraday_df.columns)}")
                        return None
                    # 获取最后一个有效的收盘价作为昨收价
                    return intraday_df['收盘'].iloc[-1]
        except KeyError as e:
            print(f"从分时数据获取昨收价时缺少关键列: {e}")
        except Exception as e:
            print(f"从分时数据获取昨收价失败: {e}")
        return None
    
    def _get_prev_close_from_hist(self, stock_code, target_date):
        """从历史数据获取昨收价"""
        try:
            # 获取最近30天的数据
            hist_df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                adjust=""
            )
            
            if not hist_df.empty:
                # 检查是否存在日期列
                if '日期' not in hist_df.columns:
                    print(f"历史数据中缺少'日期'列，列名包括: {list(hist_df.columns)}")
                    return None
                    
                hist_df['日期'] = pd.to_datetime(hist_df['日期'])
                df_before = hist_df[hist_df['日期'] < target_date]
                if not df_before.empty:
                    return df_before.iloc[-1]['收盘']
        except KeyError as e:
            print(f"从历史数据获取昨收价时缺少关键列: {e}")
        except Exception as e:
            print(f"从历史数据获取昨收价失败: {e}")
        return None
    
    def _get_prev_close_from_tushare(self, stock_code, target_date):
        """从tushare获取昨收价"""
        try:
            # 注意：tushare需要token才能使用，这里假设用户已经设置好了
            # 如果没有token，这个调用会失败
            # ts.set_token('2e9a7a0827b4c655aa6c267dc00484c6e76ab1022b5717092b44573e')

            df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date='20251001', end_date=target_date.strftime('%Y%m%d'))
            if df is not None and not df.empty:
                # 检查是否存在trade_date列
                if 'trade_date' not in df.columns:
                    print(f"tushare数据中缺少'trade_date'列，列名包括: {list(df.columns)}")
                    return None
                    
                df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
                df_before = df[df['trade_date'] < target_date]
                if not df_before.empty:
                    # 检查是否存在close列
                    if 'close' not in df_before.columns:
                        print(f"tushare数据中缺少'close'列，列名包括: {list(df_before.columns)}")
                        return None
                    return df_before.iloc[0]['close']
        except KeyError as e:
            print(f"从tushare获取昨收价时缺少关键列: {e}")
        except Exception as e:
            print(f"从tushare获取昨收价失败: {e}")
        return None
    
    def _get_prev_close_from_tencent(self, stock_code):
        """从腾讯接口获取昨收价"""
        try:
            # 腾讯接口的股票代码格式
            if stock_code.startswith('6'):
                tencent_code = 'sh' + stock_code
            else:
                tencent_code = 'sz' + stock_code
                
            # 使用akshare的腾讯接口
            df = ak.stock_tencent_daily(symbol=tencent_code)
            if not df.empty and len(df) > 1:
                # 检查是否存在close列
                if 'close' not in df.columns:
                    print(f"腾讯接口数据中缺少'close'列，列名包括: {list(df.columns)}")
                    return None
                # 返回前一天的收盘价
                return df.iloc[-2]['close']
        except KeyError as e:
            print(f"从腾讯接口获取昨收价时缺少关键列: {e}")
        except Exception as e:
            print(f"从腾讯接口获取昨收价失败: {e}")
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
                df_with_indicators['longcross_support'].any() if 'longcross_support' in df_with_indicators.columns else False or
                (df_with_indicators['主力_拉信号'].any() if '主力_拉信号' in df_with_indicators.columns else False) or
                (df_with_indicators['主力_冲信号'].any() if '主力_冲信号' in df_with_indicators.columns else False)
            )
            
            if buy_conditions:
                signals['buy'] = True
                details = []
                # 仅添加买入相关的详情
                if 'longcross_support' in df_with_indicators.columns and df_with_indicators['longcross_support'].any():
                    details.append("支撑位买入信号")
                if '主力_拉信号' in df_with_indicators.columns and df_with_indicators['主力_拉信号'].any():
                    details.append("主力拉信号")
                if '主力_冲信号' in df_with_indicators.columns and df_with_indicators['主力_冲信号'].any():
                    details.append("主力冲信号")
                signals['buy_details'] = ", ".join(details)
                
            # 检查卖出信号（只包含卖出相关的信号）
            sell_conditions = (
                (df_with_indicators['longcross_resistance'].any() if 'longcross_resistance' in df_with_indicators.columns else False) or
                (df_with_indicators['压力信号'].any() if '压力信号' in df_with_indicators.columns else False)
            )
            
            if sell_conditions:
                signals['sell'] = True
                details = []
                # 仅添加卖出相关的详情
                if 'longcross_resistance' in df_with_indicators.columns and df_with_indicators['longcross_resistance'].any():
                    details.append("阻力位卖出信号")
                if '压力信号' in df_with_indicators.columns and df_with_indicators['压力信号'].any():
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