# data_process2.py
import os
from datetime import datetime, timedelta
from pprint import pprint

import pandas
import pandas as pd

from Investment.AutoPublic.jrtt.jrtt import send_notification
from Investment.THS.AutoTrade.config.settings import trade_operations_log_file, OPERATION_HISTORY_FILE, \
    Account_holding_file, Strategy_holding_file, \
    Combination_holding_file, Strategy_portfolio_today_file, Combination_portfolio_today_file, Lhw_portfolio_today_file, \
    Robot_holding_file
from Investment.THS.AutoTrade.pages.page_common import CommonPage
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.pages.account_info import AccountInfo
from Investment.THS.AutoTrade.utils.format_data import normalize_time
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger(trade_operations_log_file)
common_page = CommonPage()
account_info = AccountInfo()
trader = TradeLogic()

_operation_history_cache = None
_operation_history_cache_time = None


def read_portfolio_or_operation_data(file_path, sheet_name=None):
    """
    通用函数用于读取投资组合或操作历史数据。

    参数:
        file_path (str): Excel 文件路径。
        sheet_name (str, optional): 要读取的工作表名称，默认为当前日期。

    返回:
        pd.DataFrame: 包含 '标的名称', '操作', '新比例%' 的 DataFrame。
    """
    global _operation_history_cache, _operation_history_cache_time
    #检查是否需要刷新缓存，超过一分钟或强制刷新
    # current_time = datetime.now()
    # if _operation_history_cache_time is None or (current_time - _operation_history_cache_time).total_seconds() > 60:
    #     _operation_history_cache = read_portfolio_or_operation_data(file_path, sheet_name)
    #     _operation_history_cache_time = current_time


    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
    all_dfs = []

    if sheet_name is None:
        sheet_name = today
    elif sheet_name == 'all':
        sheet_name = None  # 用于后续判断读取所有sheet

    if not os.path.exists(file_path):
        logger.warning(f"文件不存在: {file_path}")
        return [pd.DataFrame()]

    try:
        with pd.ExcelFile(file_path, engine='openpyxl') as xls:
            sheets = xls.sheet_names

            if sheet_name is None:
                # 读取所有sheet
                sheets_to_read = sheets
            else:
                sheets_to_read = [sheet_name] if sheet_name in sheets else []

            for sn in sheets_to_read:
                df = pd.read_excel(xls, sheet_name=sn)

                if df is not None:
                    all_dfs.append(df)
                    logger.info(f"✅ 读取数据成功: {file_path}, 表: {sn}, 共 {len(df)} 条记录")

            if not sheets_to_read:
                logger.warning(f"未找到可读取的工作表: {file_path}")
    except Exception as e:
        logger.error(f"❌ 读取文件 {file_path} 失败: {e}", exc_info=True)
        return [pd.DataFrame()]

    if not all_dfs:
        all_dfs = [pd.DataFrame()]

    # 合并所有数据并去重
    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df.drop_duplicates(inplace=True)

    return combined_df


