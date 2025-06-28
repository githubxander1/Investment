# account_info.py
import time
import pandas as pd
import uiautomator2 as u2

from Investment.THS.AutoTrade.config.settings import Account_holding_stockes_info_file
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger("get_account_info")  # 创建日志实例

# 连接设备
try:
    d = u2.connect()
    # # 保存xml文件
    # ui_xml = d.dump_hierarchy(pretty=True)
    # with open(account_xml_file, 'w', encoding='utf-8') as f:
    #     f.write(ui_xml)
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


def extract_stock_info(max_swipe_attempts=5, retry_top=3):
    """提取持仓股票信息，支持滑动加载更多，并过滤无效条目"""
    logger.info('正在获取账户持仓信息...')

    qingcang = d(text="查看已清仓股票")
    stock_list_node = d(resourceId="com.hexin.plat.android:id/recyclerview_id")
    stocks = []
    seen_stocks = set()  # 用于记录已添加的股票名称，避免重复

    for _ in range(max_swipe_attempts):
        if not stock_list_node.exists:
            break
        try:
            stock_items = stock_list_node.child(className="android.widget.RelativeLayout")

            for stock_item in stock_items:
                # 获取标的名称
                stock_name_node = stock_item.child(className="android.widget.TextView", index=0)
                stock_name = stock_name_node.get_text() if stock_name_node.exists else "None"
                if stock_name in ["隐藏", "新标准券", "None"]:
                    continue
                if stock_name in seen_stocks:
                    continue
                seen_stocks.add(stock_name)

                # 获取市值
                market_value_node = stock_item.child(className="android.widget.TextView", index=1)
                market_value = market_value_node.get_text() if market_value_node.exists else "None"

                # 获取HorizontalScrollView中的LinearLayout
                horizontal_scrollview = stock_item.child(className="android.widget.HorizontalScrollView")
                daily_profit_loss = profit_loss = cost = current_price = position_available = "None"
                daily_profit_loss_rate = profit_loss_rate = "None"

                if horizontal_scrollview.exists:
                    linear_layouts = horizontal_scrollview.child(className="android.widget.LinearLayout")
                    if len(linear_layouts) >= 5:

                        # 盈亏/盈亏率
                        profit_loss_node = linear_layouts[1].child(className="android.widget.TextView", index=0)
                        profit_loss_rate_node = linear_layouts[1].child(className="android.widget.TextView", index=1)
                        profit_loss = profit_loss_node.get_text() if profit_loss_node.exists else "None"
                        profit_loss_rate = profit_loss_rate_node.get_text() if profit_loss_rate_node.exists else "None"

                        # 当日盈亏/盈亏率
                        daily_profit_loss_node = linear_layouts[2].child(className="android.widget.TextView", index=0)
                        daily_profit_loss_rate_node = linear_layouts[2].child(className="android.widget.TextView", index=1)
                        daily_profit_loss = daily_profit_loss_node.get_text() if daily_profit_loss_node.exists else "None"
                        daily_profit_loss_rate = daily_profit_loss_rate_node.get_text() if daily_profit_loss_rate_node.exists else "None"

                        # 成本/现价
                        cost_node = linear_layouts[4].child(className="android.widget.TextView", index=0)
                        current_price_node = linear_layouts[4].child(className="android.widget.TextView", index=1)
                        cost = cost_node.get_text() if cost_node.exists else "None"
                        current_price = current_price_node.get_text() if current_price_node.exists else "None"

                        # 持仓/可用
                        position_available_node1 = linear_layouts[3].child(className="android.widget.TextView", index=0)
                        position_available_node2 = linear_layouts[3].child(className="android.widget.TextView", index=1)
                        position_available = f"{position_available_node1.get_text()}/{position_available_node2.get_text()}" \
                            if position_available_node1.exists and position_available_node2.exists else "None"

                # 构造字典时，将“None”替换为空字符串，便于后续处理
                stocks.append({
                    "标的名称": stock_name,
                    "市值": market_value,
                    "盈亏/盈亏率": f"{profit_loss}/{profit_loss_rate}",
                    "当日盈亏/盈亏率": f"{daily_profit_loss}/{daily_profit_loss_rate}",
                    "成本/现价": f"{cost}/{current_price}",
                    "持仓/可用": position_available,
                })
        except Exception as e:
            logger.error(f"处理股票信息失败: {e}")
            time.sleep(1)
            continue

        # 检查是否到底（是否有“查看已清仓股票”按钮）
        if qingcang.exists:
            break

        # 向下滑动
        d.swipe(0.5, 0.7, 0.5, 0.3, duration=0.25)
        time.sleep(0.5)

    # 数据清洗：移除“None”的字段
    stocks_df = pd.DataFrame(stocks).drop_duplicates(subset=["标的名称"])
    stocks_df.replace("None", "", inplace=True)
    logger.info(f'获取账户持仓信息完成，共 {len(stocks_df)} 条有效数据,\n{stocks_df}')
    return stocks_df



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

            # 保存到 Excel 文件
            with pd.ExcelWriter(Account_holding_stockes_info_file, engine='openpyxl') as writer:
                header_info_df.to_excel(writer, index=False, sheet_name="表头数据")
                stocks_df.to_excel(writer, index=False, sheet_name="持仓数据")
                logger.info(f"✅ 账户信息成功保存至 {Account_holding_stockes_info_file}")

            # 返回顶部
            return_to_top()
            return True

        except Exception as e:
            logger.error(f"第 {attempt + 1} 次尝试失败: {e}")
            logger.warning(f"解析字段时发生异常: {e}")
            profit_loss = profit_loss_rate = daily_profit_loss = daily_profit_loss_rate = cost = current_price = position_available = "None"

    logger.error("❌ 更新账户数据失败，超过最大重试次数")
    return False


if __name__ == '__main__':
    update_holding_info()
