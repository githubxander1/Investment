import time
from datetime import datetime, timedelta
import json
import pandas as pd
import requests
from pprint import pprint
import asyncio

from Investment.THS.AutoTrade.config.settings import Robot_portfolio_today_file
from Investment.THS.AutoTrade.scripts.data_process import read_today_portfolio_record, save_to_operation_history_excel
from Investment.THS.AutoTrade.utils.format_data import determine_market, normalize_time, standardize_dataframe, \
    get_new_records
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger(__name__)

# 时间转换工具
def convert_timestamp(timestamp):
    """将毫秒时间戳转为可读日期"""
    if timestamp and timestamp > 0:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return None

# 获取成交明细
def get_trade_details(robot_id):
    url = "http://ai.api.traderwin.com/api/ai/robot/history.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "27129c04fb43a33723a9f7720f280ff9",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    payload = {
        "index": 1,
        "pageSize": 5,
        "cmd": "9013",
        "robotId": robot_id,
        "type": -1  # 查询全部交易
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        # pprint(response_data)
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


def extract_trade_data(robots):
    today = datetime.now().date().strftime("%Y-%m-%d")

    all_today_trades = []
    for robot_name, robot_id in robots.items():
        result = get_trade_details(robot_id)
        if result and result.get("message", {}).get("state") == 0:
            data_list = result.get("data", {}).get("data", [])

            for trade in data_list:
                code = trade.get("symbol")
                market = determine_market(code)
                trade_date = convert_timestamp(trade.get("tradeDate"))
                if trade_date and trade_date.startswith(today):
                    trade_info = {
                        # "交易ID": trade.get("logId"),
                        # "机器人ID": trade.get("robotId"),
                        "名称": robot_name,
                        "操作": "买入" if trade.get("type") == 1 else "卖出" if trade.get("type") == 0 else "已取消",
                        "标的名称": trade.get("symbolNmae"),
                        "代码": code,
                        "最新价": trade.get("price"),  # 原成交价格
                        "新比例%": 0,
                        "市场": market,
                        "时间": convert_timestamp(trade.get("created")),
                        "交易数量": trade.get("shares"),
                        # "买入价格": trade.get("buyPrice"),
                        # "交易金额": trade.get("balance"),
                        # "完成时间": convert_timestamp(trade.get("tradeTime"))
                        # "时间": convert_timestamp(trade.get("buyDate")),#原买入时间
                    }
                    all_today_trades.append(trade_info)
                    # 通知格式输出
                    # print(f"[{datetime.now().strftime('%Y-%m-%d')}] "
                    #       f"名称：{trade_info['名称']}，"
                    #       f"操作：{trade_info['操作']}，"
                    #       f"标的名称：{trade_info['标的名称']}，"
                    #       f"市场：{trade_info['市场']}，"
                    #       f"最新价：{trade_info['最新价']}，"
                    #       f"时间：{trade_info['时间']},"
                    #       f"新比例%：{trade_info['新比例%']}")
                    # f"代码：{trade_info['代码']}，"
                    # f"数量：{trade_info['交易数量']}，"
                    # f"买入价格：{trade_info['买入价格']}，"

        else:
            print(f"⚠️ 获取 {robot_name} 成交记录失败")

    if all_today_trades:  # 列表非空（空列表 [] 会被视为 False，所以 if my_list 等价于"非空"）
       df = pd.DataFrame(all_today_trades)
       return df
    # 当没有数据时，返回一个空的 DataFrame，列名与有数据时一致
    return pd.DataFrame(columns=['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间'])