def save_to_excel_append(df, filename, sheet_name=None, index=False):
    """
    通用函数：将DataFrame追加写入Excel文件的指定工作表。

    参数:
        df (pd.DataFrame): 要写入的数据。
        filename (str): 文件路径。
        sheet_name (str): 工作表名称，默认为当前日期。
        index (bool): 是否写入行索引。
    """
    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
    if sheet_name is None:
        sheet_name = today

    try:
        # 统一数据类型
        if '新比例%' in df.columns:
            df['新比例%'] = pd.to_numeric(df['新比例%'], errors='coerce').fillna(0.0).round(2)
        if '最新价' in df.columns:
            df['最新价'] = pd.to_numeric(df['最新价'], errors='coerce').fillna(0.0).round(2)
        if '代码' in df.columns:
            df['代码'] = df['代码'].astype(str).str.zfill(6)

        # 处理字符串列
        for col in ['名称', '标的名称', '操作']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        # 填充空值
        df = df.fillna('')

        # 如果文件不存在，创建新文件并写入
        if not os.path.exists(filename):
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=index)
            logger.info(f"✅ 创建并写入文件: {filename}, 表: {sheet_name}")
            return

        # 文件存在，读取现有数据
        existing_data = {}
        try:
            with pd.ExcelFile(filename, engine='openpyxl') as xls:
                # 读取所有现有工作表
                for sn in xls.sheet_names:
                    existing_data[sn] = pd.read_excel(xls, sheet_name=sn)
        except Exception as e:
            logger.warning(f"读取现有文件时出现问题: {e}，将覆盖文件")
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=index)
            logger.info(f"✅ 重新创建并写入文件: {filename}, 表: {sheet_name}")
            return

        # 如果目标工作表存在，合并数据
        if sheet_name in existing_data:
            try:
                combined_df = pd.concat([existing_data[sheet_name], df], ignore_index=True)
                # 去除重复行（基于所有列）
                combined_df = combined_df.drop_duplicates(keep='last')
            except Exception as e:
                logger.warning(f"合并数据时出现问题: {e}，使用新数据")
                combined_df = df
        else:
            combined_df = df

        # 更新目标工作表数据
        existing_data[sheet_name] = combined_df

        # 重新排序工作表，确保最新工作表在最前面
        ordered_sheets = [sheet_name]  # 最新工作表放在第一位
        for sn in sorted(existing_data.keys(), reverse=True):  # 按字母倒序排列其他表
            if sn != sheet_name:
                ordered_sheets.append(sn)

        # 按照新顺序重新组织数据
        reordered_data = {sn: existing_data[sn] for sn in ordered_sheets}

        # 重新写入所有工作表
        with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
            for sn, data in reordered_data.items():
                # 确保数据类型正确后再写入
                if '代码' in data.columns:
                    data['代码'] = data['代码'].astype(str).str.zfill(6)
                if '新比例%' in data.columns:
                    data['新比例%'] = pd.to_numeric(data['新比例%'], errors='coerce').fillna(0.0).round(2)
                if '最新价' in data.columns:
                    data['最新价'] = pd.to_numeric(data['最新价'], errors='coerce').fillna(0.0).round(2)

                # 处理字符串列
                for col in ['名称', '标的名称', '操作']:
                    if col in data.columns:
                        data[col] = data[col].astype(str).str.strip()

                data.to_excel(writer, sheet_name=sn, index=index)

        logger.info(f"✅ 成功追加写入文件: {filename}, 表: {sheet_name}，新增{len(df)}条记录")

    except PermissionError:
        logger.error(f"❌ 文件被占用，无法写入: {filename}，请关闭文件后重试")
    except Exception as e:
        logger.error(f"❌ 追加写入文件 {filename} 失败: {e}", exc_info=True)


def read_today_portfolio_record(file_path):
    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
    # print(f'读取调仓记录文件日期{today}')
    if os.path.exists(file_path):
        try:
            with pd.ExcelFile(file_path, engine='openpyxl') as portfolio_record_xlsx:
                if today in portfolio_record_xlsx.sheet_names:
                    portfolio_record_history_df = pd.read_excel(portfolio_record_xlsx, sheet_name=today)

                    # 去重处理
                    portfolio_record_history_df.drop_duplicates(
                        subset=['标的名称', '操作', "新比例%", '时间'],
                        inplace=True
                    )
                    logger.info(f"读取去重后的操作历史文件完成, {len(portfolio_record_history_df)}条 \n{portfolio_record_history_df}")
                else:
                    portfolio_record_history_df = pd.DataFrame(columns=[
                        "名称", "操作", "标的名称", "代码", "最新价", "新比例%", "市场", "时间"
                    ])
                    logger.warning(f"今日表不存在: {today}")
        except Exception as e:
            logger.error(f"读取操作历史文件失败: {e}", exc_info=True)
            portfolio_record_history_df = pd.DataFrame(columns=[
                "名称", "操作", "标的名称", "代码", "最新价", "新比例%", "市场", "时间"
            ])
    else:
        portfolio_record_history_df = pd.DataFrame(columns=[
            "名称", "操作", "标的名称", "代码", "最新价", "新比例%", "市场", "时间"
        ])
        logger.warning(f"文件不存在: {file_path}")

    # print(f"读取的数据类型: \n{portfolio_record_history_df.dtypes}")
    return portfolio_record_history_df


