import os
import time
import logging
import requests
import schedule
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright, TimeoutError
import urllib3
import warnings

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# -------------------------- 1. 日志配置初始化（全局生效） --------------------------
def init_logger(log_dir: str = "./proxy_logs"):
    """
    初始化日志系统：同时输出到控制台和按日命名的日志文件，格式包含时间、级别、模块、消息

    Args:
        log_dir: 日志文件保存目录（默认当前目录下proxy_logs文件夹）
    """
    # 创建日志目录（不存在则创建）
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 日志文件命名（按日期，如：proxy_crawl_20251030.log）
    today_date = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"proxy_crawl_{today_date}.log")

    # 日志格式配置
    log_format = "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # 1. 配置控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))

    # 2. 配置文件 handler（UTF-8编码，避免中文乱码）
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # 文件日志记录DEBUG及以上级别（更详细）
    file_handler.setFormatter(logging.Formatter(log_format, date_format))

    # 3. 全局日志器配置
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # 全局日志级别（需低于各handler级别）
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # 避免日志重复输出（移除默认handler）
    if root_logger.handlers:
        root_logger.handlers = root_logger.handlers[-2:]  # 只保留控制台和文件handler

    logging.info("✅ 日志系统初始化完成，日志文件保存路径：%s", log_file)


# -------------------------- 2. 代理有效性验证（多线程并发） --------------------------
def verify_single_proxy(
        ip: str,
        port: int,
        timeout: float = 5.0,
        test_urls: dict = None
) -> bool:
    """
    验证单个代理的有效性：测试HTTP/HTTPS连通性，返回是否可用

    Args:
        ip: 代理IP地址
        port: 代理端口
        timeout: 超时时间（秒，默认5秒，避免长时间阻塞）
        test_urls: 测试站点字典（key: 协议, value: 测试URL）

    Returns:
        bool: 代理可用返回True，不可用返回False
    """
    # 使用类似curl的方式验证代理
    try:
        # 使用http://azenv.net/验证代理
        response = requests.get(
            "http://azenv.net/",
            proxies={
                "http": f"http://{ip}:{port}",
                "https": f"http://{ip}:{port}"
            },
            timeout=timeout,
            verify=False
        )
        
        # 检查响应内容中是否包含代理信息
        if response.status_code == 200:
            content = response.text
            # 检查响应中是否包含IP地址，确认代理工作正常
            if ip in content:
                logging.debug("✅ 代理可用（CURL方式）：%s:%s", ip, port)
                return True
            else:
                logging.debug("❌ 代理无效（响应异常）：%s:%s，响应内容：%s", ip, port, content[:50])
                return False
        else:
            logging.debug("❌ 代理无效（状态码）：%s:%s，状态码：%d", ip, port, response.status_code)
            return False
    except requests.exceptions.ConnectTimeout:
        logging.debug("❌ 代理超时（连接超时）：%s:%s", ip, port)
        return False
    except requests.exceptions.ProxyError:
        logging.debug("❌ 代理错误（无法连接代理）：%s:%s", ip, port)
        return False
    except Exception as e:
        logging.warning("❌ 代理验证异常：%s:%s，异常信息：%s", ip, port, str(e)[:100])
        return False


def verify_proxy_batch(
        proxy_df: pd.DataFrame,
        max_workers: int = 10,
        timeout: float = 5.0
) -> pd.DataFrame:
    """
    批量验证代理有效性（多线程并发），返回过滤后的有效代理DataFrame

    Args:
        proxy_df: 待验证的代理DataFrame（需包含"IP Address"和"Port"列）
        max_workers: 最大并发线程数（默认10，避免并发过高被测试站点封禁）
        timeout: 单个代理验证超时时间（秒）

    Returns:
        pd.DataFrame: 仅包含有效代理的DataFrame（空则返回空DataFrame）
    """
    if proxy_df.empty:
        logging.warning("⚠️  待验证代理为空，无需验证")
        return pd.DataFrame()

    logging.info("📋 开始批量验证代理，待验证数量：%d，并发线程数：%d，超时时间：%ds",
                 len(proxy_df), max_workers, timeout)

    # 存储有效代理的索引
    valid_proxy_indices = []

    # 多线程执行验证
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 为每个代理提交验证任务（返回 (任务, 代理索引) 映射）
        task_map = {}
        for idx, row in proxy_df.iterrows():
            ip = str(row["IP Address"]).strip()
            port = int(row["Port"])  # 确保端口为整数
            task = executor.submit(verify_single_proxy, ip=ip, port=port, timeout=timeout)
            task_map[task] = idx

        # 遍历完成的任务，收集有效代理索引
        for task in as_completed(task_map):
            idx = task_map[task]
            if task.result():  # 若代理有效，记录索引
                valid_proxy_indices.append(idx)

    # 过滤有效代理
    valid_proxy_df = proxy_df.loc[valid_proxy_indices].reset_index(drop=True)
    logging.info("📊 代理验证完成：待验证%d条 → 有效%d条 → 无效%d条",
                 len(proxy_df), len(valid_proxy_df), len(proxy_df) - len(valid_proxy_df))

    return valid_proxy_df


