from uiautomator2 import UiObjectNotFoundError
import time

import uiautomator2

from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger("page.log")

class CommonPage:

    def __init__(self):
        self.d = uiautomator2.connect()
        self.back_button = self.d(resourceId='com.hexin.plat.android:id/title_bar_left_container')
        # trade_button_entry = self.d(className="android.widget.RelativeLayout")[24]
        self.application_store = self.d(resourceId="com.hexin.plat.android:id/textView")[12]

        # 交易页
        self.trade_button_entry = self.d(resourceId="com.hexin.plat.android:id/icon")[3]
        self.moni = self.d(resourceId="com.hexin.plat.android:id/tab_mn")
        self.Agu = self.d(resourceId="com.hexin.plat.android:id/tab_a")
        self.current_account_trade = self.d(resourceId="com.hexin.plat.android:id/qs_name_text")
        # self.current_account_trade_name = self.current_account_trade.get_text()

        self.holding_entry = self.d(resourceId='com.hexin.plat.android:id/menu_holdings_text', text='持仓')
        # 账户页
        self.current_account = self.d(resourceId="com.hexin.plat.android:id/page_title_view")
        # self.current_account_name = self.current_account.get_text()
        self.keyong = self.d(resourceId="com.hexin.plat.android:id/capital_cell_title")[4]
        self.current_text = self.d(resourceId="com.hexin.plat.android:id/currency_text", text="人民币账户 A股")
        self.share_button = self.d(resourceId="com.hexin.plat.android:id/share_container")
        self.search_button = self.d(resourceId="com.hexin.plat.android:id/search_container")
        self.moni_account = self.d(resourceId="com.hexin.plat.android:id/division_name_text")

    # 国债列表

    def safe_click(self, element, timeout=3):
        try:
            if element.wait(timeout=timeout):
                element.click()
                return True
            else:
                logger.warning("点击失败：元素不存在")
                return False
        except UiObjectNotFoundError:
            logger.error("元素未找到")
            return False

    # 判断当前在哪个页面
    def where_page(self):
        moni = self.d(resourceId="com.hexin.plat.android:id/tab_mn")
        current_text = self.d(resourceId="com.hexin.plat.android:id/currency_text", text="人民币账户 A股")
        guozhailist = self.d(text="我要回购")
        guozhaipingzhong = self.d(resourceId="com.hexin.plat.android:id/stock_pinzhong")
    
        if self.application_store.exists():
            return "首页"
        elif moni.exists():
            # logger.info("当前页面: 交易页")
            return "交易页"
        elif self.search_button.exists():
            # logger.info("当前页面: 账户页")
            return "账户页"
        elif guozhailist.exists(timeout=3):
            # logger.info("当前页面: 国债列表页")
            return "国债列表页"
        elif guozhaipingzhong.exists():
            # logger.info("当前页面: 国债品种页")
            return "国债品种页"
        else:
            self.back_button.click()
            return "当前在未知页,尝试返回"
    # def ensure_on_account_page(self):
    #     """确保当前在账户页"""
    #     current_page = common_page.where_page()
    #     logger.info(f"当前页面: {current_page}")
    #
    #     # 确保在账户页
    #     if not current_page == "账户页":
    #         if current_page == "首页":
    #             # 如果没有可用按钮，则点击持仓入口
    #             self.trade_button_entry.click()
    #             time.sleep(1)
    #             if not self.search_button.exists:
    #                 print("没有分享按钮")
    #                 self.click_holding_stock_entry()
    #         elif current_page == "交易页":
    #             self.click_holding_stock_entry()
    #         elif current_page == "国债列表页":
    #             self.click_back()
    #         elif current_page == "国债品种页":
    #             self.click_back()
    #             self.click_back()
    #         else:
    #             logger.error("无法返回账户页")
    #             return False
    #         logger.info("已切换至: 账户页")
    #     else:
    #         return True
    def goto_account_page(self):
            """确保当前在账户页"""
            time.sleep(1)
            current_page = self.where_page()
            logger.info(f"当前页面: {current_page}")

            # 确保在账户页
            if current_page == "账户页":
                return True

            # 确保在账户页
            # if not current_page == "账户页":
            elif current_page == "首页":
                # 如果没有可用按钮，则点击持仓入口
                self.trade_button_entry.click()
                time.sleep(1)
                if not self.search_button.exists:
                    # print("没有分享按钮")
                    self.holding_entry.click()
            elif current_page == "交易页":
                self.holding_entry.click()
            elif current_page == "国债列表页":
                self.back_button.click()
            elif current_page == "国债品种页":
                self.back_button.click()
                self.back_button.click()
            else:
                logger.error("无法返回账户页")
                return False

            # 再次确认是否已进入账户页
            if self.where_page() == "账户页":
                logger.info("✅ 已切换至: 账户页")
                return True
            else:
                logger.error("❌ 无法返回账户页")
                return False
    def goto_trade_page(self,max_retry=3):
        for _ in range(max_retry):
            current_page = self.where_page()
            if current_page == "交易页":
                logger.info("已切换至: 交易页")
                return True
            elif current_page == "首页":
                self.trade_button_entry.click()
            elif current_page == "账户页":
                self.back_button.click()
            elif current_page == "国债列表页":
                self.back_button.click()
                self.back_button.click()
            elif current_page == "国债品种页":
                self.back_button.click()
                self.back_button.click()
                self.back_button.click()
            time.sleep(1)
    
        logger.error("多次尝试后仍无法进入交易页")
        return False
    
    def change_account(self,to_account):
        """
        切换账户，必须在交易页执行，因为有切换模拟
        判断当前页面
            如果当前为交易页，获取账户名
            判断当前账户
                如果当前为目标账户,跳过
                如果当前不为目标账户，执行切换操作
        :current_account_name: 当前账户
        :param to_account: 目标账户名称（如 "模拟" / "川财证券" / "长城证券"）
        :return: 成功与否
        """
        time.sleep(1)
        # 切换到交易页
        self.goto_trade_page()
    
        # 切换账户逻辑
        if self.current_account_trade.exists():
            self.current_account = self.current_account_trade.get_text()
        elif self.moni_account.exists():
            self.current_account = self.moni_account.get_text()
        else:
            logger.info("账户定位失败")
            return False

        if self.current_account == to_account :
            logger.info(f"当前已是 {to_account} 账户，无需切换")
            self.holding_entry.click()
            return True

        elif to_account == "模拟练习区":
            self.moni.click()
            time.sleep(1)
            self.holding_entry.click()
            logger.info("切换至模拟账户成功")
            return True
        else:
            time.sleep(1)
            self.Agu.click()

            account_dialog = self.d(resourceId="com.hexin.plat.android:id/wt_multi_data_item_qs_name", text=to_account)
            loggin_button = self.d(resourceId="com.hexin.plat.android:id/weituo_btn_login")
            password_input = self.d(resourceId="com.hexin.plat.android:id/weituo_edit_trade_password")
            keeplogin_checkbox = self.d(resourceId="com.hexin.plat.android:id/rtv_keeplogin_tips")
            keeplogin_24h = self.d(resourceId="com.hexin.plat.android:id/tv_keeplogin_24h")
    
            password_changcheng = '660493'
            password_chuangcai = '170212'

            # 开始切换账户
            if self.current_account_trade.get_text() != to_account:
    
                self.current_account_trade.click()
                account_dialog.click()

                # 登录账户
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
                else:
                    logger.info(f"已切换至 {to_account} 账户已登录")
                    self.holding_entry.click()
                    return True
            else:
                _current_account = self.current_account
                logger.info(f"📌 当前登录账户名称: {self.current_account_trade.get_text()}")
                return True
if __name__ == '__main__':
    c = CommonPage()
    c.change_account("川财证券")
    c.change_account("长城证券")
    c.change_account("模拟练习区")