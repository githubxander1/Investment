import requests
import json
import pandas as pd


def get_selected_stocks(tiaojian_tree):
    """
    根据条件树获取选股结果

    Args:
        tiaojian_tree (dict): 选股条件树

    Returns:
        pandas.DataFrame: 选股结果
    """
    # 请求URL
    url = "https://prod-lianghuawang-api.yd.com.cn/labelEntrance/l/findStockMsgByQuery"

    # 请求头信息
    headers = {
        "accept": "application/json",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTkzMDYwODcsImlhdCI6MTc1NjYyNzY4N30.X0-5V2cE50X1zeNhILkVw_SgdBMbqUwWwywIFrkxrTY",
        "Content-Type": "application/json",
        "Host": "prod-lianghuawang-api.yd.com.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.12.0"
    }

    # 请求体
    payload = {
        "tiaojianTree": json.dumps(tiaojian_tree)
    }

    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, json=payload)

        # 检查响应状态
        if response.status_code == 200:
            response_data = response.json()

            # 检查是否有数据返回
            if response_data.get("code") == 0 and response_data.get("data"):
                data = response_data["data"]
                stocks = []

                for item in data.get("list", []):
                    stocks.append({
                        "股票代码": item.get("stockCode"),
                        "股票名称": item.get("stockName"),
                        "最新价": item.get("newPrice"),
                        "涨跌幅": round(item.get("zdf", 0), 2),
                        "换手率": round(item.get("hsl", 0), 2),
                        "市盈率": round(item.get("syldyn", 0), 2),
                        "市净率": round(item.get("sjldyn", 0), 2),
                        "总市值": item.get("zsz"),
                        "流通市值": item.get("ltsz"),
                        "成交额": item.get("cje"),
                        "成交额排名": item.get("cjeRank"),
                        "行业": item.get("industryName"),
                        "上市天数": item.get("ssDay")
                    })

                # 转换为DataFrame
                df = pd.DataFrame(stocks)
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


def get_all_selected_stocks(tiaojian_tree):
    """
    获取所有选股结果（包括分页）

    Args:
        tiaojian_tree (dict): 选股条件树

    Returns:
        pandas.DataFrame: 所有选股结果
    """
    all_stocks = []
    page_num = 1
    page_size = 10

    while True:
        # 更新分页参数
        tiaojian_tree["selfParams"] = [
            {"ids": "66001", "abbrs": "writeTime", "titles": "日期", "value": 1756656000000},
            {"ids": "66002", "abbrs": "periodicalReport", "titles": "定期报告", "value": "最新"},
            {"ids": "66004", "abbrs": "EMA28", "titles": "排序", "value": "asc"}
        ]

        # 更新分页信息
        tiaojian_tree["pageNum"] = page_num
        tiaojian_tree["pageSize"] = page_size

        # 请求URL
        url = "https://prod-lianghuawang-api.yd.com.cn/labelEntrance/l/findStockMsgByQuery"

        # 请求头信息
        headers = {
            "accept": "application/json",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTkzMDYwODcsImlhdCI6MTc1NjYyNzY4N30.X0-5V2cE50X1zeNhILkVw_SgdBMbqUwWwywIFrkxrTY",
            "Content-Type": "application/json",
            "Host": "prod-lianghuawang-api.yd.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.12.0"
        }

        # 请求体
        payload = {
            "tiaojianTree": json.dumps(tiaojian_tree)
        }

        try:
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                response_data = response.json()

                if response_data.get("code") == 0 and response_data.get("data"):
                    data = response_data["data"]
                    stock_list = data.get("list", [])

                    if not stock_list:  # 没有更多数据
                        break

                    for item in stock_list:
                        all_stocks.append({
                            "股票代码": item.get("stockCode"),
                            "股票名称": item.get("stockName"),
                            "最新价": item.get("newPrice"),
                            "涨跌幅": round(item.get("zdf", 0), 2),
                            "换手率": round(item.get("hsl", 0), 2),
                            "市盈率": round(item.get("syldyn", 0), 2),
                            "市净率": round(item.get("sjldyn", 0), 2),
                            "总市值": item.get("zsz"),
                            "流通市值": item.get("ltsz"),
                            "成交额": item.get("cje"),
                            "成交额排名": item.get("cjeRank"),
                            "行业": item.get("industryName"),
                            "上市天数": item.get("ssDay")
                        })

                    # 如果返回的数据少于请求的数量，说明已经到最后一页
                    if len(stock_list) < page_size:
                        break

                    page_num += 1
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

    if all_stocks:
        return pd.DataFrame(all_stocks)
    else:
        return pd.DataFrame()


