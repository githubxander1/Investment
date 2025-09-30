import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
from collections import deque
import requests
import logging

# 配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
STOCKS = ["000001", "600519"]  # 监控的股票/ETF代码
DINGTALK_WEBHOOK = "你的钉钉机器人Webhook"
HISTORY_DAYS = 480  # 480日最高价
CACHE = {}  # 历史最高价缓存

# 初始化分时数据队列（30分钟窗口）
stock_min_data = {code: deque(maxlen=30) for code in STOCKS}
signals = {code: {"buy": False, "sell": False} for code in STOCKS}


def preload_historical_high():
    """每日开盘前预加载480日最高价"""
    for code in STOCKS:
        try:
            df = ak.stock_zh_a_daily(symbol=code, start_date=(
                        datetime.date.today() - datetime.timedelta(days=HISTORY_DAYS)).strftime("%Y%m%d"))
            CACHE[code] = df['high'].max()
            logger.info(f"{code} 480日最高价预加载完成: {CACHE[code]:.2f}")
        except:
            logger.error(f"{code} 历史数据加载失败")


def get_realtime_min_data(code):
    """获取最新1分钟分时数据"""
    try:
        df = ak.stock_zh_a_minute(symbol=code, period="1", adjust="qfq")
        if df.empty:
            return None
        latest = df.iloc[0].to_dict()
        return {
            "time": datetime.datetime.strptime(latest["timestamp"], "%Y-%m-%d %H:%M:%S").time(),
            "open": float(latest["open"]),
            "high": float(latest["high"]),
            "low": float(latest["low"]),
            "close": float(latest["close"]),
            "volume": float(latest["volume"]),
            "amount": float(latest["amount"])
        }
    except Exception as e:
        logger.error(f"{code} 分时数据获取失败: {e}")
        return None


def calculate_day_indicators(data, code):
    """计算日间指标（支撑/阻力/MACD等）"""
    H1 = max(data["open"], data["high"])
    L1 = min(data["open"], data["low"])
    P1 = H1 - L1

    # 支撑阻力位（分时版本）
    resistance = L1 + P1 * 7 / 8
    support = L1 + P1 * 0.5 / 9

    # MACD（12,26,9参数）
    close_series = pd.Series([d["close"] for d in stock_min_data[code]])
    ema12 = close_series.ewm(span=12, adjust=False).mean()
    ema26 = close_series.ewm(span=26, adjust=False).mean()
    dif = ema12.iloc[-1] - ema26.iloc[-1]
    dea = pd.Series(dif).ewm(span=9, adjust=False).mean().iloc[-1]
    macd = 2 * (dif - dea)

    # 量价关系
    volume_price = (data["volume"] / data["close"]) / 3 if data["close"] != 0 else 0
    buy_ratio = 0
    sell_ratio = 0
    if len(stock_min_data[code]) >= 2:
        prev_close = stock_min_data[code][-2]["close"]
        if data["close"] > prev_close:
            buy_ratio = (volume_price / sum([d["volume"] for d in stock_min_data[code]])) * 100
        elif data["close"] < prev_close:
            sell_ratio = (volume_price / sum([d["volume"] for d in stock_min_data[code]])) * 100

    return {
        "support": support,
        "resistance": resistance,
        "macd": macd,
        "buy_ratio": buy_ratio,
        "sell_ratio": sell_ratio,
        "xg": CACHE.get(code, np.nan)  # 480日最高价
    }


def check_signals(indicators, data, code):
    """多指标信号融合判断"""
    buy_signal = False
    sell_signal = False

    # 1. 支撑位买入（分时线下穿支撑）
    if data["close"] < indicators["support"] and not signals[code]["buy"]:
        buy_signal = True

    # 2. 阻力位卖出（分时线上穿阻力）
    if data["close"] > indicators["resistance"] and not signals[code]["sell"]:
        sell_signal = True

    # 3. 突破480日高点
    if not np.isnan(indicators["xg"]) and data["close"] > indicators["xg"]:
        buy_signal = True

    # 4. MACD金叉
    if indicators["macd"] > 0 and len(stock_min_data[code]) >= 2:
        prev_macd = stock_min_data[code][-2].get("macd", 0)
        if indicators["macd"] > prev_macd and prev_macd < 0:
            buy_signal = True

    # 5. 量价买入比例>60%
    if indicators["buy_ratio"] > 60:
        buy_signal = True

    signals[code] = {"buy": buy_signal, "sell": sell_signal}
    return buy_signal, sell_signal


