# -*- coding: utf-8 -*-
# 功能：抓取东方财富网分时数据，用pandas转为DataFrame（便于数据分析）
import random
from pprint import pprint

import requests
import pandas as pd
from urllib.error import URLError, HTTPError


def fetch_free_proxies():
    """从免费网站获取代理"""
    import requests
    from bs4 import BeautifulSoup

    proxies = []
    try:
        # 示例：从free-proxy-list.net获取
        url = "https://free-proxy-list.net/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 解析代理列表
        rows = soup.select("#table-responsive fpl-list > tbody > tr")
        rows = [row for row in rows if row.find('td', class_='hx')]
        for row in rows[:20]:  # 取前20个
            cells = row.find_all('td')
            if cells[4].text == 'elite proxy' and cells[6].text == 'yes':
                ip = cells[0].text
                port = cells[1].text
                proxies.append(f"http://{ip}:{port}")

    except Exception as e:
        print(f"获取代理失败: {e}")

    return proxies

def validate_proxy(proxy_url, test_url="http://httpbin.org/ip", timeout=5):
    """验证代理是否可用并返回响应时间"""
    try:
        proxies = {'http': proxy_url, 'https': proxy_url}
        start_time = time.time()
        response = requests.get(test_url, proxies=proxies, timeout=timeout)
        response_time = time.time() - start_time

        if response.status_code == 200:
            # 更新代理评分
            conn = sqlite3.connect('../proxy_pool.db')
            c = conn.cursor()
            c.execute('''UPDATE proxies SET 
                        success_count = success_count + 1,
                        response_time = ?,
                        last_used = ?,
                        score = score + 0.1
                        WHERE address = ?''',
                     (response_time, time.time(), proxy_url.replace('http://', '')))
            conn.commit()
            conn.close()
            return True, response_time
    except Exception as e:
        # 记录失败
        conn = sqlite3.connect('../proxy_pool.db')
        c = conn.cursor()
        c.execute('''UPDATE proxies SET 
                    fail_count = fail_count + 1,
                    score = score - 0.2
                    WHERE address = ?''',
                 (proxy_url.replace('http://', ''),))
        conn.commit()
        conn.close()

    return False, None

import sqlite3
from datetime import datetime
import time
import redis

class DistributedProxyPool:
    """分布式代理池管理"""
    def __init__(self, redis_host='localhost', redis_port=6379, refresh_interval=3600):
        self.redis = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.proxy_key = "proxy_pool:valid_proxies"
        self.refresh_interval = refresh_interval
        self.last_refresh = 0
        self._setup_refresh_task()

    def _setup_refresh_task(self):
        """设置定时刷新任务"""
        import threading
        def refresh_task():
            while True:
                self.check_refresh()
                time.sleep(self.refresh_interval)

        thread = threading.Thread(target=refresh_task, daemon=True)
        thread.start()

    def check_refresh(self):
        """检查是否需要刷新代理池"""
        if time.time() - self.last_refresh > self.refresh_interval:
            logger.info("正在自动刷新代理池...")
            self.last_refresh = time.time()
            try:
                new_proxies = fetch_free_proxies()
                for proxy in new_proxies:
                    self.add_proxy(proxy)
                logger.info(f"成功刷新代理池，新增代理: {len(new_proxies)}个")
            except Exception as e:
                logger.error(f"刷新代理池失败: {str(e)}")

    def add_proxy(self, proxy):
        """添加代理到池"""
        self.redis.zadd(self.proxy_key, {proxy: time.time()})

    def get_proxy(self):
        """获取最佳代理"""
        proxies = self.redis.zrevrange(self.proxy_key, 0, 20)
        return random.choice(proxies) if proxies else None

    def report_proxy_status(self, proxy, success):
        """报告代理使用状态"""
        if success:
            self.redis.zincrby(self.proxy_key, 1, proxy)
        else:
            self.redis.zincrby(self.proxy_key, -2, proxy)

