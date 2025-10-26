# -*- coding: utf-8 -*-
# 功能：抓取东方财富网分时数据，用pandas转为DataFrame（便于数据分析）

import urllib.request
import pandas as pd
import json
import random
import time
import requests
import gzip
import io
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 反爬措施 - User-Agent池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
]

# 反爬措施 - 随机延时函数
def random_delay(min_delay=0.5, max_delay=2.0):
    """
    随机延时，防止过于频繁的请求
    :param min_delay: 最小延时（秒）
    :param max_delay: 最大延时（秒）
    """
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

# 获取当前时间戳
def get_timestamp():
    return int(time.time() * 1000)

# 获取随机User-Agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)

def create_request_with_proxy(url, proxy=None):
    """
    创建带代理和反爬头的请求
    :param url: 请求URL
    :param proxy: 代理字典，格式如 {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
    :return: Request对象
    """
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 移除Accept-Encoding，避免自动压缩导致的解码问题
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }
    
    request = urllib.request.Request(url, headers=headers)
    return request

def get_eastmoney_fenshi_with_pandas(secid="1.688103", proxy=None, retry=3):
    """
    抓取分时数据并转为DataFrame
    :param secid: 股票标识（格式：市场.股票代码，1=沪市，0=深市，如1.688103、0.300059）
    :param proxy: 代理字典，格式如 {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
    :param retry: 重试次数
    :return: 分时数据DataFrame（无数据则返回空DataFrame）
    """
    # 1. 构造请求URL（参数含义：fields1=基础字段，fields2=分时字段，mpi=最大数据量）
    timestamp = get_timestamp()
    url = (
        f'http://push2.eastmoney.com/api/qt/stock/details/sse'  # 修改URL为更常用的地址
        f'?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55'  # f51=时间，f52=价格等
        f'&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281'  # mpi=最大返回2000条数据
        f'&fltt=2&pos=-0&secid={secid}'  # secid=目标股票标识
        f'&_={timestamp}'  # 添加时间戳防止缓存
    )
    
    logger.info(f"正在请求URL: {url}")

    # 2. 发送请求并读取响应（支持重试）
    for attempt in range(retry):
        try:
            logger.info(f"第 {attempt+1} 次尝试获取数据...")
            request = create_request_with_proxy(url, proxy)
            
            # 使用proxy_handler如果提供了代理
            opener = urllib.request.build_opener()
            if proxy:
                proxy_handler = urllib.request.ProxyHandler(proxy)
                opener.add_handler(proxy_handler)
            
            logger.info("正在发送网络请求...")
            with opener.open(request, timeout=10) as response:  # 减少超时时间
                logger.info("收到网络响应，正在读取内容...")
                # 读取响应内容
                content = response.read()
                logger.info(f"响应内容大小: {len(content)} 字节")
                
                # 尝试解压缩gzip数据
                try:
                    # 检查是否是gzip压缩数据（gzip魔数：0x1f8b）
                    if content.startswith(b'\x1f\x8b'):
                        logger.info("检测到gzip压缩数据，正在解压...")
                        buffer = io.BytesIO(content)
                        with gzip.GzipFile(fileobj=buffer, mode='rb') as f:
                            content = f.read()
                            logger.info(f"gzip解压后内容大小: {len(content)} 字节")
                except Exception as e:
                    logger.warning(f"尝试解压缩gzip数据失败：{e}，将尝试直接解码")
                
                # 尝试多种编码解码
                encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
                data_str = None
                
                for encoding in encodings:
                    try:
                        data_str = content.decode(encoding)
                        logger.info(f"使用 {encoding} 编码解码成功，解码后长度: {len(data_str)}")
                        break
                    except UnicodeDecodeError:
                        logger.warning(f"使用 {encoding} 编码解码失败")
                        continue
                
                if data_str is None:
                    logger.error("无法解码响应内容，尝试了多种编码")
                    return pd.DataFrame()
                
                logger.info(f"解码后数据前200字符: {repr(data_str[:200])}")
                
                # 响应格式为 "data:{...}"，需去除前缀"data:"
                if data_str.startswith('data:'):
                    data_str = data_str[5:]  # 去除"data:"前缀而不是使用lstrip
                    logger.info("已去除'data:'前缀")
                
                if not data_str:
                    logger.warning("响应为空，未获取到数据")
                    return pd.DataFrame()
                
                logger.info("正在解析JSON数据...")
                # 3. 解析数据并转为DataFrame
                try:
                    # 使用json.loads替代eval，更安全
                    data_dict = json.loads(data_str)
                    logger.info(f"JSON解析成功: {list(data_dict.keys()) if isinstance(data_dict, dict) else '非字典结构'}")
                    
                    # 检查是否有数据
                    if 'data' not in data_dict or not data_dict['data']:
                        logger.warning("数据字典中无分时数据")
                        return pd.DataFrame()
                    
                    # 获取具体的分时数据（根据实际接口返回调整）
                    # 东方财富接口可能返回details字段，是一个字符串，需要分割
                    data_part = data_dict['data']
                    logger.info(f"data部分类型: {type(data_part)}")
                    logger.info(f"data部分内容预览: {str(data_part)[:200] if data_part else 'None'}")
                    
                    # 根据实际返回结构调整
                    details = ""
                    if isinstance(data_part, dict):
                        details = data_part.get('details', '')
                        logger.info(f"从dict中获取details字段: {type(details)}, 长度: {len(details) if hasattr(details, '__len__') else 'N/A'}")
                    elif isinstance(data_part, str):
                        details = data_part
                        logger.info(f"直接使用data_part作为details: {type(details)}, 长度: {len(details)}")
                    elif isinstance(data_part, list):
                        details = ";".join([str(item) for item in data_part])
                        logger.info(f"将list转换为字符串: {type(details)}, 长度: {len(details)}")
                    else:
                        details = str(data_part)
                        logger.info(f"将其他类型转换为字符串: {type(details)}, 长度: {len(details)}")
                    
                    if not details:
                        logger.warning("details字段为空")
                        # 尝试其他可能的字段
                        if isinstance(data_part, dict):
                            logger.info(f"data中所有键: {list(data_part.keys())}")
                            # 尝试其他可能包含数据的字段
                            for key in data_part.keys():
                                value = data_part[key]
                                logger.info(f"键 {key}: 类型 {type(value)}, 内容预览: {str(value)[:100] if value else 'None'}")
                        return pd.DataFrame()
                    
                    # 如果details不是字符串而是列表或其他类型
                    if not isinstance(details, str):
                        logger.info("details不是字符串，尝试转换为字符串")
                        details = str(details)
                    
                    # 处理details数据（假设是分号分隔的记录，逗号分隔的字段）
                    # 格式示例：'15:00:00,10.23,1000;15:00:03,10.24,1200;...'
                    records = []
                    items = details.split(';')
                    logger.info(f"分割后的项目数量: {len(items)}")
                    
                    # 限制处理的项目数量以避免卡顿
                    max_items = min(1000, len(items))
                    logger.info(f"将处理前 {max_items} 个项目")
                    
                    for i, item in enumerate(items[:max_items]):
                        if item:
                            try:
                                parts = item.split(',')
                                if len(parts) >= 5:  # 确保有足够的字段
                                    # 解析时间、价格、成交量等
                                    time_str = parts[0]
                                    price = float(parts[1])
                                    volume = int(parts[2])
                                    amount = float(parts[3])
                                    bs_type = int(parts[4])  # 买卖类型
                                    
                                    records.append({
                                        '时间': time_str,
                                        '价格': price,
                                        '成交量': volume,
                                        '成交额': amount,
                                        '买卖类型': bs_type
                                    })
                                else:
                                    logger.debug(f"项目 {i} 分割后不足5个字段: {item}")
                            except (ValueError, IndexError) as e:
                                logger.debug(f"解析单条数据失败: {item}, 错误: {e}")
                                continue
                    
                    logger.info(f"共解析到 {len(records)} 条记录")
                    # 创建DataFrame
                    if records:
                        df = pd.DataFrame(records)
                        logger.info(f"创建DataFrame完成，形状: {df.shape}")
                        
                        # 添加完整日期（当前日期）
                        # today = datetime.now().strftime('%Y-%m-%d')
                        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                        df['完整时间'] = df['时间'].apply(lambda x: f"{yesterday} {x}")
                        df['完整时间'] = pd.to_datetime(df['完整时间'])
                        logger.info("时间列处理完成")
                        
                        return df
                    else:
                        logger.warning("未能解析到有效数据记录")
                        return pd.DataFrame()
                        
                except json.JSONDecodeError as e:
                    logger.error(f"数据JSON解析失败：{e}")
                    logger.error(f"原始数据内容: {data_str[:500]}...")
                    return pd.DataFrame()
                except Exception as e:
                    logger.error(f"数据处理过程中发生错误：{e}")
                    import traceback
                    logger.error(f"详细错误信息：{traceback.format_exc()}")
                    return pd.DataFrame()
                    
        except HTTPError as e:
            logger.error(f"请求错误（状态码：{e.code}）：{e.reason}，第{attempt+1}次尝试")
            if attempt == retry - 1:
                return pd.DataFrame()
            random_delay(1, 3)  # 增加重试间隔
        except URLError as e:
            logger.error(f"URL错误或网络问题：{e.reason}，第{attempt+1}次尝试")
            if attempt == retry - 1:
                return pd.DataFrame()
            random_delay(1, 3)  # 增加重试间隔
        except Exception as e:
            logger.error(f"未知错误：{e}，第{attempt+1}次尝试")
            import traceback
            logger.error(f"详细错误信息：{traceback.format_exc()}")
            if attempt == retry - 1:
                return pd.DataFrame()
            random_delay(1, 3)  # 增加重试间隔
    
    return pd.DataFrame()

