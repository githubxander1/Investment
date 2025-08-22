import time
# from pprint import pprint

import fake_useragent
import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import Strategy_id_to_name, Strategy_ids, Ai_Strategy_holding_file, \
    Strategy_portfolio_today_file
from Investment.THS.AutoTrade.pages.page_common import CommonPage
from Investment.THS.AutoTrade.scripts.data_process import write_operation_history
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
import os
import datetime
from Investment.THS.AutoTrade.utils.format_data import determine_market, normalize_time

logger = setup_logger(__name__)
trader = TradeLogic()
ua = fake_useragent.UserAgent()
def get_latest_position(strategy_id):
    """单接口：获取并提取保存今日数据"""
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit?strategyId={strategy_id}"
    headers = {"User-Agent": ua.random}

    try:
        data = requests.get(url, headers=headers, timeout=10)
        data.raise_for_status()
        data = data.json()
        # logger.info(f"策略 获取数据成功id:{strategy_id} {Strategy_id_to_name.get(strategy_id, '未知策略')} ")
        # pprint(data)

        result = data.get('result', {})
        latest_trade_infos = result.get('latestTrade', {})
        position_stocks = result.get('positionStocks', {})

        # 计算lastest_trade_infos和position_stocks里各有多少条数据
        trade_count = len(latest_trade_infos.get('tradeStocks', []))
        position_count = len(position_stocks)
        lastest_trade_date = normalize_time(latest_trade_infos.get('tradeDate', ''))
        # logger.info(f"策略 {strategy_id} 获取数据成功，持仓数据: {position_count} 条，{lastest_trade_date}交易数据: {trade_count} 条")

        # today = datetime.datetime.now().date()
        # yestoday = (datetime.date.today() - datetime.timedelta(days=1))
        position_stocks_results = []
        for position_stock_info in position_stocks:
            stk_code = str(position_stock_info.get('stkCode', '').split('.')[0]).zfill(6)
            position_stocks_results.append({
                '名称': Strategy_id_to_name.get(strategy_id, '未知策略'),
                '操作': '买入',
                '标的名称': position_stock_info.get('stkName', ''),
                '代码': str(position_stock_info.get('stkCode', '').split('.')[0]).zfill(6),
                '市场': determine_market(stk_code),
                '最新价': round(float(position_stock_info.get('price', 0)), 2),
                '盈亏比例%': round(float(position_stock_info.get('profitAndLossRatio', 0)) * 100, 2),
                '新比例%': round(float(position_stock_info.get('positionRatio', 0)) * 100, 2),
                '时间': position_stock_info.get('positionDate', ''),
                '行业': position_stock_info.get('industry', ''),
            })

        position_stocks_df = pd.DataFrame(position_stocks_results)
        # 提取市场为 沪深A股的数据，去掉st的
        position_stocks_df = position_stocks_df[position_stocks_df['市场'] == '沪深A股']
        # 去掉名称含st的
        # position_stocks_df = position_stocks_df[~position_stocks_df['标的名称'].str.contains('ST')]
        # print(position_stocks_df)

        # today = str(datetime.date.today())
        # position_stocks_df.to_excel('AiStrategy_position.xlsx', sheet_name= today,index=False)
        return position_stocks_df
    except requests.RequestException as e:
        # logger.error(f"请求失败 (Strategy ID: {strategy_id}): {e}")
        return []


