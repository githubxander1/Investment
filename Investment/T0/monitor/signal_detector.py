# T0交易系统信号检测模块
from pprint import pprint

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
# 注释掉其他指标的导入
# from Investment.T0.indicators.extended_indicators import calculate_tdx_indicators as calc_extended
# from Investment.T0.indicators.volume_price_indicators import (calculate_volume_price_indicators,
#                                                calculate_support_resistance,
#                                                calculate_fund_flow_indicators,
#                                                detect_signals)

class SignalDetector:
    """信号检测器"""
    
    def __init__(self, stock_code):
        self.stock_code = stock_code
        # 只保留阻力支撑指标的信号状态
        self.prev_signals = {
            'resistance_support': {'buy': False, 'sell': False},
            # 注释掉其他指标的信号状态
            # 'extended': {'buy': False, 'sell': False},
            # 'volume_price': {'buy': False, 'sell': False},
            # 新增策略信号状态
            'price_ma_deviation': {'buy': False, 'sell': False},
            'volatility': {'buy': False, 'sell': False},
            'momentum_reversal': {'buy': False, 'sell': False}
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

    def get_prev_close(self, stock_code=None, trade_date=None):
        """
        获取股票前收盘价的方法，尝试多种方式
        
        Args:
            stock_code: 股票代码，默认为self.stock_code
            trade_date: 交易日期，默认为当天
            
        Returns:
            float: 前收盘价，如果获取失败则返回None
        """
        if stock_code is None:
            stock_code = self.stock_code
            
        if trade_date is None:
            # 使用当天日期
            from datetime import datetime, timedelta
            # 尝试获取昨天的日期作为前一交易日
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            trade_date = yesterday
            
        try:
            # 方法1：尝试从akshare的daily数据获取前收盘价
            try:
                import akshare as ak
                df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=trade_date,
                    end_date=trade_date,
                    adjust=""
                )
                if not df.empty and '收盘' in df.columns:
                    return df['收盘'].iloc[0]
            except Exception as e:
                print(f"方法1获取前收盘价失败: {e}")
                
            # 方法2：尝试从akshare的实时行情获取前收盘价
            try:
                df = ak.stock_zh_a_spot_em()
                stock_data = df[df['代码'] == stock_code]
                if not stock_data.empty and '昨收' in stock_data.columns:
                    return stock_data['昨收'].iloc[0]
            except Exception as e:
                print(f"方法2获取前收盘价失败: {e}")
                
            # 方法3：尝试从分时数据中推断
            try:
                from datetime import datetime
                df = self.get_stock_data()
                if df is not None and not df.empty and '开盘' in df.columns:
                    # 使用今日开盘价作为备选
                    return df['开盘'].dropna().iloc[0] if not df['开盘'].dropna().empty else None
            except Exception as e:
                print(f"方法3获取前收盘价失败: {e}")
                
        except Exception as e:
            print(f"获取前收盘价时发生异常: {e}")
            
        return None
    
    def detect_all_signals(self):
        """检测所有指标的信号"""
        # 获取数据
        df = self.get_stock_data()
        if df is None or df.empty:
            return None

        # 使用类方法获取前收盘价
        prev_close = self.get_prev_close()
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0] if not df['开盘'].dropna().empty else 0
            
        # 检测各指标信号
        resistance_support_signals = self.detect_resistance_support_signals(df, prev_close)
        # extended_signals = self.detect_extended_signals(df, prev_close)
        # volume_price_signals = self.detect_volume_price_signals(df, prev_close)

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
        
        # 检测新策略信号
        from Investment.T0.core.new_strategy_interface import StrategyFactory
        
        # 价格均线偏离策略
        price_ma_strategy = StrategyFactory.create_strategy('price_ma_deviation')
        if price_ma_strategy:
            result = price_ma_strategy.analyze(self.stock_code)
            if result:
                df_indicators, signals = result
                # 检查买入信号
                if signals['buy_signals'] and not self.prev_signals['price_ma_deviation']['buy']:
                    new_signals.append({
                        'indicator': '价格均线偏离',
                        'type': '买入',
                        'details': f"价格均线偏离策略触发买入信号"
                    })
                    log_signal(self.stock_code, '价格均线偏离', '买入', '价格均线偏离策略触发买入信号')
                    self.prev_signals['price_ma_deviation']['buy'] = True
                elif not signals['buy_signals']:
                    self.prev_signals['price_ma_deviation']['buy'] = False
                
                # 检查卖出信号
                if signals['sell_signals'] and not self.prev_signals['price_ma_deviation']['sell']:
                    new_signals.append({
                        'indicator': '价格均线偏离',
                        'type': '卖出',
                        'details': f"价格均线偏离策略触发卖出信号"
                    })
                    log_signal(self.stock_code, '价格均线偏离', '卖出', '价格均线偏离策略触发卖出信号')
                    self.prev_signals['price_ma_deviation']['sell'] = True
                elif not signals['sell_signals']:
                    self.prev_signals['price_ma_deviation']['sell'] = False
        
        # 波动率策略
        volatility_strategy = StrategyFactory.create_strategy('volatility')
        if volatility_strategy:
            result = volatility_strategy.analyze(self.stock_code)
            if result:
                df_indicators, signals = result
                # 检查买入信号
                if signals['buy_signals'] and not self.prev_signals['volatility']['buy']:
                    new_signals.append({
                        'indicator': '波动率',
                        'type': '买入',
                        'details': f"波动率策略触发买入信号"
                    })
                    log_signal(self.stock_code, '波动率', '买入', '波动率策略触发买入信号')
                    self.prev_signals['volatility']['buy'] = True
                elif not signals['buy_signals']:
                    self.prev_signals['volatility']['buy'] = False
                
                # 检查卖出信号
                if signals['sell_signals'] and not self.prev_signals['volatility']['sell']:
                    new_signals.append({
                        'indicator': '波动率',
                        'type': '卖出',
                        'details': f"波动率策略触发卖出信号"
                    })
                    log_signal(self.stock_code, '波动率', '卖出', '波动率策略触发卖出信号')
                    self.prev_signals['volatility']['sell'] = True
                elif not signals['sell_signals']:
                    self.prev_signals['volatility']['sell'] = False
        
        # 动量反转策略
        momentum_strategy = StrategyFactory.create_strategy('momentum_reversal')
        if momentum_strategy:
            result = momentum_strategy.analyze(self.stock_code)
            if result:
                df_indicators, signals = result
                # 检查买入信号
                if signals['buy_signals'] and not self.prev_signals['momentum_reversal']['buy']:
                    new_signals.append({
                        'indicator': '动量反转',
                        'type': '买入',
                        'details': f"动量反转策略触发买入信号"
                    })
                    log_signal(self.stock_code, '动量反转', '买入', '动量反转策略触发买入信号')
                    self.prev_signals['momentum_reversal']['buy'] = True
                elif not signals['buy_signals']:
                    self.prev_signals['momentum_reversal']['buy'] = False
                
                # 检查卖出信号
                if signals['sell_signals'] and not self.prev_signals['momentum_reversal']['sell']:
                    new_signals.append({
                        'indicator': '动量反转',
                        'type': '卖出',
                        'details': f"动量反转策略触发卖出信号"
                    })
                    log_signal(self.stock_code, '动量反转', '卖出', '动量反转策略触发卖出信号')
                    self.prev_signals['momentum_reversal']['sell'] = True
                elif not signals['sell_signals']:
                    self.prev_signals['momentum_reversal']['sell'] = False
        
        return new_signals

