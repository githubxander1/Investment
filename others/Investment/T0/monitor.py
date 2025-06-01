from pprint import pprint

import akshare as ak
import os
import logging
from datetime import datetime, time as tm
from apscheduler.schedulers.blocking import BlockingScheduler
from plyer import notification
import pandas as pd
import requests
import json

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载 indicator 模块（根据你的路径调整）
from others.Investment.T0.real1 import indicator1
from others.Investment.T0.real2 import indicator2
from real3 import indicator3


class StockMonitor:
    def __init__(self):
        self.config = {
            "dingtalk_webhook": "https://oapi.dingtalk.com/robot/send?access_token=ad751f38f241c5088b291765818cfe294c2887198b93655e0e20b1605a8cd6a2",
            "stocks": ["159920", "513130", "600900"],
            "monitor_interval": 60,
            "cache_dir": "cache"
        }

        # 初始化缓存目录
        if not os.path.exists(self.config['cache_dir']):
            os.makedirs(self.config["cache_dir"])

        # 初始化缓存结构
        self.price_cache = {}
        self.load_cache_from_csv()

        # 初始化钉钉 Webhook
        self.dingtalk_webhook = self.config['dingtalk_webhook']

        # 存储信号状态
        self.last_signals = {stock: {'buy': False, 'sell': False} for stock in self.config['stocks']}

        logger.info("股票监控系统已初始化")

    def load_cache_from_csv(self):
        """从CSV加载已有缓存"""
        for stock_code in self.config['stocks']:
            cache_file = os.path.join(self.config['cache_dir'], f"{stock_code}.csv")
            if os.path.exists(cache_file):
                df = pd.read_csv(cache_file)
                self.price_cache[stock_code] = df.to_dict(orient='records')
            else:
                self.price_cache[stock_code] = []

    def save_cache_to_csv(self, stock_code):
        """将缓存保存到CSV文件"""
        cache_file = os.path.join(self.config['cache_dir'], f"{stock_code}.csv")
        if stock_code in self.price_cache and self.price_cache[stock_code]:
            df = pd.DataFrame(self.price_cache[stock_code])
            df.to_csv(cache_file, index=False)

    def append_to_cache(self, stock_code, data):
        """向缓存中追加一条记录"""
        self.price_cache.setdefault(stock_code, []).append(data)
        # 控制缓存大小，保留最近 5 条
        while len(self.price_cache[stock_code]) > 5:
            self.price_cache[stock_code].pop(0)
        self.save_cache_to_csv(stock_code)

    def is_trading_time(self):
        """判断当前是否为交易日的交易时间"""
        now = datetime.now()
        weekday = now.weekday()

        # 判断是否为周末
        if weekday >= 5:
            return False

        # 判断是否为交易时间段
        current_time = now.time()
        morning_start = tm(9, 30)
        morning_end = tm(11, 30)
        afternoon_start = tm(13, 0)
        afternoon_end = tm(15, 0)

        return (morning_start <= current_time <= morning_end) or (afternoon_start <= current_time <= afternoon_end)

    def get_realtime_data(self, stock_code):
        """
        使用 akshare 获取沪深 A 股实时行情
        :param stock_code: 不带市场前缀的股票代码，如 "000001"
        :return: dict 包含最新行情信息
        """
        try:
            df = ak.stock_zh_a_spot_em()
            df = df[df['代码'] == stock_code]
            if df.empty:
                logger.warning(f"无法获取股票 {stock_code} 的实时行情")
                return None

            latest = df.iloc[0].to_dict()
            return {
                'code': latest['代码'],
                'name': latest['名称'],
                'open': float(latest['今开']),
                'high': float(latest['最高']),
                'low': float(latest['最低']),
                'close': float(latest['最新价']),
                'pre_close': float(latest['昨收']),
                'volume': int(latest['成交量']),
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.error(f"获取股票 {stock_code} 实时行情失败: {e}")
            return None

    def get_pre_close_price(self, stock_code):
        """
        使用 akshare 获取指定股票的前一日收盘价
        :param stock_code: 不带市场前缀的股票代码，如 "000001"
        :return: 前一日收盘价 (float)
        """
        try:
            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="")
            if df.empty:
                logger.warning(f"无法获取股票 {stock_code} 的历史行情数据")
                return None

            if len(df) >= 2:
                pre_close = df.iloc[-2]['收盘']
                return float(pre_close)
            else:
                logger.warning(f"股票 {stock_code} 历史数据不足两天")
                return None
        except Exception as e:
            logger.error(f"获取股票 {stock_code} 前一日收盘价失败: {e}")
            return None

    def get_stock_data(self, stock_code):
        """获取股票分时行情"""
        try:
            df = ak.stock_zh_a_tick_tx_js(symbol=stock_code)
            pprint(df)
            if df.empty:
                logger.warning(f"无法获取股票 {stock_code} 的分时数据")
                return None

            latest = df.iloc[-1]
            time_str = latest['成交时间']

            return {
                'code': stock_code,
                'open': float(df.iloc[0]['成交价格']),
                'high': df['成交价格'].max(),
                'low': df['成交价格'].min(),
                'close': float(latest['成交价格']),
                'pre_close': self.get_pre_close_price(stock_code),
                'time': time_str,
                'volume': int(latest['成交量'])
            }

        except Exception as e:
            logger.error(f"获取股票 {stock_code} 数据失败: {e}")
            return None

    def calculate_indicators(self, records):
        close = pd.Series([r['close'] for r in records])
        high = pd.Series([r['high'] for r in records])
        low = pd.Series([r['low'] for r in records])
        volume = pd.Series([r['volume'] for r in records])

        ind1 = indicator1(close, volume, high, low)
        ind2 = indicator2(close, volume, high, low, close.index)
        ind3 = indicator3(close, high, low)

        buy_count = sum([
            bool(ind1['buy_signal'].iloc[-1]),
            bool(ind2['buy_signal'].iloc[-1]),
            bool(ind3['buy_signal'].iloc[-1]),
        ])

        sell_count = sum([
            bool(ind1['sell_signal'].iloc[-1]),
            bool(ind2['sell_signal'].iloc[-1]),
            bool(ind3['sell_signal'].iloc[-1]),
        ])

        return {
            'resistance': (ind1['resistance'] + ind2['resistance'] + ind3['resistance']) / 3,
            'support': (ind1['support'] + ind2['support'] + ind3['support']) / 3,
            'current_price': records[-1]['close'],
            'buy_signal': buy_count >= 2,
            'sell_signal': sell_count >= 2,
        }

    def send_notification(self, message):
        """发送系统通知"""
        try:
            notification.notify(
                title="股票监控提醒",
                message=message,
                app_name="Stock Monitor",
                timeout=10
            )
            logger.info("系统通知发送成功")
        except Exception as e:
            logger.error(f"系统通知发送失败: {e}")

    def send_dingtalk(self, message):
        """发送钉钉消息"""
        try:
            headers = {'Content-Type': 'application/json'}
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"【股票监控提醒】\n{message}"
                }
            }

            response = requests.post(self.dingtalk_webhook, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            logger.info("钉钉消息发送成功")
        except Exception as e:
            logger.error(f"钉钉消息发送失败: {e}")

    def send_signal_notification(self, stock_code, message, is_buy):
        key = 'buy' if is_buy else 'sell'
        if self.last_signals[stock_code][key]:
            return
        self.last_signals[stock_code][key] = True
        self.send_notification(message)
        self.send_dingtalk(message)

    def monitor_stock(self, stock_code):
        logger.info(f"正在监控股票: {stock_code}")

        stock_data = self.get_realtime_data(stock_code)
        if not stock_data:
            return

        # 加入缓存
        self.append_to_cache(stock_code, stock_data)

        # 构造指标序列
        records = self.price_cache[stock_code]
        if len(records) < 3:
            return

        # 提取指标数据
        indicators = self.calculate_indicators(records)

        # 判断是否触发信号
        if indicators['buy_signal']:
            msg = f"{stock_code} 触发【买入信号】：支撑位 {indicators['support']:.2f}"
            self.send_signal_notification(stock_code, msg, is_buy=True)

        if indicators['sell_signal']:
            msg = f"{stock_code} 触发【卖出信号】：阻力位 {indicators['resistance']:.2f}"
            self.send_signal_notification(stock_code, msg, is_buy=False)

    def start_monitoring(self):
        """开始监控所有股票"""
        logger.info("启动股票监控系统...")

        scheduler = BlockingScheduler()

        # 添加监控任务
        for stock_code in self.config['stocks']:
            logger.info(f"首次获取股票 {stock_code} 数据用于初始化缓存")
            stock_data = self.get_realtime_data(stock_code)
            if stock_data:
                self.append_to_cache(stock_code, stock_data)

            scheduler.add_job(
                func=lambda code=stock_code: self.monitor_stock(code),
                trigger='interval',
                seconds=self.config['monitor_interval'],
                name=f"monitor_{stock_code}"
            )

        logger.info(f"已设置 {len(self.config['stocks'])} 只股票的监控任务")

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("股票监控系统已停止")


if __name__ == "__main__":
    monitor = StockMonitor()
    stock_code = "000001"

    # 测试实时行情
    # data = monitor.get_realtime_data(stock_code)
    # print("实时行情:", data)

    # 测试前一日收盘价
    pre_close = monitor.get_pre_close_price(stock_code)
    print("前一日收盘价:", pre_close)

    # 启动监控
    monitor.start_monitoring()
