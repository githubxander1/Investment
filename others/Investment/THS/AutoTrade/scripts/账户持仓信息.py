# 账户持仓信息.py
import pandas as pd
import uiautomator2 as u2

from others.Investment.THS.AutoTrade.config.settings import Holding_Stockes_info_file

# 连接设备
try:
    d = u2.connect()
except Exception as e:
    print(f"连接设备失败: {e}")
    exit(1)

# 获取UI层次结构
tree = d.dump_hierarchy()
# print(tree)

# 定义一个函数来查找特定resource-id的节点
def find_node_by_resource_id(resource_id):
    return d(resourceId=resource_id)

# 定义一个函数来查找特定文本的节点
def find_node_by_text(text):
    return d(text=text)

# 提取表头信息
def extract_header_info():
    header_info = {}

    # 总资产
    total_asset_node = d(resourceId="com.hexin.plat.android:id/capital_cell_value", className="android.widget.TextView", index=2)
    header_info["总资产"] = total_asset_node.get_text() if total_asset_node.exists else "未找到"

    # 浮动盈亏
    float_profit_loss_node = d(resourceId="com.hexin.plat.android:id/capital_cell_value", className="android.widget.TextView", index=1)
    header_info["浮动盈亏"] = float_profit_loss_node.get_text() if float_profit_loss_node.exists else "未找到"

    # 当日盈亏
    daily_profit_loss_node = d(resourceId="com.hexin.plat.android:id/dangri_yingkui_value", className="android.widget.TextView", index=0)
    daily_profit_loss_rate_node = d(resourceId="com.hexin.plat.android:id/dangri_yingkuibi_value", className="android.widget.TextView", index=1)
    daily_profit_loss = daily_profit_loss_node.get_text() if daily_profit_loss_node.exists else "未找到"
    daily_profit_loss_rate = daily_profit_loss_rate_node.get_text() if daily_profit_loss_rate_node.exists else "未找到"
    header_info["当日盈亏/盈亏率"] = f"{daily_profit_loss}/{daily_profit_loss_rate}"

    # 总市值
    total_market_value_node = d(resourceId="com.hexin.plat.android:id/capital_cell_value", className="android.widget.TextView", index=2)
    header_info["总市值"] = total_market_value_node.get_text() if total_market_value_node.exists else "未找到"

    # 可用
    available_node = d(resourceId="com.hexin.plat.android:id/capital_cell_value", className="android.widget.TextView", index=3)
    header_info["可用"] = available_node.get_text() if available_node.exists else "未找到"

    # 可取
    available_for_withdrawal_node = d(resourceId="com.hexin.plat.android:id/capital_cell_value", className="android.widget.TextView", index=4)
    header_info["可取"] = available_for_withdrawal_node.get_text() if available_for_withdrawal_node.exists else "未找到"

    return header_info

