from pprint import pprint
import requests
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime, timedelta
import os
import random

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

        # 提取所需字段
        latestTrade_info = []
        for trade in trade_stocks:
            name = trade.get('stkName', 'N/A')
            operation = trade.get('operationType', 'N/A')
            # 使用 latestTrade 的 tradeDate 作为时间
            time_str = trade_date  # 使用 latestTrade 的 tradeDate
            price = trade.get('tradePrice', 'N/A')
            quantity = trade.get('tradeAmount', 'N/A')

            latestTrade_info.append({
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '操作': operation,
                '股票名称': name,
                '价格': price,
                '数量': quantity,
                '时间': time_str,
            })

        positions_info = []
        for position in position_stocks:
            name = position.get('stkName', 'N/A')
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
                '名称': name,
                '行业': industry,
                '价格': price,
                '持仓日期': position_date_str,
                '持仓比例': position_ratio,
                '盈亏比例': profit_and_loss_ratio,
            })

        return latestTrade_info, positions_info, trade_date
    else:
        print(f"请求失败，状态码: {response.status_code}，策略ID: {strategy_id}")
        return [], [], 'N/A'

def save_to_excel(df, filename, sheet_name, index=False):
    if not os.path.exists(filename):
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
    else:
        try:
            with pd.ExcelFile(filename) as xls:
                if sheet_name in xls.sheet_names:
                    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                        existing_df = pd.read_excel(xls, sheet_name=sheet_name)
                        combined_df = pd.concat([existing_df, df], ignore_index=True).drop_duplicates()
                        combined_df.to_excel(writer, sheet_name=sheet_name, index=index)
                else:
                    with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                        df.to_excel(writer, sheet_name=sheet_name, index=index)
        except Exception as e:
            print(f"读取或写入Excel文件时发生错误: {e}")

def simulate_trading(trades_df):
    import akshare as ak

    trading_log = []
    portfolio = {}

    for _, row in trades_df.iterrows():
        stock_name = row['股票名称']
        operation = row['操作']
        price = float(row['价格'])
        quantity = int(row['数量'])  # 确保数量是整数
        time = row['时间']

        if operation == 'BUY':
            if stock_name not in portfolio:
                portfolio[stock_name] = {'quantity': quantity, 'buy_price': price}
            else:
                portfolio[stock_name]['quantity'] += quantity
                portfolio[stock_name]['buy_price'] = (portfolio[stock_name]['quantity'] * portfolio[stock_name]['buy_price'] + quantity * price) / (portfolio[stock_name]['quantity'] + quantity)

            trading_log.append({
                '时间': time,
                '操作': operation,
                '股票名称': stock_name,
                '价格': price,
                '数量': quantity,
                '盈亏': 'N/A',
                '盈亏比例': 'N/A'
            })
        elif operation == 'SALE':
            if stock_name in portfolio:
                buy_price = portfolio[stock_name]['buy_price']
                held_quantity = portfolio[stock_name]['quantity']

                if quantity > held_quantity:
                    print(f"卖出数量 {quantity} 超过持有数量 {held_quantity}，股票名称: {stock_name}")
                    continue

                sell_value = price * quantity
                buy_value = buy_price * quantity
                profit = sell_value - buy_value
                profit_ratio = (profit / buy_value) * 100

                trading_log.append({
                    '时间': time,
                    '操作': operation,
                    '股票名称': stock_name,
                    '价格': price,
                    '数量': quantity,
                    '盈亏': profit,
                    '盈亏比例': f"{profit_ratio:.2f}%"
                })

                portfolio[stock_name]['quantity'] -= quantity
                if portfolio[stock_name]['quantity'] == 0:
                    del portfolio[stock_name]

    trading_log_df = pd.DataFrame(trading_log)
    return trading_log_df

def generate_random_trades(num_days=10):
    stocks = ['网宿科技', '豆神教育', '华闻集团', '光线传媒', '其他股票1', '其他股票2']
    operations = ['BUY', 'SALE']
    start_date = datetime.now() - timedelta(days=num_days)

    all_trades = []

    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime('%Y%m%d')

        num_trades = random.randint(2, 5)  # 每天随机生成2到5笔交易

        for _ in range(num_trades):
            stock = random.choice(stocks)
            operation = random.choice(operations)
            price = round(random.uniform(5, 20), 2)  # 随机生成价格在5到20之间
            quantity = random.randint(100, 1000) * 100  # 随机生成数量是100的倍数

            all_trades.append({
                '策略名称': '随机策略',
                '操作': operation,
                '股票名称': stock,
                '价格': price,
                '数量': quantity,
                '时间': date_str
            })

    return pd.DataFrame(all_trades)

# 加载现有的交易数据
try:
    existing_trades_df = pd.read_excel('trades.xlsx', sheet_name='AllTrades')
except FileNotFoundError:
    existing_trades_df = pd.DataFrame(columns=['策略名称', '操作', '股票名称', '价格', '数量', '时间'])

# # 生成随机交易数据
# random_trades_df = generate_random_trades()
# # 打印随机生成的交易数据
# print("随机生成的交易数据:")
# print(random_trades_df)
# # 合并现有的交易数据和随机生成的数据
# combined_trades_df = pd.concat([existing_trades_df, random_trades_df], ignore_index=True).drop_duplicates()

# 打印合并后的交易数据
# print("合并后的交易数据:")
# print(combined_trades_df)

# 创建当天交易信息的 DataFrame
current_date = datetime.now().date().strftime('%Y%m%d')
print(current_date)
# today_trades_df = combined_trades_df[combined_trades_df['时间'] == current_date]
# # 打印当天交易信息
print("\n当天交易信息:")
print(today_trades_df)

# 保存交易信息到 Excel
# save_to_excel(today_trades_df, 'trades.xlsx', 'TodayTrades')
# save_to_excel(combined_trades_df, 'trades.xlsx', 'AllTrades')

# 模拟交易并记录操作日志
# trading_log_df = simulate_trading(today_trades_df)
# print("\n交易操作日志:")
# print(trading_log_df)

# 保存交易操作日志到 Excel
# save_to_excel(trading_log_df, 'trading_log.xlsx', 'TradingLog')