def get_eastmoney_fenshi_by_date(stock_code, trade_date=None, proxy=None):
    """
    根据股票代码和日期获取东方财富分时数据
    
    :param stock_code: 股票代码（如：600030）
    :param trade_date: 交易日期（格式：YYYY-MM-DD 或 YYYYMMDD）
    :param proxy: 代理字典，格式如 {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
    :return: 分时数据DataFrame
    """
    # 确定市场代码（1=沪市，0=深市）
    if stock_code.startswith(('6', '5')):  # 沪市股票或基金
        secid = f"1.{stock_code}"
    else:  # 深市股票或基金
        secid = f"0.{stock_code}"
    
    logger.info(f"开始获取股票 {stock_code} 的分时数据，secid: {secid}")
    
    # 获取分时数据
    df = get_eastmoney_fenshi_with_pandas(secid, proxy)
    
    # 如果有日期参数，需要过滤数据
    if not df.empty and trade_date and '完整时间' in df.columns:
        # 确保 trade_date 是正确的格式
        if isinstance(trade_date, str):
            if '-' in trade_date:
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
            else:
                trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
        else:
            trade_date_obj = trade_date
            
        # 格式化为目标日期字符串
        target_date_str = trade_date_obj.strftime('%Y-%m-%d')
        
        # 过滤数据，只保留目标日期的数据
        df = df[df['完整时间'].dt.strftime('%Y-%m-%d') == target_date_str]
    
    # 重命名列以匹配akshare的格式
    if not df.empty:
        # 确保包含必要的列
        required_columns = ['时间', '价格']
        if all(col in df.columns for col in required_columns):
            # 计算开盘、最高、最低等
            # 这里简化处理，实际可能需要更复杂的逻辑
            df['开盘'] = df['价格']
            df['收盘'] = df['价格']
            df['最高'] = df['价格']
            df['最低'] = df['价格']
            
            # 重新排序列
            result_df = df[['时间', '开盘', '收盘', '最高', '最低', '成交量', '成交额']]
            logger.info(f"成功获取股票 {stock_code} 的分时数据，共 {len(result_df)} 条记录")
            return result_df
    
    logger.warning(f"未获取到股票 {stock_code} 的有效分时数据")
    return pd.DataFrame()

