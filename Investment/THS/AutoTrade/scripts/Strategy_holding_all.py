import os
import time
from datetime import datetime, timedelta
from pprint import pprint

import openpyxl
import pandas as pd
import requests
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
# import logger

from Investment.THS.AutoTrade.utils.format_data import determine_market, normalize_time
from Investment.THS.AutoTrade.utils.logger import setup_logger
logger = setup_logger("strategy_fetch.log")

# 配置日志记录
# logger.basicConfig(
#     level=logger.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logger.FileHandler("strategy_fetch.log", encoding="utf-8"),
#         logger.StreamHandler()
#     ]
# )

# 导入配置
from Investment.THS.AutoTrade.config.settings import Strategy_ids, Strategy_id_to_name, Strategy_holding_file, \
    Ai_Strategy_holding_file


def parse_position_date(date_value):
    """统一解析日期时间值"""
    if date_value == 'N/A':
        return 'N/A'

    if isinstance(date_value, int):
        try:
            # 处理毫秒时间戳
            position_date_s = date_value / 1000
            position_date = datetime.fromtimestamp(position_date_s)
            return position_date.strftime('%Y-%m-%d %H:%M:%S')
        except (OverflowError, OSError, ValueError) as e:
            logger.error(f"日期转换失败: {str(e)}")
            return 'Invalid Date'

    if isinstance(date_value, str):
        # 尝试常见日期格式解析
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y-%m-%d', '%Y%m%d'):
            try:
                d = datetime.strptime(date_value, fmt)
                return d.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue

    return 'Invalid Date'

def get_strategy_name(strategy_id):
    """获取策略名称，优先使用本地映射，否则标记为未知策略"""
    name = Strategy_id_to_name.get(str(strategy_id), None)
    if name is None:
        logger.warning(f"发现未映射的策略ID: {strategy_id}")
        return f"未知策略({strategy_id})"
    return name

def fetch_strategy_profit(strategy_id):
    """获取指定策略的收益信息"""
    ua = UserAgent()
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
    params = {"strategyId": strategy_id}
    headers = {"User-Agent": ua.random}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        # pprint(data)
        position_stocks = data.get('result', {}).get('positionStocks', [])
        # 提取positionStocks所需字段
        positions_info = []
        for position in position_stocks:
            try:
                # 提取基础信息
                name = position.get('stkName', 'N/A')
                code = str(position.get('stkCode', 'N/A').split('.')[0]).zfill(6)
                market = determine_market(code)
                industry = position.get('industry', 'N/A')

                # 处理数值字段
                price = float(position.get('price', 0)) if position.get('price') not in (None, '') else 'N/A'

                position_ratio_str = position.get('positionRatio', '0')
                # if isinstance(position_ratio_str, (int, float)):
                #     position_ratio_str = str(position_ratio_str)  # 确保是字符串类型
                # position_ratio = float(position_ratio_str.strip('%')) if position_ratio_str not in ('', 'N/A') else 'N/A'
                position_ratio = round(position_ratio_str,2)

                profit_and_loss_ratio_str = position.get('profitAndLossRatio', '0')
                # if isinstance(profit_and_loss_ratio_str, (int, float)):
                #     profit_and_loss_ratio_str = str(profit_and_loss_ratio_str)  # 确保是字符串类型
                # profit_and_loss_ratio = float(profit_and_loss_ratio_str) if profit_and_loss_ratio_str not in ('', 'N/A') else 'N/A'
                profit_and_loss_ratio = round(profit_and_loss_ratio_str,2)
                # # 格式化百分比
                # if isinstance(position_ratio, (int, float)):
                #     position_ratio = f"{position_ratio * 100:.2f}"
                # if isinstance(profit_and_loss_ratio, (int, float)):
                #     profit_and_loss_ratio = f"{profit_and_loss_ratio * 100:.2f}"

                # 处理日期
                position_date_str = parse_position_date(position.get('positionDate', 'N/A'))

                # 添加持仓信息
                positions_info.append({
                    '名称': get_strategy_name(strategy_id),
                    '操作': '买入',
                    '标的名称': name,
                    '代码': code,
                    '最新价': round(price, 3) if isinstance(price, (int, float)) else price,# 原价格
                    '新比例%': position_ratio,#原持仓比例
                    '市场': market,
                    '时间': position_date_str,#持仓日期
                    '行业': industry,
                    '盈亏比例': profit_and_loss_ratio,
                })

            except Exception as e:
                logger.error(f"处理单个持仓信息时出错: {str(e)}")
                continue

        logger.info(f"成功获取策略 {strategy_id} 的 {len(positions_info)} 条持仓信息")

        position_info_df = pd.DataFrame(positions_info)
        # print(position_info_df['新比例%'])
        return position_info_df

    except requests.exceptions.RequestException as e:
        logger.error(f"请求策略 {strategy_id} 数据失败: {str(e)}")
        return []