# -------------------------- 3. 核心爬取函数（整合验证+日志） --------------------------
def crawl_free_proxies(
        target_url: str,
        save_dir: str = "./proxy_data",
        filter_invalid: bool = True,
        verify_proxies: bool = True,  # 是否开启代理验证
        max_workers: int = 10,
        verify_timeout: float = 5.0
) -> pd.DataFrame:
    """
    无头模式爬取免费代理 → （可选）过滤无效IP → （可选）验证有效性 → 保存CSV → 返回DataFrame

    Args:
        target_url: 目标代理页面URL
        save_dir: CSV保存目录
        filter_invalid: 是否过滤内网/无效IP（0.0.0.0、127.0.0.1等）
        verify_proxies: 是否开启代理有效性验证（默认开启）
        max_workers: 代理验证最大并发线程数
        verify_timeout: 单个代理验证超时时间（秒）

    Returns:
        pd.DataFrame: 有效代理DataFrame（失败返回None）
    """
    logging.info("🚀 开始爬取免费代理，目标URL：%s", target_url)

    # 1. 初始化保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        logging.debug("📂 创建代理数据保存目录：%s", save_dir)

    # 2. Playwright无头爬取
    browser = None
    context = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,  # 改为无头模式
                args=["--no-sandbox", "--disable-dev-shm-usage"]  # 解决Linux权限问题
            )
            context = browser.new_context()
            page = context.new_page()
            logging.debug("🌐 启动无头Chromium浏览器，访问目标页面")

            # 访问页面（超时30秒）
            page.goto(target_url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=20000)  # 等待网络空闲
            logging.debug("✅ 目标页面加载完成")

            # 3. 提取代理数据（使用新的方法）
            logging.debug("📥 开始提取代理数据...")
            
            # 使用JavaScript提取代理数据
            proxy_data = page.evaluate("""() => {
                const rows = [];
                // 等待表格加载完成
                const ipElements = Array.from(document.querySelectorAll('td:nth-child(1)'));
                const portElements = Array.from(document.querySelectorAll('td:nth-child(2)'));
                const codeElements = Array.from(document.querySelectorAll('td:nth-child(3)'));
                const countryElements = Array.from(document.querySelectorAll('td:nth-child(4)'));
                const anonymityElements = Array.from(document.querySelectorAll('td:nth-child(5)'));
                const googleElements = Array.from(document.querySelectorAll('td:nth-child(6)'));
                const httpsElements = Array.from(document.querySelectorAll('td:nth-child(7)'));
                const checkedElements = Array.from(document.querySelectorAll('td:nth-child(8)'));
                
                for (let i = 0; i < Math.min(ipElements.length, portElements.length); i++) {
                    const ip = ipElements[i].textContent.trim();
                    const port = portElements[i] ? portElements[i].textContent.trim() : '';
                    const code = codeElements[i] ? codeElements[i].textContent.trim() : '';
                    const country = countryElements[i] ? countryElements[i].textContent.trim() : '';
                    const anonymity = anonymityElements[i] ? anonymityElements[i].textContent.trim() : '';
                    const google = googleElements[i] ? googleElements[i].textContent.trim() : '';
                    const https = httpsElements[i] ? httpsElements[i].textContent.trim() : '';
                    const checked = checkedElements[i] ? checkedElements[i].textContent.trim() : '';
                    
                    if (ip && port) {
                        rows.push({
                            ip, port, code, country, anonymity, google, https, checked
                        });
                    }
                }
                
                return rows;
            }""")
            
            logging.debug("📥 提取代理数据完成，共获取 %d 条记录", len(proxy_data))

            # 4. 转换为DataFrame
            if not proxy_data:
                logging.error("❌ 未获取到代理数据")
                return None
                
            df = pd.DataFrame(proxy_data)
            # 重命名列以匹配原有格式
            df = df.rename(columns={
                'ip': 'IP Address',
                'port': 'Port',
                'code': 'Code',
                'country': 'Country',
                'anonymity': 'Anonymity',
                'google': 'Google',
                'https': 'Https',
                'checked': 'Last Checked'
            })
            
            logging.info("📊 代理数据解析完成，共%d条记录（字段：%s）",
                         len(df), ", ".join(df.columns.tolist()))

            # 5. 过滤内网/无效IP
            if filter_invalid:
                invalid_ips = ["0.0.0.0", "127.0.0.1", "localhost"]
                before_filter = len(df)
                df = df[~df["IP Address"].isin(invalid_ips)]
                df = df[df["Port"].apply(lambda x: str(x).isdigit())]  # 过滤非数字端口
                logging.info("🔍 过滤无效IP/端口：过滤前%d条 → 过滤后%d条", before_filter, len(df))

            # 6. 代理有效性验证（可选）
            if verify_proxies and not df.empty:
                df = verify_proxy_batch(df, max_workers=max_workers, timeout=verify_timeout)

            # 7. 保存CSV（按日期命名）
            today_date = datetime.now().strftime("%Y%m%d")
            save_path = os.path.join(save_dir, f"free_proxies_valid_{today_date}.csv")  # 文件名加valid区分有效代理
            df.to_csv(save_path, index=False, encoding="utf-8-sig")
            logging.info("💾 有效代理数据保存完成，路径：%s，有效记录数：%d", save_path, len(df))

            return df

    except TimeoutError:
        logging.error("❌ 爬取超时：页面加载或元素定位超过30秒（目标URL：%s）", target_url)
    except Exception as e:
        logging.error("❌ 爬取异常：%s", str(e), exc_info=True)  # exc_info=True记录完整堆栈信息
    finally:
        # 安全关闭浏览器
        try:
            if context:
                context.close()
        except:
            pass
        try:
            if browser:
                browser.close()
        except:
            pass
        logging.debug("🔌 关闭无头Chromium浏览器")

    return None


