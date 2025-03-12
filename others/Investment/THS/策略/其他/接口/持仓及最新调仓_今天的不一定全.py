import requests
from fake_useragent import UserAgent

from others.Investment.THS.策略.其他.工具包.determine_market_with_code import determine_market


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