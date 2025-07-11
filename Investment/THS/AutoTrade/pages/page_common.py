import time

import uiautomator2

from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger("page.log")
d = uiautomator2.connect()

trade_button_entry = d(resourceId="com.hexin.plat.android:id/icon")[3]
# trade_button_entry = d(className="android.widget.RelativeLayout")[24]
back_button = d(resourceId='com.hexin.plat.android:id/title_bar_left_container')

moni = d(resourceId="com.hexin.plat.android:id/tab_mn")
Agu = d(resourceId="com.hexin.plat.android:id/tab_a")
current_account = d(resourceId="com.hexin.plat.android:id/page_title_view")

holding_entry = d(resourceId='com.hexin.plat.android:id/menu_holdings_text', text='持仓')
# 账户页
keyong = d(resourceId="com.hexin.plat.android:id/capital_cell_title")[4]
current_text = d(resourceId="com.hexin.plat.android:id/currency_text", text="人民币账户 A股")
share_button = d(resourceId="com.hexin.plat.android:id/share_container")
search_button = d(resourceId="com.hexin.plat.android:id/search_container")
# 判断当前在哪个页面
def where_page():
    application_store = d(resourceId="com.hexin.plat.android:id/textView")[12]
    moni = d(resourceId="com.hexin.plat.android:id/tab_mn")
    current_text = d(resourceId="com.hexin.plat.android:id/currency_text", text="人民币账户 A股")
    guozhailist = d(text="我要回购")
    guozhaipingzhong = d(resourceId="com.hexin.plat.android:id/stock_pinzhong")

    if application_store.exists():
        # logger.info("当前页面: 首页")
        return "首页"
    elif moni.exists():
        # logger.info("当前页面: 交易页")
        return "交易页"
    elif search_button.exists():
        # logger.info("当前页面: 账户页")
        return "账户页"
    elif guozhailist.exists():
        # logger.info("当前页面: 国债列表页")
        return "国债列表页"
    elif guozhaipingzhong.exists():
        # logger.info("当前页面: 国债品种页")
        return "国债品种页"
    else:
        back_button.click()
        return "当前在未知页,尝试返回"

def ensure_on_account_page():
        """确保当前在账户页"""
        time.sleep(1)
        current_page = where_page()
        logger.info(f"当前页面: {current_page}")

        # 确保在账户页
        if not current_page == "账户页":
            if current_page == "首页":
                # 如果没有可用按钮，则点击持仓入口
                trade_button_entry.click()
                time.sleep(1)
                if not search_button.exists:
                    print("没有分享按钮")
                    holding_entry.click()
            elif current_page == "交易页":
                holding_entry.click()
            elif current_page == "国债列表页":
                back_button.click()
            elif current_page == "国债品种页":
                back_button.click()
                back_button.click()
            else:
                logger.error("无法返回账户页")
                return False
            logger.info("已切换至: 账户页")
        else:
            return True
def change_account(self, to_account):
    """
    切换账户，必须在交易页执行
    :param to_account: 目标账户名称（如 "模拟" / "川财证券" / "长城证券"）
    :return: 成功与否
    """
    current_page = where_page()
    logger.info(f"当前页面: {current_page}, 正在尝试切换至账户: {to_account}")

    # 确保在交易页
    if current_page != "交易页":
        logger.warning("不在交易页，尝试返回交易页...")
        if current_page == "首页":
            # trade_button = d(resourceId="com.hexin.plat.android:id/icon")[4]
            trade_button_entry.click()
        elif current_page == "账户页":
            back_button.click()
        elif current_page == "国债列表页":
            back_button.click()
            back_button.click()
        elif current_page == "国债品种页":
            back_button.click()
            back_button.click()
            back_button.click()
        else:
            logger.error("无法返回交易页，切换账户失败")
            return False


    # 确保进入交易页
    if where_page() != "交易页":
        logger.error("无法返回交易页，切换账户失败")
        return False
    # Agu = d(resourceId="com.hexin.plat.android:id/tab_a")
    # 切换账户逻辑
    if to_account == "模拟":
        # moni = d(resourceId="com.hexin.plat.android:id/tab_mn")
        if not moni.exists(timeout=3):
            logger.error("找不到模拟账户入口")
            return False
        moni.click()
        holding_entry.click()
        logger.info("切换至模拟账户成功")
        return True
    else:
        # back_button.click()
        # Agu = d(resourceId="com.hexin.plat.android:id/tab_a")
        Agu.click()
        time.sleep(1)
        holding_entry.click()

        # current_account = d(resourceId="com.hexin.plat.android:id/page_title_view")

        if current_account == to_account:
            logger.info(f"当前已是 {to_account} 账户，无需切换")
            return True

        account_dialog = d(resourceId="com.hexin.plat.android:id/wt_multi_data_item_qs_name", text=to_account)
        loggin_button = d(resourceId="com.hexin.plat.android:id/weituo_btn_login")
        password_input = d(resourceId="com.hexin.plat.android:id/weituo_edit_trade_password")
        keeplogin_checkbox = d(resourceId="com.hexin.plat.android:id/rtv_keeplogin_tips")
        keeplogin_24h = d(resourceId="com.hexin.plat.android:id/tv_keeplogin_24h")

        password_changcheng = '660493'
        password_chuangcai = '170212'

        current_account_name = current_account.get_text()

        if current_account_name != to_account:

            current_account.click()
            account_dialog.click()

            if loggin_button.exists():
                loggin_button.click()

                if to_account == '长城证券':
                    time.sleep(1)
                    password_input.set_text(password_changcheng)
                else:
                    password_input.set_text(password_chuangcai)

                keeplogin_checkbox.click()
                if keeplogin_24h.exists():
                    keeplogin_24h.click()

                loggin_button.click()
                time.sleep(1)

            current_account_name2 = current_account.get_text()
            if current_account_name2 == to_account:
                _current_account = to_account
                logger.info(f"✅ 成功切换至账户: {to_account}")
                return True
            else:
                logger.warning(f"⚠️ 切换账户失败，当前仍为: {current_account_name2}")
                return False
        else:
            _current_account = current_account_name
            logger.info(f"📌 当前登录账户名称: {current_account_name}")
            return True