async def Robot_main():
    # 机器人列表
    robots = {
        "有色金属": "8afec86a-e573-411a-853f-5a9a044d89ae",
        "钢铁": "89c1be35-08a6-47f6-a8c9-1c64b405dab6",
        "建筑行业": "ca2d654c-ab95-448e-9588-cbc89cbb7a9e"
    }
    all_today_trades_df = extract_trade_data(robots)
    # all_today_trades_df = all_today_trades_df[all_today_trades_df["市场"] == "沪深A股"]
    # 读取历史数据
    history_data_file = Robot_portfolio_today_file
    expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间']
    try:
        # 打印数据列的数据类型
        history_data_df = read_today_portfolio_record(history_data_file)
        # print(f'历史数据列的数据类型:\n{history_data_df.dtypes}')
        if not history_data_df.empty:
            history_data_df['代码'] = history_data_df['代码'].astype(str).str.zfill(6)  # 立即转为 str
            history_data_df['新比例%'] = history_data_df['新比例%'].round(2).astype(float)
        else:
            history_data_df = pd.DataFrame(columns=expected_columns)
    except Exception:  # 读取历史数据失败，初始化保存一个
        history_data_df = pd.DataFrame(columns=expected_columns)
        today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
        save_to_operation_history_excel(history_data_df, history_data_file, f'{today}', index=False)
        # history_data_df.to_csv(history_data_df_file, index=False)
        # print(f'初始化历史记录文件: {history_data_df_file}')

    # 标准化数据格式
    all_today_trades_df = standardize_dataframe(all_today_trades_df)
    history_data_df = standardize_dataframe(history_data_df)
    # print(f'读取历史记录: {history_data_df}')
    # print(f'历史记录数据类型: {history_data_df.dtypes}')

    # 获取新增数据
    new_data_df = get_new_records(all_today_trades_df, history_data_df)
    # print(f'获取新增数据: new_data_df)')

    # 保存新增数据并通知
    if new_data_df.empty:
        logger.info("---------------Robot 无新增交易数据----------------")
        # # 即使没有新增数据，也打印一下今日数据
        # if not all_today_trades_df.empty:
        #     today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
        #     save_to_operation_history_excel(all_today_trades_df, history_data_file, f'{today}')
        #     all_today_trades_df_print_without_header = all_today_trades_df.to_string(index=False)
        #     send_notification(f"{len(all_today_trades_df)} 条Robot调仓（今日全部）：\n{all_today_trades_df_print_without_header}")
        return False, None
    # with open(OPRATION_RECORD_DONE_FILE, 'w') as f:
    #     f.write('1')
    # 打印并保存新增数据
    # new_data_df_without_sc = new_data_df.drop(columns=['理由'], errors='ignore')
    # print(new_data_df_without_sc)

    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
    # header = not os.path.exists(history_data_file) or os.path.getsize(history_data_file) == 0
    save_to_operation_history_excel(new_data_df, history_data_file, f'{today}')
    # logger.info(f"✅ 保存新增调仓数据成功 \n{new_data_df}")
    # from Investment.THS.AutoTrade.utils.file_monitor import update_file_status
    # update_file_status(history_data_df_file)

    # 发送通知
    new_data_df_print_without_header = all_today_trades_df.to_string(index=False)
    # print(f"新增的数据各列数据类型：\n{all_today_trades_df.dtypes}")
    send_notification(f"{len(new_data_df)} 条新增Robot调仓：\n{new_data_df_print_without_header}")
    # logger.info("✅ 检测到新增策略调仓，准备启动自动化交易")
    # from Investment.THS.AutoTrade.utils.event_bus import event_bus
    # event_bus.publish('new_trades_available', new_data_df)
    # from Investment.THS.AutoTrade.utils.trade_utils import mark_new_trades_as_scheduled
    #
    # mark_new_trades_as_scheduled(new_data_df, OPERATION_HISTORY_FILE)

    return True, new_data_df
    # today = datetime.now().date().strftime("%Y-%m-%d")
    #
    # all_today_trades = []
    # for robot_name, robot_id in robots.items():
    #     result = get_trade_details(robot_id)
    #     if result and result.get("message", {}).get("state") == 0:
    #         data_list = result.get("data", {}).get("data", [])
    #
    #         for trade in data_list:
    #             code = trade.get("symbol")
    #             market = determine_market(code)
    #             trade_date = convert_timestamp(trade.get("tradeDate"))
    #             if trade_date and trade_date.startswith(today):
    #                 trade_info = {
    #                     # "交易ID": trade.get("logId"),
    #                     # "机器人ID": trade.get("robotId"),
    #                     "名称": robot_name,
    #                     "操作": "买入" if trade.get("type") == 1 else "卖出" if trade.get("type") == 0 else "已取消",
    #                     "标的名称": trade.get("symbolNmae"),
    #                     "代码": code,
    #                     "最新价": trade.get("price"),#原成交价格
    #                     "新比例%": 0,
    #                     "市场": market,
    #                     "时间": convert_timestamp(trade.get("created")),
    #                     "交易数量": trade.get("shares"),
    #                     # "买入价格": trade.get("buyPrice"),
    #                     # "交易金额": trade.get("balance"),
    #                     # "完成时间": convert_timestamp(trade.get("tradeTime"))
    #                     # "时间": convert_timestamp(trade.get("buyDate")),#原买入时间
    #                 }
    #                 all_today_trades.append(trade_info)
    #                 # 通知格式输出
    #                 # print(f"[{datetime.now().strftime('%Y-%m-%d')}] "
    #                 #       f"名称：{trade_info['名称']}，"
    #                 #       f"操作：{trade_info['操作']}，"
    #                 #       f"标的名称：{trade_info['标的名称']}，"
    #                 #       f"市场：{trade_info['市场']}，"
    #                 #       f"最新价：{trade_info['最新价']}，"
    #                 #       f"时间：{trade_info['时间']},"
    #                 #       f"新比例%：{trade_info['新比例%']}")
    #                       # f"代码：{trade_info['代码']}，"
    #                       # f"数量：{trade_info['交易数量']}，"
    #                       # f"买入价格：{trade_info['买入价格']}，"
    #
    #     else:
    #         print(f"⚠️ 获取 {robot_name} 成交记录失败")

    # if all_today_trades is not None:
    #     all_today_trades_df  = pd.DataFrame(all_today_trades)
    #     send_notification(f" 新增交易 {len(all_today_trades_df)}条：\n{all_today_trades_df}")
    #     logger.info(f"今日有新增数据:/n{all_today_trades_df}")
    #     # print(all_today_trades_df)
    #     all_today_trades_df.to_excel(Robot_portfolio_today_file, index=False)
    #     logger.info(f"已保存Robot今日数据到文件：{Robot_portfolio_today_file}")
    #     return True, all_today_trades_df
    # logger.info("⚠️ Robot今日无新增数据")
    # return False, None

#
# 定时执行函数
# def schedule_daily_check(target_time="09:31"):
#     while True:
#         now = datetime.now()
#         today_time = now.strftime("%H:%M")
#         if today_time == target_time:
#             print(f"⏰ 正在检查 {now.strftime('%Y-%m-%d')} 的交易记录...")
#             Robot_main()
#             time.sleep(60)  # 避免重复执行
#         else:
#             time.sleep(30)  # 每30秒检查一次时间

# 启动定时任务
if __name__ == "__main__":
    # schedule_daily_check()
    # print(Robot_main())
    asyncio.run(Robot_main())