def update_chart(frame):
    """实时分时图表更新"""
    plt.clf()
    for code in STOCKS:
        if not stock_min_data[code]:
            continue

        df = pd.DataFrame(stock_min_data[code])
        time_labels = [d.strftime("%H:%M") for d in df["time"]]

        # 主图：分时线+支撑阻力+480日高点
        plt.subplot(2, 1, 1)
        plt.title(f"{code} 1分钟分时图")
        plt.plot(time_labels, df["close"], label="收盘价", color="blue")
        plt.plot(time_labels, df["support"], label="支撑位", color="magenta", linestyle="--")
        plt.plot(time_labels, df["resistance"], label="阻力位", color="green", linestyle="--")
        if not np.isnan(df["xg"].iloc[-1]):
            plt.plot(time_labels, [df["xg"].iloc[-1]] * len(time_labels), label="480日高点", color="cyan",
                     linestyle=":")

        # 标注买卖信号
        for i, row in df.iterrows():
            if row["buy_signal"]:
                plt.scatter(time_labels[i], row["close"], marker="^", color="red", s=100, label="买入")
            if row["sell_signal"]:
                plt.scatter(time_labels[i], row["close"], marker="v", color="green", s=100, label="卖出")

        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend(loc="upper left", fontsize="small")
        plt.xlabel("时间")
        plt.ylabel("价格")

        # 副图：MACD柱状图
        plt.subplot(2, 1, 2)
        plt.title("MACD指标")
        bars = plt.bar(time_labels, df["macd"], color="red" if df["macd"].iloc[-1] > 0 else "green")
        for bar in bars:
            if bar.get_height() < 0:
                bar.set_color("green")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.xlabel("时间")
        plt.ylabel("MACD值")

    plt.tight_layout()
    plt.pause(0.1)


def monitor_job():
    """核心监控任务"""
    now = datetime.datetime.now()
    current_time = now.time()

    # 检查是否在交易时段
    in_session = any(s[0] <= current_time <= s[1] for s in TRADING_SESSIONS)
    if not in_session:
        logger.info("非交易时段，跳过监控")
        return

    for code in STOCKS:
        # 获取最新1分钟数据
        data = get_realtime_min_data(code)
        if not data:
            continue

        # 计算指标
        indicators = calculate_day_indicators(data, code)
        buy_signal, sell_signal = check_signals(indicators, data, code)

        # 组装完整数据
        full_data = {
            **data,
            **indicators,
            "buy_signal": buy_signal,
            "sell_signal": sell_signal
        }
        stock_min_data[code].append(full_data)

        # 生成表格
        table = pd.DataFrame([full_data]).T.reset_index()
        table.columns = ["指标", "值"]
        logger.info(f"\n{code} 最新分时数据:\n{table.to_string(index=False)}")

        # 触发通知
        if buy_signal or sell_signal:
            msg = f"""【做T信号】{code}
时间：{now.strftime("%H:%M:%S")}
现价：{data["close"]:.2f}
信号：{'买入' if buy_signal else ''} {'卖出' if sell_signal else ''}
支撑：{indicators["support"]:.2f} | 阻力：{indicators["resistance"]:.2f}
MACD：{indicators["macd"]:.4f}"""
            logger.info(msg)
            send_dingtalk_alert(msg)


def send_dingtalk_alert(message):
    """钉钉通知"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {"isAtAll": False}
    }
    try:
        response = requests.post(DINGTALK_WEBHOOK, json=payload, headers=headers, timeout=5)
        if response.status_code != 200:
            logger.error(f"钉钉通知失败：{response.text}")
    except Exception as e:
        logger.error(f"钉钉通知异常：{e}")


if __name__ == "__main__":
    # 每日开盘前预加载历史数据
    preload_historical_high()

    # 启动实时监控（每分钟执行一次）
    schedule.every(1).minutes.do(monitor_job)

    # 启动图表界面
    fig = plt.figure(figsize=(12, 8))
    ani = FuncAnimation(fig, update_chart, interval=1000, cache_frame_data=False)
    logger.info("分时监控系统启动，按Ctrl+C退出")

    try:
        while True:
            schedule.run_pending()
            plt.pause(1)
    except KeyboardInterrupt:
        logger.info("系统停止")
        plt.close()