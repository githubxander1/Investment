from datetime import datetime

import pandas as pd
import requests
from fake_useragent import UserAgent

from others.量化投资.THS.自动化交易_同花顺.config.settings import Strategy_ids
from others.量化投资.THS.自动化交易_同花顺.utils.determine_market import determine_market

# 手动创建策略ID到策略名称的映射

strategy_id_to_name = {
    '155259': 'TMT资金流入战法',
    '155680': 'GPT定期精选',
    '138036': '低价小盘股战法',
    '155270': '中字头概念',
    '137789': '高现金毛利战法',
    '138006': '连续五年优质股战法',
    '136567': '净利润同比大增低估值战法',
    '138127': '归母净利润高战法',
    '118188': '均线粘合平台突破'
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
                '价格': round(price, 3),
                '持仓比例': position_ratio,
                '盈亏比例': profit_and_loss_ratio,
                '持仓日期': position_date_str,
            })

        return positions_info
    else:
        print(f"请求失败，状态码: {response.status_code}，策略ID: {strategy_id}")
        return []

def save_to_excel(df, filename, sheet_name, index=False):
    # 保存DataFrame到Excel文件
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index)

def main():
    # 要查询的策略ID列表
    strategy_ids = Strategy_ids

    # 存储所有策略的持仓信息
    all_positions_info = []

    # 遍历每个策略ID，获取其持仓信息
    for strategy_id in strategy_ids:
        positions_info = fetch_strategy_profit(strategy_id)
        all_positions_info.extend(positions_info)
    positions_df = pd.DataFrame(all_positions_info)
    #去掉股票代码列
    positions_df_without_code = positions_df.drop(columns=['股票代码', '市场'])
    print(positions_df_without_code)

    # 创建DataFrame
    last_positions_df = pd.DataFrame(all_positions_info)

    # 检查是否有数据并保存
    if not last_positions_df.empty:
        positions_file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\data\策略最新持仓_所有.xlsx'
        save_to_excel(last_positions_df, positions_file_path, '策略最新持仓')
    else:
        print("No position data to save.")

def job():
    if datetime.now().weekday() < 5:  # 0-4 对应周一到周五
        main()

# schedule.every().day.at("09:32").do(job)

if __name__ == '__main__':
    main()
