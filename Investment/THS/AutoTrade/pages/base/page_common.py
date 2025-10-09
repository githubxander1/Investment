from uiautomator2 import UiObjectNotFoundError
import time
import uiautomator2
from Investment.THS.AutoTrade.pages.base.page_base import BasePage
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger("page_common.log")

class CommonPage(BasePage):
    """
    通用页面操作类，提供各页面通用的操作方法
    """

    def __init__(self, d=None):
        super().__init__(d)
        # 首页元素
        self.application_store = self.d(text="首页", selected=True)
        
        # 交易页元素
        self.trade_button_entry = self.d(resourceId="com.hexin.plat.android:id/icon")[3]
        self.moni = self.d(resourceId="com.hexin.plat.android:id/tab_mn")
        self.Agu = self.d(resourceId="com.hexin.plat.android:id/tab_a")
        self.current_account_trade = self.d(resourceId="com.hexin.plat.android:id/qs_name_text")
        self.holding_entry = self.d(resourceId='com.hexin.plat.android:id/menu_holdings_text', text='持仓')
        
        # 账户页元素
        self.current_account = self.d(resourceId="com.hexin.plat.android:id/page_title_view")
        self.keyong = self.d(resourceId="com.hexin.plat.android:id/capital_cell_title")[4]
        self.current_text = self.d(resourceId="com.hexin.plat.android:id/currency_text", text="人民币账户 A股")
        self.share_button = self.d(resourceId="com.hexin.plat.android:id/share_container")
        self.search_button = self.d(resourceId="com.hexin.plat.android:id/search_container")
        self.account_title = self.d(resourceId="com.hexin.plat.android:id/page_title_view")
        self.moni_account = self.d(resourceId="com.hexin.plat.android:id/division_name_text")
        
        # 返回按钮
        self.back_button = self.d(resourceId="com.hexin.plat.android:id/title_bar_img")

    def safe_click(self, element, timeout=3):
        """
        安全点击元素
        
        Args:
            element: 要点击的元素
            timeout: 等待超时时间
            
        Returns:
            bool: 点击是否成功
        """
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

    def where_page(self):
        """
        判断当前在哪个页面
        
        Returns:
            str: 页面名称
        """
        trade = self.d(resourceId="com.hexin.plat.android:id/title", text="交易")
        account_name = self.d(resourceId="com.hexin.plat.android:id/qs_name_text")
        guozhailist = self.d(text="我要回购", selected=True)
        guozhaipingzhong = self.d(resourceId="com.hexin.plat.android:id/stock_pinzhong")
    
        if self.application_store.exists():
            return "首页"
        # elif trade.exists() and trade.info.get('selected') == True:
        elif account_name.exists():
            return "交易入口页"
        elif self.search_button.exists():
            return "账户页"
        elif guozhailist.exists(timeout=3):
            return "国债列表页"
        elif guozhaipingzhong.exists():
            return "国债品种页"
        else:
            self.back_button.click()
            return "当前在未知页,尝试返回"

    def goto_account_page(self):
        """
        确保当前在账户页
        
        Returns:
            bool: 是否成功切换到账户页
        """
        time.sleep(1)
        logger.info("正在切换至: 账户页")
        current_page = self.where_page()
        logger.info(f"当前页面: {current_page}")

        # 确保在账户页
        if current_page == "账户页":
            return True
        elif current_page == "首页":
            # 如果没有可用按钮，则点击持仓入口
            self.trade_button_entry.click()
            time.sleep(1)
            if not self.search_button.exists:
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

    def goto_trade_page(self, max_retry=3):
        """
        切换到交易入口页
        
        Args:
            max_retry: 最大重试次数
            
        Returns:
            bool: 是否成功切换到交易页
        """
        logger.info("正在切换至: 交易入口页")
        for _ in range(max_retry):
            current_page = self.where_page()
            if current_page == "交易入口页":
                logger.info("已切换至: 交易入口页")
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
    
    def change_account(self, to_account):
        """
        切换账户，必须在交易页执行
        
        Args:
            to_account: 目标账户名称
            
        Returns:
            bool: 是否成功切换账户
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

        if self.current_account == to_account:
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
            password_zhongtai = '170212'
            password_zhongshan = '660493'

            # 开始切换账户
            if self.current_account_trade.get_text() != to_account:
                self.current_account_trade.click()
                account_dialog.click()
                logger.info(f"点击账户切换弹窗")

                # 登录账户
                if loggin_button.exists():
                    loggin_button.click()
                    logger.info("点击登录按钮")
    
                    if to_account == '长城证券':
                        time.sleep(1)
                        password_input.set_text(password_changcheng)
                        logger.info(f"输入密码: {password_changcheng}")
                    elif to_account == '中泰证券':
                        password_input.set_text(password_zhongtai)
                        logger.info(f"输入密码: {password_zhongtai}")
                    elif to_account == '川财证券':
                        password_input.set_text(password_chuangcai)
                        logger.info(f"输入密码: {password_chuangcai}")
                    elif to_account == '中山证券':
                        password_input.set_text(password_zhongshan)
                        logger.info(f"输入密码: {password_zhongshan}")
    
                    keeplogin_checkbox.click()
                    if keeplogin_24h.exists():
                        keeplogin_24h.click()
                        logger.info("勾选24小时登录")
    
                    loggin_button.click()
                    logger.info("点击登录按钮")
                    # time.sleep(1)
                    if self.d(resourceId="com.hexin.plat.android:id/qs_name", text=to_account).exists():
                        logger.info("登录成功")
                        # self.holding_entry.click()
                        # logger.info("点击持仓按钮(入口)")
                        return True
                    else:
                        logger.error("登录失败")
                        return False
                else:
                    logger.warning(f"已切换至 {to_account} 账户已登录")
                    # self.holding_entry.click()
                    # logger.info("点击持仓按钮(入口)")
                    return True
            else:
                _current_account = self.current_account
                logger.info(f"📌 当前登录账户名称: {self.current_account_trade.get_text()}")
                return True

if __name__ == '__main__':
    com = CommonPage()
    # print(com.where_page())
    # com.goto_trade_page()
    # com.goto_account_page()
    # com.change_account("中泰证券")