import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
from datetime import time
import schedule
import requests
import logging
from collections import deque

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 全局变量
STOCKS = ["000001", "600519", "510300"]  # 监控股票代码
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=ad751f38f241c5088b291765818cfe294c2887198b93655e0e20b1605a8cd6a2"
HISTORY_DAYS = 480  # 历史数据天数
DATA_WINDOW = 20  # 图表显示窗口大小

# 初始化数据队列
stock_data = {code: deque(maxlen=DATA_WINDOW) for code in STOCKS}
signals = {code: {"buy": False, "sell": False} for code in STOCKS}


def get_historical_high(stock_code):
    """获取480日最高价"""
    try:
        df = ak.stock_zh_a_daily(symbol=stock_code,
                                 start_date=(datetime.date.today() - datetime.timedelta(days=HISTORY_DAYS)).strftime(
                                     "%Y%m%d"))
        return df['high'].max()
    except Exception as e:
        logger.error(f"获取{stock_code}历史数据失败: {e}")
        return np.nan


def calculate_indicators(data, code):
    """计算所有指标"""
    # 基础数据
    open_price = data['open']
    high_price = data['high']
    low_price = data['low']
    close_price = data['close']
    volume = data['volume']
    amount = data['amount']

    # 1. 支撑阻力位计算
    H1 = max(open_price, high_price)
    L1 = min(open_price, low_price)
    P1 = H1 - L1
    resistance = L1 + P1 * 7 / 8  # 阻力位
    support = L1 + P1 * 0.5 / 9  # 支撑位

    # 2. 480日最高价
    xg = get_historical_high(code)

    # 3. 成交量加权均线
    if volume == 0:
        vwap = close_price
    else:
        vwap = amount / (volume * 100)  # 注意单位转换

    # 4. MACD计算
    ema12 = pd.Series(close_price).ewm(span=12, adjust=False).mean()
    ema26 = pd.Series(close_price).ewm(span=26, adjust=False).mean()
    dif = ema12[-1] - ema26[-1]
    dea = pd.Series(dif).ewm(span=9, adjust=False).mean()[-1]
    macd = 2 * (dif - dea)

    # 5. 量价关系
    volume_price = (volume / close_price) / 3 if close_price != 0 else 0
    a2 = np.where((volume_price > 0.2) & (close_price > data['pre_close']), volume_price, 0).sum()
    a3 = np.where((volume_price > 0.2) & (close_price < data['pre_close']), volume_price, 0).sum()
    a6 = a2 + a3
    buy_ratio = (100 * a2 / a6) if a6 != 0 else 0
    sell_ratio = (100 * a3 / a6) if a6 != 0 else 0

    # 信号判断
    buy_signal = False
    sell_signal = False

    # 支撑位买入信号
    if close_price < support and not signals[code]["buy"]:
        buy_signal = True
    # 阻力位卖出信号
    if close_price > resistance and not signals[code]["sell"]:
        sell_signal = True
    # 突破480日高点
    if close_price > xg and not np.isnan(xg):
        buy_signal = True

    signals[code] = {"buy": buy_signal, "sell": sell_signal}

    return {
        "code": code,
        "close": close_price,
        "support": support,
        "resistance": resistance,
        "xg": xg,
        "vwap": vwap,
        "macd": macd,
        "buy_ratio": buy_ratio,
        "sell_ratio": sell_ratio,
        "buy_signal": buy_signal,
        "sell_signal": sell_signal
    }


def get_realtime_data(stock_code):
    """获取实时行情数据"""
    try:
        df = ak.stock_realtime_quotes(symbol=stock_code)
        if df.empty:
            logger.warning(f"{stock_code}无实时数据")
            return None
        data = df.iloc[0].to_dict()
        data['pre_close'] = float(data['pre_close'])
        data['open'] = float(data['open'])
        data['high'] = float(data['high'])
        data['low'] = float(data['low'])
        data['close'] = float(data['close'])
        data['volume'] = float(data['volume'])
        data['amount'] = float(data['amount'])
        return data
    except Exception as e:
        logger.error(f"{stock_code}获取数据失败: {e}")
        return None


