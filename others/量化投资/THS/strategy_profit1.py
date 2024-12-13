import os
from pprint import pprint
import requests
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime

# 手动创建策略ID到策略名称的映射
strategy_id_to_name = {
    '155259': 'TMT资金流入战法',
    '155680': 'GPT定期精选',
    '138036': '低价小盘股战法',
    '138386': '主力控盘低价股战法',
    '118188': '均线粘合平台突破',
    # '155182': '国资云强势股'
    # 添加更多策略ID和名称
}

def fetch_strategy_profit(strategy_id):
    ua = UserAgent()
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
    params = {
        "strategyId": strategy_id
    }
    headers = {
        "User-Agent": ua.random
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # pprint(data)

        # 提取 latestTrade 信息
        latest_trade = data.get('result', {}).get('latestTrade', {})
        trade_date = latest_trade.get('tradeDate', 'N/A')
        trade_stocks = latest_trade.get('tradeStocks', [])

        # 提取 positionStocks 信息
        position_stocks = data.get('result', {}).get('positionStocks', [])

        # 提取latestTrade所需字段
        latestTrade_info = []
        for trade in trade_stocks:
            name = trade.get('stkName', 'N/A')
            code = trade.get('stkCode', 'N/A').split('.')[0]  # 提取股票代码
            market = determine_market(code)  # 判断市场
            operation = trade.get('operationType', 'N/A')
            # 使用 latestTrade 的 tradeDate 作为时间
            time_str = trade_date  # 使用 latestTrade 的 tradeDate
            price = trade.get('tradePrice', 'N/A')
            quantity = trade.get('tradeAmount', 'N/A')

            latestTrade_info.append({
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '操作': operation,
                '股票名称': name,
                '股票代码': code,
                '市场': market,
                '价格': price,
                '数量': quantity,
                '时间': time_str,
            })

        # 提取positionStocks所需字段
        positions_info = []
        for position in position_stocks:
            name = position.get('stkName', 'N/A')
            code = position.get('stkCode', 'N/A').split('.')[0]  # 提取股票代码
            market = determine_market(code)  # 判断市场
            industry = position.get('industry', 'N/A')
            price = position.get('price', 'N/A')
            position_date_ms = position.get('positionDate', 'N/A')
            position_ratio = position.get('positionRatio', 'N/A')
            profit_and_loss_ratio = position.get('profitAndLossRatio', 'N/A')

            # 将 positionDate 从毫秒时间戳转换为可读的日期时间格式
            if isinstance(position_date_ms, int):
                position_date_s = position_date_ms / 1000
                position_date = datetime.fromtimestamp(position_date_s)
                position_date_str = position_date.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(position_date_ms, str):
                position_date_str = position_date_ms
            else:
                position_date_str = 'N/A'

            # 将 positionRatio 和 profitAndLossRatio 转换为百分比形式
            if isinstance(position_ratio, (int, float)):
                position_ratio = f"{position_ratio * 100:.2f}%"
            if isinstance(profit_and_loss_ratio, (int, float)):
                profit_and_loss_ratio = f"{profit_and_loss_ratio * 100:.2f}%"

            positions_info.append({
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '股票名称': name,
                '股票代码': code,
                '市场': market,
                '行业': industry,
                '价格': price,
                '持仓比例': position_ratio,
                '盈亏比例': profit_and_loss_ratio,
                '持仓日期': position_date_str,
            })

        return latestTrade_info, positions_info, trade_date
    else:
        print(f"请求失败，状态码: {response.status_code}，策略ID: {strategy_id}")
        return [], [], 'N/A'

def determine_market(stock_code):
    # 根据股票代码判断市场
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('300'):
        return '创业板'
    elif stock_code.startswith(('4', '8')):
        return '北交所'
    else:
        return '其他'

def save_to_excel(df, filename, sheet_name, index=False):
    # 保存DataFrame到Excel文件
    if not os.path.exists(filename):
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
    else:
        try:
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=index)
        except Exception as e:
            print(f"读取或写入Excel文件时发生错误: {e}")

# 要查询的策略ID列表
strategy_ids = ['155259', '155680', '138036', '138386', '118188']

# 存储所有策略的交易信息和持仓信息
all_latestTrade_info = []
all_positions_info = []
all_latest_trade_dates = []

# 遍历每个策略ID，获取其交易信息和持仓信息
for strategy_id in strategy_ids:
    latestTrade_info, positions_info, trade_date = fetch_strategy_profit(strategy_id)
    all_latestTrade_info.extend(latestTrade_info)
    all_positions_info.extend(positions_info)
    all_latest_trade_dates.append((strategy_id, trade_date))

# 创建DataFrame
trades_df = pd.DataFrame(all_latestTrade_info)
positions_df = pd.DataFrame(all_positions_info)

# 打印DataFrame
# print("最新交易信息:")
# print(trades_df)

# 创建当天交易信息的DataFrame
current_date = datetime.now().date().strftime('%Y%m%d')
today_trades_df = trades_df[trades_df['时间'] == current_date]

# 合并行业信息到当天交易信息中
today_trades_with_industry = pd.merge(today_trades_df, positions_df[['股票名称', '行业']], on='股票名称', how='left')

# 打印当天交易信息
print("\n当天交易信息:")
print(today_trades_with_industry)
print("\n持仓信息:")
print(positions_df)

# 保存当天交易信息和持仓信息到同一个Excel文件的不同工作表
filename = 'trades_and_positions.xlsx'
if not today_trades_with_industry.empty:
    save_to_excel(today_trades_with_industry, filename, 'TodayTrades')
if not positions_df.empty:
    save_to_excel(positions_df, filename, 'Positions')