def read_operation_history(history_file, force_refresh=False):
    """
    读取当日操作历史

    参数:
        history_file (str): 历史文件路径
        force_refresh (bool): 是否强制刷新缓存
    """
    global _operation_history_cache, _operation_history_cache_time

    # 检查是否需要刷新缓存（超过1分钟或强制刷新）
    current_time = datetime.now()
    if not force_refresh and _operation_history_cache is not None:
        if _operation_history_cache_time and (current_time - _operation_history_cache_time).seconds < 60:
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
                # 添加更完整的唯一标识
                history_df['_id'] = history_df.apply(
                    lambda x: f"{x['标的名称']}_{x['操作']}_{x['新比例%']}", axis=1)
                logger.info(f"✅ 读取操作历史成功，共 {len(history_df)} 条记录\n{history_df}")
                _operation_history_cache = history_df
                _operation_history_cache_time = current_time
                return history_df
    except Exception as e:
        logger.warning(f"读取操作历史失败，可能文件被占用或损坏: {e}")
    return pd.DataFrame(columns=['标的名称', '操作', '新比例%'])


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


def save_to_operation_history_excel(df, filename, sheet_name, index=False):
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
    global _operation_history_cache

    today = datetime.now().strftime('%Y-%m-%d')
    filename = OPERATION_HISTORY_FILE

    try:
        # 如果文件不存在，创建新文件并将数据保存到第一个 sheet
        if not os.path.exists(filename):
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=today, index=False)
            logger.info(f"✅ 创建并保存数据到Excel文件: {filename}, 表名称: {today} \n{df}")
            # 更新缓存
            _operation_history_cache = df
            return

        # ✅ 先读取今天的sheet已有数据
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

        # 更新缓存
        _operation_history_cache = combined_df

    except Exception as e:
        error_info = f"❌ 写入操作记录失败: {e}"
        logger.error(error_info)
        send_notification(error_info)
        raise


