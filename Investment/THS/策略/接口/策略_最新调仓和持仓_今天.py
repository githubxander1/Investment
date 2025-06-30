from datetime import datetime

import pandas as pd
import requests
from fake_useragent import UserAgent
# 手动创建策略ID到策略名称的映射
from plyer import notification

strategy_id_to_name = {
    '155259': 'TMT资金流入战法',
    '155680': 'GPT定期精选',
    '138036': '低价小盘股战法',
    # '138386': '主力控盘低价股战法',
    '155270': '中字头概念',
    '137789': '高现金毛利战法',
    '138006': '连续五年优质股战法',
    '136567': '净利润同比大增低估值战法',
    '138127': '归母净利润高战法',
    '118188': '均线粘合平台突破'
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

        # 提取 latestTrade 信息
        latest_trade = data.get('result', {}).get('latestTrade', {})
        trade_date = latest_trade.get('tradeDate', 'N/A')
        trade_stocks = latest_trade.get('tradeStocks', [])

        # 提取latestTrade所需字段
        latestTrade_info = []
        for trade in trade_stocks:
            name = trade.get('stkName', 'N/A')
            code = trade.get('stkCode', 'N/A').split('.')[0]  # 提取股票代码
            market = determine_market(code)  # 判断市场
            operation = trade.get('operationType', 'N/A')
            time_str = trade_date  # 使用 latestTrade 的 tradeDate
            price = trade.get('tradePrice', 'N/A')
            quantity = trade.get('tradeAmount', 'N/A')

            latestTrade_info.append({
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '操作': operation,
                '股票名称': name,
                # '股票代码': code,
                '市场': market,
                '价格': price,
                '数量': quantity,
                '时间': time_str,
            })

        # 提取 positionStocks 信息
        position_stocks = data.get('result', {}).get('positionStocks', [])
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
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index)

def main():
    # 要查询的策略ID列表
    strategy_ids = ['155259', '155270', '137789',
                    '155680', '138006']
    #待卖出国光股份，新华文轩，燕京啤酒后去掉118188

    # 存储所有策略的交易信息和持仓信息
    all_latestTrade_info = []
    all_positions_info = []
    all_today_trades_info = []

    # 当前日期
    current_date = datetime.now().date().strftime('%Y%m%d')

    # 遍历每个策略ID，获取其交易信息和持仓信息
    for strategy_id in strategy_ids:
        latestTrade_info, positions_info, trade_date = fetch_strategy_profit(strategy_id)
        all_latestTrade_info.extend(latestTrade_info)
        all_positions_info.extend(positions_info)

        # 提取当天的交易信息
        today_trades = [trade for trade in latestTrade_info if trade['时间'] == current_date]
        all_today_trades_info.extend(today_trades)

        # 过滤掉创业板股票的交易信息
        all_latestTrade_info = [trade for trade in all_latestTrade_info if not trade['市场'] == '创业板']
        all_today_trades_info = [trade for trade in all_today_trades_info if not trade['市场'] == '创业板']

    # 创建DataFrame
    last_trades_df = pd.DataFrame(all_latestTrade_info)
    last_positions_df = pd.DataFrame(all_positions_info)
    today_trades_df = pd.DataFrame(all_today_trades_info)

    strategy_file_path = '策略最新持仓_所有.xlsx'
    # 检查是否有数据并保存
    if not last_positions_df.empty:
        positions_file_path = strategy_file_path
        save_to_excel(last_positions_df, positions_file_path, '策略最新持仓')
    else:
        print("No position testdata to save.")

    if not last_trades_df.empty:
        trades_file_path = strategy_file_path
        save_to_excel(last_trades_df, trades_file_path, '策略最新调仓')
    else:
        print("No trade testdata to save.")

    if not today_trades_df.empty:
        today_trades_file_path = strategy_file_path
        save_to_excel(today_trades_df, today_trades_file_path, '策略今天调仓')
    else:
        print("No today's trade testdata available.")

    # 打印当天交易信息到控制台
    print("\n当天交易信息:")
    if not today_trades_df.empty:
        print(today_trades_df)
        # 发送系统通知
        notification.notify(
            title="今日调仓提醒",
            message="发现今日有新的调仓操作！策略",
            app_name="量化投资监控",
            timeout=10
        )
    else:
        print("No today's trade testdata available.")


def job():
    if datetime.now().weekday() < 5:  # 0-4 对应周一到周五
        main()

# schedule.every().day.at("09:32").do(job)

if __name__ == '__main__':
    main()
