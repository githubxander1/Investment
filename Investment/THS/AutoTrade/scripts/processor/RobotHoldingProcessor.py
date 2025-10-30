import pandas as pd
import akshare as ak
import os
import time
import random
import requests
import json
from datetime import datetime

from Investment.THS.AutoTrade.config.settings import Robot_portfolio_today_file, robots
from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.format_data import determine_market, get_new_records, standardize_dataframe, normalize_time
from Investment.THS.AutoTrade.scripts.data_process import read_today_portfolio_record, save_to_operation_history_excel
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.utils.enhanced_requests import post

logger = setup_logger(__name__)

# 所有股票信息文件路径
ALL_STOCKS_FILE = '../holding/all_stocks.xlsx'
Stock_zh_a_spot = 'stock_zh_a_spot.xlsx'

# 全局变量存储股票信息
all_stocks_df = None

class RobotHoldingProcessor(CommonHoldingProcessor):
    def __init__(self):
        super().__init__(account_name="长城证券")

    def load_all_stocks(self):
        """加载所有股票信息到内存中"""
        global all_stocks_df

        # 首先尝试从本地Excel文件加载股票信息
        if os.path.exists(ALL_STOCKS_FILE):
            try:
                logger.info("正在从本地Excel文件加载股票信息...")
                all_stocks_df = pd.read_excel(ALL_STOCKS_FILE)
                logger.info(f"从本地Excel文件成功加载 {len(all_stocks_df)} 条股票信息")
                return
            except Exception as e:
                logger.error(f"从本地Excel文件加载股票信息失败: {e}")

        # 如果本地文件不存在或加载失败，则从网络获取
        if not os.path.exists(Stock_zh_a_spot):
            logger.info("本地Stock_zh_a_spotExcel文件不存在，正在尝试通过 stock_zh_a_spot 获取所有股票信息...")
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    logger.info(f"正在尝试通过 stock_zh_a_spot 获取所有股票信息... (第 {attempt + 1} 次尝试)")
                    # 添加随机延迟，避免请求过于频繁
                    time.sleep(random.uniform(1, 2))

                    # 使用stock_zh_a_spot获取所有股票信息
                    all_stocks_df = ak.stock_zh_a_spot()
                    #增加一列'市场'
                    if not all_stocks_df.empty and '代码' in all_stocks_df.columns:
                        all_stocks_df['市场'] = all_stocks_df['代码'].apply(lambda x: determine_market(x))

                    # 保存到Excel文件供以后使用
                    all_stocks_df.to_excel(ALL_STOCKS_FILE, index=False)
                    logger.info(f"已保存所有股票信息到 {ALL_STOCKS_FILE}")
                    logger.info(f"通过 stock_zh_a_spot 成功获取 {len(all_stocks_df)} 条股票信息")
                    return

                except Exception as e:
                    logger.error(f"第 {attempt + 1} 次尝试获取股票信息失败: {e}")
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # 指数退避
                        logger.info(f"等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    continue

            logger.error("所有方法都失败，无法获取股票信息")
            all_stocks_df = pd.DataFrame()

    def get_stock_name_by_code(self, code):
        """根据股票代码获取股票名称"""
        global all_stocks_df

        if all_stocks_df is None or all_stocks_df.empty:
            return f"未知股票({code})"

        # 查找匹配的股票代码
        matching_stocks = all_stocks_df[all_stocks_df['代码'] == code]
        if not matching_stocks.empty:
            return matching_stocks.iloc[0]['名称']

        # 如果6位代码没找到，尝试添加市场前缀查找
        if not code.startswith(('sh', 'sz')):
            # 尝试上海市场
            sh_code = f"sh{code}" if code.startswith('6') else f"sz{code}"
            matching_stocks = all_stocks_df[all_stocks_df['代码'] == sh_code]
            if not matching_stocks.empty:
                return matching_stocks.iloc[0]['名称']

        return f"未知股票({code})"

    def fetch_robot_data(self, robot_id, token="27129c04fb43a33723a9f7720f280ff9"):
        """获取单个机器人的数据"""
        url = "http://ai.api.traderwin.com/api/ai/robot/get.json"

        headers = {
            "Content-Type": "application/json",
            "from": "Android",
            "token": token,
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        payload = {
            "cmd": "9015",
            "robotId": robot_id
        }

        # 实现重试机制和超时处理
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = post(url, headers=headers, data=json.dumps(payload), timeout=10)
                response_json = response.json()
                return response_json
            except requests.RequestException as e:
                error_msg = f"第 {attempt + 1} 次尝试，请求机器人 {robot_id} 数据失败: {e}"
                logger.warning(error_msg)
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    logger.error(error_msg)
                    send_notification(error_msg)
                    return None

        return None

    def extract_robot_data(self, response_data):
        """提取机器人持仓数据并转换为统一格式"""
        if not response_data or not isinstance(response_data, dict) or 'data' not in response_data:
            logger.error("无效的响应数据")
            return pd.DataFrame(), pd.DataFrame()

        data = response_data['data']
        if not isinstance(data, dict):
            logger.error("响应数据中的data字段格式异常")
            return pd.DataFrame(), pd.DataFrame()

        # 提取持仓股票信息
        positions_data = []
        logs = data.get('logs', [])
        if not isinstance(logs, list):
            logger.error("响应数据中的logs字段格式异常")
            logs = []
            
        # 先计算总持仓量，用于计算比例
        total_shares = sum([log.get('shares', 0) for log in logs if isinstance(log, dict)])
        
        for log in logs:
            if not isinstance(log, dict):
                logger.warning(f"日志数据格式异常: {log}")
                continue
                
            symbol = log.get('symbol', '')
            symbol_name = log.get('symbolName', None)

            # 获取股票名称
            if symbol_name and symbol_name.strip() and symbol_name != 'None':
                stock_name = symbol_name.strip()
            else:
                # 从股票代码中提取纯数字部分用于查找名称
                code = symbol.replace('sh', '').replace('sz', '') if symbol.startswith(('sh', 'sz')) else symbol
                stock_name = self.get_stock_name_by_code(code)

            # 确定市场
            market = determine_market(symbol)
            
            # 计算新比例%
            shares = log.get('shares', 0)
            new_ratio = (shares / total_shares * 100) if total_shares > 0 else 0

            position_item = {
                "股票代码": symbol,
                "股票名称": stock_name,
                "市场": market,
                "最新价": log.get('price', ''),
                "成本价": log.get('basePrice', ''),
                "持仓量": shares,
                "新比例%": round(new_ratio, 2),  # 添加新比例%字段
                "市值": log.get('marketValue', ''),
                "今日盈亏": log.get('todayGains', ''),
                "累计盈亏": log.get('totalGains', ''),
                "今日收益率": (log.get('todayGains', 0) / log.get('todayCost', 1)) * 100 if log.get('todayCost', 0) != 0 else 0,
                "累计收益率": (log.get('totalGains', 0) / log.get('lockCost', 1)) * 100 if log.get('lockCost', 0) != 0 else 0,
            }
            positions_data.append(position_item)

        # 将提取的数据转换为 DataFrame
        combo_df = pd.DataFrame([data])  # 保留原始data用于组合信息
        stocks_df = pd.DataFrame(positions_data)

        return combo_df, stocks_df

    def save_all_robot_holding_data(self):
        """
        获取所有机器人的持仓数据，并保存到 Excel 文件中，当天数据保存在第一个sheet
        """
        logger.info("📂 开始获取并保存所有机器人持仓数据")
        
        today = datetime.now().strftime('%Y-%m-%d')
        all_holdings_df = self.get_all_robot_current_holdings()
        
        # 检查是否获取到有效数据
        if all_holdings_df is None:
            logger.error("❌ 未获取到有效机器人持仓数据，无法保存")
            return False
            
        if all_holdings_df.empty:
            logger.warning("⚠️ 获取到的机器人持仓数据为空")
            send_notification("⚠️ 机器人持仓数据为空，请检查接口是否正常")
            return False  # 数据为空也视为保存失败

        file_path = Robot_portfolio_today_file

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
            # 如果出错，至少保存今天的数据
            try:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    all_holdings_df.to_excel(writer, sheet_name=today, index=False)
                logger.info(f"✅ 文件保存完成，sheet: {today}")
                return True  # 成功保存数据，返回True
            except Exception as e2:
                logger.error(f"❌ 保存今日数据也失败了: {e2}")
                send_notification(f"❌ 机器人持仓数据保存失败: {e2}")
                return False  # 保存失败，返回False

    def execute_robot_trades(self):
        """执行机器人策略的调仓操作"""
        try:
            logger.info("🔄 开始执行机器人策略调仓操作")
            
            # 首先获取当前机器人持仓数据用于变化检测（不保存到文件）
            current_holdings = self.get_all_robot_current_holdings()
            if current_holdings is None:
                error_msg = "❌ 未获取到机器人持仓数据，跳过调仓操作"
                logger.error(error_msg)
                send_notification(error_msg)
                return False
            
            # 保存最新持仓数据到文件
            save_result = self.save_all_robot_holding_data()
            if not save_result:
                error_msg = "❌ 机器人持仓数据保存失败，跳过调仓操作"
                logger.error(error_msg)
                send_notification(error_msg)
                return False

            # 使用CommonHoldingProcessor中的方法执行交易操作
            from Investment.THS.AutoTrade.config.settings import Robot_holding_file
            success = self.operate_result(
                holding_file=Robot_holding_file,
                portfolio_today_file=Robot_portfolio_today_file,
                account_name="长城证券"
            )

            if success:
                logger.info("✅ 机器人策略调仓执行完成")
                # send_notification("✅ 机器人策略调仓执行完成")
            else:
                error_msg = "❌ 机器人策略调仓执行失败"
                logger.error(error_msg)
                send_notification(error_msg)
                
            return success
        except Exception as e:
            error_msg = f"执行机器人策略调仓操作时出错: {e}"
            logger.error(error_msg)
            send_notification(error_msg)
            return False

    def compare_holding_changes(self):
        """比较机器人持仓变化并通知新增数据"""
        try:
            logger.info("🔄 开始比较机器人持仓变化")
            
            # 获取当前持仓数据
            current_holdings = self.get_all_robot_current_holdings()
            if current_holdings is None:
                warning_msg = "❌ 未获取到当前机器人持仓数据"
                logger.error(warning_msg)
                send_notification(warning_msg)
                return
            
            if current_holdings.empty:
                logger.info("📋 当前机器人持仓数据为空")
                return
            
            # 读取历史持仓数据
            from Investment.THS.AutoTrade.config.settings import Robot_holding_file
            history_file = Robot_holding_file
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
                send_notification(f"📈 机器人新增持仓 {len(new_data)} 条：\n{new_data_print}")
                
                # 保存新增数据到文件
                today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
                save_to_operation_history_excel(new_data, history_file, f'{today}', index=False)
                logger.info("💾 新增持仓数据已保存到文件")
            else:
                logger.info("✅ 机器人持仓无变化")
                
        except Exception as e:
            error_msg = f"比较机器人持仓变化时出错: {e}"
            logger.error(error_msg)
            send_notification(error_msg)

    def get_all_robot_current_holdings(self):
        """
        获取所有机器人的当前持仓数据，用于比较是否发生变化
        """
        logger.info("🔍 开始获取所有机器人当前持仓数据用于变化检测")
        
        # 加载所有股票信息
        self.load_all_stocks()
        
        # 获取所有机器人的持仓数据
        all_holdings = []
        success_count = 0  # 记录成功获取数据的机器人数量
        total_count = len(robots)  # 总机器人数量
        
        for name, id in robots.items():
            response_data = self.fetch_robot_data(id)
            if response_data and response_data.get("message", {}).get("state") == 0:
                # 提取数据
                _, positions_df = self.extract_robot_data(response_data)
            else:
                positions_df = pd.DataFrame()
            
            # 只保留沪深A股的
            if not positions_df.empty and '市场' in positions_df.columns:
                positions_df = positions_df[positions_df['市场'] == '沪深A股']
                # 按价格从低到高排序
                if '最新价' in positions_df.columns:
                    positions_df = positions_df.sort_values('最新价', ascending=True)
            
            # 特殊处理：对于"钢铁"机器人，只允许卖出操作，不允许买入
            if name == "钢铁" and not positions_df.empty:
                # 清空持仓数据，这样就只会产生卖出操作，不会有买入操作
                positions_df = pd.DataFrame(columns=positions_df.columns)
                logger.info(f"🤖 对机器人 {name} 进行特殊处理：只允许卖出，清空买入信号")
            
            # 特殊处理：对于"有色金属"机器人，只允许卖出操作，不允许买入
            if name == "有色金属" and not positions_df.empty:
                # 清空持仓数据，这样就只会产生卖出操作，不会有买入操作
                positions_df = pd.DataFrame(columns=positions_df.columns)
                logger.info(f"🤖 对机器人 {name} 进行特殊处理：只允许卖出，清空买入信号")
            
            if positions_df is not None and not positions_df.empty:
                logger.info(f"📊 机器人{id}({name})持仓数据:{len(positions_df)}条")
                logger.debug(f"\n{positions_df}")
                all_holdings.append(positions_df)
                success_count += 1
            else:
                logger.info(f"⚠️ 没有获取到机器人{id}({name})的持仓数据")

        # 检查数据获取情况
        if success_count == 0:
            logger.error("❌ 未获取到任何机器人持仓数据")
            send_notification("❌ 未获取到任何机器人持仓数据")
            return None
        elif success_count < total_count:
            logger.warning(f"⚠️ 部分机器人数据获取失败: {success_count}/{total_count}")
            send_notification(f"⚠️ 机器人数据获取异常: {success_count}/{total_count} 个机器人数据获取成功")
        
        all_holdings_df = pd.concat(all_holdings, ignore_index=True)
        logger.info(f"📈 总计获取到 {len(all_holdings_df)} 条持仓记录（先沪深）")
        return all_holdings_df

if __name__ == '__main__':
    processor = RobotHoldingProcessor()
    success = processor.execute_robot_trades()
    if success:
        logger.info("✅ 机器人策略调仓执行完成")
    else:
        logger.error("❌ 机器人策略调仓执行失败")
    
    # 比较持仓变化
    # processor.compare_holding_changes()