def get_difference_holding():
    """
    对比账户持仓与策略/组合持仓数据，找出差异：
        - 需要卖出：在账户中存在，但不在策略/组合中；
        - 需要买入：在策略/组合中存在，但不在账户中；
    """
    try:
        # 检查必要文件是否存在
        required_files = {
            "账户持仓文件": Account_holding_file,
            "策略持仓文件": Strategy_holding_file,
            "组合持仓文件": Combination_holding_file,
            "Robot持仓文件": Robot_holding_file
        }

        for file_desc, file_path in required_files.items():
            if not os.path.exists(file_path):
                logger.error(f"{file_desc}不存在: {file_path}")
                return {"error": f"{file_desc}不存在"}

        # 读取账户持仓数据（从所有账户的持仓数据表中读取）
        account_dfs = []
        try:
            with pd.ExcelFile(Account_holding_file, engine='openpyxl') as xls:
                account_sheets = xls.sheet_names

                for sheet in account_sheets:
                    if sheet.endswith('_持仓数据'):  # 只读取持仓数据表
                        try:
                            df = pd.read_excel(xls, sheet_name=sheet)
                            if not df.empty and '标的名称' in df.columns:
                                # 只保留标的名称列，并添加账户标识
                                df_filtered = df[['标的名称']].copy()
                                df_filtered['账户'] = sheet.replace('_持仓数据', '')
                                account_dfs.append(df_filtered)
                                logger.info(f"✅ 成功读取账户 {sheet} 的持仓数据，共 {len(df_filtered)} 条记录")
                        except Exception as e:
                            logger.warning(f"读取账户工作表 {sheet} 失败: {e}")
        except Exception as e:
            logger.error(f"读取账户持仓文件失败: {e}")
            return {"error": "读取账户持仓文件失败"}

        if not account_dfs:
            logger.error("无法从账户文件中读取有效的持仓数据")
            return {"error": "无法读取账户持仓数据"}

        # 合并所有账户的持仓数据
        account_df = pd.concat(account_dfs, ignore_index=True).drop_duplicates(subset=['标的名称'])
        logger.info(f"合并后账户持仓数据共 {len(account_df)} 条记录")

        # 读取策略持仓数据
        try:
            if os.path.exists(Strategy_holding_file) and os.path.getsize(Strategy_holding_file) > 0:
                strategy_df = pd.read_excel(Strategy_holding_file)
                if strategy_df.empty:
                    logger.warning("策略持仓文件为空")
                    strategy_df = pd.DataFrame(columns=['标的名称'])
            else:
                logger.warning("策略持仓文件不存在或为空")
                strategy_df = pd.DataFrame(columns=['标的名称'])
        except Exception as e:
            logger.error(f"读取策略持仓文件失败: {e}")
            strategy_df = pd.DataFrame(columns=['标的名称'])

        # 读取组合持仓数据
        try:
            if os.path.exists(Combination_holding_file) and os.path.getsize(Combination_holding_file) > 0:
                combination_df = pd.read_excel(Combination_holding_file)
                if combination_df.empty:
                    logger.warning("组合持仓文件为空")
                    combination_df = pd.DataFrame(columns=['标的名称'])
            else:
                logger.warning("组合持仓文件不存在或为空")
                combination_df = pd.DataFrame(columns=['标的名称'])
        except Exception as e:
            logger.error(f"读取组合持仓文件失败: {e}")
            combination_df = pd.DataFrame(columns=['标的名称'])

        logger.info(f"账户持仓数据:\n{account_df[['标的名称']]}\n")
        if not strategy_df.empty:
            logger.info(f"策略持仓数据:\n{strategy_df[['标的名称']]}\n")
        if not combination_df.empty:
            logger.info(f"组合持仓数据:\n{combination_df[['标的名称']]}\n")

        # 合并策略和组合中的所有标的名称
        combined_dfs = []
        if not strategy_df.empty and '标的名称' in strategy_df.columns:
            combined_dfs.append(strategy_df[['标的名称']])
        if not combination_df.empty and '标的名称' in combination_df.columns:
            combined_dfs.append(combination_df[['标的名称']])

        if combined_dfs:
            combined_holdings = pd.concat(combined_dfs, ignore_index=True).drop_duplicates(subset=['标的名称']).reset_index(drop=True)
        else:
            combined_holdings = pd.DataFrame(columns=['标的名称'])

        logger.info(f"策略和组合合并后持仓数据共 {len(combined_holdings)} 条记录")

        # 需要排除的标的名称
        excluded_holdings = ["工商银行", "中国电信", "可转债ETF", "国债政金债ETF"]

        # 1. 找出需要卖出的标的（在账户中存在，但不在策略/组合中，且不在排除列表中）
        if not account_df.empty and not combined_holdings.empty:
            to_sell_candidates = account_df[~account_df['标的名称'].isin(combined_holdings['标的名称'])]
            to_sell = to_sell_candidates[~to_sell_candidates['标的名称'].isin(excluded_holdings)].copy()  # 添加 .copy()
        else:
            to_sell = pd.DataFrame(columns=account_df.columns) if not account_df.empty else pd.DataFrame()

        if not to_sell.empty:
            logger.warning("⚠️ 发现需卖出的标的:")
            logger.info(f"\n{to_sell[['标的名称']] if '标的名称' in to_sell.columns else to_sell}")
        else:
            logger.info("✅ 当前无需卖出的标的")

        # 2. 找出需要买入的标的（在策略/组合中存在，但不在账户中，且不在排除列表中）
        if not combined_holdings.empty and not account_df.empty:
            to_buy_candidates = combined_holdings[~combined_holdings['标的名称'].isin(account_df['标的名称'])]
            to_buy = to_buy_candidates[~to_buy_candidates['标的名称'].isin(excluded_holdings)]
        elif not combined_holdings.empty:
            # 如果账户持仓为空，则所有策略/组合持仓都是需要买入的（除去排除项）
            to_buy = combined_holdings[~combined_holdings['标的名称'].isin(excluded_holdings)]
        else:
            to_buy = pd.DataFrame(columns=['标的名称'])

        if not to_buy.empty:
            logger.warning("⚠️ 发现需买入的标的:")
            logger.info(f"\n{to_buy[['标的名称']] if '标的名称' in to_buy.columns else to_buy}")
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