def Ai_strategy_main():
    """主函数"""
    Strategy_ids = ['156275']
    all_positions_info = []

    all_positions_info = fetch_strategy_profit(Strategy_ids[0])
    # print(all_positions_info["新比例%"])

    if all_positions_info is not None:
        # 检查是否存在 '市场' 列再进行过滤
        if '市场' in all_positions_info.columns:
            all_positions_info = all_positions_info[all_positions_info['市场'] == '沪深A股']
        else:
            logger.warning("DataFrame 中没有 '市场' 列，跳过市场过滤")

        # 去重处理
        all_positions_info = all_positions_info.drop_duplicates(subset=['标的名称', '操作', '新比例%', '时间'])
        # 打印结果（不包含股票代码和市场列）
        # positions_df_without_code = positions_df.drop(columns=['代码', '行业'], errors='ignore')
        # print("\n持仓信息：")
        # print(positions_df_without_code.to_string(index=False))
        # print(all_positions_info.to_string(index=False))
        # today = datetime.today().strftime('%Y-%m-%d')
        # print(today)
        # all_positions_info.to_excel(Strategy_holding_file,sheet_name=today,index=False)
        save_to_excel_by_date(all_positions_info, Ai_Strategy_holding_file)  # 按日期保存
        time.sleep(2)
        datas = compare_today_yesterday(Ai_Strategy_holding_file)  # 对比数据
        # print(type(datas))
        return True, datas
    else:
        logger.info("没有获取到任何持仓数据需要保存")
        return False, None
def save_to_excel_by_date(df, file_path):
    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
    try:
        if not os.path.exists(file_path):
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # print(f"文件不存在时要保存的df : {df}")
                df.to_excel(writer, sheet_name=today, index=False)
            logger.info(f"✅ 创建并保存数据到Excel文件: {file_path}, 表名称: {today}")
            return

        # # 文件存在，读取现有 sheet
        with pd.ExcelFile(file_path, engine='openpyxl') as xls:
            existing_sheets = xls.sheet_names

        # # 如果已有 today sheet
        if today in existing_sheets:
            today_existing_df = pd.read_excel(file_path, sheet_name=today)
            wb = openpyxl.load_workbook(file_path)
            sheets = wb.sheetnames
            if today in sheets:
                wb.move_sheet(today, offset=-len(sheets) + 1)
                wb.save(file_path)
                logger.info(f"✅ 新增今日数据并置顶到Excel文件: {file_path}, 表名称: {today}")
            else:
                logger.warning(f"⚠️ sheet {today} 写入失败")
            # return
            # print(f"today_existing_df : {today_existing_df}")
        #     # combined_df = pd.concat([today_existing_df, df], ignore_index=True)
        #     # combined_df = combined_df.drop_duplicates(subset=['标的名称', '操作', '新比例%', '时间'])
            #
            # with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
            #         # print(f"要保存的df : {combined_df}")
            #     df.to_excel(writer,sheet_name=today, index=False)
            #     logger.info(f"✅ 更新今日数据到Excel文件: {file_path}, 表名称: {today}")
        # else:
        #     # 新增 today sheet 并置顶
        #     with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        #         df.to_excel(writer, sheet_name=today, index=False)

        # 使用 openpyxl 移动 sheet 到最前面
    except Exception as e:
        logger.error(f"❌ 保存数据到Excel失败: {str(e)}")

from datetime import datetime, timedelta

def get_previous_workday():
    today = datetime.now().date()
    one_day = timedelta(days=1)

    # 获取昨天的日期
    yesterday = today - one_day

    # 如果昨天是周末，继续往前找工作日
    while yesterday.weekday() >= 5:  # 5 是周六，6 是周日
        yesterday -= one_day

    return yesterday.strftime('%Y-%m-%d')

# 示例使用
previous_workday = get_previous_workday()
print(f"Previous workday: {previous_workday}")

