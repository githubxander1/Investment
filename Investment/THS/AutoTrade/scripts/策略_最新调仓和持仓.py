from datetime import datetime
import pandas as pd
import requests
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import logging

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../../new/策略/strategy_fetch.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 导入配置
from Investment.THS.AutoTrade.config.settings import Strategy_ids, Strategy_id_to_name, Strategy_info_file
from Investment.THS.AutoTrade.utils.determine_market import determine_market

# 策略ID到策略名称的映射
# strategy_id_to_name = {
#     '155259': 'TMT资金流入战法',
#     '155680': 'GPT定期精选',
#     '155273': '国资云',
#     '138036': '低价小盘股战法',
#     '155270': '中字头概念',
#     '137789': '高现金毛利战法',
#     '138006': '连续五年优质股战法',
#     '136567': '净利润同比大增低估值战法',
#     '138127': '归母净利润高战法',
#     '118188': '均线粘合平台突破'
# }

def parse_position_date(date_value):
    """统一解析日期时间值"""
    if date_value == 'N/A':
        return 'N/A'

    if isinstance(date_value, int):
        try:
            # 处理毫秒时间戳
            position_date_s = date_value / 1000
            position_date = datetime.fromtimestamp(position_date_s)
            return position_date.strftime('%Y-%m-%d %H:%M:%S')
        except (OverflowError, OSError, ValueError) as e:
            logging.error(f"日期转换失败: {str(e)}")
            return 'Invalid Date'

    if isinstance(date_value, str):
        # 尝试常见日期格式解析
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y-%m-%d', '%Y%m%d'):
            try:
                d = datetime.strptime(date_value, fmt)
                return d.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue

    return 'Invalid Date'

def get_strategy_name(strategy_id):
    """获取策略名称，优先使用本地映射，否则标记为未知策略"""
    name = Strategy_id_to_name.get(str(strategy_id), None)
    if name is None:
        logging.warning(f"发现未映射的策略ID: {strategy_id}")
        return f"未知策略({strategy_id})"
    return name

def fetch_strategy_profit(strategy_id):
    """获取指定策略的收益信息"""
    ua = UserAgent()
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
    params = {"strategyId": strategy_id}
    headers = {"User-Agent": ua.random}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        position_stocks = data.get('result', {}).get('positionStocks', [])
        # 提取positionStocks所需字段
        positions_info = []
        for position in position_stocks:
            try:
                # 提取基础信息
                name = position.get('stkName', 'N/A')
                code = position.get('stkCode', 'N/A').split('.')[0]
                market = determine_market(code)
                industry = position.get('industry', 'N/A')

                # 处理数值字段
                price = float(position.get('price', 0)) if position.get('price') not in (None, '') else 'N/A'
                position_ratio = float(position.get('positionRatio', 0)) if position.get('positionRatio') not in (None, '') else 'N/A'
                profit_and_loss_ratio = float(position.get('profitAndLossRatio', 0)) if position.get('profitAndLossRatio') not in (None, '') else 'N/A'

                # 格式化百分比
                if isinstance(position_ratio, (int, float)):
                    position_ratio = f"{position_ratio * 100:.2f}%"
                if isinstance(profit_and_loss_ratio, (int, float)):
                    profit_and_loss_ratio = f"{profit_and_loss_ratio * 100:.2f}%"

                # 处理日期
                position_date_str = parse_position_date(position.get('positionDate', 'N/A'))

                # 添加持仓信息
                positions_info.append({
                    '策略名称': get_strategy_name(strategy_id),
                    '股票名称': name,
                    '股票代码': code,
                    '市场': market,
                    '行业': industry,
                    '价格': round(price, 3) if isinstance(price, (int, float)) else price,
                    '持仓比例': position_ratio,
                    '盈亏比例': profit_and_loss_ratio,
                    '持仓日期': position_date_str,
                })

            except Exception as e:
                logging.error(f"处理单个持仓信息时出错: {str(e)}")
                continue

        logging.info(f"成功获取策略 {strategy_id} 的 {len(positions_info)} 条持仓信息")
        return positions_info

    except requests.exceptions.RequestException as e:
        logging.error(f"请求策略 {strategy_id} 数据失败: {str(e)}")
        return []

def save_to_csv(df, file_path):
    """保存DataFrame到CSV文件"""
    try:
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        logging.info(f"数据已成功保存至 {file_path}")
    except Exception as e:
        logging.error(f"保存CSV文件失败: {str(e)}")

def main():
    """主函数"""
    all_positions_info = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetch_strategy_profit, sid) for sid in Strategy_ids]

        for future in futures:
            try:
                result = future.result()
                if result:
                    all_positions_info.extend(result)
            except Exception as e:
                logging.error(f"执行线程时发生错误: {str(e)}")

    if all_positions_info:
        positions_df = pd.DataFrame(all_positions_info)

        # 打印结果（不包含股票代码和市场列）
        positions_df_without_code = positions_df.drop(columns=['股票代码', '市场'], errors='ignore')
        print("\n持仓信息：")
        print(positions_df_without_code.to_string(index=False))

        # 保存完整数据
        save_to_csv(positions_df, Strategy_info_file)
    else:
        logging.info("没有获取到任何持仓数据需要保存")

def job():
    """定时任务入口"""
    if datetime.now().weekday() < 5:  # 0-4 对应周一到周五
        main()

if __name__ == '__main__':
    main()
