import time
import sys
import os
import datetime
import traceback
from datetime import datetime as dt
from pprint import pprint

import fake_useragent
import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import Strategy_id_to_name, Strategy_ids, Ai_Strategy_holding_file, \
    Strategy_portfolio_today_file, OPERATION_HISTORY_FILE, Account_holding_file, Strategy_holding_file
from Investment.THS.AutoTrade.pages.account_info import AccountInfo
from Investment.THS.AutoTrade.pages.page_common import CommonPage
from Investment.THS.AutoTrade.scripts.data_process import write_operation_history, save_to_excel_append, read_operation_history
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.format_data import determine_market, normalize_time
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger(__name__)
trader = TradeLogic()
ua = fake_useragent.UserAgent()
common_page = CommonPage()

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
        allProfit = round(result.get('allProfit', 0),2)
        allProfitPrice = round(result.get('allProfitPrice', 0),2)
        foundDate = result.get('foundDate', '')
        todayProfit = round(result.get('todayProfit', 0),2)
        todayProfitPrice = round(result.get('todayProfitPrice', 0),2)
        logger.info(f"{strategy_id} 成立时间: {foundDate}, 总盈亏: {allProfitPrice}({allProfit}%), 今日盈亏: {todayProfit}% 盈亏金额: {todayProfitPrice}, \n今日交易数据: {trade_count} 条,持仓数据: {position_count} 条, ")

        # today = datetime.datetime.now().date()
        # yestoday = (datetime.date.today() - datetime.timedelta(days=1))
        position_stocks_results = []
        for position_stock_info in position_stocks:
            stk_code = str(position_stock_info.get('stkCode', '').split('.')[0]).zfill(6)
            position_stocks_results.append({
                '名称': Strategy_id_to_name.get(strategy_id, '未知策略'),
                # '操作': '买入',
                '标的名称': position_stock_info.get('stkName', ''),
                '代码': str(position_stock_info.get('stkCode', '').split('.')[0]).zfill(6),
                '市场': determine_market(stk_code),
                '最新价': round(float(position_stock_info.get('price', 0)), 2),# 成交价
                '盈亏比例%': round(float(position_stock_info.get('profitAndLossRatio', 0)) * 100, 2),
                '新比例%': round(float(position_stock_info.get('positionRatio', 0)) * 100, 2),# 持仓比例
                '时间': position_stock_info.get('positionDate', ''),#持仓时间
                '行业': position_stock_info.get('industry', ''),
            })

        position_stocks_df = pd.DataFrame(position_stocks_results)
        return position_stocks_df
    except requests.RequestException as e:
        logger.error(f"请求失败 (Strategy ID: {strategy_id}): {e}")
        return []


