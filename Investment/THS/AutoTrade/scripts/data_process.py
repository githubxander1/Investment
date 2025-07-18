# data_process.py
import os
from datetime import datetime

import pandas
import pandas as pd

from Investment.THS.AutoTrade.config.settings import trade_operations_log_file, OPERATION_HISTORY_FILE, \
    Account_holding_file, Strategy_holding_file, \
    Combination_holding_file
from Investment.THS.AutoTrade.pages.page_common import CommonPage
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.pages.account_info import AccountInfo
from Investment.THS.AutoTrade.utils.format_data import normalize_time
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger(trade_operations_log_file)
common_page = CommonPage()
account_info = AccountInfo()
trader = TradeLogic()
def read_portfolio_record_history(file_path):
    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
    # print(f'读取调仓记录文件日期{today}')
    if os.path.exists(file_path):
        try:
            with pd.ExcelFile(file_path, engine='openpyxl') as operation_history_xlsx:
                if today in operation_history_xlsx.sheet_names:
                    portfolio_record_history_df = pd.read_excel(operation_history_xlsx, sheet_name=today)

                    # 显式转换关键列的类型
                    portfolio_record_history_df['代码'] = portfolio_record_history_df['代码'].astype(str).str.zfill(6)
                    # portfolio_record_history_df['新比例%'] = portfolio_record_history_df['新比例%'].astype(float).round(2)
                    portfolio_record_history_df['最新价'] = portfolio_record_history_df['最新价'].astype(float).round(2)

                    # 去重处理
                    portfolio_record_history_df.drop_duplicates(
                        subset=['标的名称', '操作', '新比例%', '时间'],
                        inplace=True
                    )
                    logger.info(f"读取去重后的操作历史文件完成, {len(portfolio_record_history_df)}条 \n{portfolio_record_history_df}")
                else:
                    portfolio_record_history_df = pd.DataFrame(columns=[
                        "名称", "操作", "标的名称", "代码", "最新价", "新比例%", "市场", "时间"
                    ])
                    logger.warning(f"历史文件表不存在: {today}")
        except Exception as e:
            logger.error(f"读取操作历史文件失败: {e}", exc_info=True)
            portfolio_record_history_df = pd.DataFrame(columns=[
                "名称", "操作", "标的名称", "代码", "最新价", "新比例%", "市场", "时间"
            ])
    else:
        portfolio_record_history_df = pd.DataFrame(columns=[
            "名称", "操作", "标的名称", "代码", "最新价", "新比例%", "市场", "时间"
        ])

    # print(f"读取的数据类型: \n{portfolio_record_history_df.dtypes}")
    return portfolio_record_history_df
def safe_concat(history_df, new_df):
    """安全的DataFrame拼接"""
    if history_df.empty:
        return new_df.copy()
    if new_df.empty:
        return history_df.copy()

    # 显式统一列顺序和类型
    all_columns = set(history_df.columns) | set(new_df.columns)
    for col in all_columns:
        if col not in history_df.columns:
            history_df[col] = ''
        if col not in new_df.columns:
            new_df[col] = ''

    # 显式转换为对象类型
    history_df = history_df.astype(object)
    new_df = new_df.astype(object)

    return pd.concat([history_df, new_df], ignore_index=True, sort=False)

def save_to_excel(df, filename, sheet_name, index=False):
    """追加保存DataFrame到Excel文件，默认今天的在第一张表"""
    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))  # 获取今天的日期

    # 统一数据类型
    df['新比例%'] = df['新比例%'].astype(float).round(2)
    df['最新价'] = df['最新价'].astype(float).round(2)
    df['代码'] = df['代码'].astype(str).str.zfill(6)

    # 保存到 Excel
    try:
        # 标准化数据类型
        df = df.fillna('')
        df = df.infer_objects(copy=False)
        # 如果文件不存在，创建新文件并将数据保存到第一个 sheet
        if not os.path.exists(filename):
            # print(f"保存的df {df}")
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=today, index=index)
                #打印数据类型
                # print(f"保存的数据类型: \n{df.dtypes}")
            logger.info(f"✅ 创建并保存数据到Excel文件: {filename}, 表名称: {today} \n{df}")
            return

        # 文件存在，读取现有数据
        with pd.ExcelFile(filename, engine='openpyxl') as xls:
            history_sheets = xls.sheet_names
            history_df = pd.read_excel(xls, sheet_name=sheet_name) if sheet_name in history_sheets else pd.DataFrame()

        # 如果今天的数据需要保存到第一个 sheet
        if sheet_name == today:
            # 读取现有第一个 sheet 的数据（如果存在）
            if history_sheets and history_sheets[0] == today:
                history_df = pd.read_excel(filename, sheet_name=today)
                # 读取的数据类型
                # print(f"保存时，读取的数据类型: \n{history_df.dtypes}")
                combined_df = safe_concat(history_df, df)
                # 显式清理无效值
                combined_df = combined_df.replace(['nan', 'NaN', 'N/A', 'None', None], '').infer_objects(copy=False)

                # 重新排序并设置索引
                # combined_df = combined_df[expected_columns]

                combined_df.drop_duplicates(subset=['名称', '操作', '标的名称', '代码', '最新价', '新比例%'], inplace=True)
            else:
                combined_df = df

            # 保存到第一个 sheet
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                combined_df.to_excel(writer, sheet_name=today, index=index)
                #打印数据类型
                # print(f"保存的数据类型: \n{combined_df.dtypes}")

            # 读取并保存其他 sheet 的数据
            other_sheets_data = {}
            for sheet in history_sheets:
                if sheet != today:
                    other_sheets_data[sheet] = pd.read_excel(filename, sheet_name=sheet)

            with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
                combined_df.to_excel(writer, sheet_name=today, index=index)
                for sheet, data in other_sheets_data.items():
                    data.to_excel(writer, sheet_name=sheet, index=index)

            logger.info(f"✅ 成功追加数据到Excel文件的第一个sheet: {filename}, 表名称: {today} \n{combined_df}")
        else:
            # 对于非今天的 sheet，直接追加或替换
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=index)
            logger.info(f"✅ 成功追加数据到Excel文件的指定sheet: {filename}, 表名称: {sheet_name} \n{df}")

    except Exception as e:
        logger.error(f"❌ 保存数据到Excel文件失败: {e}", exc_info=True)