def get_difference_holding():
    """
    对比 AiStrategy_position.xlsx 中当天和前一天的持仓数据，找出买入和卖出标的
    - 如果昨天sheet不存在，将今天所有持仓视为买入
    - 如果文件不存在，直接退出
    """
    file_path = Ai_Strategy_holding_file
    today = str(datetime.date.today())
    today_date = datetime.date.today()

    # ✅ 日期调整逻辑
    if today_date.weekday() == 0:  # 周一
        yestoday_date = today_date - datetime.timedelta(days=3)  # 上周五
        logger.info(f"📅 周一特殊处理：对比日期调整为 {yestoday_date}")
    else:
        yestoday_date = today_date - datetime.timedelta(days=1)  # 普通日期

    yestoday = str(yestoday_date)

    # ✅ 文件不存在直接退出
    if not os.path.exists(file_path):
        logger.error(f"❌ 文件 {file_path} 不存在，程序退出")
        return {'to_buy': pd.DataFrame(), 'to_sell': pd.DataFrame()}

    # 读取Excel文件
    try:
        with pd.ExcelFile(file_path) as xls:
            # ✅ 今天sheet不存在，直接退出
            if today not in xls.sheet_names:
                logger.warning(f"❌ 今天 {today} 的sheet不存在，返回空")
                return {'to_buy': pd.DataFrame(), 'to_sell': pd.DataFrame()}

            # ✅ 读取今天持仓数据
            today_positions_df = pd.read_excel(xls, sheet_name=today, index_col=0)

            # ✅ 特殊处理：周一且周日sheet不存在时
            if yestoday not in xls.sheet_names and today_date.weekday() == 0:
                logger.warning(f"⚠️ 周一特殊处理：未找到 {yestoday} 的sheet，尝试查找最近交易日")

                # ✅ 查找最近存在的sheet（倒序查找5个工作日）
                for i in range(1, 6):  # 最多查找前5个工作日
                    recent_date = today_date - datetime.timedelta(days=i)
                    if str(recent_date) in xls.sheet_names:
                        yestoday = str(recent_date)
                        logger.info(f"🔁 找到最近交易日：{yestoday}")
                        yestoday_positions_df = pd.read_excel(xls, sheet_name=yestoday, index_col=0)
                        break
                else:
                    # ✅ 如果没有找到任何历史sheet，将今天所有持仓视为买入
                    logger.info(f"🆕 未找到历史sheet，将今天所有持仓视为买入")
                    today_positions_df['操作'] = '买入'
                    return {
                        'to_buy': today_positions_df,
                        'to_sell': pd.DataFrame()
                    }
            elif yestoday not in xls.sheet_names:
                # ✅ 非周一的常规处理
                logger.info(f"⚠️ 昨天 {yestoday} 的sheet不存在，将今天所有持仓视为买入")
                today_positions_df['操作'] = '买入'
                return {
                    'to_buy': today_positions_df,
                    'to_sell': pd.DataFrame()
                }
            else:
                # ✅ 正常读取昨天数据
                yestoday_positions_df = pd.read_excel(xls, sheet_name=yestoday, index_col=0)

    except Exception as e:
        logger.error(f"❌ 读取Excel文件失败: {str(e)}")
        return {'to_buy': pd.DataFrame(), 'to_sell': pd.DataFrame()}

    # ✅ 数据对比逻辑（保持不变）
    today_stocks = set(today_positions_df['标的名称'].str.strip().str.upper())
    yestoday_stocks = set(yestoday_positions_df['标的名称'].str.strip().str.upper())

    # ✅ 找出买入和卖出
    to_buy_df = today_positions_df[~today_positions_df['标的名称'].isin(yestoday_stocks)].copy()
    to_sell_df = yestoday_positions_df[~yestoday_positions_df['标的名称'].isin(today_stocks)].copy()

    # ✅ 添加操作列
    to_buy_df['操作'] = '买入'
    to_sell_df['操作'] = '卖出'

    # ✅ 输出结果
    logger.info(f"📊 今日({today})持仓标的: {today_positions_df['标的名称'].tolist()}")
    logger.info(f"📊 对比日期: {yestoday}")
    logger.info(f"✅ 要买入标的:\n{to_buy_df[['标的名称']]}\n")
    logger.info(f"✅ 要卖出标的:\n{to_sell_df[['标的名称']]}\n")

    return {
        'to_buy': to_buy_df,
        'to_sell': to_sell_df
    }

def sava_all_strategy_holding_data():
    """
    获取所有策略的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
    """
    all_holdings = []
    for id in Strategy_ids:
        positions_df = get_latest_position(id)
        if positions_df is not None:
            all_holdings.append(positions_df)
        else:
            logger.info(f"没有获取到策略数据，策略ID: {id}")

    today = str(datetime.date.today())
    all_holdings_df = pd.concat(all_holdings, ignore_index=True)

    file_path = Ai_Strategy_holding_file

    # 创建一个字典来存储所有工作表数据
    all_sheets_data = {}

    try:
        # 如果文件存在，读取现有数据
        if os.path.exists(file_path):
            with pd.ExcelFile(file_path) as xls:
                existing_sheets = xls.sheet_names

            # 读取除今天以外的所有现有工作表
            with pd.ExcelFile(file_path) as xls:
                for sheet_name in existing_sheets:
                    if sheet_name != today:
                        all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name, index_col=0)

        # 将今天的数据放在第一位
        all_sheets_data = {today: all_holdings_df, **all_sheets_data}

        # 写入所有数据到Excel文件（覆盖模式）
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
            for sheet_name, df in all_sheets_data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=True)

        logger.info(f"✅ 所有持仓数据已保存，{today} 数据位于第一个 sheet，共 {len(all_holdings_df)} 条")

    except Exception as e:
        logger.error(f"❌ 保存持仓数据失败: {e}")
        # 如果出错，至少保存今天的数据
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                all_holdings_df.to_excel(writer, sheet_name=today, index=True)
            logger.info(f"✅ 文件保存完成，sheet: {today}")
        except Exception as e2:
            logger.error(f"❌ 保存今日数据也失败了: {e2}")