def get_difference_holding():
    """
    对比账户实际持仓与策略今日持仓数据，找出差异：
        - 需要卖出：在账户中存在，但不在策略今日持仓中；
        - 需要买入：在策略今日持仓中存在，但不在账户中；
    """
    logger.info("开始对比账户实际持仓与策略今日持仓数据...")
    try:
        # 检查必要文件是否存在
        required_files = {
            "账户持仓文件": Account_holding_file,
            "策略持仓文件": Ai_Strategy_holding_file,
        }

        for file_desc, file_path in required_files.items():
            if not os.path.exists(file_path):
                logger.error(f"{file_desc}不存在: {file_path}")
                return {"error": f"{file_desc}不存在"}

        # 更新川财证券账户持仓数据
        logger.info("正在更新川财证券账户持仓数据...")
        account_info = AccountInfo()
        update_success = account_info.update_holding_info_for_account("川财证券")
        if not update_success:
            logger.warning("更新川财证券账户持仓数据失败")
            return {"error": "更新川财证券账户持仓数据失败"}

        logger.info("✅ 川财证券账户持仓数据更新完成")

        # 读取川财证券账户持仓数据
        account_df = pd.DataFrame()
        try:
            with pd.ExcelFile(Account_holding_file, engine='openpyxl') as xls:
                # 只读取川财证券的持仓数据
                sheet_name = "川财证券_持仓数据"
                if sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    if not df.empty and '标的名称' in df.columns:
                        # 只保留标的名称列
                        account_df = df[['标的名称']].copy()
                        account_df['账户'] = "川财证券"
                        logger.info(f"✅ 成功读取川财证券账户的持仓数据，共 {len(account_df)} 条记录")
                    else:
                        logger.warning(f"川财证券账户持仓数据为空或不包含标的名称列")
                else:
                    logger.warning(f"账户文件中没有川财证券的持仓数据表: {sheet_name}")
        except Exception as e:
            logger.error(f"读取川财证券账户持仓文件失败: {e}")
            return {"error": "读取川财证券账户持仓文件失败"}

        if account_df.empty:
            logger.info("川财证券账户无持仓数据")

        # 读取策略今日持仓数据
        today = str(datetime.date.today())
        try:
            if os.path.exists(Ai_Strategy_holding_file):
                with pd.ExcelFile(Ai_Strategy_holding_file, engine='openpyxl') as xls:
                    if today in xls.sheet_names:
                        strategy_df = pd.read_excel(xls, sheet_name=today)
                        if strategy_df.empty:
                            logger.warning("策略持仓文件为空")
                            strategy_df = pd.DataFrame(columns=['标的名称'])
                    else:
                        logger.warning(f"策略持仓文件中没有今天的sheet: {today}")
                        strategy_df = pd.DataFrame(columns=['标的名称'])
            else:
                logger.warning("策略持仓文件不存在")
                strategy_df = pd.DataFrame(columns=['标的名称'])
        except Exception as e:
            logger.error(f"读取策略持仓文件失败: {e}")
            strategy_df = pd.DataFrame(columns=['标的名称'])

        # logger.info(f"川财证券账户持仓数据:\n{account_df[['标的名称']] if not account_df.empty else '无数据'}\n")
        if not strategy_df.empty:
            logger.info(f"策略今日持仓数据:{len(strategy_df)} 条记录)\n{strategy_df[['标的名称']]}\n")

        # 需要排除的标的名称
        excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

        # 1. 找出需要卖出的标的（在账户中存在，但不在策略今日持仓中，且不在排除列表中）
        if not account_df.empty and not strategy_df.empty:
            to_sell_candidates = account_df[~account_df['标的名称'].isin(strategy_df['标的名称'])]
            to_sell = to_sell_candidates[~to_sell_candidates['标的名称'].isin(excluded_holdings)].copy()
        elif not account_df.empty:
            # 如果策略持仓为空，则所有账户持仓都是需要卖出的（除去排除项）
            to_sell = account_df[~account_df['标的名称'].isin(excluded_holdings)].copy()
        else:
            to_sell = pd.DataFrame(columns=account_df.columns) if not account_df.empty else pd.DataFrame()

        if not to_sell.empty:
            logger.warning(f"⚠️ 发现需卖出的标的: {len(to_sell)} 条")
            logger.info(f"\n{to_sell[['标的名称']] if '标的名称' in to_sell.columns else to_sell}")
            # 添加操作列
            to_sell['操作'] = '卖出'
        else:
            logger.info("✅ 当前无需卖出的标的")

        # 2. 找出需要买入的标的（在策略今日持仓中存在，但不在账户中，且不在排除列表中）
        if not strategy_df.empty and not account_df.empty:
            to_buy_candidates = strategy_df[~strategy_df['标的名称'].isin(account_df['标的名称'])]
            to_buy = to_buy_candidates[~to_buy_candidates['标的名称'].isin(excluded_holdings)]
        elif not strategy_df.empty:
            # 如果账户持仓为空，则所有策略持仓都是需要买入的（除去排除项）
            to_buy = strategy_df[~strategy_df['标的名称'].isin(excluded_holdings)]
        else:
            to_buy = pd.DataFrame(columns=['标的名称'])

        if not to_buy.empty:
            logger.warning(f"⚠️ 发现需买入的标的: {len(to_buy)} 条")
            logger.info(f"\n{to_buy[['标的名称']] if '标的名称' in to_buy.columns else to_buy}")
            # 添加操作列
            to_buy['操作'] = '买入'
        else:
            logger.info("✅ 当前无需买入的标的")

        # 构建完整差异报告
        difference_report = {
            "to_sell": to_sell,
            "to_buy": to_buy
        }

        return difference_report

    except Exception as e:
        error_msg = f"处理持仓差异时发生错误: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}