# 高级接口：支持与akshare兼容的接口
def stock_zh_a_hist_min_em(symbol, period="1", start_date=None, end_date=None, adjust="", proxy=None):
    """
    东方财富-股票-个股分时数据（与akshare接口兼容）
    
    :param symbol: 股票代码
    :param period: 周期，这里固定为"1"表示1分钟
    :param start_date: 开始日期，格式：YYYYMMDD
    :param end_date: 结束日期，格式：YYYYMMDD
    :param adjust: 复权类型，这里不使用
    :param proxy: 代理字典
    :return: 分时数据DataFrame
    """
    # 使用东方财富接口获取数据
    df = get_eastmoney_fenshi_by_date(symbol, start_date, proxy)
    
    # 如果没有成功获取数据，可以尝试使用另一个接口
    if df.empty:
        logger.info(f"尝试使用备用接口获取股票 {symbol} 的数据")
        # 这里可以实现备用接口逻辑
        pass
    
    return df

# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 设置代理（可选）
    # proxy = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
    proxy = None  # 不使用代理
    
    # 抓取沪市600030的分时数据
    stock_code = "600030"
    print(f"开始获取股票 {stock_code} 的分时数据...")
    df_fenshi = get_eastmoney_fenshi_by_date(stock_code=stock_code, proxy=proxy)
    print(f"DataFrame形状：{df_fenshi.shape}")  # 打印数据行数和列数
    if not df_fenshi.empty:
        print("\nDataFrame前5行：")
        print(df_fenshi.head())
        # 可选：导出为Excel或CSV
        df_fenshi.to_excel(f"{stock_code}分时数据.xlsx", index=False)
        df_fenshi.to_csv(f"{stock_code}分时数据.csv", index=False, encoding="utf-8-sig")
    else:
        print("未获取到有效数据")