def write_operation_history(df):
    """将操作记录写入Excel文件，按日期作为sheet名，并确保今日sheet位于第一个"""
    today = datetime.now().strftime('%Y-%m-%d')
    filename = OPERATION_HISTORY_FILE

    try:
        # 如果文件不存在，直接写入新文件
        if not os.path.exists(filename):
            save_to_excel(df, filename, sheet_name=today, index=False)
            logger.info(f"成功写入操作记录到 {today} 表 {filename}")
            return

        # ✅ 先读取已有数据
        with pd.ExcelFile(filename, engine='openpyxl') as xls:
            history_sheets = xls.sheet_names
            old_df = pd.read_excel(xls, sheet_name=today) if today in history_sheets else pd.DataFrame()

        # 合并新旧数据并去重
        combined_df = pd.concat([old_df, df], ignore_index=True)
        combined_df.drop_duplicates(subset=['标的名称', '操作', '新比例%'], keep='last', inplace=True)

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
        logger.error(f"❌ 写入操作记录失败: {e}")
        raise

_operation_history_cache = None
def read_operation_history(history_file):
    """读取当日操作历史"""
    global _operation_history_cache
    if _operation_history_cache is not None:
        return _operation_history_cache

    today = datetime.now().strftime('%Y-%m-%d')
    # 昨天
    # today = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    # print(f'读取历史文件日期：{today}')
    if not os.path.exists(history_file):
        return pd.DataFrame(columns=['标的名称', '操作', '新比例%'])

    try:
        with pd.ExcelFile(history_file, engine='openpyxl') as f:
            if today in f.sheet_names:
                history_df = pd.read_excel(f, sheet_name=today)
                history_df['标的名称'] = history_df['标的名称'].astype(str).str.strip()
                history_df['操作'] = history_df['操作'].astype(str).str.strip()
                history_df['新比例%'] = history_df['新比例%'].astype(float).round(2)
                history_df['_id'] = history_df.apply(lambda x: f"{x['标的名称']}_{x['操作']}_{x['新比例%']}", axis=1)
                logger.info(f"✅ 读取操作历史成功，共 {len(history_df)} 条记录\n{history_df}")
                _operation_history_cache = history_df
                return history_df
    except Exception as e:
        logger.warning(f"读取操作历史失败，可能文件被占用或损坏: {e}")
    return pd.DataFrame(columns=['标的名称', '操作', '新比例%'])