def sava_all_strategy_holding_data():
    """
    获取所有策略的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
    """
    all_holdings = []
    for id in Strategy_ids:
        positions_df = get_latest_position(id)
        # 只保留沪深A股的
        positions_df = positions_df[positions_df['市场'] == '沪深A股']
        logger.info(f"{id}持仓数据:{len(positions_df)}\n{positions_df}")
        if positions_df is not None and not positions_df.empty:
            all_holdings.append(positions_df)
        else:
            logger.info(f"没有获取到策略数据，策略ID: {id}")

    today = str(datetime.date.today())
    if not all_holdings:
        logger.warning("未获取到任何策略持仓数据")
        return

    all_holdings_df = pd.concat(all_holdings, ignore_index=True)

    file_path = Ai_Strategy_holding_file

    # 创建一个字典来存储所有工作表数据
    all_sheets_data = {}

    try:
        # 如果文件存在，读取现有数据
        if os.path.exists(file_path):
            with pd.ExcelFile(file_path) as xls:
                existing_sheets = xls.sheet_names
                logger.info(f"保存前文件中已存在的工作表: {existing_sheets}")

            # 读取除今天以外的所有现有工作表
            with pd.ExcelFile(file_path) as xls:
                for sheet_name in existing_sheets:
                    if sheet_name != today:
                        # 注意不使用index_col参数
                        all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

        # 将今天的数据放在第一位
        all_sheets_data = {today: all_holdings_df, **all_sheets_data}
        logger.info(f"即将保存的所有工作表: {list(all_sheets_data.keys())}")

        # 写入所有数据到Excel文件（覆盖模式），注意不保存索引
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
            for sheet_name, df in all_sheets_data.items():
                logger.info(f"正在保存工作表: {sheet_name}")
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        logger.info(f"✅ 所有持仓数据已保存，{today} 数据位于第一个 sheet，共 {len(all_holdings_df)} 条")

    except Exception as e:
        logger.error(f"❌ 保存持仓数据失败: {e}")
        # 如果出错，至少保存今天的数据
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                all_holdings_df.to_excel(writer, sheet_name=today, index=False)
            logger.info(f"✅ 文件保存完成，sheet: {today}")
        except Exception as e2:
            logger.error(f"❌ 保存今日数据也失败了: {e2}")


def get_stock_to_operate(history_file_path, portfolio_file_path):
    """
    获取需要操作的股票列表，避免重复操作
    """
    # 读取操作历史记录
    try:
        history_df = read_operation_history(history_file_path)
    except Exception as e:
        logger.error(f"读取操作历史记录失败: {e}")
        history_df = pd.DataFrame(columns=['标的名称', '操作', '新比例%'])

    # 读取今日调仓数据
    try:
        import datetime as dt
        today = dt.now().strftime('%Y-%m-%d')
        with pd.ExcelFile(portfolio_file_path) as xls:
            if today in xls.sheet_names:
                portfolio_df = pd.read_excel(xls, sheet_name=today)
            else:
                logger.warning(f"今日调仓数据不存在: {today}")
                return pd.DataFrame()
    except Exception as e:
        logger.error(f"读取今日调仓数据失败: {e}")
        return pd.DataFrame()

    if portfolio_df.empty:
        logger.info("✅ 当前无调仓数据，无需执行交易")
        return pd.DataFrame()

    # 筛选出未执行的操作
    to_operate_list = []
    for index, row in portfolio_df.iterrows():
        stock_name = row['标的名称'].strip()
        operation = row['操作'].strip()
        new_ratio = float(row['新比例%']) if pd.notna(row['新比例%']) else 0.0

        # 检查是否已执行 - 使用更精确的匹配
        exists = history_df[
            (history_df['标的名称'] == stock_name) &
            (history_df['操作'] == operation) &
            (abs(history_df['新比例%'] - new_ratio) < 0.01)  # 使用近似相等比较
        ]

        if not exists.empty:
            logger.info(f"✅ 已处理过: {stock_name} {operation} {new_ratio}%")
            continue

        to_operate_list.append(row)

    to_operate_df = pd.DataFrame(to_operate_list)
    logger.info(f"需要执行的操作共 {len(to_operate_df)} 条")
    return to_operate_df


