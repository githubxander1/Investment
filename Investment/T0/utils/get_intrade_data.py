
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List
import akshare as ak
import os
import sys

from Investment.T0.data_source.data2dfcf import get_eastmoney_fenshi_with_pandas
from Investment.T0.utils.logger import setup_logger

logger = setup_logger('get_intrade_data')

def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    获取分时数据（优先从缓存读取，缓存不存在时从API获取）

    Args:
        stock_code: 股票代码
        trade_date: 交易日期

    Returns:
        分时数据DataFrame
    """
    logger.info(f"=" * 60)
    logger.info(f"开始加载分时数据")
    logger.info(f"股票代码: {stock_code}")
    logger.info(f"交易日期: {trade_date}")

    # 尝试使用akshare获取真实数据（直接从接口获取，不使用缓存）
    try:
        logger.info(f"尝试使用akshare获取真实数据")

        # 使用akshare的stock_zh_a_minute接口获取分时数据
        # df = ak.stock_zh_a_minute(symbol=market_stock_code, period="1", adjust="qfq")
        df = ak.stock_zh_a_hist_min_em(symbol=stock_code, start_date=f'{trade_date} 09:31:00',
                                       end_date=f'{trade_date} 15:00:00', period="1", adjust="qfq")
        if df is not None and not df.empty:
            logger.info(f"✅ 成功获取akshare数据，数据行数: {len(df)}")
            logger.info(f"原始数据列名: {df.columns.tolist()}")
            logger.info(f"原始数据前5行:\n{df.head()}")

            if df is not None and not df.empty:
                logger.info(f"✅ 成功获取akshare数据，数据行数: {len(df)}")

                # 处理数据格式
                if '时间' in df.columns:
                    df['时间'] = pd.to_datetime(df['时间'])

                logger.info(f"数据列: {', '.join(df.columns.tolist())}")
                logger.info(f"✅ 成功加载 {stock_code} 的分时数据")
                logger.info(f"=" * 60)

                return df
            else:
                logger.warning(f"指定日期({trade_date})没有数据或数据质量不佳")

    except Exception as e:
        logger.error(f"使用akshare获取数据失败: {e}")
        import traceback
        traceback.print_exc()

    # 如果akshare失败，尝试使用data2dfcf.py中的方法
    try:
        logger.info("尝试使用data2dfcf.py中的方法获取数据")
        # 导入data2dfcf.py中的函数
        # sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # from data2dfcf import get_eastmoney_fenshi_with_pandas

        # # 构造secid (1表示沪市，0表示深市)
        # if stock_code.startswith('6'):
        #     secid = f"1.{stock_code}"
        # else:
        #     secid = f"0.{stock_code}"

        # 获取数据
        df = get_eastmoney_fenshi_with_pandas(secid=stock_code)

        if df is not None and not df.empty:
            logger.info(f"✅ 成功使用data2dfcf获取数据，数据行数: {len(df)}")

            # 重命名列以匹配所需格式
            df = df.rename(columns={
                '时间': '时间',
                '最新价': '收盘',
                '成交量(手)': '成交量'
            })

            # 添加缺失的列
            if '开盘' not in df.columns:
                df['开盘'] = df['收盘']
            if '最高' not in df.columns:
                df['最高'] = df['收盘']
            if '最低' not in df.columns:
                df['最低'] = df['收盘']
            if '成交额' not in df.columns:
                # 确保数据类型正确后再进行计算
                df['收盘'] = pd.to_numeric(df['收盘'], errors='coerce')
                df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
                df['成交额'] = (df['收盘'] * df['成交量'] * 100).astype('float')  # 成交量单位是手，需要转换为股

            # 处理数据格式
            if '时间' in df.columns:
                df['时间'] = pd.to_datetime(df['时间'])

            logger.info(f"数据列: {', '.join(df.columns.tolist())}")
            logger.info(f"✅ 成功加载 {stock_code} 的分时数据")
            logger.info(f"=" * 60)

            return df
    except Exception as e:
        logger.error(f"使用data2dfcf获取数据失败: {e}")
        import traceback
        traceback.print_exc()

    logger.error(f"❌ 无法获取分时数据")
    return None