# get_account_info.py
import time
import xml.etree.ElementTree as ET
import pandas as pd
import os
import uiautomator2 as u2

# from Investment.THS.AutoTrade.utils import logger

# get_account_info.py

from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger("get_account_info")  # 创建日志实例

def scroll_to_bottom(d, max_swipes=5):
    """
    自动滑动到底部以加载更多持仓数据
    :param d: uiautomator2 的设备对象
    :param max_swipes: 最大滑动次数
    """
    for i in range(max_swipes):
        # 查找 RecyclerView 并滑动一次
        recycler_view = d(resourceId='com.hexin.plat.android:id/recyclerview_id')
        if not recycler_view.exists:
            logger.warning("未找到持仓列表，无法滑动")
            break

        # 滑动操作：从屏幕中间向上滑动
        bounds = recycler_view.info['bounds']
        start_y = bounds['bottom'] - 50
        end_y = bounds['top'] + 50

        d.swipe(360, start_y, 360, end_y, 0.2)
        time.sleep(1)  # 等待新数据加载

        # 判断是否已经到达底部（比如连续两次滑动后内容不变）
        current_xml = d.dump_hierarchy()
        if i > 0 and current_xml == previous_xml:
            logger.info("已到达底部，停止滑动")
            break
        previous_xml = current_xml


def parse_account_xml(xml_file_path):
    """
    从保存的 account_ui_xml.xml 中解析持仓信息
    :param xml_file_path: XML 文件路径
    :return: 持仓股票信息 DataFrame
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    stocks = []

    # 查找 RecyclerView 或包含持仓列表的容器节点
    stock_container = None
    for node in root.findall('.//node[@class="androidx.recyclerview.widget.RecyclerView"]'):
        if node.attrib.get('resource-id') == 'com.hexin.plat.android:id/recyclerview_id':
            stock_container = node
            break

    if stock_container is None or len(stock_container) == 0:
        raise ValueError("未找到持仓列表节点")

    # 遍历每个持仓项
    for item in stock_container.findall('.//node[@class="android.widget.RelativeLayout"]'):
        name_node = item.find('.//node[@class="android.widget.TextView"][@index="0"]')
        price_node = item.find('.//node[@class="android.widget.TextView"][@index="1"]')

        stock_name = name_node.attrib.get('text', '未找到') if name_node is not None else '未找到'

        if stock_name == '未找到':
            continue

        # 查找持仓信息所在的 LinearLayout
        linear_layouts = item.findall('.//node[@class="android.widget.LinearLayout"]')
        if len(linear_layouts) < 5:
            continue

        # 盈亏 / 盈亏率
        profit_loss = linear_layouts[1].find('.//node[@index="0"]')
        profit_rate = linear_layouts[1].find('.//node[@index="1"]')
        profit = profit_loss.attrib.get('text', '') if profit_loss is not None else ''
        rate = profit_rate.attrib.get('text', '') if profit_rate is not None else ''
        profit_loss_rate = f"{profit}/{rate}"

        # 当日盈亏 / 盈亏率
        daily_profit_loss = linear_layouts[2].find('.//node[@index="0"]')
        daily_rate = linear_layouts[2].find('.//node[@index="1"]')
        daily_profit = daily_profit_loss.attrib.get('text', '') if daily_profit_loss is not None else ''
        daily_rate_text = daily_rate.attrib.get('text', '') if daily_rate is not None else ''
        daily_profit_loss_rate = f"{daily_profit}/{daily_rate_text}"

        # 成本 / 现价
        cost_price = linear_layouts[4].find('.//node[@index="0"]')
        current_price = linear_layouts[4].find('.//node[@index="1"]')
        cost = cost_price.attrib.get('text', '') if cost_price is not None else ''
        current = current_price.attrib.get('text', '') if current_price is not None else ''
        cost_current = f"{cost}/{current}"

        # 持仓 / 可用
        position_available = linear_layouts[3].find('.//node[@index="0"]')
        available = linear_layouts[3].find('.//node[@index="1"]')
        pos = position_available.attrib.get('text', '') if position_available is not None else ''
        avail = available.attrib.get('text', '') if available is not None else ''
        position_available_str = f"{pos}/{avail}"

        stocks.append({
            "标的名称": stock_name,
            "盈亏/盈亏率": profit_loss_rate,
            "当日盈亏/盈亏率": daily_profit_loss_rate,
            "成本/现价": cost_current,
            "持仓/可用": position_available_str
        })

    stocks_df = pd.DataFrame(stocks).drop_duplicates(subset=["标的名称"])

    # 创建输出目录
    output_dir = r'D:\Xander\Inverstment\Investment\THS\AutoTrade\output'
    os.makedirs(output_dir, exist_ok=True)

    # 导出 Excel
    output_path = os.path.join(output_dir, '持仓信息.xlsx')
    stocks_df.to_excel(output_path, index=False)
    print(stocks_df)
    return stocks_df


if __name__ == '__main__':
    d = u2.connect()  # 连接设备
    d.app_start("com.hexin.plat.android")  # 启动同花顺 App
    d(text="持仓").click()  # 点击持仓页面

    time.sleep(2)  # 等待页面加载

    # 执行多次滑动以加载全部持仓
    scroll_to_bottom(d)

    # 保存当前页面的 XML 文件
    xml_content = d.dump_hierarchy()
    with open(r"D:\Xander\Inverstment\Investment\THS\AutoTrade\scripts\account_ui_xml.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

    # 解析并导出
    df = parse_account_xml(r"D:\Xander\Inverstment\Investment\THS\AutoTrade\scripts\account_ui_xml.xml")