class RequestThrottler:
    """智能请求频率控制器"""
    def __init__(self, min_delay=1.0, max_delay=5.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = 0
        self.error_count = 0

    def wait(self):
        """根据历史请求情况智能延迟"""
        base_delay = random.uniform(self.min_delay, self.max_delay)
        # 根据错误次数增加延迟
        penalty = min(10, self.error_count * 0.5)
        actual_delay = base_delay + penalty

        elapsed = time.time() - self.last_request_time
        if elapsed < actual_delay:
            time.sleep(actual_delay - elapsed)

        self.last_request_time = time.time()

    def record_error(self):
        """记录请求错误"""
        self.error_count += 1

    def record_success(self):
        """记录请求成功"""
        self.error_count = max(0, self.error_count - 1)

def init_proxy_db():
    """初始化代理数据库"""
    conn = sqlite3.connect('../proxy_pool.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS proxies
                 (address TEXT PRIMARY KEY,
                  https INTEGER,
                  last_used REAL,
                  success_count INTEGER,
                  fail_count INTEGER,
                  response_time REAL,
                  score REAL)''')
    conn.commit()
    conn.close()

def get_proxies():
    """获取并验证代理池"""
    init_proxy_db()
    proxy_list = fetch_free_proxies()
    valid_proxies = []

    # 多线程验证代理
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(
            lambda p: (p, validate_proxy(p)),
            proxy_list
        )
        for proxy, is_valid in results:
            if is_valid:
                valid_proxies.append({'http': proxy, 'https': proxy})
                # 存入数据库
                conn = sqlite3.connect('../proxy_pool.db')
                c = conn.cursor()
                c.execute('''INSERT OR IGNORE INTO proxies 
                            (address, https, last_used, success_count, fail_count, response_time, score)
                            VALUES (?, 1, 0, 0, 0, 0, 5.0)''',
                         (proxy.replace('http://', ''),))
                conn.commit()
                conn.close()

    # 从数据库获取评分最高的代理
    conn = sqlite3.connect('../proxy_pool.db')
    c = conn.cursor()
    c.execute('''SELECT address FROM proxies 
                WHERE https=1 
                ORDER BY score DESC, response_time ASC
                LIMIT 20''')
    db_proxies = [{'http': f"http://{row[0]}", 'https': f"http://{row[0]}"}
                 for row in c.fetchall()]
    conn.close()

    print(f"可用代理数: {len(db_proxies)}")
    return db_proxies if db_proxies else [
        {'http': None, 'https': None}  # 无代理时返回空
    ]

def send_alert(message, level="warning"):
    """发送报警通知（支持邮件和Webhook）"""
    try:
        # 邮件报警
        try:
            import smtplib
            from email.mime.text import MIMEText

            smtp_server = "smtp.example.com"
            smtp_port = 587
            sender = "alerts@example.com"
            receiver = "admin@example.com"
            password = "your_password"

            msg = MIMEText(f"[{level.upper()}] 数据采集报警\n\n{message}")
            msg['Subject'] = f"[{level.upper()}] 数据采集异常"
            msg['From'] = sender
            msg['To'] = receiver

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
        except:
            pass

        # 钉钉Webhook
        try:
            import requests
            import json

            dingtalk_webhook = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"[{level.upper()}] 数据采集报警\n{message}"
                }
            }
            requests.post(dingtalk_webhook, json=data, timeout=5)
        except:
            pass

        # 企业微信Webhook
        try:
            import requests
            import json

            wechat_webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"[{level.upper()}] 数据采集报警\n{message}"
                }
            }
            requests.post(wechat_webhook, json=data, timeout=5)
        except:
            pass

    except Exception as e:
        print(f"发送报警失败: {e}")

import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """配置日志记录器"""
    logger = logging.getLogger('stock_data')
    logger.setLevel(logging.INFO)

    # 文件日志（最大10MB，保留3个备份）
    file_handler = RotatingFileHandler(
        '../stock_data.log',
        maxBytes=10*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))

    # 控制台日志
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()

def get_eastmoney_fenshi_with_pandas(secid="1.688103", use_proxy=False, max_retries=3, enable_alert=True):
    """
    抓取分时数据并转为DataFrame
    :param secid: 股票标识（格式：市场.股票代码，1=沪市，0=深市，如1.688103、0.300059）
    :param use_proxy: 是否使用代理
    :param max_retries: 最大重试次数
    :param enable_alert: 是否启用报警
    :return: 分时数据DataFrame（无数据则返回空DataFrame）
    """
    # 1. 构造请求URL（参数含义：fields1=基础字段，fields2=分时字段，mpi=最大数据量）
    url = (
        f'http://16.push2.eastmoney.com/api/qt/stock/details/sse'
        f'?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55'  # f51=时间，f52=价格等（需参考接口文档)
        f'&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281'  # mpi=最大返回2000条数据
        f'&fltt=2&pos=-0&secid={secid}'  # secid=目标股票标识
    )

    # 2. 发送请求并读取响应
    for attempt in range(max_retries):
        try:
            import random
            import time

            # 反爬措施
            headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]),
            'Referer': 'http://quote.eastmoney.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
        }

            # 随机延迟1-3秒
            time.sleep(random.uniform(1, 3))

            req = requests.get(url, headers=headers)

            if use_proxy:
                proxies = get_proxies()
                proxy = random.choice(proxies)
                proxy_handler = requests.ProxyHandler(proxy)
                opener = requests.build_opener(proxy_handler)
                response = opener.open(req, timeout=10)
            else:
                response = requests.urlopen(req, timeout=10)

            with response as res:
                # 响应格式为 "data:{...}"，需去除前缀"data:"
                data_str = response.readline().decode('utf-8').lstrip('data:')
                if not data_str:
                    print("响应为空，未获取到数据")
                    return pd.DataFrame()

                try:
                    import json
                    # 确保去除前缀"data:"后的字符串是完整JSON
                    if not data_str.startswith('{'):
                        data_str = data_str[data_str.find('{'):]

                    data_dict = json.loads(data_str)
                    print(f"原始数据预览: {data_str[:200]}...")  # 打印部分原始数据用于调试

                    # 获取分时数据路径
                    if 'data' not in data_dict:
                        print("响应中缺少data字段")
                        return pd.DataFrame()

                    data_content = data_dict['data']
                    preprice = data_content.get('prePrice', 0)  # 注意字段名是prePrice不是preprice
                    details = data_content.get('details', [])

                    if not details:
                        print("分时数据为空")
                        return pd.DataFrame()

                    # 解析所有分时数据
                    data = []
                    for detail in details:
                        try:
                            items = detail.split(',')
                            if len(items) >= 5:
                                time = items[0]
                                price = float(items[1])
                                volume = int(items[2])
                                operation = items[3]
                                trade_type = items[4]

                                data.append({
                                    "昨收价": preprice,
                                    "时间": time,
                                    "最新价": price,
                                    "涨跌幅(%)": (price - preprice) / preprice * 100 if preprice else 0,
                                    "成交量(手)": volume,
                                    "操作": operation,
                                    "交易类型": trade_type
                                })
                        except Exception as e:
                            print(f"解析分时数据行出错: {e}, 行内容: {detail}")
                            continue

                    print(f"成功解析 {len(data)} 条分时数据")
                    df = pd.DataFrame(data)
                    df.to_csv(f'{secid}分时.csv', index=False)
                    return df
                except Exception as e:
                    print(f"数据解析失败: {e}")
                    return pd.DataFrame()
        except HTTPError as e:
            print(f"请求错误（状态码：{e.code}）：{e.reason}")
            return pd.DataFrame()
        except URLError as e:
                error_msg = f"URL错误或网络问题：{e.reason}\n股票: {secid}\n尝试次数: {attempt + 1}/{max_retries}"
                print(error_msg)

                if attempt < max_retries - 1:
                    retry_delay = random.uniform(2, 5)
                    print(f"将在 {retry_delay:.1f} 秒后重试 ({attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    continue

                if enable_alert:
                    send_alert(error_msg)
                return pd.DataFrame()

    return pd.DataFrame()


# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # get_proxies()
    pprint(fetch_free_proxies())
    # 抓取沪市688103的分时数据（secid=1.688103）
    # stock_code = "600030"
    # df_fenshi = get_eastmoney_fenshi_with_pandas(secid=f"1.{stock_code}")#1为沪市，0为深市
    # print(f"DataFrame形状：{df_fenshi.shape}")  # 打印数据行数和列数
    # if not df_fenshi.empty:
    #     print("\nDataFrame前5行：")
    #     print(df_fenshi.head())
    #     # 可选：导出为Excel或CSV
    #     df_fenshi.to_excel(f"{stock_code}分时数据.xlsx", index=False)
    #     df_fenshi.to_csv(f"{stock_code}分时数据.csv", index=False, encoding="utf-8-sig")