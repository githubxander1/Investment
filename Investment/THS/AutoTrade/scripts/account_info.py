# account_info1.py
import time
import xml.etree.ElementTree as ET
import pandas as pd
import uiautomator2 as u2

from Investment.THS.AutoTrade.config.settings import Account_holding_stockes_info_file,account_xml_file
from Investment.THS.AutoTrade.utils.logger import setup_logger
# from Investment.THS.AutoTrade.pages.page_guozhai import GuozhaiPage

logger = setup_logger("account_info.log")  # 创建日志实例

# 连接设备
try:
    d = u2.connect()
    # # 保存xml文件
    account_xml_file = account_xml_file
    ui_xml = d.dump_hierarchy(pretty=True)
    with open(account_xml_file, 'w', encoding='utf-8') as f:
        f.write(ui_xml)
except Exception as e:
    logger.error(f"连接设备失败: {e}")
    exit(1)

def click_holding_stock_button(self):
    holding_button = self.d(className='android.widget.TextView', text='持仓')
    holding_button.click()
    logger.info("点击持仓按钮")
def return_to_top(retry=3):
    # if return_to_top():
    #     return True
    # top_indicator = d(resourceId="com.hexin.plat.android:id/capital_cell_value",
    #                   className="android.widget.TextView", index=2)

    total_cangwei_node = d(resourceId="com.hexin.plat.android:id/total_cangwei_text")
    for i in range(retry):
        if total_cangwei_node.exists:
            logger.info("已回到顶部")
            return True
        d.swipe(0.5, 0.2, 0.5, 0.8, duration=0.25)
        time.sleep(1)
    # logger.warning("未能成功返回顶部，请检查UI状态")
    return False