# 对比account_info文件和Strategy_holding以及Combination_holding文件,如果account_info里有其他两个文件里没有的股票标的，则卖出操作，反之买入（除了工商银行，中国电信，可转债ETF，国债证金债ETF）
def get_difference_holding():
    """
    对比账户持仓与策略/组合持仓数据，找出差异：
        - 需要卖出：在账户中存在，但在策略/组合中不存在；
        - 需要买入：在策略/组合中存在，但在账户中不存在；
    """
    try:
        # 读取持仓数据
        account_df = pd.read_excel(Account_holding_file, sheet_name="持仓数据")
        strategy_df = pd.read_excel(Strategy_holding_file)
        combination_df = pd.read_excel(Combination_holding_file)

        logger.info(f"账户持仓数据:\n{account_df[['标的名称']]}\n")
        logger.info(f"策略持仓数据:\n{strategy_df[['标的名称']]}\n")
        logger.info(f"组合持仓数据:\n{combination_df[['标的名称']]}\n")

        # 合并策略和组合中的所有标的名称
        combined_holdings = pd.concat([
            strategy_df[['标的名称']],
            combination_df[['标的名称']]
        ]).drop_duplicates().reset_index(drop=True)

        # 需要排除的标的名称
        excluded_holdings = ["工商银行","中国电信","可转债ETF","国债政金债ETF"]

        # 1.找出需要卖出的标的（在账户中存在，但不在策略 / 组合中，且不在排除列表中）
        to_sell_candidates = account_df[~account_df['标的名称'].isin(combined_holdings['标的名称'])]
        to_sell = to_sell_candidates[~to_sell_candidates['标的名称'].isin(excluded_holdings)]

        if not to_sell.empty:
            logger.warning("⚠️ 发现需卖出的标的:")
            # print("需卖出的标的:")
            print(to_sell[['标的名称', '持仓/可用']])
        else:
            logger.info("✅ 当前无需卖出的标的")

        # 2. 找出需要买入的标的（在策略/组合中存在，但不在账户中）
        to_buy_candidates = combined_holdings[~combined_holdings['标的名称'].isin(account_df['标的名称'])]
        to_buy = to_buy_candidates
        if not to_buy.empty:
            logger.warning("⚠️ 发现需买入的标的:")
            print("需买入的标的:")
            print(to_buy[['标的名称']])
        else:
            logger.info("✅ 当前无需买入的标的")

        # 构建完整差异报告
        difference_report = {
            "to_sell": to_sell,
            "to_buy": to_buy
        }

        return difference_report

    except Exception as e:
        logger.error(f"处理持仓差异时发生错误: {e}", exc_info=True)
        return {"error": str(e)}

def process_excel_files(ths_page, file_paths, operation_history_file, history_df=None):
    if history_df is None:
        history_df = read_operation_history(operation_history_file)

    for file_path in file_paths:
        logger.info(f"🔄 检测到文件更新，即将处理: {file_path}")

        # 检查文件是否存在且非空
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            logger.warning(f"⚠️ 文件不存在或为空: {file_path}")
            continue

        try:
            # 读取要处理的文件
            df = read_portfolio_record_history(file_path)
            if df.empty:
                logger.warning(f"文件 {file_path} 为空，跳过处理")
                continue

            # 默认账户（非 AI市场追踪策略 时使用）
            default_account = "川财证券"

            for index, row in df.iterrows():
                strategy_name = row['名称'].strip()
                stock_name = row['标的名称'].strip()
                operation = row['操作'].strip()
                new_ratio = float(row['新比例%'])

                # 根据策略切换账户
                if strategy_name == "AI市场追踪策略":
                    logger.info("检测到 AI市场追踪策略，切换账户为 模拟")
                    common_page.change_account("模拟练习区")
                elif strategy_name in ["GPT定期精选","中字头资金流入战法", "低价小市值股战法", "高现金毛利战法"]:
                    common_page.change_account("长城证券")
                else:
                    common_page.change_account(default_account)

                logger.info(f"🛠️ 要处理: {operation} {stock_name} 比例:{new_ratio}")

                # 判断是否已执行
                exists = history_df[
                    (history_df['标的名称'] == stock_name) &
                    (history_df['操作'] == operation) &
                    (history_df['新比例%'] == round(new_ratio, 2))
                ]
                if not exists.empty:
                    logger.info(f"✅ 已处理过: {stock_name}")
                    continue

                logger.info(f"🚀 开始交易: {operation} {stock_name}")
                # update_holding_info_all()
                # logger.info("更新持仓信息完成")

                status, info = trader.operate_stock(operation, stock_name)

                # 构造记录
                operate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                record = pd.DataFrame([{
                    '标的名称': stock_name,
                    '操作': operation,
                    '新比例%': new_ratio,
                    '状态': status,
                    '信息': info,
                    '时间': operate_time
                }])

                # 写入历史
                write_operation_history(record)
                logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

        except pandas.errors.EmptyDataError:
            logger.error(f"处理文件 {file_path} 失败: 文件为空或格式错误")
        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}", exc_info=True)

if __name__ == '__main__':
    diff_result = get_difference_holding()

    if 'error' in diff_result:
        print("持仓差异分析失败，请查看日志。")
    else:
        if not diff_result['to_sell'].empty:
            print("💡 发现需卖出的股票：")
            print(diff_result['to_sell'][['标的名称', '持仓/可用']])
        if not diff_result['to_buy'].empty:
            print("💡 发现需买入的股票：")
            print(diff_result['to_buy'][['标的名称']])

    # file_paths = [
    #     Strategy_portfolio_today_file,Combination_portfolio_today_file
    # ]
    # # from auto_trade_on_ths import THSPage
    # import uiautomator2 as u2
    # d = u2.connect()
    # package_name = "com.hexin.plat.android"
    # d.app_start(package_name, wait=True)
    # logger.info(f"启动App成功: {package_name}")
    # ths_page = THSPage(d)
    # process_excel_files(ths_page=ths_page, file_paths=file_paths, operation_history_file=OPERATION_HISTORY_FILE, holding_stock_file=None)