if __name__ == '__main__':
    stock_code = '000333'
    # 日期换成这种格式"1979-09-01 09:32:00"
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    print(yesterday)
    sd = SignalDetector(stock_code)

    #东方财富-分时
    # prev_date_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    # prev_date_str = prev_date_str + " 15:00:00"
    # intraday_df = ak.stock_zh_a_hist_min_em(
    #     symbol=stock_code,
    #     period="1",
    #     start_date=prev_date_str,
    #     end_date=prev_date_str,
    #     adjust=""
    # )
    # pprint(intraday_df)

    target_date = yesterday
    # daily_df = ak.stock_zh_a_hist(
    #     symbol=stock_code,
    #     period="daily",
    #     start_date=target_date,
    #     end_date=target_date,
    #     adjust=""
    # )
    # print(daily_df)
    print(sd._get_prev_close_from_akshare_daily(stock_code, yesterday))
    # print(sd._get_prev_close_from_akshare_spot(stock_code))
    # print(sd._get_prev_close_from_intraday(stock_code, f'{yesterday} 09:32:00'))
    print(sd._get_prev_close_from_intraday(stock_code))
    # hist_df = ak.stock_zh_a_hist(
    #     symbol=stock_code,
    #     period="daily",
    #     start_date=target_date,
    #     end_date=target_date,
    #     adjust=""
    # )
    # print(hist_df)
    print(sd._get_prev_close_from_hist(stock_code, target_date))