def get_stock_to_operate(trade_history_file, today_portfolio_file):
    # 默认账户（非 AI市场追踪策略 时使用）
    # default_account = "中泰证券"  # 组合
    today_portfolio_df = read_portfolio_or_operation_data(today_portfolio_file,today)
    print(f"[调试] 获取今日持仓数据: {today_portfolio_df}")
    trade_history_df = read_portfolio_or_operation_data(trade_history_file,today)
    print(f"[调试] 获取交易记录数据: {trade_history_df}")

    to_operate_list = []
    for index, row in today_portfolio_df.iterrows():
        strategy_name = row['名称'].strip()
        stock_name = row['标的名称'].strip()
        operation = row['操作'].strip()
        new_ratio = float(row['新比例%'])

        # 判断是否已执行 - 使用更精确的匹配
        exists = trade_history_df[
            (trade_history_df['标的名称'] == stock_name) &
            (trade_history_df['操作'] == operation) &
            (abs(trade_history_df['新比例%'] - new_ratio) < 0.01)  # 使用近似相等比较
            ]

        if not exists.empty:
            logger.info(f"✅ 已处理过: {stock_name} {operation} {new_ratio}%")
            continue
        to_operate_list.append(exists)

def extract_operations_to_perform_for_portfolio_file(file_paths):
    """
    提取所有需要执行的操作，不实际执行交易
    适用于: portfolio_today和trade_history文件

    返回:
        dict: 按账户分组的操作列表
        {
            "川财证券": [
                {"strategy_name": "...", "stock_name": "...", "operation": "...", "new_ratio": ..., ...},
                ...
            ],
            "长城证券": [...],
            "中泰证券": [...]
        }
    """
    # 强制刷新操作历史缓存
    operation_history_file = OPERATION_HISTORY_FILE
    history_df = read_operation_history(operation_history_file, force_refresh=True)

    # 创建已处理记录的索引集合，提高查找效率
    processed_operations = set()
    for _, row in history_df.iterrows():
        key = (row['标的名称'], row['操作'], round(row['新比例%'], 2))
        processed_operations.add(key)

    # 按账户分组的操作字典
    operations_by_account = {
        "川财证券": [],
        "长城证券": [],
        "中泰证券": []
    }

    for file_path in file_paths:
        logger.info(f"🔄 检测到文件更新，即将处理: {file_path}")

        # 检查文件是否存在且非空
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            logger.warning(f"⚠️ 文件不存在或为空: {file_path}")
            continue

        try:
            # 读取要处理的文件
            today_portfolio_df = read_today_portfolio_record(file_path)
            if today_portfolio_df.empty:
                logger.warning(f"文件 {file_path} 为空，跳过处理")
                continue

            # 遍历所有操作
            for index, row in today_portfolio_df.iterrows():
                strategy_name = row['名称'].strip()
                stock_name = row['标的名称'].strip()
                operation = row['操作'].strip()
                new_ratio = float(row['新比例%'])
                price = float(row['最新价'])

                logger.info(f"🛠️ 要处理: {operation} {stock_name} {price} 比例:{new_ratio}")

                # 检查是否已处理
                operation_key = (stock_name, operation, round(new_ratio, 2))
                if operation_key in processed_operations:
                    logger.info(f"✅ 已处理过: {stock_name} {operation} {price} 比例:{new_ratio}%")
                    continue

                # 确定账户类型
                if strategy_name in ["AI市场追踪策略", "GPT定期精选"]:  # 策略
                    account = "川财证券"
                elif strategy_name in ["有色金属", '钢铁', '建筑行业']:  # 机器人
                    account = "长城证券"
                else:  # 组合
                    account = "中泰证券"

                # 添加到对应账户的操作列表中
                operations_by_account[account].append({
                    "strategy_name": strategy_name,
                    "stock_name": stock_name,
                    "operation": operation,
                    "price": price,
                    "new_ratio": new_ratio,
                    "file_path": file_path  # 用于日志记录
                })

                # logger.info(f"📝 记录操作: {account} - {operation} {stock_name} {price} 比例:{new_ratio}")

        except pandas.errors.EmptyDataError:
            logger.error(f"处理文件 {file_path} 失败: 文件为空或格式错误")
        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}", exc_info=True)

    # 过滤掉空的账户列表
    operations_by_account = {k: v for k, v in operations_by_account.items() if v}
    operations_by_account_df = pandas.DataFrame(operations_by_account)

    if not operations_by_account:
        logger.info("✅ 没有需要执行的操作")
    else:
        for account, operations in operations_by_account.items():
            logger.info(f"📋 账户 {account} 需要执行 {len(operations)} 个操作\n{operations_by_account_df}")

    return operations_by_account


