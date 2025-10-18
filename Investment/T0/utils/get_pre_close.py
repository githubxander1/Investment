from datetime import timedelta, datetime
import akshare as ak
import pandas as pd


def get_prev_close_from_intraday(stock_code, trade_date):
    """从东方财富网-行情首页-沪深京 A 股-每日分时行情分时数据获取昨收价
    stock_code格式：000000
    trade_date格式：YYYY-MM-DD
    """
    try:
        # 获取前一天的日期
        # prev_date_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        prev_date_str = trade_date + " 15:00:00"
        intraday_df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=prev_date_str,
            end_date=prev_date_str,
            adjust=""
        )
        if not intraday_df.empty:
            return intraday_df['收盘'].iloc[-1]

        # if not intraday_df.empty:
        #     # 检查是否存在时间列
        #     time_col = None
        #     for col in ['时间', 'date', 'datetime', 'timestamp']:
        #         if col in intraday_df.columns:
        #             time_col = col
        #             break
        #
        #     if time_col is None:
        #         print(f"分时数据中缺少时间列，列名包括: {list(intraday_df.columns)}")
        #         return None
        #
        #     # 获取前一天的收盘价
        #     intraday_df[time_col] = pd.to_datetime(intraday_df[time_col])
        #     # 过滤掉午休时间的数据
        #     intraday_df = intraday_df[
        #         ~((intraday_df[time_col].dt.hour == 11) & (intraday_df[time_col].dt.minute >= 30)) &
        #         ~(intraday_df[time_col].dt.hour == 12)
        #         ]
        #
        #     if not intraday_df.empty:
        #         # 检查是否存在收盘列
        #         if '收盘' not in intraday_df.columns:
        #             print(f"分时数据中缺少'收盘'列，列名包括: {list(intraday_df.columns)}")
        #             return None
        #         # 获取最后一个有效的收盘价作为昨收价
            # return intraday_df['收盘'].iloc[-1]
    except KeyError as e:
        print(f"从分时数据获取昨收价时缺少关键列: {e}")
    except Exception as e:
        print(f"从分时数据获取昨收价失败: {e}")
    return None


def get_prev_close_from_hist(stock_code, trade_date):
    """从历史数据获取昨收价
    stock_code格式：000000
    trade_date格式：YYYYMMDD
    """
    trade_date = trade_date.replace("-", "")
    try:
        hist_df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=trade_date,
            end_date=trade_date,
            adjust=""
        )

        if not hist_df.empty:
            return hist_df.iloc[-1]['收盘']
    except KeyError as e:
        print(f"从历史数据获取昨收价时缺少关键列: {e}")
    except Exception as e:
        print(f"从历史数据获取昨收价失败: {e}")
    return None

def get_prev_close(stock_code, trade_date=None):
    """获取昨收价"""
    if trade_date is None:
        trade_date = datetime.now().strftime('%Y%m%d')

    trade_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

    # 尝试多个数据源获取昨收价
    data_sources = [
        # 从分时数据获取
        lambda: get_prev_close_from_intraday(stock_code, trade_date),
        # 从历史数据获取
        lambda: get_prev_close_from_hist(stock_code, trade_date),
        # 从 akshare 实时行情获取
        # lambda: _get_prev_close_from_akshare_spot(stock_code),
        # 从 tushare 获取（如果可用）
        # lambda: _get_prev_close_from_tushare(stock_code, yesterday) if TUSHARE_AVAILABLE else None,
    ]

    for i, data_source in enumerate(data_sources):
        # 跳过不可用的数据源
        if data_source is None:
            continue

        try:
            prev_close = data_source()
            if prev_close is not None:
                print(f"✅ 成功从数据源 {i + 1} 获取昨收价: {prev_close:.2f}")
                return prev_close
        except Exception as e:
            print(f"数据源 {i + 1} 获取昨收价失败: {e}")
            continue

    print("❌ 所有数据源均无法获取昨收价")
    return None
# def _get_prev_close_from_tushare(stock_code, trade_date):
#     """从tushare获取昨收价"""
#     try:
#         # 注意：tushare需要token才能使用，这里假设用户已经设置好了
#         # 如果没有token，这个调用会失败
#         # ts.set_token('2e9a7a0827b4c655aa6c267dc00484c6e76ab1022b5717092b44573e')
#
#         df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date='20251001', end_date=trade_date.strftime('%Y%m%d'))
#         if df is not None and not df.empty:
#             # 检查是否存在trade_date列
#             if 'trade_date' not in df.columns:
#                 print(f"tushare数据中缺少'trade_date'列，列名包括: {list(df.columns)}")
#                 return None
#
#             df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
#             df_before = df[df['trade_date'] < trade_date]
#             if not df_before.empty:
#                 # 检查是否存在close列
#                 if 'close' not in df_before.columns:
#                     print(f"tushare数据中缺少'close'列，列名包括: {list(df_before.columns)}")
#                     return None
#                 return df_before.iloc[0]['close']
#     except KeyError as e:
#         print(f"从tushare获取昨收价时缺少关键列: {e}")
#     except Exception as e:
#         print(f"从tushare获取昨收价失败: {e}")
#     return None
# stock_code = '000001'
# trade_date = '2025-10-17'
# print(get_prev_close('000001', '2025-10-17'))
# print(get_prev_close_from_hist('000001', '2025-10-17'))
# print(get_prev_close_from_intraday('000001', '2025-10-17'))
# hist_df = ak.stock_zh_a_hist(
#             symbol=stock_code,
#             period="daily",
#             start_date=trade_date,
#             end_date=trade_date,
#             adjust=""
#         )
# print(hist_df)