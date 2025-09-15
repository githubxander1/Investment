import datetime
import os
from pprint import pprint

import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import (
    Combination_holding_file, all_ids, id_to_name, Combination_headers
)
from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.format_data import determine_market, get_new_records, standardize_dataframe, normalize_time
from Investment.THS.AutoTrade.scripts.data_process import read_today_portfolio_record, save_to_operation_history_excel
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger(__name__)

class CombinationHoldingProcessor(CommonHoldingProcessor):
    def __init__(self):
        super().__init__(account_name="中泰证券")
        self.previous_holdings = None

    # 获取单个组合的持仓数据
    def get_single_holding_data(self, portfolio_id):
        """获取单个组合的持仓数据"""
        url = f"https://t.10jqka.com.cn/portfolio/relocate/user/getPortfolioHoldingData?id={portfolio_id}"
        headers = Combination_headers

        try:
            response = requests.get(url, headers=headers, timeout=10)  # 增加超时设置
            response.raise_for_status()

            data = response.json()
            # pprint(data)
            
            # 检查返回数据是否有效
            if "result" not in data or "positions" not in data["result"]:
                logger.warning(f"组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})返回数据格式异常")
                return pd.DataFrame()

            positions = data["result"]["positions"]
            
            # 检查是否有持仓数据
            if not positions:
                logger.info(f"组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})当前无持仓")
                return pd.DataFrame()

            holding_data = []
            for position in positions:
                code = str(position.get("code", "")).zfill(6)
                holding_data.append({
                    "名称": id_to_name.get(portfolio_id, f'组合{portfolio_id}'),
                    # "操作": '买入',
                    "标的名称": position.get("name", ""),
                    "代码": code,
                    "最新价": position["price"],
                    "新比例%": position.get("positionRealRatio", 0) * 100,
                    "市场": determine_market(code),
                    "成本价": position["costPrice"],
                    "收益率(%)": position.get("incomeRate", 0) * 100,
                    "盈亏比例(%)": position.get("profitLossRate", 0) * 100,
                    "时间": datetime.datetime.now().strftime('%Y-%m-%d')
                })

            return pd.DataFrame(holding_data)

        except requests.exceptions.Timeout:
            error_msg = f"请求组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})持仓数据超时"
            logger.error(error_msg)
            send_notification(error_msg)
            return pd.DataFrame()
        except requests.exceptions.RequestException as e:
            error_msg = f"请求组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})持仓数据失败: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return pd.DataFrame()
        except Exception as e:
            error_msg = f"处理组合{portfolio_id}({id_to_name.get(str(portfolio_id), '未知组合')})持仓数据时出错: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return pd.DataFrame()

    # 获取所有组合的当前持仓数据
    def get_all_combination_current_holdings(self):
        """
        获取所有组合的当前持仓数据，用于比较是否发生变化
        """
        logger.info("-" * 50)
        logger.info("🔍 开始：获取所有组合当前持仓数据用于变化检测")
        
        # 获取所有组合的持仓数据
        all_holdings = []
        success_count = 0  # 记录成功获取数据的组合数量
        total_count = len(all_ids)  # 总组合数量
        
        for id in all_ids:
            positions_df = self.get_single_holding_data(id)
            # # 只保留沪深A股的
            # positions_df = positions_df[positions_df['市场'] == '沪深A股']
            # # 按价格从低到高排序
            # positions_df = positions_df.sort_values('最新价', ascending=True)
            
            if positions_df is not None and not positions_df.empty:
                logger.debug(f"📊 组合{id}({id_to_name.get(str(id), '未知组合')})持仓数据:{len(positions_df)}条\n{positions_df}")
                all_holdings.append(positions_df)
                success_count += 1
            else:
                logger.info(f"⚠️ 没有获取到组合{id}({id_to_name.get(str(id), '未知组合')})的持仓数据")

        # 检查数据获取情况
        if success_count == 0:
            logger.error("❌ 未获取到任何组合持仓数据")
            return None
        elif success_count < total_count:
            logger.warning(f"⚠️ 部分组合数据获取失败: {success_count}/{total_count}")
            send_notification(f"⚠️ 组合数据获取异常: {success_count}/{total_count} 个组合数据获取成功")
        
        all_holdings_df = pd.concat(all_holdings, ignore_index=True)
        # 只保留沪深A股的
        all_holdings_df = all_holdings_df[all_holdings_df['市场'] == '沪深A股']
        # 按价格从低到高排序
        all_holdings_df = all_holdings_df.sort_values('最新价', ascending=True)
        logger.info(f"📈 结束：获取所有组合当前持仓数据 总计获取到 {len(all_holdings_df)} 条持仓记录（限沪深）")
        logger.info("-" * 50)
        return all_holdings_df

    # 保存所有组合的持仓数据
    def save_all_combination_holding_data(self, all_holdings_df=None):
        """
        获取所有组合的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
        保持索引，从1开始
        
        参数:
            all_holdings_df (pd.DataFrame): 可选的持仓数据，如果已存在则不需要重新获取
        """
        logger.info("📂 开始：获取并保存所有组合持仓数据")
        
        # 如果没有提供持仓数据，则获取一次
        if all_holdings_df is None:
            today = str(datetime.date.today())
            all_holdings_df = self.get_all_combination_current_holdings()
        else:
            today = str(datetime.date.today())
        
        # 检查是否获取到有效数据
        if all_holdings_df is None:
            logger.error("❌ 未获取到有效组合持仓数据，无法保存")
            send_notification("⚠️ 组合持仓数据获取失败，请检查接口是否正常")
            return False
            
        if all_holdings_df.empty:
            logger.warning("⚠️ 获取到的组合持仓数据为空")
            send_notification("⚠️ 组合持仓数据为空，请检查接口是否正常")
            return False  # 数据为空也视为保存失败

        file_path = Combination_holding_file

        # 创建一个字典来存储所有工作表数据
        all_sheets_data = {}

        try:
            # 如果文件存在，读取现有数据
            if os.path.exists(file_path):
                with pd.ExcelFile(file_path) as xls:
                    existing_sheets = xls.sheet_names
                    logger.info(f"💾 保存前文件中已存在的工作表: {existing_sheets}")

                # 读取除今天以外的所有现有工作表
                with pd.ExcelFile(file_path) as xls:
                    for sheet_name in existing_sheets:
                        if sheet_name != today:
                            all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

            # 将今天的数据放在第一位
            all_sheets_data = {today: all_holdings_df, **all_sheets_data}
            logger.info(f"📦 即将保存的所有工作表: {list(all_sheets_data.keys())}")

            # 写入所有数据到Excel文件（覆盖模式），注意不保存索引
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                for sheet_name, df in all_sheets_data.items():
                    logger.info(f"💾 正在保存工作表: {sheet_name} ({len(df)} 条记录)")
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            logger.info(f"✅ 所有持仓数据已保存，{today} 数据位于第一个 sheet，共 {len(all_holdings_df)} 条")

            return True  # 成功保存数据，返回True

        except Exception as e:
            logger.error(f"❌ 保存持仓数据失败: {e}")
            send_notification(f"❌ 组合持仓数据保存失败: {e}")
            # 如果出错，至少保存今天的数据
            try:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    all_holdings_df.to_excel(writer, sheet_name=today, index=False)
                logger.info(f"✅ 文件保存完成，sheet: {today}")
                return True  # 成功保存数据，返回True
            except Exception as e2:
                logger.error(f"❌ 保存今日数据也失败了: {e2}")
                send_notification(f"❌ 组合持仓数据保存失败: {e2}")
                return False  # 保存失败，返回False

    # 找出新增的持仓
    def compare_holding_changes(self):
        """比较持仓变化并通知新增数据"""
        try:
            logger.info("🔄 开始：比较组合持仓变化")

            # 获取当前持仓数据
            current_holdings = self.get_all_combination_current_holdings()
            if current_holdings is None:
                warning_msg = "❌ 未获取到当前组合持仓数据"
                logger.error(warning_msg)
                send_notification(warning_msg)
                return

            if current_holdings.empty:
                logger.info("📋 当前组合持仓数据为空")
                return

            # 读取历史持仓数据
            history_file = Combination_holding_file
            try:
                history_holdings = read_today_portfolio_record(history_file)
                if history_holdings.empty:
                    logger.info("📋 历史持仓数据为空")
            except Exception as e:
                logger.warning(f"读取历史持仓数据失败: {e}")
                history_holdings = pd.DataFrame()

            # 标准化数据格式
            current_holdings = standardize_dataframe(current_holdings)
            history_holdings = standardize_dataframe(history_holdings)

            # 获取新增数据
            new_data = get_new_records(current_holdings, history_holdings)

            if not new_data.empty:
                logger.info(f"🆕 发现 {len(new_data)} 条新增持仓数据")
                logger.info(f"\n{new_data}")

                # 发送通知
                new_data_print = new_data.to_string(index=False)
                send_notification(f"📈 组合新增持仓 {len(new_data)} 条：\n{new_data_print}")

                # 保存新增数据到文件
                today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
                save_to_operation_history_excel(new_data, history_file, f'{today}', index=False)
                logger.info("💾 新增持仓数据已保存到文件")
            else:
                logger.info("✅ 组合持仓无变化")

        except Exception as e:
            error_msg = f"比较组合持仓变化时出错: {e}"
            logger.error(error_msg)
            send_notification(error_msg)

    # 执行操作
    def execute_combination_trades(self):
        """执行组合策略的调仓操作"""
        try:
            logger.info("-" * 50)
            logger.info("🔄 开始：执行组合策略调仓操作")
            
            # 1. 读取holding_file里的历史记录
            history_file = Combination_holding_file
            try:
                history_holdings = read_today_portfolio_record(history_file)
                if history_holdings.empty:
                    logger.info("📋 历史持仓数据为空")
            except Exception as e:
                logger.warning(f"读取历史持仓数据失败: {e}")
                history_holdings = pd.DataFrame()
            
            # 2. 获取所有的策略，接口返回的持仓数据
            current_holdings = self.get_all_combination_current_holdings()
            if current_holdings is None:
                error_msg = "❌ 未获取到组合持仓数据，跳过调仓操作"
                logger.error(error_msg)
                send_notification(error_msg)
                return False
            
            # 3. 对比历史记录和本次接口返回的持仓，检查是否有新增（在保存之前对比）
            # 标准化数据格式
            current_holdings_standard = standardize_dataframe(current_holdings.copy())
            history_holdings_standard = standardize_dataframe(history_holdings.copy())
            
            # 获取新增数据
            new_data = get_new_records(current_holdings_standard, history_holdings_standard)
            
            # 4. 保存最新持仓数据到文件
            save_result = self.save_all_combination_holding_data(current_holdings)
            if not save_result:
                error_msg = "❌ 组合持仓数据保存失败"
                logger.error(error_msg)
                send_notification(error_msg)
                return False
            
            # 5. 如果有新增数据，继续后续操作
            if new_data.empty:
                logger.info("✅ 组合持仓无变化，跳过后续操作")
                return True

            logger.info(f"🆕 发现 {len(new_data)} 条新增持仓数据")
            logger.debug(f"\n{new_data}")

            # 4. 有新增数据，更新实际账户的持仓，然后找出接口返回和实际账户持仓的不同数据
            # 保存新增数据到今日调仓文件
            from Investment.THS.AutoTrade.config.settings import Combination_portfolio_today_file
            today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
            try:
                save_to_operation_history_excel(new_data, Combination_portfolio_today_file, f'{today}', index=False)
                logger.info("💾 新增持仓数据已保存到今日调仓文件")
            except Exception as e:
                logger.error(f"❌ 保存新增持仓数据到今日调仓文件失败: {e}")
                send_notification(f"❌ 保存新增持仓数据到今日调仓文件失败: {e}")

            # 5. 把新增的不同的数据交给operate_result去执行
            success = self.operate_result(
                holding_file=Combination_holding_file,
                portfolio_today_file=Combination_portfolio_today_file,
                account_name="中泰证券"
            )

            if success:
                logger.info("✅ 组合策略调仓执行完成")
                send_notification("✅ 组合策略调仓执行完成")
            else:
                error_msg = "❌ 组合策略调仓执行失败"
                logger.error(error_msg)
                send_notification(error_msg)
                
            return success
        except Exception as e:
            error_msg = f"执行组合策略调仓操作时出错: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return False



if __name__ == '__main__':
    processor = CombinationHoldingProcessor()
    success = processor.execute_combination_trades()
    if not success:
        # logger.info("🎉 组合策略调仓任务成功完成")
    # else:
        logger.error("❌ 组合策略调仓任务失败")
    
    # 比较持仓变化
    processor.compare_holding_changes()
#     '''
#     优化execute_combination_trades，文件总的逻辑是：
# 1.读取holding_file里的历史记录，
# 2.获取所有的策略，接口返回的持仓数据，保存到holding_file，
# 3. 对比holding_file里的历史记录和本次接口返回的持仓，如果有新增，更新实际账户的持仓，然后再找出接口返回和实际账户持仓的不同数据（要买和要卖的数据），附加保存到Combination_portfolio_today_file，没有新增就不执行后面的，包括更新账户数据
# 5.把新增的不同的数据交给operate_result去执行
# '''