def operate_result(max_retries=3):
    """
    执行调仓操作，包含异常处理和重试机制
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            sava_all_strategy_holding_data()
            time.sleep(2)

            # 获取持仓差异
            diff_result = get_difference_holding()

            if 'error' in diff_result:
                logger.error(f"获取持仓差异失败: {diff_result['error']}")
                return False

            to_sell = diff_result.get('to_sell', pd.DataFrame())
            to_buy = diff_result.get('to_buy', pd.DataFrame())

            # 检查是否需要执行任何操作
            if to_sell.empty and to_buy.empty:
                logger.info("✅ 当前无持仓差异，无需执行交易")
                return True

            # 读取操作历史记录
            try:
                history_df = read_operation_history(OPERATION_HISTORY_FILE)
                logger.info("历史操作记录:")
                logger.info(f"\n{history_df.to_string(index=False) if not history_df.empty else '无历史记录'}")
            except Exception as e:
                logger.error(f"读取操作历史记录失败: {e}")
                history_df = pd.DataFrame(columns=['标的名称', '操作', '新比例%'])

            # 准备所有操作的列表
            all_operations = []

            # 添加卖出操作（先执行卖出）
            if not to_sell.empty:
                logger.info("🔍 检查卖出操作是否已执行...")
                for _, row in to_sell.iterrows():
                    stock_name = row['标的名称']
                    operation = '卖出'
                    new_ratio = 0

                    # 检查是否已在历史记录中
                    if not history_df.empty:
                        exists = history_df[
                            (history_df['标的名称'] == stock_name) &
                            (history_df['操作'] == operation) &
                            (abs(history_df['新比例%'] - new_ratio) < 0.01)
                        ]

                        if not exists.empty:
                            logger.info(f"✅ 卖出 {stock_name} 已在历史记录中存在，跳过")
                            continue

                    all_operations.append({
                        'stock_name': stock_name,
                        'operation': operation,
                        'new_ratio': new_ratio,
                        'strategy_name': 'AI市场追踪策略'
                    })

            # 添加买入操作（后执行买入）
            if not to_buy.empty:
                logger.info("🔍 检查买入操作是否已执行...")
                # 按最新价从低到高排序买入操作
                to_buy_sorted = to_buy.sort_values('最新价', ascending=True)
                logger.info(f"📈 买入顺序（按价格从低到高）: \n{to_buy_sorted[['标的名称', '最新价']].to_string(index=False)}")

                for _, row in to_buy_sorted.iterrows():
                    stock_name = row['标的名称']
                    operation = '买入'
                    new_ratio = None  # 买入时无需新比例

                    # 检查是否已在历史记录中
                    if not history_df.empty:
                        # 对于买入操作，我们检查是否已经买入该股票
                        exists = history_df[
                            (history_df['标的名称'] == stock_name) &
                            (history_df['操作'] == operation)
                        ]

                        if not exists.empty:
                            logger.info(f"✅ 买入 {stock_name} 已在历史记录中存在，跳过")
                            continue

                    all_operations.append({
                        'stock_name': stock_name,
                        'operation': operation,
                        'new_ratio': new_ratio,
                        'strategy_name': 'AI市场追踪策略'
                    })

            # 检查是否有需要执行的操作
            if not all_operations:
                logger.info("✅ 所有操作均已执行过，无需重复操作")
                return True

            # 准备保存到今日调仓文件的数据
            today_trades = []

            # 遍历每一项操作，执行交易
            for op in all_operations:
                stock_name = op['stock_name']
                operation = op['operation']
                new_ratio = op['new_ratio']
                strategy_name = op['strategy_name']

                logger.info(f"🛠️ 要处理: {operation} {stock_name}")

                # 切换到对应账户
                common_page.change_account('川财证券')
                logger.info(f"✅ 已切换到账户: 川财证券")

                # 调用交易逻辑
                status, info = trader.operate_stock(
                    operation=operation,
                    stock_name=stock_name,
                    volume=100 if operation == "买入" else None,
                    new_ratio=new_ratio
                )

                # 检查交易是否成功执行
                if status is None:
                    logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                    continue

                # 构造记录
                operate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                record = pd.DataFrame([{
                    '名称': strategy_name,
                    '标的名称': stock_name,
                    '操作': operation,
                    '新比例%': new_ratio if new_ratio is not None else 0,
                    '状态': status,
                    '信息': info,
                    '账户': '川财证券',  # 执行账户
                    '时间': operate_time
                }])

                # 写入历史
                write_operation_history(record)
                logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

                # 添加到今日调仓数据中
                today_trades.append({
                    '名称': strategy_name,  # 策略名称
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
                    with pd.ExcelWriter(Strategy_portfolio_today_file, engine='openpyxl') as writer:
                        for sheet_name, df in all_sheets_data.items():
                            df.to_excel(writer, sheet_name=sheet_name, index=False)

                    logger.info(f"✅ 今日调仓数据已保存到 {Strategy_portfolio_today_file}，sheet: {today}")
                except Exception as e:
                    logger.error(f"❌ 保存今日调仓数据失败: {e}")

            return True  # 成功执行

        except Exception as e:
            retry_count += 1
            error_msg = f"❌ 第 {retry_count} 次执行出现异常: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)

            # 发送通知
            send_notification(f"策略调仓执行异常: {str(e)}")

            if retry_count < max_retries:
                logger.info(f"等待10秒后进行第 {retry_count + 1} 次重试...")
                time.sleep(10)

                # 尝试重新进入交易页面
                try:
                    common_page.goto_trade_page()
                    logger.info("✅ 成功重新进入交易页面")
                except Exception as page_error:
                    logger.error(f"重新进入交易页面失败: {str(page_error)}")
            else:
                logger.error("❌ 已达到最大重试次数，程序终止")
                send_notification("策略调仓执行失败，已达到最大重试次数")
                return False

    return False


def write_operation_history(df):
    """将操作记录写入Excel文件，按日期作为sheet名，并确保今日sheet位于第一个"""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = OPERATION_HISTORY_FILE

    try:
        # 确保数据包含必要的列
        expected_columns = ['名称', '标的名称', '操作', '新比例%', '状态', '信息', '账户', '时间']
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ''  # 添加缺失的列

        # 重新排列列的顺序
        df = df[expected_columns]

        # 如果文件不存在，创建新文件并将数据保存到第一个 sheet
        if not os.path.exists(filename):
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=today, index=False)
            logger.info(f"✅ 创建并保存数据到Excel文件: {filename}, 表名称: {today} \n{df}")
            return

        # ✅ 先读取今天的sheet已有数据
        with pd.ExcelFile(filename, engine='openpyxl') as xls:
            history_sheets = xls.sheet_names
            old_df = pd.read_excel(xls, sheet_name=today) if today in history_sheets else pd.DataFrame(columns=expected_columns)

        # 合并新旧数据并去重
        combined_df = pd.concat([old_df, df], ignore_index=True)
        combined_df.drop_duplicates(subset=['名称', '标的名称', '操作', '新比例%', '账户'], keep='last', inplace=True)

        # 读取其他 sheet 的数据
        other_sheets_data = {}
        with pd.ExcelFile(filename, engine='openpyxl') as xls:
            for sheet in xls.sheet_names:
                if sheet != today:
                    other_sheets_data[sheet] = pd.read_excel(xls, sheet_name=sheet)

        # 重新写入所有 sheet，确保 today 是第一个
        with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
            combined_df.to_excel(writer, sheet_name=today, index=False)
            for sheet, data in other_sheets_data.items():
                data.to_excel(writer, sheet_name=sheet, index=False)

        logger.info(f"✅ 成功写入操作记录到 {today} 表 {filename}")

    except Exception as e:
        error_info = f"❌ 写入操作记录失败: {e}"
        logger.error(error_info)
        send_notification(error_info)
        raise


if __name__ == '__main__':
    try:
        success = operate_result()
        if success:
            logger.info("✅ 策略调仓执行完成")
        else:
            logger.error("❌ 策略调仓执行失败")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
        sys.exit(0)
    except Exception as e:
        error_msg = f"程序执行出现未捕获异常: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        send_notification(error_msg)
        sys.exit(1)