def compare_today_yesterday(file_path):
    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
    # yesterday_sheet = 1
    previous_workday = get_previous_workday()
    print(f"previous_workday:{previous_workday}")
    # yesterday = normalize_time((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))

    try:
        with pd.ExcelFile(file_path) as xls:
            sheets = xls.sheet_names
            print(f"sheets:{sheets}")

        if today not in sheets or previous_workday not in sheets:
            logger.warning("⚠️ 今天或昨天 sheet 不存在")
            return {}

        # 读取两个sheet并确保字段一致
        today_df = pd.read_excel(file_path, sheet_name=today)
        print(f"today_df:\n{today_df}")

        previous_workday_df = pd.read_excel(file_path, sheet_name=previous_workday)
        print(f"previous_workday_df:\n{previous_workday_df}")
        # 显式去重
        today_df = today_df.drop_duplicates(subset=['标的名称'])
        previous_workday_df = previous_workday_df.drop_duplicates(subset=['标的名称'])

        # 确保字段统一处理
        today_df['标的名称'] = today_df['标的名称'].astype(str).str.strip()
        previous_workday_df['标的名称'] = previous_workday_df['标的名称'].astype(str).str.strip()

        # 正确找出差异
        to_buy = today_df[~today_df['标的名称'].isin(previous_workday_df['标的名称'])]
        to_sell = previous_workday_df[~previous_workday_df['标的名称'].isin(today_df['标的名称'])]

        logger.info(f"✅ 今天有而昨天没有的标的（买入）:\n{to_buy['标的名称']}")
        logger.info(f"✅ 昨天有而今天没有的标的（卖出）:\n{to_sell['标的名称']}")

        datas = {
            'to_buy': to_buy[['标的名称']],#可转换成列表 [].tolist(
            'to_sell': to_sell[['标的名称']]
        }
        if datas is not None:
            logger.info("✅ 获取持仓差异成功")
            return datas
        else:
            logger.info("没有获取到任何持仓差异")
            return None

    except Exception as e:
        logger.error(f"❌ 对比数据失败: {str(e)}")
        return {}

def sava_all_strategy_holding_data():
    all_holdings = []
    for id in Strategy_ids:
        positions_df = fetch_strategy_profit(id)
        if positions_df is not None:
            # positions_df.to_excel(Strategy_holding_file,index=False)
            all_holdings.append(positions_df)
            # save_to_excel_by_date(positions_df, Strategy_holding_file)  # 按日期保存
            # compare_today_yesterday(Strategy_holding_file)  # 对比数据
        else:
            logger.info(f"没有获取到策略数据，策略ID: {id}")
    all_holdings_df = pd.concat(all_holdings, ignore_index=True)
    all_holdings_df.to_excel(Strategy_holding_file)
    print(f"所有:\n{all_holdings_df}")
# def job():
#     """定时任务入口"""
#     if datetime.now().weekday() < 5:  # 0-4 对应周一到周五
#         main()

if __name__ == '__main__':
    # import os
    #
    # file_path = Ai_Strategy_holding_file
    #
    # if os.path.exists(file_path):
    #     print(f"文件 {file_path} 存在")
    # else:
    #     print(f"文件 {file_path} 不存在")
    #
    # import pandas as pd
    #
    # try:
    #     with pd.ExcelFile(file_path) as xls:
    #         sheet_names = xls.sheet_names
    #         print(f"文件中的表名: {sheet_names}")
    #         for sheet_name in sheet_names:
    #             try:
    #                 df = pd.read_excel(file_path, sheet_name=sheet_name)
    #                 print(f"\n表名: {sheet_name}\n内容:\n{df}")
    #             except Exception as e:
    #                 print(f"读取表 {sheet_name} 失败: {e}")
    # except Exception as e:
    #     print(f"读取 Excel 文件失败: {e}")




    # print(main())
    holding_success, ai_datas = Ai_strategy_main()
    # sava_all_strategy_holding_data()
    print(ai_datas)
    #
    # to_sell = ai_datas.get("to_sell")
    # to_buy = ai_datas.get("to_buy")
    # print("to_sell:", to_sell)
    # print("to_buy:", to_buy)
    # 示例调用
    # positions_df = fetch_strategy_profit('156275')  # 获取策略数据
    # pprint(positions_df)
    # save_to_excel_by_date(positions_df, Strategy_holding_file)  # 按日期保存
    # compare_today_yesterday(Strategy_holding_file)  # 对比数据