def extract_stock_info():
    # 查找“查看已清仓股票”按钮
    qingcang = d(text="查看已清仓股票")

    # 获取股票列表
    stock_list_node = d(resourceId="com.hexin.plat.android:id/recyclerview_id")
    stocks = []
    while True:
        if stock_list_node.exists:
            # 获取所有股票项
            stock_items = stock_list_node.child(className="android.widget.RelativeLayout")
            new_stocks = []

            for stock_item in stock_items:
                # 获取股票名
                stock_name_node = stock_item.child(className="android.widget.TextView", index=0)
                stock_name = stock_name_node.get_text() if stock_name_node.exists else "未找到"

                # 获取市值
                market_value_node = stock_item.child(className="android.widget.TextView", index=1)
                market_value = market_value_node.get_text() if market_value_node.exists else "未找到"

                # 获取HorizontalScrollView中的LinearLayout
                horizontal_scrollview = stock_item.child(className="android.widget.HorizontalScrollView")
                daily_profit_loss = "未找到"
                daily_profit_loss_rate = "未找到"
                cost = "未找到"
                current_price = "未找到"
                position_available = "未找到"
                profit_loss = "未找到"
                profit_loss_rate = "未找到"

                if horizontal_scrollview.exists:
                    linear_layouts = horizontal_scrollview.child(className="android.widget.LinearLayout")
                    if len(linear_layouts) > 3:
                        # 获取盈亏/盈亏率
                        profit_loss_node = linear_layouts[1].child(className="android.widget.TextView", index=0)
                        profit_loss_rate_node = linear_layouts[1].child(className="android.widget.TextView", index=1)
                        profit_loss = profit_loss_node.get_text() if profit_loss_node.exists else "未找到"
                        profit_loss_rate = profit_loss_rate_node.get_text() if profit_loss_rate_node.exists else "未找到"

                        # 获取当日盈亏/盈亏率
                        daily_profit_loss_node = linear_layouts[2].child(className="android.widget.TextView", index=0)
                        daily_profit_loss_rate_node = linear_layouts[2].child(className="android.widget.TextView", index=1)
                        daily_profit_loss = daily_profit_loss_node.get_text() if daily_profit_loss_node.exists else "未找到"
                        daily_profit_loss_rate = daily_profit_loss_rate_node.get_text() if daily_profit_loss_rate_node.exists else "未找到"

                        # 获取成本/现价
                        cost_node = linear_layouts[4].child(className="android.widget.TextView", index=0)
                        current_price_node = linear_layouts[4].child(className="android.widget.TextView", index=1)
                        cost = cost_node.get_text() if cost_node.exists else "未找到"
                        current_price = current_price_node.get_text() if current_price_node.exists else "未找到"

                        # 获取持仓/可用
                        position_available_node1 = linear_layouts[3].child(className="android.widget.TextView", index=0)
                        position_available_node2 = linear_layouts[3].child(className="android.widget.TextView", index=1)
                        position_available = f"{position_available_node1.get_text()}/{position_available_node2.get_text()}" if position_available_node1.exists and position_available_node2.exists else "未找到"


                new_stocks.append({
                    "股票名": stock_name,
                    # "市值": market_value,
                    "盈亏/盈亏率": f"{profit_loss}/{profit_loss_rate}",
                    "当日盈亏/盈亏率": f"{daily_profit_loss}/{daily_profit_loss_rate}",
                    "成本/现价": f"{cost}/{current_price}",
                    "持仓/可用": position_available,
                })

            # 去重
            new_stocks_df = pd.DataFrame(new_stocks)
            if not new_stocks_df.empty:
                new_stocks_df = new_stocks_df.drop_duplicates(subset=["股票名"])

                # 过滤已存在的股票
                existing_stocks_df = pd.DataFrame(stocks)
                if not existing_stocks_df.empty:
                    new_stocks_df = new_stocks_df[~new_stocks_df["股票名"].isin(existing_stocks_df["股票名"])]

                # 更新股票列表
                stocks.extend(new_stocks_df.to_dict(orient="records"))

                # # 打印新增股票
                # if not new_stocks_df.empty:
                #     print("新增股票:")
                #     print(new_stocks_df)
                # else:
                #     print("没有新增股票")

            # 检查“查看已清仓股票”按钮是否存在
            if qingcang.exists:
                print("找到“查看已清仓股票”按钮，停止滑动")
                break

            # 执行下滑操作，从屏幕底部滑动到顶部
            d.swipe(0.5, 0.8, 0.5, 0.2, duration=0.5)

            # 检查是否有新的股票项
            if len(new_stocks_df) == 0:
                print("没有新的股票项，继续滑动")
        else:
            break

    # 提取完所有股票信息后，再滑动到最上面
    while True:
        total_asset_node = d(resourceId="com.hexin.plat.android:id/capital_cell_value",
                             className="android.widget.TextView", index=2)
        d.swipe(0.5, 0.2, 0.5, 0.8, duration=0.25)
        # if not stock_list_node.child(className="android.widget.RelativeLayout").exists:
        if total_asset_node.exists:
            break

    return stocks

def update_holding_info():
    # 提取表头信息
    header_info = extract_header_info()
    header_df = pd.DataFrame([header_info])
    print("表头信息:")
    print(header_df)

    # 提取股票信息
    stocks = extract_stock_info()

    # 打印当前股票列表
    stocks_df = pd.DataFrame(stocks)
    print("当前股票列表:")
    print(stocks_df)

    # 保存到Excel文件
    with pd.ExcelWriter(Holding_Stockes_info_file) as writer:
        header_df.to_excel(writer, index=False, sheet_name="表头信息")
        stocks_df.to_excel(writer, index=False, sheet_name="持仓数据")

if __name__ == '__main__':
    update_holding_info()
