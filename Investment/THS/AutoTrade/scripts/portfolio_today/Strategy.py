import time
import sys
import os
import datetime
import traceback
from datetime import datetime as dt

import fake_useragent
import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import Strategy_id_to_name, Strategy_ids, Ai_Strategy_holding_file, \
    Strategy_portfolio_today_file, OPERATION_HISTORY_FILE
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
        logger.info(f"交易数据: {trade_count} 条,持仓数据: {position_count} 条")
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

    # 定义昨天的日期：如果周一，则对比日期调整为周五
    yestoday = str(yestoday_date)

    # ✅ 文件不存在直接退出
    if not os.path.exists(file_path):
        logger.error(f"❌ 文件 {file_path} 不存在，程序退出")
        return pd.DataFrame()

    # 读取Excel文件
    try:
        with pd.ExcelFile(file_path) as xls:
            # ✅ 今天sheet不存在，直接退出
            if today not in xls.sheet_names:
                logger.warning(f"❌ 今天 {today} 的sheet不存在，返回空")
                return pd.DataFrame()

            # ✅ 读取今天持仓数据
            today_positions_df = pd.read_excel(xls, sheet_name=today, index_col=0)
            logger.info(f"今天的持仓数据：\n{today_positions_df}")

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
                        logger.info(f"上一交易日持仓数据：{yestoday_positions_df}")
                        break
                else:
                    # ✅ 如果没有找到任何历史sheet，将今天所有持仓视为买入
                    logger.info(f"🆕 未找到历史sheet，将今天所有持仓视为买入")
                    today_positions_df['操作'] = '买入'
                    return today_positions_df
            elif yestoday not in xls.sheet_names:
                # ✅ 非周一的常规处理
                logger.info(f"⚠️ 昨天 {yestoday} 的sheet不存在，将今天所有持仓视为买入")
                today_positions_df['操作'] = '买入'
                return today_positions_df
            else:
                # ✅ 正常读取昨天数据
                yestoday_positions_df = pd.read_excel(xls, sheet_name=yestoday, index_col=0)
                logger.info(f"昨天持仓数据：\n{yestoday_positions_df}")

    except Exception as e:
        logger.error(f"❌ 读取Excel文件失败: {str(e)}")
        return pd.DataFrame()

    # ✅ 数据对比逻辑（保持不变）
    today_stocks = set(today_positions_df['标的名称'].str.strip().str.upper())
    yestoday_stocks = set(yestoday_positions_df['标的名称'].str.strip().str.upper())

    # ✅ 找出买入和卖出
    to_buy_df = today_positions_df[~today_positions_df['标的名称'].isin(yestoday_stocks)].copy()
    to_sell_df = yestoday_positions_df[~yestoday_positions_df['标的名称'].isin(today_stocks)].copy()

    # ✅ 为买入数据添加操作标识
    to_buy_df['操作'] = '买入'

    # ✅ 为卖出数据添加操作标识
    to_sell_df['操作'] = '卖出'

    # ✅ 统一列结构以避免NaN
    # 确保两份数据都有相同的列
    common_columns = ['名称', '操作', '标的名称', '代码', '最新价', '盈亏比例%', '新比例%', '市场', '时间', '行业']

    # 为买入数据填充缺失的列（如果有的话）
    for col in common_columns:
        if col not in to_buy_df.columns:
            if col == '操作':
                to_buy_df[col] = '买入'
            elif col in ['代码', '最新价', '盈亏比例%', '新比例%']:
                to_buy_df[col] = None  # 或者可以设置为0
            elif col == '市场':
                to_buy_df[col] = '沪深A股'  # 假设默认市场
            elif col == '行业':
                to_buy_df[col] = None
            else:
                to_buy_df[col] = ''

    # 为卖出数据填充缺失的列
    for col in common_columns:
        if col not in to_sell_df.columns:
            if col == '操作':
                to_sell_df[col] = '卖出'
            elif col in ['最新价', '盈亏比例%', '新比例%']:
                to_sell_df[col] = 0
            elif col == '行业':
                to_sell_df[col] = None
            elif col == '代码':
                to_sell_df[col] = None
            else:
                to_sell_df[col] = ''

    # 确保列的顺序一致
    to_buy_df = to_buy_df[common_columns]
    to_sell_df = to_sell_df[common_columns]

    # 合并
    portfolio_df = pd.concat([to_buy_df, to_sell_df], ignore_index=True)

    # 去重
    portfolio_df = portfolio_df.drop_duplicates(subset=['标的名称'])
    portfolio_df = portfolio_df.reset_index(drop=True)
    logger.info(f"汇总的调仓数据：{len(portfolio_df)} 条 \n{portfolio_df}")
    save_to_excel_append(portfolio_df, Strategy_portfolio_today_file, sheet_name=today)

    # ✅ 输出结果
    logger.info(f"📊 今日({today})持仓标的: {today_positions_df['标的名称'].tolist()}")
    logger.info(f"📊 对比日期: {yestoday}")
    logger.info(f"✅ 要买入标的:\n{to_buy_df}\n")
    logger.info(f"✅ 要卖出标的:\n{to_sell_df}\n")

    return portfolio_df


def sava_all_strategy_holding_data():
    """
    获取所有策略的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
    """
    all_holdings = []
    for id in Strategy_ids:
        positions_df = get_latest_position(id)
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
            diff_result_df = get_difference_holding()

            # 检查返回的DataFrame是否为空
            if diff_result_df.empty:
                logger.info("✅ 当前无持仓差异，无需执行交易")
                return True

            # 按操作类型分组，优先执行卖出操作
            sell_operations = diff_result_df[diff_result_df['操作'] == '卖出']
            buy_operations = diff_result_df[diff_result_df['操作'] == '买入']

            # 对买入操作按最新价排序（从低到高）
            if not buy_operations.empty:
                # 确保最新价列存在且为数值类型
                buy_operations = buy_operations.copy()
                buy_operations['最新价'] = pd.to_numeric(buy_operations['最新价'], errors='coerce')
                buy_operations = buy_operations.sort_values('最新价', ascending=True, na_position='last')
                buy_operations = buy_operations.reset_index(drop=True)
                logger.info(f"📈 买入顺序（按价格从低到高）: {buy_operations[['标的名称', '最新价']].to_string(index=False)}")

            # 合并操作，将卖出操作放在前面，买入操作按价格排序
            ordered_operations = pd.concat([sell_operations, buy_operations], ignore_index=True)

            # 准备保存到今日调仓文件的数据
            today_trades = []

            # 遍历每一行，执行交易
            for index, row in ordered_operations.iterrows():
                stock_name = row['标的名称']
                operation = row['操作']
                strategy_name = row.get('名称', 'AI市场追踪策略')  # 获取策略名称，默认为AI市场追踪策略
                # 修复：从原始数据中获取策略名称，而不是从合并后的DataFrame中
                # strategy_name = row['名称']

                logger.info(f"🛠️ 要处理: {operation} {stock_name}")

                # 特殊处理：卖出时全仓卖出
                if operation == "卖出":
                    new_ratio = 0
                else:
                    new_ratio = None  # 买入时无需新比例

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
                # operate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                operate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                record = pd.DataFrame([{
                    '名称': strategy_name,  # 策略名称
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

                # 添加到今日调仓数据中，用于保存到Strategy_portfolio_today.xlsx
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
                logger.info(f"等待30秒后进行第 {retry_count + 1} 次重试...")
                time.sleep(30)

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
