# account_info.py
import time
import xml.etree.ElementTree as ET
import pandas as pd
import uiautomator2 as u2

from Investment.THS.AutoTrade.config.settings import Account_holding_stockes_info_file, account_xml_file
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import account_xml_file

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

        # 打印部分 XML 内容用于调试
        with open(xml_path, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # 读取前 2000 字符
        logger.debug(f"XML 片段:\n{content}")

        stocks = []

        # 定位 RecyclerView
        parent = root.find(".//node[@resource-id='com.hexin.plat.android:id/recyclerview_id']")
        if parent is None:
            logger.warning("未找到 recyclerview_id 节点")
            return []

        # 遍历所有子节点
        for item in parent.findall(".//node[@class='android.widget.RelativeLayout']"):
            name_node = item.find(".//*[@class='android.widget.TextView'][@index='0']")
            market_value_node = item.find(".//*[@class='android.widget.TextView'][@index='1']")
            h_scroll = item.find(".//*[@class='android.widget.HorizontalScrollView']")

            if h_scroll is None:
                continue

            ll_list = h_scroll.findall(".//*[@class='android.widget.LinearLayout']")
            if len(ll_list) < 5:
                continue

            # 提取各个字段
            stock_name = name_node.attrib.get('text', '') if name_node is not None else ''
            market_value = market_value_node.attrib.get('text', '') if market_value_node is not None else ''

            profit_loss_nodes = ll_list[1].findall(".//*[@class='android.widget.TextView']")
            profit_loss = profit_loss_rate = ""
            if len(profit_loss_nodes) >= 2:
                profit_loss = profit_loss_nodes[0].attrib.get('text', '')
                profit_loss_rate = profit_loss_nodes[1].attrib.get('text', '')

            position_available_nodes = ll_list[2].findall(".//*[@class='android.widget.TextView']")
            position = available = ""
            if len(position_available_nodes) >= 2:
                position = position_available_nodes[0].attrib.get('text', '')
                available = position_available_nodes[1].attrib.get('text', '')

            cost_nodes = ll_list[3].findall(".//*[@class='android.widget.TextView']")
            cost = current_price = ""
            if len(cost_nodes) >= 2:
                cost = cost_nodes[0].attrib.get('text', '')
                current_price = cost_nodes[1].attrib.get('text', '')

            if any(kw in stock_name for kw in ["清仓", "新标准券", "隐藏"]):
                continue

            if not stock_name or stock_name == "None":
                continue

            stocks.append({
                "标的名称": stock_name,
                "市值": market_value,
                "持仓": position,
                "可用": available,
                "成本价": cost,
                "当前价": current_price,
                "盈亏金额": profit_loss,
                "盈亏比例": profit_loss_rate
            })

        return stocks

    except Exception as e:
        logger.error(f"解析 XML 失败: {e}")
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
            xml_content = d.dump_hierarchy(pretty=True)
            with open(account_xml_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)

            parsed_stocks = parse_stock_from_xml(account_xml_file)
            new_count = 0

            for stock in parsed_stocks:
                name = stock["标的名称"]
                if name in seen_stocks or any(kw in name for kw in ["清仓", "新标准券", "隐藏", "持仓管理"]):
                    continue
                seen_stocks.add(name)
                stocks.append(stock)
                new_count += 1

            logger.info(f"第 {attempt + 1} 次尝试新增 {new_count} 条有效持仓")

            qingcang = d(text="查看已清仓股票")
            if qingcang.exists:
                logger.info("检测到‘查看已清仓股票’，已加载全部持仓")
                break

            d.swipe(0.5, 0.7, 0.5, 0.3, duration=0.25)
            time.sleep(1.5)

        except Exception as e:
            logger.error(f"处理持仓信息失败: {e}", exc_info=True)
            time.sleep(1)
            continue

    df = pd.DataFrame(stocks).drop_duplicates(subset=["标的名称"])
    df.replace("", pd.NA, inplace=True)
    logger.info(f"✅ 成功提取持仓数据，共 {len(df)} 条:\n{df}")
    return df





def update_holding_info(retries=3):
    """更新持仓信息到Excel文件"""
    logger.info("开始更新账户持仓信息...")
    for attempt in range(retries):
        try:
            header_info_df = extract_header_info()
            stocks_df = extract_stock_info()

            if header_info_df.empty or stocks_df.empty:
                logger.warning(f"第 {attempt + 1} 次尝试：获取的数据为空，跳过保存。")
                time.sleep(2)
                continue

            # 保存到 Excel
            with pd.ExcelWriter(Account_holding_stockes_info_file, engine='openpyxl') as writer:
                header_info_df.to_excel(writer, index=False, sheet_name="表头数据")
                stocks_df.to_excel(writer, index=False, sheet_name="持仓数据")
                logger.info(f"✅ 账户信息成功保存至 {Account_holding_stockes_info_file}")

            return_to_top()
            return True

        except Exception as e:
            logger.error(f"第 {attempt + 1} 次尝试失败: {e}")

    logger.error("❌ 更新账户数据失败，超过最大重试次数")
    return False



if __name__ == '__main__':
    update_holding_info()
    # d = uiautomator2.connect()
    # d.screenshot("screenshot1.png")
    #
    # import os
    # import subprocess
    # import time
    #
    #
    # def capture_screen_adb(save_path="screenshot.png", retry=3):
    #     for i in range(retry):
    #         try:
    #             # 执行 ADB 命令截图并拉取到本地
    #             subprocess.run("adb shell where adb", check=True)
    #             subprocess.run("adb shell screencap -p /sdcard/screenshot.png", check=True)
    #             subprocess.run(f"adb pull /sdcard/screenshot.png {save_path}", check=True)
    #             if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
    #                 print(f"✅ 截图成功: {save_path}")
    #                 return save_path
    #             else:
    #                 print("❌ 截图失败或文件为空，重试中...")
    #                 time.sleep(1)
    #         except Exception as e:
    #             print(f"❌ 截图异常: {e}")
    #     return None
    #
    # capture_screen_adb()
