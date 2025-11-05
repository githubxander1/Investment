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

    # def is_trading_time(self):
    #     """判断是否为交易时间"""
    #     now = datetime.now().time()
    #     # 交易时间段：9:30-11:30 和 13:00-15:00
    #     morning_session = time(9, 30) <= now <= time(11, 30)
    #     afternoon_session = time(13, 0) <= now <= time(15, 0)
    #     return morning_session or afternoon_session

    def is_market_closed(self):
        """判断是否已收盘"""
        now = datetime.now().time()
        return now > time(15, 0)


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