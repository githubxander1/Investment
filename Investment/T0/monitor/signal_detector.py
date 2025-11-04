# T0交易系统信号检测模块
from pprint import pprint

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Investment.T0.utils.logger import log_signal
# 只导入综合T+0策略，移除其他指标
from Investment.T0.indicators.comprehensive_t0_strategy import analyze_comprehensive_t0

class SignalDetector:
    """信号检测器"""

    def __init__(self, stock_code):
        self.stock_code = stock_code
        # 只保留综合T+0策略的信号状态
        self.prev_signals = {
            'comprehensive_t0': {'buy': False, 'sell': False, 'has_open_position': False}
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
            # 尝试从缓存获取数据
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_dir = os.path.join(project_root, 'cache', 'fenshi_data')
            cache_file = os.path.join(cache_dir, f'{self.stock_code}_{trade_date}_fenshi.csv')

            # 如果找不到，也尝试在T0_Optimized项目的缓存目录查找
            if not os.path.exists(cache_file):
                optimized_cache_dir = os.path.join(os.path.dirname(project_root), 'T0_Optimized', 'cache', 'fenshi_data')
                cache_file = os.path.join(optimized_cache_dir, f'{self.stock_code}_{trade_date}_fenshi.csv')

            if os.path.exists(cache_file):
                df = pd.read_csv(cache_file)
                print(f"从缓存文件 {cache_file} 读取股票数据")
            else:
                # 生成模拟数据
                print(f"未找到缓存数据，生成模拟数据 for {self.stock_code}")
                # 创建时间序列（模拟交易日的分时数据）
                times = []
                for hour in [9, 10, 11, 13, 14]:
                    start_min = 30 if hour == 9 else 0
                    end_min = 31 if hour == 11 else 60
                    for minute in range(start_min, end_min):
                        if (hour == 11 and minute > 30) or (hour > 14):
                            break
                        times.append(f"{hour:02d}:{minute:02d}:00")

                # 生成模拟价格数据
                base_price = np.random.uniform(10, 100)
                price_changes = np.random.normal(0, 0.01, len(times))
                prices = base_price * np.exp(np.cumsum(price_changes))

                # 创建DataFrame
                df = pd.DataFrame({
                    '时间': times,
                    '开盘': prices,
                    '最高': prices * (1 + np.random.uniform(0, 0.02, len(times))),
                    '最低': prices * (1 - np.random.uniform(0, 0.02, len(times))),
                    '收盘': prices,
                    '成交量': np.random.randint(1000, 100000, len(times))
                })

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

                # 重试时再次尝试从缓存获取
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                cache_dir = os.path.join(project_root, 'cache', 'fenshi_data')
                cache_file = os.path.join(cache_dir, f'{self.stock_code}_{trade_date}_fenshi.csv')

                # 如果找不到，也尝试在T0_Optimized项目的缓存目录查找
                if not os.path.exists(cache_file):
                    optimized_cache_dir = os.path.join(os.path.dirname(project_root), 'T0_Optimized', 'cache', 'fenshi_data')
                    cache_file = os.path.join(optimized_cache_dir, f'{self.stock_code}_{trade_date}_fenshi.csv')

                if os.path.exists(cache_file):
                    df = pd.read_csv(cache_file)
                    print(f"重试时从缓存文件 {cache_file} 读取股票数据")
                else:
                    # 再次生成模拟数据
                    print(f"重试时未找到缓存数据，重新生成模拟数据 for {self.stock_code}")
                    # 创建时间序列（模拟交易日的分时数据）
                    times = []
                    for hour in [9, 10, 11, 13, 14]:
                        start_min = 30 if hour == 9 else 0
                        end_min = 31 if hour == 11 else 60
                        for minute in range(start_min, end_min):
                            if (hour == 11 and minute > 30) or (hour > 14):
                                break
                            times.append(f"{hour:02d}:{minute:02d}:00")

                    # 生成模拟价格数据
                    base_price = np.random.uniform(10, 100)
                    price_changes = np.random.normal(0, 0.01, len(times))
                    prices = base_price * np.exp(np.cumsum(price_changes))

                    # 创建DataFrame
                    df = pd.DataFrame({
                        '时间': times,
                        '开盘': prices,
                        '最高': prices * (1 + np.random.uniform(0, 0.02, len(times))),
                        '最低': prices * (1 - np.random.uniform(0, 0.02, len(times))),
                        '收盘': prices,
                        '成交量': np.random.randint(1000, 100000, len(times))
                    })


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

    def get_prev_close(self, stock_code=None, trade_date=None):
        """
        获取股票前收盘价的方法，使用缓存或模拟数据

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
            # 尝试从缓存获取前收盘价
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            prev_close_cache = os.path.join(project_root, 'cache', 'prev_close')
            cache_file = os.path.join(prev_close_cache, f'{stock_code}_{trade_date}.txt')

            # 如果找不到，也尝试在T0_Optimized项目的缓存目录查找
            if not os.path.exists(cache_file):
                optimized_cache_dir = os.path.join(os.path.dirname(project_root), 'T0_Optimized', 'cache', 'prev_close')
                cache_file = os.path.join(optimized_cache_dir, f'{stock_code}_{trade_date}.txt')

            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    prev_close = float(f.read().strip())
                print(f"从缓存文件 {cache_file} 读取前收盘价")
                return prev_close

            # 方法2：尝试从股票列表中获取
            try:
                # 这里不再使用akshare获取实时行情，而是生成模拟数据
                print(f"未找到缓存数据，生成模拟前收盘价 for {stock_code}")
                # 生成合理范围内的模拟前收盘价
                import random
                prev_close = round(random.uniform(5, 150), 2)  # 生成5-150之间的随机价格
                return prev_close
            # adjust=""
            # )
            # if not df.empty and '收盘' in df.columns:
            #         return df['收盘'].iloc[0]
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

    def detect_comprehensive_t0_signals(self):
        """检测综合T+0策略信号"""
        try:
            # 获取是否有未完成的T操作
            has_open_position = self.prev_signals['comprehensive_t0']['has_open_position']

            # 执行综合T+0策略分析
            result = analyze_comprehensive_t0(
                self.stock_code,
                trade_date=None,  # 使用默认日期（今天）
                has_open_position=has_open_position
            )

            if result is None:
                return None

            df, trades = result

            # 获取最新的信号
            latest_buy_signal = df['Buy_Signal'].iloc[-1] if len(df) > 0 else False
            latest_sell_signal = df['Sell_Signal'].iloc[-1] if len(df) > 0 else False

            # 更新持仓状态
            if latest_buy_signal and not has_open_position:
                # 买入信号且当前无持仓，设置为有持仓
                self.prev_signals['comprehensive_t0']['has_open_position'] = True
            elif latest_sell_signal and has_open_position:
                # 卖出信号且当前有持仓，设置为无持仓
                self.prev_signals['comprehensive_t0']['has_open_position'] = False

            return {
                'buy': latest_buy_signal,
                'sell': latest_sell_signal,
                'has_open_position': self.prev_signals['comprehensive_t0']['has_open_position'],
                'buy_details': f"综合T+0策略买入信号，买入评分: {df['buy_score'].iloc[-1]:.1f}" if latest_buy_signal else '',
                'sell_details': f"综合T+0策略卖出信号，卖出评分: {df['sell_score'].iloc[-1]:.1f}" if latest_sell_signal else ''
            }

        except Exception as e:
            print(f"检测综合T+0策略信号时出错: {e}")
            return None

    def detect_all_signals(self):
        """检测所有指标的信号"""
        # 检测综合T+0策略信号（现在是唯一的指标）
        comprehensive_t0_signals = self.detect_comprehensive_t0_signals()

        # 检查是否有新信号
        new_signals = []

        # 综合T+0策略信号
        if comprehensive_t0_signals:
            # 检查是否有新的买入信号
            if comprehensive_t0_signals['buy'] and not self.prev_signals['comprehensive_t0']['buy']:
                new_signals.append({
                    'indicator': '综合T+0',
                    'type': '买入',
                    'details': comprehensive_t0_signals['buy_details']
                })
                log_signal(self.stock_code, '综合T+0', '买入', comprehensive_t0_signals['buy_details'])

            # 检查是否有新的卖出信号
            if comprehensive_t0_signals['sell'] and not self.prev_signals['comprehensive_t0']['sell']:
                new_signals.append({
                    'indicator': '综合T+0',
                    'type': '卖出',
                    'details': comprehensive_t0_signals['sell_details']
                })
                log_signal(self.stock_code, '综合T+0', '卖出', comprehensive_t0_signals['sell_details'])

            # 更新之前的信号状态
            self.prev_signals['comprehensive_t0']['buy'] = comprehensive_t0_signals['buy']
            self.prev_signals['comprehensive_t0']['sell'] = comprehensive_t0_signals['sell']

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