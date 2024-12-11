import uiautomator2 as u2
import time

# 连接到模拟器或设备
d = u2.connect()
print("已连接到设备")

# 启动同花顺App
d.app_start("com.hexin.plat.android")
print("已启动同花顺App")

# 等待应用启动
time.sleep(5)
print("等待应用启动完成")

# 点击“交易”选项卡
d.xpath('//*[@content-desc="交易"]/android.widget.ImageView[1]').click()
time.sleep(3)
print("已点击“交易”选项卡")

# 点击“持仓”按钮
# d(resourceId="com.hexin.plat.android:id/menu_holdings_text").click()
# time.sleep(5)

# 获取持仓列表
def get_holdings():
    holdings = []
    while True:
        print("正在获取当前可见的持仓项")
        items = d.xpath('//*[@resource-id="com.hexin.plat.android:id/recyclerview_id"]/android.widget.RelativeLayout').all()
        for item in items:
            item_info = item.get_text()
            holdings.append(item_info)
            print(f"获取到持仓项: {item_info}")

        # 检查是否还有更多数据
        if not d(scrollable=True).exists:
            print("没有更多持仓数据可滚动")
            break

        # 下拉加载更多数据
        d.swipe_ext("down", scale=0.9)
        time.sleep(2)
        print("已下拉加载更多持仓数据")

    return holdings

# 点击持仓-撤单
# d.xpath('//*[@resource-id="com.hexin.plat.android:id/navi_buttonbar"]/android.widget.RelativeLayout[3]').click()
# d.xpath('//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]')

# 点击交易-撤单
d(resourceId="com.hexin.plat.android:id/menu_withdrawal").click()
print("已点击交易-撤单")
# 获取所有撤单情况

def get_all_cancellations():
    cancellations = []
    while True:
        print("正在获取当前可见的撤单项")
        items = d.xpath(
            '//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout').all()

        for idx, item in enumerate(items):
            # 获取撤单项的名称
            name_xpath = item.xpath(
                './android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView[1]')
            name = name_xpath.get_text() if name_xpath.exists else "N/A"

            # 获取撤单项的委托价
            price_xpath = item.xpath(
                './android.widget.LinearLayout[1]/android.widget.TextView[@resource-id="com.hexin.plat.android:id/result2"]')
            price = price_xpath.get_text() if price_xpath.exists else "N/A"

            # 获取撤单项的委托数量
            quantity_xpath = item.xpath(
                './android.widget.LinearLayout[1]/android.widget.LinearLayout[3]/android.widget.LinearLayout[1]/android.widget.TextView[1]')
            quantity = quantity_xpath.get_text() if quantity_xpath.exists else "N/A"

            # 获取撤单项的买入卖出状态和成功与否状态
            status_xpath = item.xpath(
                './android.widget.LinearLayout[1]/android.widget.LinearLayout[4]/android.widget.TextView[1]')
            success_xpath = item.xpath(
                './android.widget.LinearLayout[1]/android.widget.LinearLayout[4]/android.widget.TextView[2]')
            status = status_xpath.get_text() if status_xpath.exists else "N/A"
            success = success_xpath.get_text() if success_xpath.exists else "N/A"

            # 将信息存储在字典中
            cancellation_info = {
                "name": name,
                "price": price,
                "quantity": quantity,
                "status": status,
                "success": success
            }
            cancellations.append(cancellation_info)
            print(f"获取到撤单项: 名称={name}, 委托价={price}, 委托数量={quantity}, 状态={status}, 成功与否={success}")

        # 检查是否还有更多数据
        if not d(scrollable=True).exists:
            print("没有更多撤单数据可滚动")
            break

        # 下拉加载更多数据
        d.swipe_ext("up", scale=0.9)
        time.sleep(2)
        print("已下拉加载更多撤单数据")

    return cancellations


# 获取所有撤单
all_cancellations = get_all_cancellations()

# 打印所有撤单
for cancellation in all_cancellations:
    print(f"撤单信息: 名称={cancellation['name']}, 委托价={cancellation['price']}, 委托数量={cancellation['quantity']}, 状态={cancellation['status']}, 成功与否={cancellation['success']}")

# 获取所有持仓
# all_holdings = get_holdings()
#
# # 打印所有持仓
# for holding in all_holdings:
#     print(f"持仓信息: {holding}")

# 点击第一个持仓进入明细页面
# first_holding_xpath = '//*[@resource-id="com.hexin.plat.android:id/recyclerview_id"]/android.widget.RelativeLayout[1]'
# d.xpath(first_holding_xpath).click()
# time.sleep(3)
#
# # 点击“明细”按钮
# detail_button_xpath = '//*[@resource-id="com.hexin.plat.android:id/function_horizontal_scroll_view"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]'
# d.xpath(detail_button_xpath).click()
# time.sleep(5)

# 在这里可以继续获取明细页面的数据
# 例如，获取明细页面的某个元素的文本
# detail_info = d(resourceId="com.hexin.plat.android:id/some_detail_element_id").get_text()
# print(detail_info)

# 返回上一页
# d.press("back")
# time.sleep(2)

# 返回首页
# d.press("back")
# time.sleep(2)

# 关闭应用
d.app_stop("com.hexin.plat.android")
print("已关闭同花顺App")