def parse_stock_from_xml(xml_path):
    """
    解析持仓股票信息：标的名称、市值、持仓/可用、盈亏/盈亏率
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        stocks = []

        # 查找 RecyclerView（模糊匹配）
        parents = root.findall(".//*[@resource-id='com.hexin.plat.android:id/recyclerview_id']")
        if not parents:
            logger.warning("未找到 recyclerview_id 节点")
            return []

        parent = parents[0]

        # 遍历所有子节点
        items = parent.findall(".//*[@class='android.widget.RelativeLayout']")

        for item in items:
            name_nodes = item.findall(".//*[@class='android.widget.TextView']")
            if len(name_nodes) < 2:
                continue

            # 重点：强化“标的名称”的识别逻辑
            stock_name = name_nodes[0].get('text', '').strip()
            if not stock_name or any(c.isdigit() for c in stock_name):  # 如果包含数字，大概率不是股票名
                continue

            market_value = name_nodes[1].get('text', '').strip()
            # print(f'名称{stock_name}')
            # print(f'市值{market_value}')

            # HorizontalScrollView
            h_scrolls = item.findall(".//*[@class='android.widget.HorizontalScrollView']")
            if not h_scrolls:
                continue

            ll_list = h_scrolls[0].findall(".//*[@class='android.widget.LinearLayout']")

            profit_loss = ll_list[1].findall(".//*[@class='android.widget.TextView']")
            profit_loss_text = profit_loss[0].get('text', '') if len(profit_loss) >= 1 else ''
            profit_loss_rate_text = profit_loss[1].get('text', '') if len(profit_loss) >= 2 else ''

            position_available = ll_list[2].findall(".//*[@class='android.widget.TextView']")
            position = position_available[0].get('text', '') if len(position_available) >= 1 else ''
            available = position_available[1].get('text', '') if len(position_available) >= 2 else ''

            cost_price = ll_list[3].findall(".//*[@class='android.widget.TextView']")
            cost = cost_price[0].get('text', '') if len(cost_price) >= 1 else ''
            current_price = cost_price[1].get('text', '') if len(cost_price) >= 2 else ''

            if any(kw in stock_name for kw in ["清仓", "新标准券", "隐藏", "持仓管理"]):
                continue

            if not stock_name or stock_name == "None":
                continue

            stocks.append({
                "标的名称": stock_name,
                "市值": market_value,
                "盈亏/盈亏率": f"{profit_loss_text}/{profit_loss_rate_text}",
                "持仓/可用": f"{position}/{available}",
                # "当日盈亏/盈亏率": f"{daily_profit_loss}/{daily_profit_loss_rate}",
                "成本/现价": f"{cost}/{current_price}",
            })

        return stocks

    except Exception as e:
        logger.error(f"解析 XML 失败: {e}", exc_info=True)
        return []

def extract_header_info():
    """提取账户表头信息：总资产、浮动盈亏、总市值、可用、可取"""
    logger.info('正在获取账户表头信息...')
    header_info = {}

    try:
        # 仓位
        total_cangwei_node = d(resourceId="com.hexin.plat.android:id/total_cangwei_text")
        header_info["仓位"] = total_cangwei_node.get_text() if total_cangwei_node.exists else "None"

        # 总资产
        total_asset_node = d(resourceId="com.hexin.plat.android:id/capital_cell_value",
                             className="android.widget.TextView", index=2)
        header_info["总资产"] = total_asset_node.get_text() if total_asset_node.exists else "None"

        # 总市值
        total_market_value_node = d.xpath('(//*[@resource-id="com.hexin.plat.android:id/capital_cell_value"])[3]')
        header_info["总市值"] = total_market_value_node.get_text() if total_market_value_node.exists else "None"

        # 浮动盈亏
        float_profit_loss_node = d(resourceId="com.hexin.plat.android:id/capital_cell_value",
                                   className="android.widget.TextView", index=1)
        header_info["浮动盈亏"] = float_profit_loss_node.get_text() if float_profit_loss_node.exists else "None"

        # 可用
        available_node = d.xpath('(//*[@resource-id="com.hexin.plat.android:id/capital_cell_value"])[4]')
        header_info["可用"] = available_node.get_text() if available_node.exists else "None"

        # 可取
        available_for_withdrawal_node = d.xpath('(//*[@resource-id="com.hexin.plat.android:id/capital_cell_value"])[5]')
        header_info["可取"] = available_for_withdrawal_node.get_text() if available_for_withdrawal_node.exists else "None"

        header_info_df = pd.DataFrame([header_info])
        logger.info(f"账户表头信息完成: \n{header_info_df}")
        return header_info_df

    except Exception as e:
        logger.error(f"获取账户表头信息失败: {e}")
        return pd.DataFrame()


def scroll_and_dump(retry=3, min_stocks=3):
    """
    滑动并重新 dump XML，直到获取足够多的持仓数据
    :param retry: 最大重试次数
    :param min_stocks: 最小持仓数
    :return: 成功解析的股票列表
    """
    for i in range(retry):
        # 保存当前页面的 XML
        xml_content = d.dump_hierarchy(pretty=True)
        with open(account_xml_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        # 解析持仓
        stocks = parse_stock_from_xml(account_xml_file)
        logger.info(f"第 {i + 1} 次尝试，共提取到 {len(stocks)} 条持仓信息")

        if len(stocks) >= min_stocks:
            logger.info("✅ 已获取足够持仓信息")
            return stocks

        # 向上滑动（模拟加载更多）
        logger.info("🔄 页面持仓不足，开始滑动加载...")
        d.swipe(0.5, 0.7, 0.5, 0.3, duration=0.5)
        time.sleep(2)  # 等待加载

    logger.warning("⚠️ 达到最大重试次数，持仓数据仍不足")
    return stocks


def extract_stock_info(max_swipe_attempts=5):
    """提取持仓股票信息，支持滑动加载更多，并过滤无效条目"""
    logger.info('正在获取账户持仓信息...')

    stocks = []
    seen_stocks = set()

    for attempt in range(max_swipe_attempts):
        try:
            # 获取当前页面的 XML 并保存为临时文件
            xml_content = d.dump_hierarchy(pretty=True)
            temp_xml_path = f"{account_xml_file}.tmp{attempt}"
            with open(temp_xml_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)

            # 解析当前页面的持仓信息
            parsed_stocks = parse_stock_from_xml(temp_xml_path)
            new_count = 0

            for stock in parsed_stocks:
                name = stock["标的名称"]
                if name in seen_stocks or any(kw in name for kw in ["清仓", "新标准券", "隐藏", "持仓管理"]):
                    continue
                seen_stocks.add(name)
                stocks.append(stock)
                new_count += 1

            logger.info(f"第 {attempt + 1} 次尝试新增 {new_count} 条有效持仓")

            # 检查是否到底（是否有“查看已清仓股票”按钮）
            qingcang = d(text="查看已清仓股票")
            if qingcang.exists:
                logger.info("检测到‘查看已清仓股票’，已加载全部持仓")
                return_to_top()
                break

            # 向下滑动
            d.swipe(0.5, 0.7, 0.5, 0.3, duration=0.25)
            time.sleep(1.5)

        except Exception as e:
            logger.error(f"处理持仓信息失败: {e}", exc_info=True)
            time.sleep(1)
            continue

    # 去重并清理空值
    df = pd.DataFrame(stocks).drop_duplicates(subset=["标的名称"])
    df.replace("", pd.NA, inplace=True)
    logger.info(f"✅ 成功提取持仓数据，共 {len(df)} 条:\n{df}")
    return df


# def get_header_info(retries=3):
#     """仅提取账户表头信息（不处理持仓）"""
#     logger.info("开始获取账户表头信息...")
#     for attempt in range(retries):
#         try:
#             header_info_df = extract_header_info()
#             if not header_info_df.empty:
#                 return header_info_df.to_dict(orient='records')[0]
#             time.sleep(2)
#         except Exception as e:
#             logger.error(f"第 {attempt + 1} 次尝试失败: {e}")
#     logger.error("❌ 获取账户表头信息失败")
#     return None


def get_buying_power():
    """获取可用资金"""
    try:
        header_info = extract_header_info()
        if header_info.empty:
            return None
        buy_available = float(header_info["可用"].iloc[0].replace(',', ''))
        return buy_available
    except Exception as e:
        logger.error(f"获取可用资金失败: {e}")
        return None


def get_stock_available(stock_name):
    """获取指定股票的持仓/可用数量"""
    try:
        stock_holding_df = extract_stock_info()
        stock_row = stock_holding_df[stock_holding_df["标的名称"] == stock_name]

        if not stock_row.empty:
            # 确保 stock_row 为单行数据
            stock_row = stock_row.iloc[0]

            position_available = stock_row.get("持仓/可用", "")
            if isinstance(position_available, str):
                parts = position_available.strip().split('/')
                if len(parts) >= 2:
                    position = float(parts[0])
                    available = float(parts[1])
                    return available
                else:
                    logger.warning(f"持仓/可用字段格式错误: {position_available}")
                    return None
            else:
                logger.warning(f"持仓/可用字段不是字符串: {position_available}")
                return None
        else:
            logger.warning(f"{stock_name} 不在持仓中")
            return None
    except Exception as e:
        logger.error(f"获取持仓失败: {e}")
        return None

def update_holding_info_all():
    """
    获取当前账户持仓信息，并保存到 Excel 文件
    """
    logger.info("开始更新账户持仓信息...")
    # ths = GuozhaiPage(d)
    # ths.ensure_on_holding_page()
    try:
        header_info_df = extract_header_info()
        stocks_df = extract_stock_info()

        if header_info_df.empty or stocks_df.empty:
            logger.warning("无法保存持仓信息：数据为空")
            return False

        with pd.ExcelWriter(Account_holding_stockes_info_file, engine='openpyxl') as writer:
            header_info_df.to_excel(writer, index=False, sheet_name="表头数据")
            stocks_df.to_excel(writer, index=False, sheet_name="持仓数据")

        logger.info(f"✅ 账户持仓信息已更新并保存至 {Account_holding_stockes_info_file}")
        return True
    except Exception as e:
        logger.error(f"❌ 保存持仓信息失败: {e}", exc_info=True)
        return False




if __name__ == '__main__':
    # get_stock_holding('中国电信')
    # header_info = extract_header_info()
    # buy_available = float(header_info["可用"].iloc[0].replace(',', ''))
    # print(f"可用金额: {buy_available}")

    _current_stock_name = '中国银行'
    # print(get_stock_available(_current_stock_name))
    print(get_buying_power())
    # stock_holding = get_stock_holding(_current_stock_name)
    # if not stock_holding:
    #     print(f'{_current_stock_name} 没有持仓')
    # else:
    #     position_available = stock_holding.get("持仓/可用", "")
    #     print(f"持仓/可用: {position_available}")
    #     print(f"可用为: {position_available}")
    #
    #     if isinstance(position_available, str):
    #         parts = position_available.strip().split('/')
    #         if len(parts) >= 2:
    #             position = float(parts[0])
    #             available = float(parts[1])
    #             print(f"持仓: {position}, 可用: {available}")

    # # 判断类型：如果是字符串，则尝试 split；否则直接取整数
    # if isinstance(position_available, str):
    #     parts = position_available.strip().split('/')
    #     if len(parts) < 2:
    #         logger.error(f"持仓/可用字段格式错误: {position_available}")
    #         return False, f"持仓/可用字段异常: {position_available}", None
    #     try:
    #         sale_available = int(float(parts[1]))
    #     except ValueError as e:
    #         logger.error(f"解析持仓/可用字段失败: {e}")
    #         return False, f"持仓/可用字段解析失败: {position_available}", None
    # elif isinstance(position_available, (int, float)):
    #     sale_available = int(float(position_available))
    # else:
    #     logger.error(f"未知类型: {type(position_available)}")
    #     return False, f"持仓/可用字段类型错误: {position_available}", None