def send_dingtalk_alert(message):
    """发送钉钉通知"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "msgtype": "text",
        "text": {
            "content": f"【股票信号提醒】\n{message}"
        },
        "at": {
            "isAtAll": False
        }
    }
    response = requests.post(DINGTALK_WEBHOOK, json=payload, headers=headers)
    if response.status_code == 200:
        logger.info("钉钉通知发送成功")
    else:
        logger.error("钉钉通知发送失败")


# def update_chart(frame):
#     """更新实时图表"""
#     plt.clf()
#     for code in STOCKS:
#         if not stock_data[code]:
#             continue
#
#         df = pd.DataFrame(stock_data[code])
#
#         # 绘制K线图
#         plt.subplot(2, 1, 1)
#         plt.title(f"{code} 实时行情")
#         plt.grid(True, linestyle='--', alpha=0.7)
#         plt.plot(df['time'], df['close'], label='收盘价', color='blue')
#         plt.plot(df['time'], df['support'], label='支撑位', color='magenta', linestyle='--')
#         plt.plot(df['time'], df['resistance'], label='阻力位', color='green', linestyle='--')
#         plt.plot(df['time'], df['xg'], label='480日高点', color='cyan', linestyle=':')
#         plt.xlabel('时间')
#         plt.ylabel('价格')
#         plt.legend()
#
#         # 标注信号
#         for i, row in df.iterrows():
#             if row['buy_signal']:
#                 plt.scatter(row['time'], row['close'], marker='^', color='red', label='买入信号')
#             if row['sell_signal']:
#                 plt.scatter(row['time'], row['close'], marker='v', color='green', label='卖出信号')
#
#         # 绘制MACD
#         plt.subplot(2, 1, 2)
#         plt.title('MACD指标')
#         plt.bar(df['time'], df['macd'], color='red' if df['macd'].iloc[-1] > 0 else 'green')
#         plt.xlabel('时间')
#         plt.ylabel('MACD值')
#
#     plt.tight_layout()
#     plt.pause(0.1)


def monitor_stock(stock_code):
    """单只股票监控逻辑"""
    data = get_realtime_data(stock_code)
    if not data:
        return

    # 计算所有指标
    indicators = calculate_indicators(data, stock_code)

    # 生成表格数据
    table = pd.DataFrame([indicators]).T.reset_index()
    table.columns = ["指标", "值"]
    logger.info(f"\n{stock_code} 实时数据:\n{table.to_string(index=False)}")

    # 检查信号
    if indicators["buy_signal"] or indicators["sell_signal"]:
        message = f"""股票：{indicators["code"]}({indicators["name"]})
现价：{indicators["close"]:.2f}
信号：{'买入' if indicators["buy_signal"] else ''} {'卖出' if indicators["sell_signal"] else ''}
支撑位：{indicators["support"]:.2f}
阻力位：{indicators["resistance"]:.2f}"""
        logger.info(f"触发信号：{message}")
        send_dingtalk_alert(message)


def job():
    """定时任务"""
    now = datetime.datetime.now()
    if not (
            (now.time() >= time(9, 30) and now.time() <= time(11, 30)) or
            (now.time() >= time(13, 30) and now.time() <= time(14, 50))
    ):
        logger.info("非交易时间段，暂停监控")
        return

    for code in STOCKS:
        monitor_stock(code)


if __name__ == "__main__":
    # 启动定时任务
    schedule.every(2).minutes.do(job)  # 每2分钟执行一次

    # # 启动图表线程
    # fig = plt.figure(figsize=(12, 8))
    # ani = FuncAnimation(fig, update_chart, interval=1000)
    # logger.info("监控系统启动，按Ctrl+C退出")

    # try:
    #     while True:
    #         schedule.run_pending()
    #         plt.pause(1)
    # except KeyboardInterrupt:
    #     logger.info("监控系统停止")
    #     plt.close()