# -------------------------- 4. 定时任务函数（整合日志） --------------------------
def schedule_daily_crawl(
        target_url: str,
        save_dir: str = "./proxy_data",
        crawl_time: str = "02:00",
        verify_proxies: bool = True,
        max_workers: int = 10,
        verify_timeout: float = 5.0
):
    """
    每天指定时间定时爬取代理（整合日志记录）

    Args:
        target_url: 目标代理页面URL
        save_dir: CSV保存目录
        crawl_time: 每天爬取时间（格式"HH:MM"）
        verify_proxies: 是否开启代理验证
        max_workers: 验证并发线程数
        verify_timeout: 验证超时时间（秒）
    """
    # 首次运行立即爬取
    logging.info("📅 首次爬取启动（当前时间：%s）", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    crawl_free_proxies(
        target_url=target_url,
        save_dir=save_dir,
        verify_proxies=verify_proxies,
        max_workers=max_workers,
        verify_timeout=verify_timeout
    )

    # 设置每日定时任务
    schedule.every().day.at(crawl_time).do(
        crawl_free_proxies,
        target_url=target_url,
        save_dir=save_dir,
        verify_proxies=verify_proxies,
        max_workers=max_workers,
        verify_timeout=verify_timeout
    )
    logging.info("⏰ 定时任务配置完成：每天 %s 自动执行代理爬取", crawl_time)
    logging.info("ℹ️  程序运行中，按 Ctrl+C 终止...")

    # 循环监听任务（每分钟检查一次）
    while True:
        schedule.run_pending()
        time.sleep(60)


# -------------------------- 程序入口（初始化日志+启动定时任务） --------------------------
if __name__ == "__main__":
    # -------------------------- 配置参数（请根据实际情况修改） --------------------------
    TARGET_URL = "https://free-proxy-list.net"  # 目标代理页面真实URL（示例：free-proxy-list.net）
    SAVE_DIR = "./proxy_data"  # 有效代理CSV保存目录
    LOG_DIR = "./proxy_logs"  # 日志文件保存目录
    DAILY_CRAWL_TIME = "02:00"  # 每日爬取时间（24小时制，如"02:00"）
    VERIFY_PROXIES = True  # 是否开启代理有效性验证
    MAX_WORKERS = 15  # 代理验证最大并发线程数（建议10-20）
    VERIFY_TIMEOUT = 6.0  # 单个代理验证超时时间（秒，建议5-10）
    # ----------------------------------------------------------------------------------

    # 1. 初始化日志系统（必须在最前面执行，确保后续流程日志正常记录）
    init_logger(log_dir=LOG_DIR)
    
    # 2. 爬取代理
    crawl_free_proxies(target_url=TARGET_URL, save_dir=SAVE_DIR, verify_proxies=VERIFY_PROXIES, 
                      max_workers=MAX_WORKERS, verify_timeout=VERIFY_TIMEOUT)

    # # 3. 启动定时爬取任务
    # try:
    #     schedule_daily_crawl(
    #         target_url=TARGET_URL,
    #         save_dir=SAVE_DIR,
    #         crawl_time=DAILY_CRAWL_TIME,
    #         verify_proxies=VERIFY_PROXIES,
    #         max_workers=MAX_WORKERS,
    #         verify_timeout=VERIFY_TIMEOUT
    #     )
    # except KeyboardInterrupt:
    #     logging.info("🛑 用户手动终止程序（Ctrl+C），程序退出")
    # except Exception as e:
    #     logging.critical("💥 程序意外终止，异常信息：%s", str(e), exc_info=True)