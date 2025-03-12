import logging
import time

import uiautomator2

logging.basicConfig(level=logging.INFO)

d = uiautomator2.connect()
d.implicitly_wait(10)

def click_back():
    click_back = d(resourceId='com.hexin.plat.android:id/title_bar_left_container')
    click_back.click()
    logging.info("点击返回按钮")
def click_trade_entry():
    trade_entry = d(resourceId='com.hexin.plat.android:id/title', text='交易')
    trade_entry.click()
    logging.info("点击交易按钮")
def buy_entry():
    buy_entry = d(resourceId='com.hexin.plat.android:id/menu_buy_text')
    buy_entry.click()
    logging.info("点击买入按钮")

def sell_entry():
    sell_entry = d(resourceId='com.hexin.plat.android:id/menu_sale_text')
    sell_entry.click()
    logging.info("点击卖出按钮")

def search_stock(stock_name):
    stock_search = d(resourceId='com.hexin.plat.android:id/content_stock')
    stock_search.click()
    logging.info("点击股票搜索框")

    auto_search = d(resourceId='com.hexin.plat.android:id/auto_stockcode', text='股票代码/简拼')
    clear = d(resourceId='com.hexin.plat.android:id/clearable_edittext_btn_clear')
    if clear.exists():
        clear.click()
    logging.info("清除股票代码")
    time.sleep(2)

    auto_search.send_keys(stock_name)
    auto_search.send_keys(stock_name)
    logging.info(f"输入股票名称: {stock_name}")
    time.sleep(1)

    recycler_view = d(resourceId='com.hexin.plat.android:id/recyclerView')
    first_item = recycler_view.child(index=0)
    first_item.click()
    logging.info("点击匹配的的第一个股票")
    time.sleep(1)

def input_volume(volume):
    volumn = d(className='android.widget.EditText')[2]
    volumn.send_keys(volume)
    logging.info(f"输入买入数量: {volume}")

def click_button_by_text(text):
    button = d(className='android.widget.TextView', text=text)
    button.click()
    logging.info(f"点击按钮: {text}")

def confirm_transaction():
    dialog_info = d(className='android.widget.Button')[1]
    dialog_info.click()
    logging.info("点击确认按钮")

def dialog_confirm():
    dialog_confirm = d(resourceId='com.hexin.plat.android:id/ok_btn', text='确定')
    dialog_confirm.click()
    logging.info("点击确认按钮")
def handle_dialog():
    # dialog_title = d(resourceId='com.hexin.plat.android:id/dialog_title')
    dialog_info = d.xpath('//*[contains(@text,"委托已提交")]')
    if dialog_info.exists:
        dialog_confirm()
        logging.info("交易委托成功")
    else:
        dialog_info = d(resourceId='com.hexin.plat.android:id/prompt_content')
        info = dialog_info.get_text()
        dialog_confirm()
        logging.info(f"交易委托失败,原因：{info}")

def buy_stock(stock_name, volume):
    buy_entry()
    search_stock( stock_name)
    input_volume(volume)
    click_button_by_text('买 入(模拟炒股)')
    confirm_transaction()
    time.sleep(1)
    handle_dialog()
    time.sleep(1)
    click_back()

def sell_stock(stock_name, volume):
    sell_entry()
    search_stock(stock_name)
    input_volume(volume)
    click_button_by_text('卖 出(模拟炒股)')
    confirm_transaction()
    time.sleep(1)
    handle_dialog()
    time.sleep(1)
    click_back()

# 示例调用
# if __name__ == "__main__":
#     pass
    # d.app_start('com.hexin.plat.android')
    # time.sleep(5)
    # click_trade_entry()
    # buy_stock('工商银行', 2000)
    # sell_stock('工商银行', 1000)
