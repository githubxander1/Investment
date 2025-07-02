# page_guozhai.py

import uiautomator2 as u2

from Investment.THS.AutoTrade.utils.logger import setup_logger

# from Investment.THS.AutoTrade.trade_main import connect_to_device
logger = setup_logger('nihuigou.log')

def guozhai_operation(d):
    logger.info("---------------------国债逆回购任务开始执行---------------------")
    # 点击右上角第二个图标（通常是国债逆回购入口）
    d(resourceId="com.hexin.plat.android:id/title_right_image")[1].click()

    # 下滑到出现“沪市”位置，然后点击 stock_list 下的第一个 LinearLayout
    d.swipe(0.5, 0.8, 0.5, 0.2)
    # hushi = d(resourceId='com.hexin.plat.android:id/title')
    # stock_list = d(resourceId="com.hexin.plat.android:id/stock_list")[2]

    # 点击第一个线性布局（通常为第一个国债逆回购选项）
    # first_item = stock_list.child(className="android.widget.LinearLayout")[0]
    # first_item.click()
    yitianqi = d(className="android.widget.LinearLayout")[20]
    yitianqi.click()

    # # 点击“借出”按钮
    d(resourceId="com.hexin.plat.android:id/btn_jiechu").click()

    # 获取提示内容并打印
    prompt_content = d(resourceId="com.hexin.plat.android:id/prompt_content")
    # print(prompt_content.get_text())

    # 点击确认按钮
    confirm = d(resourceId="com.hexin.plat.android:id/ok_btn")
    confirm.click()

    # 返回上级页面
    back = d(resourceId="com.hexin.plat.android:id/title_bar_img")
    back.click()
    back.click()
    logger.info("---------------------国债逆回购任务执行完毕---------------------")


if __name__ == '__main__':
    d = u2.connect()
    guozhai_operation(d)