def Smain():
    sava_all_strategy_holding_data()
    time.sleep(2)
    diff_result = get_difference_holding()
    logger.info(f"持仓数据差异:{len(diff_result)}条 \n{diff_result}")

    # 初始化combined_df为空的DataFrame
    combined_df = pd.DataFrame()

    if diff_result:
        to_buy = diff_result.get('to_buy')
        to_sell = diff_result.get('to_sell')

        if not to_buy.empty or not to_sell.empty:
            logger.info(
                f"发现持仓差异，准备执行交易操作：买入 {len(to_buy)} 只，卖出 {len(to_sell)} 只")
            # 合并买入/卖出数据
            combined_df = pd.concat([
                to_buy[['标的名称', '操作']],
                to_sell[['标的名称', '操作']]
            ], ignore_index=True)
    return combined_df

def operate_result():
    diff_result_df = Smain()

    # 检查返回的DataFrame是否为空
    if diff_result_df.empty:
        logger.info("✅ 当前无持仓差异，无需执行交易")
    else:
        # 按操作类型分组，优先执行卖出操作
        sell_operations = diff_result_df[diff_result_df['操作'] == '卖出']
        buy_operations = diff_result_df[diff_result_df['操作'] == '买入']

        # 合并操作，将卖出操作放在前面
        ordered_operations = pd.concat([sell_operations, buy_operations], ignore_index=True)

        # 准备保存到今日调仓文件的数据
        today_trades = []

        # 遍历每一行，执行交易
        for index, row in ordered_operations.iterrows():
            stock_name = row['标的名称']
            operation = row['操作']
            # 修复：从原始数据中获取策略名称，而不是从合并后的DataFrame中
            # strategy_name = row['名称']

            logger.info(f"🛠️ 要处理: {operation} {stock_name}")

            # 特殊处理：卖出时全仓卖出
            if operation == "卖出":
                new_ratio = 0
            else:
                new_ratio = None  # 买入时无需新比例

            # 切换到对应账户
            common_page = CommonPage()
            common_page.change_account('川财证券')
            logger.info(f"✅ 已切换到账户: 川财证券")

            # 调用交易逻辑
            status, info = trader.operate_stock(
                operation=operation,
                stock_name=stock_name,
                volume=200 if operation == "买入" else None,
                new_ratio=new_ratio
            )

            # 检查交易是否成功执行
            if status is None:
                logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                continue

            # 构造记录
            # operate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            operate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            record = pd.DataFrame([{
                '标的名称': stock_name,
                '操作': operation,
                '新比例%': new_ratio if new_ratio is not None else 0,
                '状态': status,
                '信息': info,
                '时间': operate_time
            }])

            # 写入历史
            write_operation_history(record)
            logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

            # 添加到今日调仓数据中，用于保存到Strategy_portfolio_today.xlsx
            today_trades.append({
                '名称': 'AI市场追踪策略',  # 默认策略名称
                '操作': operation,
                '标的名称': stock_name,
                '代码': '',  # 代码信息在当前数据中不可用
                '最新价': 0,  # 价格信息在当前数据中不可用
                '新比例%': new_ratio if new_ratio is not None else 0,
                '市场': '沪深A股',  # 默认市场
                '时间': datetime.datetime.now().strftime('%Y-%m-%d')
            })

        # 将今日调仓数据保存到Strategy_portfolio_today.xlsx
        if today_trades:
            today_trades_df = pd.DataFrame(today_trades)
            today = datetime.datetime.now().strftime('%Y-%m-%d')

            try:
                # 如果文件存在，读取现有数据
                if os.path.exists(Strategy_portfolio_today_file):
                    with pd.ExcelFile(Strategy_portfolio_today_file) as xls:
                        # 读取除今天以外的所有现有工作表
                        all_sheets_data = {}
                        for sheet_name in xls.sheet_names:
                            if sheet_name != today:
                                all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

                    # 将今天的数据放在第一位
                    all_sheets_data = {today: today_trades_df, **all_sheets_data}
                else:
                    # 文件不存在，创建新文件
                    all_sheets_data = {today: today_trades_df}

                # 写入所有数据到Excel文件
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    for sheet_name, df in all_sheets_data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)

                logger.info(f"✅ 今日调仓数据已保存到 {Strategy_portfolio_today_file}，sheet: {today}")
            except Exception as e:
                logger.error(f"❌ 保存今日调仓数据失败: {e}")
if __name__ == '__main__':
    file_path = Ai_Strategy_holding_file
    # if os.path.exists(file_path):
        # print(f"文件 {file_path} 已存在，请勿重复生成")
    # get_latest_position(156275)
    # get_difference_holding()
    # Smain()
    operate_result()
