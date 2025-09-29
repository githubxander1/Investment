import datetime
import os

import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import Lhw_holding_file, Lhw_ids, Lhw_ids_to_name
from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.format_data import determine_market, get_new_records, standardize_dataframe, normalize_time
from Investment.THS.AutoTrade.scripts.data_process import read_today_portfolio_record, save_to_operation_history_excel
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger(__name__)

class LhwHoldingProcessor(CommonHoldingProcessor):
    def __init__(self):
        super().__init__(account_name="中泰证券")

    def get_latest_position(self, pool_id):
        """获取量化王策略的最新持仓数据"""
        url = "https://prod-lhw-strategy-data-center.ydtg.com.cn/lhwDataCenter/getQSCurrentCCGPById"

        params = {
            "poolId": pool_id
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTY4MjQ2MDEsImlhdCI6MTc1NDE0NjIwMX0.TbqTdscc1UyS6E3XYJgu9zGEbIgDBb8X4B_HR0Jwte0",
            "Host": "prod-lhw-strategy-data-center.ydtg.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.12.0",
            "If-Modified-Since": "Sun, 03 Aug 2025 13:56:57 GMT"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            response_json = response.json()

            data = response_json.get("data", [])
            datas = []
            for item in data:
                sec_code = str(item["sec_code"]).zfill(6)
                datas.append({
                    "名称": Lhw_ids_to_name.get(pool_id, f'量化王策略{pool_id}'),
                    "操作": '买入',
                    "标的名称": item["sec_name"],
                    "代码": sec_code,
                    "最新价": item["find_price"],
                    "新比例%": round(item["position_pl"] * 100, 2),
                    "市场": determine_market(sec_code),
                    "时间": datetime.datetime.now().strftime('%Y-%m-%d'),
                    "持仓天数": item["position_day"],
                })

            datas_df = pd.DataFrame(datas)
            return datas_df

        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"处理数据时发生错误: {e}")
            return pd.DataFrame()

    def save_all_lhw_holding_data(self):
        """
        获取所有量化王策略的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
        """
        all_holdings = []
        for id in Lhw_ids:
            positions_df = self.get_latest_position(id)
            # 只保留沪深A股的
            positions_df = positions_df[positions_df['市场'] == '沪深A股']
            # 按价格从低到高排序
            positions_df = positions_df.sort_values('最新价', ascending=True)
            logger.info(f"{id}持仓数据:{len(positions_df)}\n{positions_df}")
            if positions_df is not None and not positions_df.empty:
                all_holdings.append(positions_df)
            else:
                logger.info(f"没有获取到策略数据，策略ID: {id}")

        today = str(datetime.date.today())
        if not all_holdings:
            logger.warning("未获取到任何量化王策略持仓数据")
            return

        all_holdings_df = pd.concat(all_holdings, ignore_index=True)

        file_path = Lhw_holding_file

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
                            all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

            # 将今天的数据放在第一位
            all_sheets_data = {today: all_holdings_df, **all_sheets_data}
            logger.info(f"即将保存的所有工作表: {list(all_sheets_data.keys())}")

            # 写入所有数据到Excel文件（覆盖模式），注意不保存索引
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                for sheet_name, df in all_sheets_data.items():
                    # logger.info(f"正在保存工作表: {sheet_name}")
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

    def execute_lhw_trades(self):
        """执行量化王策略的调仓操作"""
        try:
            # 保存最新持仓数据
            self.save_all_lhw_holding_data()

            # 执行调仓操作
            from Investment.THS.AutoTrade.config.settings import Lhw_portfolio_today_file
            success = self.operate_result(
                holding_file=Lhw_holding_file,
                portfolio_today_file=Lhw_portfolio_today_file,
                account_name="中泰证券"
            )

            return success
        except Exception as e:
            logger.error(f"执行量化王策略调仓操作时出错: {e}")
            return False

    def compare_holding_changes(self):
        """比较量化王策略持仓变化并通知新增数据"""
        try:
            logger.info("🔄 开始比较量化王策略持仓变化")
            
            # 获取所有量化王策略的当前持仓数据
            all_holdings = []
            for id in Lhw_ids:
                positions_df = self.get_latest_position(id)
                # 只保留沪深A股的
                positions_df = positions_df[positions_df['市场'] == '沪深A股']
                # 按价格从低到高排序
                positions_df = positions_df.sort_values('最新价', ascending=True)
                if positions_df is not None and not positions_df.empty:
                    all_holdings.append(positions_df)
                else:
                    logger.info(f"没有获取到策略数据，策略ID: {id}")

            if not all_holdings:
                logger.warning("未获取到任何量化王策略持仓数据")
                return

            current_holdings = pd.concat(all_holdings, ignore_index=True)
            
            if current_holdings.empty:
                logger.info("🔄 未获取到当前量化王策略持仓数据")
                return
            
            # 读取历史持仓数据
            history_file = Lhw_holding_file
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
                send_notification(f"📈 量化王策略新增持仓 {len(new_data)} 条：\n{new_data_print}")
                
                # 保存新增数据到文件
                today = normalize_time(datetime.datetime.now().strftime('%Y-%m-%d'))
                save_to_operation_history_excel(new_data, history_file, f'{today}', index=False)
                logger.info("💾 新增持仓数据已保存到文件")
            else:
                logger.info("✅ 量化王策略持仓无变化")
                
        except Exception as e:
            logger.error(f"比较量化王策略持仓变化时出错: {e}")

if __name__ == '__main__':
    processor = LhwHoldingProcessor()
    success = processor.execute_lhw_trades()
    if success:
        logger.info("✅ 量化王策略调仓执行完成")
    else:
        logger.error("❌ 量化王策略调仓执行失败")
    
    # 比较持仓变化
    processor.compare_holding_changes()