def process_data_to_operate(file_paths):
    """
    处理Excel文件中的交易指令，按账户分组处理以减少账户切换次数
    """
    # 提取所有需要执行的操作
    operations_by_account = extract_operations_to_perform_for_portfolio_file(file_paths)

    if not operations_by_account:
        return

    # 汇总所有操作结果用于最终通知
    all_operations_result = []

    # 按账户顺序处理
    for account, operations in operations_by_account.items():
        if not operations:
            continue

        logger.info(f"📋 开始处理账户 {account} 的 {len(operations)} 个操作")
        # 切换到对应账户
        common_page.change_account(account)
        logger.info(f"✅ 已切换到账户: {account}")

        # 执行该账户下的所有操作
        for op in operations:
            strategy_name = op["strategy_name"]
            stock_name = op["stock_name"]
            operation = op["operation"]
            new_ratio = op["new_ratio"]

            logger.info(f"🚀 开始交易: {operation} {stock_name}")

            # 初始化状态和信息
            status = None
            info = "未知错误"

            try:
                # 特殊处理：当新比例为0且操作为卖出时，强制全仓卖出
                if operation == "卖出" and new_ratio == 0:
                    logger.info(f"🎯 特殊处理: 新比例为0，将全仓卖出 {stock_name}")
                    # 直接调用交易逻辑，不依赖自动计算数量
                    status, info = trader.operate_stock(operation, stock_name, volume=None, new_ratio=new_ratio)

                # 特殊处理：AI市场追踪策略买入时使用固定股数
                elif strategy_name == "AI市场追踪策略" and operation == "买入":
                    fixed_volume = 200  # 固定买入200股
                    logger.info(f"🎯 AI市场追踪策略特殊处理: 买入 {stock_name} 固定数量 {fixed_volume} 股")
                    status, info = trader.operate_stock(operation, stock_name, volume=fixed_volume)
                else:
                    status, info = trader.operate_stock(operation, stock_name, volume=None, new_ratio=new_ratio)

                # 检查交易是否成功执行
                if status is None:
                    logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                    all_operations_result.append(f"{account}: {operation} {stock_name} 失败 - {info}")
                else:
                    logger.info(f"✅ {operation} {stock_name} 交易执行成功: {info}")
                    all_operations_result.append(f"{account}: {operation} {stock_name} 成功 - {info}")

            except Exception as e:
                logger.error(f"处理 {operation} {stock_name} 时发生异常: {e}", exc_info=True)
                info = str(e)
                all_operations_result.append(f"{account}: {operation} {stock_name} 异常 - {info}")

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

            # 更新本地历史记录DataFrame，避免在同一批次处理中重复操作
            # history_df = pd.concat([history_df, record], ignore_index=True)

        # except Exception as e:
        #     logger.error(f"处理 {operation} {stock_name} 时发生错误: {e}", exc_info=True)


    logger.info("✅ 所有文件处理完成")

    # 发送操作结果通知
    if all_operations_result:
        summary_message = "交易操作结果汇总:\n" + "\n".join(all_operations_result)
        from Investment.THS.AutoTrade.utils.notification import send_notification
        send_notification(summary_message)

