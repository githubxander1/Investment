import akshare as ak
import pandas as pd
import os
from datetime import datetime, timedelta


def get_prev_close(stock_code, trade_date):
    """从日线数据获取前一日收盘价，失败则用分时开盘价替代"""
    try:
        trade_date_dt = datetime.strptime(trade_date, '%Y%m%d')
        prev_date = (trade_date_dt - timedelta(days=1)).strftime('%Y%m%d')

        # 获取日线数据（前一日 + 当日）
        daily_df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=prev_date,
            end_date=trade_date,
            adjust=""
        )
        print(f"获取日线数据成功，日期: {daily_df['日期'].values[0]}")

        # 确保格式一致：把日期列也转为 'YYYYMMDD' 格式
        daily_df['日期'] = pd.to_datetime(daily_df['日期']).dt.strftime('%Y%m%d')
        print(daily_df)

        if daily_df.empty or prev_date not in daily_df['日期'].values:
            raise ValueError("前一日数据缺失")

        prev_close = daily_df[daily_df['日期'] == prev_date]['收盘'].values[0]
        print(f"昨收价: {prev_close:.2f}")
        return prev_close
    except Exception as e:
        print(f"昨收获取失败: {e}，将使用分时开盘价替代")
        return None


def get_cached_data(stock_code, trade_date):
    """从缓存中获取数据"""
    cache_file = f"stock_data/{stock_code}.csv"
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file)

            # 检查是否包含时间列
            if '时间' in df.columns:
                df['时间'] = pd.to_datetime(df['时间'])
                # 注意：缓存数据不设置时间列为索引，保持与网络获取数据一致的格式
                return df
            else:
                print("缓存文件中未找到时间列")
        except Exception as e:
            print(f"读取缓存文件失败: {e}")
    return None


def save_data_to_cache(df, stock_code, trade_date):
    """保存数据到缓存"""
    # 确保 stock_data 目录存在
    os.makedirs("stock_data", exist_ok=True)

    cache_file = f"stock_data/{stock_code}.csv"
    try:
        df_reset = df.reset_index()
        df_reset.to_csv(cache_file, index=False)
        print(f"数据已保存到缓存: {cache_file}")
    except Exception as e:
        print(f"保存缓存文件失败: {e}")


def fetch_intraday_data(stock_code, trade_date):
    """从网络获取分时数据"""
    try:
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=trade_date,
            end_date=trade_date,
            adjust=''
        )
        
        if df.empty:
            print("❌ 无分时数据")
            return None

        # 确保时间列存在
        if '时间' not in df.columns:
            # 查找实际的时间列
            time_col = None
            for col in df.columns:
                if '时间' in col or 'date' in col.lower() or 'time' in col.lower():
                    time_col = col
                    break
            if time_col:
                df.rename(columns={time_col: '时间'}, inplace=True)

        return df
    except Exception as e:
        print(f"获取分时数据失败: {e}")
        return None


def preprocess_intraday_data(df, trade_date):
    """预处理分时数据"""
    if df is None or df.empty:
        return None
    
    # 转换时间列
    df['时间'] = pd.to_datetime(df['时间'], errors='coerce')
    df = df[df['时间'].notna()]

    # 只保留指定日期的数据
    target_date = pd.to_datetime(trade_date, format='%Y%m%d')
    df = df[df['时间'].dt.date == target_date.date()]

    # 过滤掉 11:30 到 13:00 之间的数据
    df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
    
    if df.empty:
        print("❌ 所有时间数据均无效")
        return None
    
    return df