# 示例条件树（根据你提供的数据）
sample_tiaojian_tree = {
    "params": [
        {
            "selectTitle": "中期彩带",
            "selectId": 932,
            "selectDesc": "维持粉色",
            "selectFullDesc": "技术面特色指标>>中期彩带>>维持粉色",
            "selectItem": "技术面特色指标>>中期彩带>>维持粉色",
            "ids": "1345",
            "abbrs": "ZQCDWCFS",
            "titles": "维持粉色",
            "hasAndOr": 2,
            "canMinCustom": 0,
            "canMaxCustom": 0,
            "customMinValue": 0,
            "customMaxValue": 0
        },
        {
            "selectTitle": "剔除ST股",
            "selectId": 909,
            "selectDesc": "",
            "selectFullDesc": "选股范围:剔除ST股",
            "selectItem": "选股范围:剔除ST股",
            "ids": 909,
            "abbrs": "fst",
            "titles": "剔除ST股",
            "hasAndOr": 0,
            "canMinCustom": 0,
            "canMaxCustom": 0,
            "customMinValue": 0,
            "customMaxValue": 0
        },
        {
            "selectTitle": "剔除新股",
            "selectId": 912,
            "selectDesc": "",
            "selectFullDesc": "选股范围:剔除新股",
            "selectItem": "选股范围:剔除新股",
            "ids": 912,
            "abbrs": "fxg",
            "titles": "剔除新股",
            "hasAndOr": 0,
            "canMinCustom": 0,
            "canMaxCustom": 0,
            "customMinValue": 0,
            "customMaxValue": 0
        },
        {
            "selectTitle": "剔除次新股",
            "selectId": 911,
            "selectDesc": "",
            "selectFullDesc": "选股范围:剔除次新股",
            "selectItem": "选股范围:剔除次新股",
            "ids": 911,
            "abbrs": "fcx",
            "titles": "剔除次新股",
            "hasAndOr": 0,
            "canMinCustom": 0,
            "canMaxCustom": 0,
            "customMinValue": 0,
            "customMaxValue": 0
        },
        {
            "selectTitle": "换手率",
            "selectId": 917,
            "selectDesc": "0%-14%",
            "selectFullDesc": "技术面>>换手率>>0%-14%",
            "selectItem": "技术面>>换手率>>0%-14%",
            "ids": "1153",
            "abbrs": "huanShouLv",
            "titles": "自定义",
            "hasAndOr": 0,
            "canMinCustom": 0,
            "canMaxCustom": 14,
            "customMinValue": "0",
            "customMaxValue": "14"
        },
        {
            "selectTitle": "市净率",
            "selectId": 887,
            "selectDesc": "10",
            "selectFullDesc": "基本面>>市净率>>10",
            "selectItem": "基本面>>市净率>>10",
            "ids": "986",
            "abbrs": "shiJingLv",
            "titles": "10",
            "hasAndOr": 0,
            "canMinCustom": 0,
            "canMaxCustom": 0,
            "customMinValue": 0,
            "customMaxValue": 0
        },
        {
            "selectTitle": "市盈率",
            "selectId": 886,
            "selectDesc": "50",
            "selectFullDesc": "基本面>>市盈率>>50",
            "selectItem": "基本面>>市盈率>>50",
            "ids": "978",
            "abbrs": "shiYingLv",
            "titles": "50",
            "hasAndOr": 0,
            "canMinCustom": 0,
            "canMaxCustom": 0,
            "customMinValue": 0,
            "customMaxValue": 0
        },
        {
            "selectTitle": "彼得林奇成长指标",
            "selectId": 2453,
            "selectDesc": "0-100",
            "selectFullDesc": "基本面>>彼得林奇成长指标>>0-100",
            "selectItem": "基本面>>彼得林奇成长指标>>0-100",
            "ids": "2456",
            "abbrs": "bdlqcz",
            "titles": "自定义",
            "hasAndOr": 0,
            "canMinCustom": 0,
            "canMaxCustom": 100,
            "customMinValue": "0",
            "customMaxValue": "100"
        },
        {
            "selectTitle": "销售收现率",
            "selectId": 902,
            "selectDesc": ">0.9",
            "selectFullDesc": "基本面>>销售收现率>>>0.9",
            "selectItem": "基本面>>销售收现率>>>0.9",
            "ids": "1079",
            "abbrs": "xssxl",
            "titles": ">0.9",
            "hasAndOr": 0,
            "canMinCustom": 0,
            "canMaxCustom": 0,
            "customMinValue": 0,
            "customMaxValue": 0
        },
        {
            "selectTitle": "机构持仓",
            "selectId": 2194,
            "selectDesc": "私募基金:盈利占比>60%,年化收益>30% 且 私募基金:盈利占比>60%,年化收益>30%",
            "selectFullDesc": "核心股池>>机构持仓>>私募基金:盈利占比>60%,年化收益>30% 且 私募基金:盈利占比>60%,年化收益>30%",
            "selectItem": "核心股池>>机构持仓>>私募基金:盈利占比>60%,年化收益>30% 且 私募基金:盈利占比>60%,年化收益>30%",
            "ids": "2209,2213",
            "abbrs": "smjjylzb,smjjnhsy",
            "titles": ">60%,>30%",
            "hasAndOr": 1,
            "canMinCustom": 0,
            "canMaxCustom": 0,
            "customMinValue": 0,
            "customMaxValue": 0
        }
    ],
    "selfParams": [
        {"ids": "66001", "abbrs": "writeTime", "titles": "日期", "value": 1756656000000},
        {"ids": "66002", "abbrs": "periodicalReport", "titles": "定期报告", "value": "最新"},
        {"ids": "66004", "abbrs": "EMA28", "titles": "排序", "value": "asc"}
    ],
    "pageSize": 10,
    "pageNum": 1
}

if __name__ == '__main__':
    # 获取选股结果
    df = get_selected_stocks(sample_tiaojian_tree)

    if not df.empty:
        print("选股结果:")
        print(df.head(10))
        print(f"\n总共获取到 {len(df)} 只股票")
    else:
        print("未获取到选股结果")
