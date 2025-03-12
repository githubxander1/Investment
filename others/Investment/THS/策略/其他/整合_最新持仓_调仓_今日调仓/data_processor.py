from datetime import datetime

def determine_market(stock_code):
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

def extract_latest_trade_info(data, strategy_id, strategy_id_to_name):
    latest_trade = data.get('result', {}).get('latestTrade', {})
    trade_date = latest_trade.get('tradeDate', 'N/A')
    trade_stocks = latest_trade.get('tradeStocks', [])

    latestTrade_info = []
    for trade in trade_stocks:
        name = trade.get('stkName', 'N/A')
        code = trade.get('stkCode', 'N/A').split('.')[0]
        market = determine_market(code)
        operation = trade.get('operationType', 'N/A')
        time_str = trade_date
        price = trade.get('tradePrice', 'N/A')
        quantity = trade.get('tradeAmount', 'N/A')

        latestTrade_info.append({
            '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
            '操作': operation,
            '股票名称': name,
            '市场': market,
            '价格': price,
            '数量': quantity,
            '时间': time_str,
        })

    return latestTrade_info

def extract_latest_positions_info(data, strategy_id, strategy_id_to_name):
    position_stocks = data.get('result', {}).get('positionStocks', [])

    positions_info = []
    for position in position_stocks:
        name = position.get('stkName', 'N/A')
        code = position.get('stkCode', 'N/A').split('.')[0]
        market = determine_market(code)
        industry = position.get('industry', 'N/A')
        price = position.get('price', 'N/A')
        position_date_ms = position.get('positionDate', 'N/A')
        position_ratio = position.get('positionRatio', 'N/A')
        profit_and_loss_ratio = position.get('profitAndLossRatio', 'N/A')

        if isinstance(position_date_ms, int):
            position_date_s = position_date_ms / 1000
            position_date = datetime.fromtimestamp(position_date_s)
            position_date_str = position_date.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(position_date_ms, str):
            position_date_str = position_date_ms
        else:
            position_date_str = 'N/A'

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

    return positions_info