if __name__ == '__main__':
    # diff_result = get_difference_holding()
    #
    # if 'error' in diff_result:
    #     print("持仓差异分析失败，请查看日志。")
    # else:
    #     if not diff_result['to_sell'].empty:
    #         print("💡 发现需卖出的股票：")
    #         # 显示需要卖出的股票及其账户信息
    #         if '账户' in diff_result['to_sell'].columns:
    #             print(diff_result['to_sell'][['标的名称', '账户']])
    #         else:
    #             print(diff_result['to_sell'][['标的名称']])
    #     else:
    #         print("✅ 当前无需卖出的标的")
    #
    #     if not diff_result['to_buy'].empty:
    #         print("💡 发现需买入的股票：")
    #         print(diff_result['to_buy'][['标的名称']])
    #     else:
    #         print("✅ 当前无需买入的标的")

    # file_path = Strategy_portfolio_today_file
    # file_path = [Strategy_portfolio_today_file,Combination_portfolio_today_file]
    # file_path = [OPERATION_HISTORY_FILE,Strategy_portfolio_today_file,Combination_portfolio_today_file]
    # file_path = [Strategy_portfolio_today_file,Combination_portfolio_today_file]
    # for file in file_path:
    #     if os.path.exists(file):
    #         print(f"文件 {file} 存在")
    #     else:
    #         print(f"文件 {file} 不存在")
    #     # read_today_portfolio_record(file)
    #     portfolio_data = read_portfolio_or_operation_data(file_path)
    #     print(portfolio_data)

    today = datetime.now().strftime('%Y-%m-%d')
    # 昨天
    today = (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d')
    portfolio_file_path = r'/Investment/THS/AutoTrade/data/portfolio/Robot_portfolio_today.xlsx'
    read = read_portfolio_or_operation_data(portfolio_file_path, sheet_name=today)
    print(f"读取：\n{read}")

    file_paths = [
        # Strategy_holding_file,
        Combination_portfolio_today_file,
        Lhw_portfolio_today_file
    ]
    df = extract_operations_to_perform_for_portfolio_file(file_paths)
    pprint(df)
    # print(get_stock_to_operate(trade_history_file_path,portfolio_file_path))

        # operation_data = read_portfolio_or_operation_data(OPERATION_HISTORY_FILE, sheet_name=today)

    # file_paths = [
    #     Lhw_portfolio_today_file
    # ]
    # # from auto_trade_on_ths import THSPage
    # import uiautomator2 as u2
    # d = u2.connect()
    # package_name = "com.hexin.plat.android"
    # d.app_start(package_name, wait=True)
    # logger.info(f"启动App成功: {package_name}")
    # # ths_page = THSPage(d)
    # process_data_to_operate(file_paths=file_paths, operation_history_file=OPERATION_HISTORY_FILE)