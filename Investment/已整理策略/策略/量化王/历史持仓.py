import pandas as pd
import requests
from datetime import datetime, timedelta


def get_historical_positions(pool_id, start_date=None, end_date=None, page_size=30):
    """
    获取量化王策略的历史持仓数据

    Args:
        pool_id (int): 策略池ID
        start_date (str): 开始日期，格式 'YYYY-MM-DD'，默认为一年前
        end_date (str): 结束日期，格式 'YYYY-MM-DD'，默认为今天
        page_size (int): 每页数据条数

    Returns:
        pandas.DataFrame: 历史持仓数据
    """
    # 设置默认日期范围
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    # 请求URL
    url = "https://prod-lhw-strategy-data-center.ydtg.com.cn/lhwDataCenter/getQSHistoryCCGPByIdAndDate"

    # 请求参数
    params = {
        "poolId": pool_id,
        "startDate": start_date,
        "endDate": end_date,
        "by": "find_date",
        "ascOrDesc": "desc",
        "startIndex": 0,
        "pageSize": page_size
    }

    # 请求头信息
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTkzMDYwODcsImlhdCI6MTc1NjYyNzY4N30.X0-5V2cE50X1zeNhILkVw_SgdBMbqUwWwywIFrkxrTY",
        "Host": "prod-lhw-strategy-data-center.ydtg.com.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.12.0"
    }

    try:
        # 发送GET请求
        response = requests.get(url, params=params, headers=headers)

        # 检查响应状态
        if response.status_code == 200:
            response_data = response.json()

            # 检查是否有数据返回
            if response_data.get("code") == 0 and response_data.get("data"):
                data = response_data["data"]
                positions = []

                for item in data:
                    positions.append({
                        "策略ID": item.get("pool_id"),
                        "策略名称": item.get("pool_name"),
                        "股票代码": item.get("sec_code"),
                        "股票名称": item.get("sec_name"),
                        "持仓日期": item.get("find_date"),
                        "买入日期": item.get("buy_date"),
                        "买入价格": item.get("buy_price"),
                        "当前价格": item.get("find_price"),
                        "持仓数量": item.get("hold_vol"),
                        "持仓市值": item.get("market_value"),
                        "浮动盈亏": item.get("floating_pl"),
                        "盈亏比例": round(item.get("floating_pl_rate", 0) * 100, 2),
                        "持仓天数": item.get("position_day")
                    })

                # 转换为DataFrame
                df = pd.DataFrame(positions)
                return df
            else:
                print(f"API返回错误: {response_data.get('message', '未知错误')}")
                return pd.DataFrame()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"处理数据时发生错误: {e}")
        return pd.DataFrame()


def get_all_historical_positions(pool_id, start_date=None, end_date=None):
    """
    获取所有历史持仓数据（包括分页）

    Args:
        pool_id (int): 策略池ID
        start_date (str): 开始日期
        end_date (str): 结束日期

    Returns:
        pandas.DataFrame: 所有历史持仓数据
    """
    all_positions = []
    page_size = 100
    start_index = 0

    while True:
        # 请求URL
        url = "https://prod-lhw-strategy-data-center.ydtg.com.cn/lhwDataCenter/getQSHistoryCCGPByIdAndDate"

        # 请求参数
        params = {
            "poolId": pool_id,
            "startDate": start_date,
            "endDate": end_date,
            "by": "find_date",
            "ascOrDesc": "desc",
            "startIndex": start_index,
            "pageSize": page_size
        }

        # 请求头信息
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTkzMDYwODcsImlhdCI6MTc1NjYyNzY4N30.X0-5V2cE50X1zeNhILkVw_SgdBMbqUwWwywIFrkxrTY",
            "Host": "prod-lhw-strategy-data-center.ydtg.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.12.0"
        }

        try:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                response_data = response.json()

                if response_data.get("code") == 0 and response_data.get("data"):
                    data = response_data["data"]
                    if not data:  # 没有更多数据
                        break

                    for item in data:
                        all_positions.append({
                            "策略ID": item.get("pool_id"),
                            "策略名称": item.get("pool_name"),
                            "股票代码": item.get("sec_code"),
                            "股票名称": item.get("sec_name"),
                            "持仓日期": item.get("find_date"),
                            "买入日期": item.get("buy_date"),
                            "买入价格": item.get("buy_price"),
                            "当前价格": item.get("find_price"),
                            "持仓数量": item.get("hold_vol"),
                            "持仓市值": item.get("market_value"),
                            "浮动盈亏": item.get("floating_pl"),
                            "盈亏比例": round(item.get("floating_pl_rate", 0) * 100, 2),
                            "持仓天数": item.get("position_day")
                        })

                    # 如果返回的数据少于请求的数量，说明已经到最后一页
                    if len(data) < page_size:
                        break

                    start_index += page_size
                else:
                    print(f"API返回错误: {response_data.get('message', '未知错误')}")
                    break
            else:
                print(f"请求失败，状态码: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            break
        except Exception as e:
            print(f"处理数据时发生错误: {e}")
            break

    if all_positions:
        return pd.DataFrame(all_positions)
    else:
        return pd.DataFrame()


if __name__ == '__main__':
    # 获取特定日期范围的历史持仓数据
    df = get_historical_positions(
        pool_id=8007,
        start_date="2024-09-01",
        end_date="2025-08-31"
    )

    if not df.empty:
        print("历史持仓数据:")
        print(df.head())
        print(f"\n总共获取到 {len(df)} 条记录")
    else:
        print("未获取到历史持仓数据")

    # 获取所有历史持仓数据
    all_df = get_all_historical_positions(
        pool_id=8007,
        start_date="2024-09-01",
        end_date="2025-08-31"
    )

    if not all_df.empty:
        print("\n所有历史持仓数据:")
        print(all_df.head())
        print(f"\n总共获取到 {len(all_df)} 条记录")
    else:
        print("\n未获取到所有历史持仓数据")
