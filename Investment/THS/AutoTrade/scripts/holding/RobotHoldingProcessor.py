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
from Investment.THS.AutoTrade.utils.format_data import determine_market

logger = setup_logger(__name__)

# 所有股票信息文件路径
ALL_STOCKS_FILE = 'all_stocks.xlsx'
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

        if all_stocks_df is None:
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

        # 增加重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
                response.raise_for_status()
                response_json = response.json()
                return response_json
            except requests.RequestException as e:
                logger.error(f"第 {attempt + 1} 次尝试，请求机器人 {robot_id} 数据失败: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    return None
        return None

    def extract_robot_data(self, response_data):
        """提取机器人持仓数据并转换为统一格式"""
        if not response_data or 'data' not in response_data:
            logger.error("无效的响应数据")
            return pd.DataFrame()

        data = response_data['data']

        # 提取持仓股票信息
        positions_data = []
        for log in data.get('logs', []):
            symbol = log.get('symbol', '')
            symbol_name = log.get('symbolName', None)

            # 获取股票名称
            if symbol_name and symbol_name.strip() and symbol_name != 'None':
                stock_name = symbol_name.strip()
            else:
                # 从股票代码中提取纯数字部分用于查找名称
                code = symbol.replace('sh', '').replace('sz', '') if symbol.startswith(('sh', 'sz')) else symbol
                stock_name = self.get_stock_name_by_code(code)

            market = determine_market(symbol)

            position_item = {
                "名称": data.get('name', ''),
                "操作": "买入",  # 默认为买入持仓
                "标的名称": stock_name,
                "代码": symbol,
                "市场": market,
                "最新价": log.get('price', 0),
                "成本价": log.get('basePrice', 0),
                "持仓量": log.get('shares', 0),
                "市值": log.get('marketValue', 0),
                "新比例%": 0,  # 暂时无法计算准确比例
                "时间": datetime.now().strftime('%Y-%m-%d')
            }
            positions_data.append(position_item)

        # 将提取的数据转换为 DataFrame
        stocks_df = pd.DataFrame(positions_data)
        return stocks_df

    def save_all_robot_holding_data(self):
        """获取所有机器人的持仓数据，并保存到 Excel 文件中"""
        # 加载所有股票信息
        self.load_all_stocks()

        # 收集所有机器人的持仓数据
        all_positions = []

        # 创建一个Excel写入器
        with pd.ExcelWriter(Robot_portfolio_today_file, engine='openpyxl') as writer:
            # 遍历所有机器人
            for robot_name, robot_id in robots.items():
                logger.info(f"正在获取 {robot_name} 的数据...")

                # 获取机器人数据
                response_data = self.fetch_robot_data(robot_id)

                if response_data and response_data.get("message", {}).get("state") == 0:
                    # 提取数据
                    stocks_df = self.extract_robot_data(response_data)

                    # 以机器人的名称作为工作表名保存数据
                    # 确保工作表名称不超过31个字符
                    stocks_sheet_name = f"{robot_name}_持仓信息"[:31]

                    # 保存到Excel的不同工作表
                    if not stocks_df.empty:
                        all_positions.append(stocks_df)
                        stocks_df.to_excel(writer, sheet_name=stocks_sheet_name, index=False)
                        logger.info(f"已保存 {robot_name} 的持仓信息到工作表 {stocks_sheet_name}")
                else:
                    logger.error(f"获取 {robot_name} 数据失败")

        if all_positions:
            # 合并所有持仓数据
            all_positions_df = pd.concat(all_positions, ignore_index=False)
            all_positions_df.index = all_positions_df.index + 1

            # 只保留沪深A股
            all_positions_df = all_positions_df[all_positions_df['市场'] == '沪深A股']
            # 按价格从低到高排序
            all_positions_df = all_positions_df.sort_values('最新价', ascending=True)

            # 保存合并后的数据到Excel
            today = datetime.now().strftime('%Y-%m-%d')

            # 创建一个字典来存储所有工作表数据
            all_sheets_data = {}

            try:
                # 如果文件存在，读取现有数据
                if os.path.exists(Robot_portfolio_today_file):
                    with pd.ExcelFile(Robot_portfolio_today_file) as xls:
                        existing_sheets = xls.sheet_names
                        logger.info(f"保存前文件中已存在的工作表: {existing_sheets}")

                    # 读取除今天以外的所有现有工作表
                    with pd.ExcelFile(Robot_portfolio_today_file) as xls:
                        for sheet_name in existing_sheets:
                            if sheet_name != today:
                                all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

                # 将今天的数据放在第一位
                all_sheets_data = {today: all_positions_df, **all_sheets_data}
                logger.info(f"即将保存的所有工作表: {list(all_sheets_data.keys())}")

                # 写入所有数据到Excel文件（覆盖模式），注意不保存索引
                with pd.ExcelWriter(Robot_portfolio_today_file, engine='openpyxl', mode='w') as writer:
                    for sheet_name, df in all_sheets_data.items():
                        logger.info(f"正在保存工作表: {sheet_name}")
                        df.to_excel(writer, sheet_name=sheet_name, index=False)

                logger.info(f"✅ 所有持仓数据已保存，{today} 数据位于第一个 sheet，共 {len(all_positions_df)} 条")
                return True
            except Exception as e:
                logger.error(f"❌ 保存持仓数据失败: {e}")
                # 如果出错，至少保存今天的数据
                try:
                    with pd.ExcelWriter(Robot_portfolio_today_file, engine='openpyxl') as writer:
                        all_positions_df.to_excel(writer, sheet_name=today, index=False)
                    logger.info(f"✅ 文件保存完成，sheet: {today}")
                    return True
                except Exception as e2:
                    logger.error(f"❌ 保存今日数据也失败了: {e2}")
                    return False
        else:
            logger.warning("未获取到任何机器人持仓数据")
            return False

    def execute_robot_trades(self):
        """执行机器人策略的调仓操作"""
        try:
            # 保存最新持仓数据
            success = self.save_all_robot_holding_data()

            if not success:
                logger.error("保存机器人持仓数据失败，无法执行交易")
                return False

            # 执行调仓操作
            from Investment.THS.AutoTrade.config.settings import Robot_portfolio_today_file
            success = self.operate_result(
                holding_file=Robot_portfolio_today_file,
                portfolio_today_file=Robot_portfolio_today_file,
                account_name="长城证券"
            )

            return success
        except Exception as e:
            logger.error(f"执行机器人策略调仓操作时出错: {e}")
            return False

def main():
    processor = RobotHoldingProcessor()
    success = processor.execute_robot_trades()
    if success:
        logger.info("✅ 机器人策略调仓执行完成")
    else:
        logger.error("❌ 机器人策略调仓执行失败")

# 运行主函数
if __name__ == "__main__":
    main()
