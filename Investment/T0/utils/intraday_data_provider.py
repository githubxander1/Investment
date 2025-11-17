#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
股票分时数据提供类
专门用于获取和处理股票分时数据
"""
import json
import urllib
from urllib.error import HTTPError, URLError

import pandas as pd
import akshare as ak
from datetime import datetime
import os
import sys
from typing import Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from Investment.T0.utils.logger import setup_logger
except ImportError:
    # 如果无法导入自定义logger，则使用标准logging
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    setup_logger = lambda name: logging.getLogger(name)

logger = setup_logger('intraday_data_provider')


class IntradayDataProvider:
    """
    股票分时数据提供类
    专门用于获取和处理股票分时数据
    """

    def __init__(self):
        """初始化数据提供类"""
        pass

    def get_hist_min_em_data(self, stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
        """
        使用 stock_zh_a_hist_min_em 接口获取分时数据

        Args:
            stock_code: 股票代码
            trade_date: 交易日期

        Returns:
            分时数据DataFrame，包含以下列：
            - 时间: datetime格式的时间
            - 开盘: 开盘价
            - 收盘: 收盘价
            - 最高: 最高价
            - 最低: 最低价
            - 成交量: 成交量
            - 成交额: 成交额
            - 均价: 均价
        """
        try:
            logger.info(f"使用 stock_zh_a_hist_min_em 接口获取 {stock_code} 在 {trade_date} 的分时数据")

            # 构造时间范围
            start_time = f'{trade_date} 09:30:00'
            end_time = f'{trade_date} 15:00:00'

            # 获取数据
            df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period="1",
                start_date=start_time,
                end_date=end_time,
                adjust=""
            )

            if df is not None and not df.empty:
                logger.info(f"✅ stock_zh_a_hist_min_em 成功获取数据，数据行数: {len(df)}")
                logger.debug(f"原始数据列名: {df.columns.tolist()}")

                # 重命名列以匹配统一格式
                df = df.rename(columns={
                    '时间': '时间',
                    '开盘': '开盘',
                    '收盘': '收盘',
                    '最高': '最高',
                    '最低': '最低',
                    '成交量': '成交量',
                    '成交额': '成交额',
                    '均价': '均价'
                })

                # 确保时间列是datetime格式
                df['时间'] = pd.to_datetime(df['时间'])

                # 数据清洗：处理NaN值
                numeric_columns = ['开盘', '收盘', '最高', '最低', '均价']
                for col in numeric_columns:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')

                # 如果开盘价等数据为空，尝试用收盘价填充
                if '收盘' in df.columns:
                    df['开盘'] = df['开盘'].fillna(df['收盘'])
                    df['最高'] = df['最高'].fillna(df['收盘'])
                    df['最低'] = df['最低'].fillna(df['收盘'])
                    df['均价'] = df['均价'].fillna(df['收盘'])

                logger.debug(f"处理后数据列名: {df.columns.tolist()}")
                return df
            else:
                logger.warning(f"stock_zh_a_hist_min_em 接口未返回 {stock_code} 在 {trade_date} 的数据")
                return None

        except Exception as e:
            logger.error(f"使用 stock_zh_a_hist_min_em 接口获取数据失败: {e}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            return None

    def get_a_minute_data(self, stock_code: str) -> Optional[pd.DataFrame]:
        """
        使用 stock_zh_a_minute 接口获取分时数据

        Args:
            stock_code: 股票代码

        Returns:
            分时数据DataFrame，包含以下列：
            - 时间: datetime格式的时间 (对应原始的 'day')
            - 开盘: 开盘价 (对应原始的 'open')
            - 收盘: 收盘价 (对应原始的 'close')
            - 最高: 最高价 (对应原始的 'high')
            - 最低: 最低价 (对应原始的 'low')
            - 成交量: 成交量 (对应原始的 'volume')
            注意：此接口不提供成交额和均价
        """
        try:
            logger.info(f"使用 stock_zh_a_minute 接口获取 {stock_code} 的分时数据")

            # 根据股票代码前缀判断市场
            if stock_code.startswith('6'):
                market_stock_code = f'sh{stock_code}'
            elif stock_code.startswith(('0', '3')):
                market_stock_code = f'sz{stock_code}'
            elif stock_code.startswith('4') or stock_code.startswith('8'):
                market_stock_code = f'bj{stock_code}'
            else:
                market_stock_code = stock_code

            # 获取数据
            df = ak.stock_zh_a_minute(symbol=market_stock_code, period='1', adjust='')

            if df is not None and not df.empty:
                logger.info(f"✅ stock_zh_a_minute 成功获取数据，数据行数: {len(df)}")
                logger.debug(f"原始数据列名: {df.columns.tolist()}")

                # 重命名列以匹配统一格式
                df = df.rename(columns={
                    'day': '时间',
                    'open': '开盘',
                    'high': '最高',
                    'low': '最低',
                    'close': '收盘',
                    'volume': '成交量'
                })

                # 确保时间列是datetime格式
                df['时间'] = pd.to_datetime(df['时间'])

                # 数据清洗：确保数值列是数值类型
                numeric_columns = ['开盘', '最高', '最低', '收盘']
                for col in numeric_columns:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')

                # 添加缺失的列（成交额和均价）
                df['成交额'] = 0.0
                df['均价'] = df['收盘']  # 使用收盘价作为均价的近似值

                # 如果开盘价等数据为空，尝试用收盘价填充
                if '收盘' in df.columns:
                    df['开盘'] = df['开盘'].fillna(df['收盘'])
                    df['最高'] = df['最高'].fillna(df['收盘'])
                    df['最低'] = df['最低'].fillna(df['收盘'])

                logger.debug(f"处理后数据列名: {df.columns.tolist()}")
                return df
            else:
                logger.warning(f"stock_zh_a_minute 接口未返回 {stock_code} 的数据")
                return None

        except Exception as e:
            logger.error(f"使用 stock_zh_a_minute 接口获取数据失败: {e}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            return None

    def get_eastmoney_data(self, stock_code: str) -> Optional[pd.DataFrame]:
        """
        使用东方财富接口获取分时数据

        Args:
            stock_code: 股票代码

        Returns:
            分时数据DataFrame，包含以下列：
            - 时间: datetime格式的时间
            - 开盘: 开盘价
            - 收盘: 收盘价
            - 最高: 最高价
            - 最低: 最低价
            - 成交量: 成交量
            - 成交额: 成交额
            - 均价: 均价
        """
        try:
            logger.info(f"使用东方财富接口获取 {stock_code} 的分时数据")

            # 尝试从正确的路径导入东方财富数据获取函数
            try:
                logger.info(f"使用 eastmoney.com 获取 {stock_code} 的数据")
                # 根据股票代码前缀判断市场
                if stock_code.startswith('6'):
                    secid = f"1.{stock_code}"  # 沪市
                else:
                    secid = f"0.{stock_code}"  # 深市

                # 1. 构造请求URL（参数含义：fields1=基础字段，fields2=分时字段，mpi=最大数据量）
                url = (
                    f'http://16.push2.eastmoney.com/api/qt/stock/details/sse'
                    f'?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55'  # f51=时间，f52=价格等
                    f'&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281'  # mpi=最大返回2000条数据
                    f'&fltt=2&pos=-0&secid={secid}'  # secid=目标股票标识
                )

                # 2. 发送请求并读取响应
                with urllib.request.urlopen(url=url, timeout=10) as response:
                    # 响应格式为 "data:{...}"，需去除前缀"data:"
                    data_str = response.readline().decode('utf-8').lstrip('data:')

                    if not data_str or data_str.strip() == '{}':
                        print("响应为空，未获取到数据")
                        return pd.DataFrame()

                    # 解析JSON数据
                    data_dict = json.loads(data_str)
                    details_list = data_dict.get('data', {}).get('details', [])

                    if not details_list:
                        print("未获取到分时数据")
                        return pd.DataFrame()

            except HTTPError as e:
                print(f"请求错误（状态码：{e.code}）：{e.reason}")
                return pd.DataFrame()
            except URLError as e:
                print(f"URL错误或网络问题：{e.reason}")
                return pd.DataFrame()
            except json.JSONDecodeError as e:
                print(f"JSON解析错误：{e}")
                return pd.DataFrame()

            # 3. 解析details数据并转为DataFrame
            try:
                logger.info(f"开始解析 {stock_code} 的数据")
                # 创建存储解析后数据的列表
                parsed_data = []

                # 解析每条记录
                for detail in details_list:
                    # 每条记录格式: "时间,价格,成交量,未知,未知"
                    parts = detail.split(',')
                    if len(parts) >= 3:
                        time_str = parts[0]  # 时间
                        price = float(parts[1])  # 价格
                        volume = int(parts[2])  # 成交量

                        # 构造完整的时间字符串（假设是当天数据）
                        # 获取当前日期
                        current_date = datetime.now().strftime('%Y-%m-%d')
                        full_time_str = f"{current_date} {time_str}"

                        # 计算成交额
                        amount = price * volume * 100  # 成交量单位是手，需要转换为股

                        parsed_data.append({
                            '时间': full_time_str,
                            '开盘': price,
                            '收盘': price,
                            '最高': price,
                            '最低': price,
                            '成交量': volume,
                            '成交额': amount,
                            '均价': price
                        })

                if not parsed_data:
                    print("解析后的数据为空")
                    return pd.DataFrame()

                # 转为DataFrame
                df = pd.DataFrame(parsed_data)

                # 转换时间列为datetime格式
                df['时间'] = pd.to_datetime(df['时间'])

                # return df

                # df = get_eastmoney_fenshi_with_pandas(secid=secid)

                if df is not None and not df.empty:
                    logger.info(f"✅ 东方财富接口成功获取数据，数据行数: {len(df)}")
                    logger.debug(f"数据列名: {df.columns.tolist()}")
                    return df
                else:
                    logger.warning(f"东方财富接口未返回 {stock_code} 的数据")
                    return None

            except Exception as e:
                print(f"数据解析失败：{e}")
                return pd.DataFrame()

        except Exception as e:
            logger.error(f"使用东方财富接口获取数据失败: {e}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            return None

    def get_intraday_data(self, stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
        """
        获取分时数据的统一接口

        Args:
            stock_code: 股票代码
            trade_date: 交易日期

        Returns:
            分时数据DataFrame，包含统一格式的列：
            - 时间: datetime格式的时间
            - 开盘: 开盘价
            - 收盘: 收盘价
            - 最高: 最高价
            - 最低: 最低价
            - 成交量: 成交量
            - 成交额: 成交额
            - 均价: 均价
        """
        logger.info("=" * 60)
        logger.info("开始加载分时数据")
        logger.info(f"股票代码: {stock_code}")
        logger.info(f"交易日期: {trade_date}")

        # 如果失败，尝试使用 stock_zh_a_minute 接口
        df = self.get_a_minute_data(stock_code)
        if df is not None and not df.empty:
            logger.info("使用 stock_zh_a_minute 接口获取数据成功")
            logger.info(f"数据列: {', '.join(df.columns.tolist())}")
            logger.info(f"数据行数: {len(df)}")
            #打印前5行数据
            logger.info(f"数据前5行: \n{df.head()}")
            logger.info("=" * 60)
            return df

        # 首先尝试使用 stock_zh_a_hist_min_em 接口
        df = self.get_hist_min_em_data(stock_code, trade_date)
        if df is not None and not df.empty:
            logger.info("使用 stock_zh_a_hist_min_em 接口获取数据成功")
            logger.info(f"数据列: {', '.join(df.columns.tolist())}")
            logger.info(f"数据行数: {len(df)}")
            # 打印前5行数据
            logger.info(f"数据前5行: \n{df.head()}")
            logger.info("=" * 60)
            return df

        # 如果还失败，尝试使用东方财富接口
        df = self.get_eastmoney_data(stock_code)
        if df is not None and not df.empty:
            logger.info("使用东方财富接口获取数据成功")
            logger.info(f"数据列: {', '.join(df.columns.tolist())}")
            logger.info(f"数据行数: {len(df)}")
            # 打印前5行数据
            logger.info(f"数据前5行: \n{df.head()}")
            logger.info("=" * 60)
            return df

        # 如果都失败了
        logger.error("❌ 无法获取分时数据")
        logger.info("=" * 60)
        return None


# 保持原有的函数接口以确保向后兼容
def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    向后兼容的函数接口

    Args:
        stock_code: 股票代码
        trade_date: 交易日期

    Returns:
        分时数据DataFrame
    """
    provider = IntradayDataProvider()
    return provider.get_intraday_data(stock_code, trade_date)


if __name__ == "__main__":
    # 测试股票代码和日期
    stock_code = '513050'  # 中概互联网ETF
    start_time = '2025-11-17 09:32:00'  # 2025年11月14日
    end_time = '2025-11-17 15:00:00'  # 2025年11月14日

    # 获取分时数据
    # df = fetch_intraday_data(test_stock, test_date)
    #
    # if df is not None and not df.empty:
    #     print("\n成功获取分时数据:")
    #     print(df.head())
    # else:
    #     print("\n获取分时数据失败")
    #
    #     # 尝试查找该ETF的信息
    #     try:
    #         import akshare as ak
    #         print("\n尝试获取ETF基本信息:")
    #         etf_info = ak.fund_etf_fund_info_em(symbol=test_stock)
    #         print(etf_info)
    #     except Exception as e:
    #         print(f"获取ETF信息失败: {e}")