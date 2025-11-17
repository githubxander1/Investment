from uiautomator2 import UiObjectNotFoundError
import time
import uiautomator2
from Investment.THS.AutoTrade.pages.base.page_base import BasePage
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

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
        判断当前在哪个页面，增加安全检查避免元素未找到错误
        
        Returns:
            str: 页面名称
        """
        try:
            trade = self.d(resourceId="com.hexin.plat.android:id/title", text="交易")
            account_name = self.d(resourceId="com.hexin.plat.android:id/qs_name_text")
            guozhailist = self.d(text="我要回购", selected=True)
            guozhaipingzhong = self.d(resourceId="com.hexin.plat.android:id/stock_pinzhong")
        
            if self.application_store.exists(timeout=2):
                return "首页"
            elif account_name.exists(timeout=2):
                return "交易入口页"
            elif self.search_button.exists(timeout=2):
                return "账户页"
            elif guozhailist.exists(timeout=2):
                return "国债列表页"
            elif guozhaipingzhong.exists(timeout=2):
                return "国债品种页"
            else:
                # 使用safe_click替代直接click，避免元素不存在导致崩溃
                logger.warning("当前在未知页面，尝试安全返回")
                self.safe_click(self.back_button)
                return "当前在未知页,尝试返回"
        except Exception as e:
            logger.error(f"页面识别出错: {str(e)}")
            return "页面识别失败"

    def goto_trade_page(self, max_retry=3):
        """
        切换到交易入口页，增加重试机制和安全导航
        
        Args:
            max_retry: 最大重试次数
            
        Returns:
            bool: 是否成功切换到交易页
        """
        logger.info("正在切换至: 交易入口页")
        retry_count = 0
        
        while retry_count < max_retry:
            try:
                current_page = self.where_page()
                logger.info(f"当前页面: {current_page}")
                
                if current_page == "交易入口页":
                    logger.info("已切换至: 交易入口页")
                    return True
                elif current_page == "首页":
                    self.safe_click(self.trade_button_entry)
                elif current_page == "账户页":
                    self.safe_click(self.back_button)
                elif current_page == "国债列表页":
                    self.safe_click(self.back_button)
                    self.safe_click(self.back_button)
                elif current_page == "国债品种页":
                    # 安全地多次返回
                    for _ in range(3):
                        self.safe_click(self.back_button)
                        time.sleep(0.5)
                elif "未知" in current_page or "失败" in current_page:
                    # 未知页面时，尝试返回到首页
                    logger.info("尝试返回首页")
                    self.safe_click(self.back_button)
                    time.sleep(1)
                    # 尝试回到首页后再点击交易按钮
                    if self.application_store.exists(timeout=2):
                        self.safe_click(self.trade_button_entry)
                
                retry_count += 1
                time.sleep(1.5)  # 增加等待时间，确保页面切换完成
            
            except Exception as e:
                logger.error(f"切换页面时出错: {str(e)}")
                retry_count += 1
                time.sleep(2)
        
        error_msg = f"多次尝试后仍无法进入交易页 (尝试次数: {max_retry})"
        logger.error(error_msg)
        send_notification(error_msg)
        return False
    
    def goto_account_page(self):
        """
        导航到账户页面
        用于交易操作前进入账户页面
        """
        try:
            logger.info("正在导航到账户页面")
            # 首先导航到交易页面
            if self.goto_trade_page():
                # 检查是否需要额外操作进入账户页
                # 如果当前已经在账户页面，则直接返回成功
                if self.where_page() == "账户页":
                    logger.info("当前已经在账户页面")
                    return True
                
                # 尝试点击持仓按钮进入账户相关页面
                if hasattr(self, 'holding_entry') and self.holding_entry.exists(timeout=3):
                    self.safe_click(self.holding_entry)
                    logger.info("点击持仓按钮进入账户页面")
                    time.sleep(1.5)
                    return True
            logger.warning("导航到账户页面失败")
            return False
        except Exception as e:
            logger.error(f"导航到账户页面过程中出错: {e}")
            return False
    
    def change_account(self, to_account):
        """
        切换账户，必须在交易页执行，增加重试机制和错误处理
        
        Args:
            to_account: 目标账户名称
            
        Returns:
            bool: 是否成功切换账户
        """
        try:
            # 首先导航到交易页
            for attempt in range(3):
                try:
                    self.goto_trade_page()
                    if self.where_page() == "交易入口页":
                        logger.info(f"成功进入交易页, 第{attempt+1}次尝试")
                        break
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"导航到交易页失败: {e}")
                    time.sleep(2)
            else:
                logger.error("多次尝试后仍未进入交易页")
                send_notification("多次尝试后仍未进入交易页")
                return False

            # 尝试获取当前账户信息
            try:
                if self.current_account_trade.exists(timeout=3):
                    self.current_account = self.current_account_trade.get_text()
                elif self.moni_account.exists(timeout=3):
                    self.current_account = self.moni_account.get_text()
                else:
                    # 尝试使用其他方式定位账户信息
                    logger.warning("标准账户定位失败，尝试其他方式")
                    accounts = self.d(resourceId="com.hexin.plat.android:id/qs_name_text")
                    if accounts.exists(timeout=3):
                        self.current_account = accounts.get_text()
                    else:
                        error_msg = "账户定位失败"
                        logger.error(error_msg)
                        send_notification(error_msg)
                        return False

                logger.info(f"当前账户: {self.current_account}, 目标账户: {to_account}")
                
                # 当前已是目标账户的情况
                if self.current_account == to_account:
                    logger.info(f"当前已是 {to_account} 账户，无需切换")
                    self.safe_click(self.holding_entry)
                    return True
                
                # 处理模拟账户切换
                elif to_account == "模拟练习区":
                    self.safe_click(self.moni)
                    time.sleep(1.5)
                    self.safe_click(self.holding_entry)
                    logger.info("切换至模拟账户成功")
                    return True
                
                # 其他账户切换逻辑
                else:
                    # 点击A股按钮
                    time.sleep(1)
                    self.safe_click(self.Agu)
                    
                    # 定义元素
                    account_dialog = self.d(resourceId="com.hexin.plat.android:id/wt_multi_data_item_qs_name", text=to_account)
                    loggin_button = self.d(resourceId="com.hexin.plat.android:id/weituo_btn_login")
                    password_input = self.d(resourceId="com.hexin.plat.android:id/weituo_edit_trade_password")
                    keeplogin_checkbox = self.d(resourceId="com.hexin.plat.android:id/rtv_keeplogin_tips")
                    keeplogin_24h = self.d(resourceId="com.hexin.plat.android:id/tv_keeplogin_24h")
                    
                    # 密码定义
                    passwords = {
                        '长城证券': '660493',
                        '中泰证券': '170212',
                        '川财证券': '170212',
                        '中山证券': '660493'
                    }
                    
                    # 开始切换账户
                    if self.current_account_trade.exists() and self.current_account_trade.get_text() != to_account:
                        self.safe_click(self.current_account_trade)
                        if account_dialog.exists(timeout=3):
                            self.safe_click(account_dialog)
                            logger.info(f"点击账户切换弹窗")
                        else:
                            logger.error(f"未找到{to_account}账户选项")
                            return False
                    
                    # 登录账户
                    if loggin_button.exists():
                        self.safe_click(loggin_button)
                        logger.info("点击登录按钮")
                    
                        # 输入密码
                        if to_account in passwords and password_input.exists(timeout=3):
                            password = passwords[to_account]
                            if to_account == '长城证券':
                                time.sleep(1)
                            password_input.set_text(password)
                            logger.info(f"输入密码: {'*' * len(password)}")
                        
                        # 处理保持登录选项
                        if keeplogin_checkbox.exists(timeout=2):
                            self.safe_click(keeplogin_checkbox)
                        if keeplogin_24h.exists(timeout=2):
                            self.safe_click(keeplogin_24h)
                            logger.info("勾选24小时登录")
                        
                        # 点击登录
                        self.safe_click(loggin_button)
                        logger.info("点击登录按钮")
                        
                        # 验证登录成功
                        if self.d(resourceId="com.hexin.plat.android:id/qs_name", text=to_account).exists(timeout=5):
                            logger.info("登录成功")
                            return True
                        else:
                            logger.warning(f"已切换至 {to_account} 账户")
                            return True
                    else:
                        logger.warning(f"已切换至 {to_account} 账户")
                        return True
            except Exception as e:
                logger.error(f"账户切换过程中出错: {str(e)}")
                
                # 尝试重新导航到交易页
                for attempt in range(3):
                    try:
                        self.goto_trade_page()
                        logger.info(f"尝试重新导航到交易页，第{attempt+1}次")
                        # 重新尝试账户切换
                        if self.current_account_trade.exists():
                            if self.current_account_trade.get_text() != to_account:
                                self.safe_click(self.current_account_trade)
                                account_dialog = self.d(resourceId="com.hexin.plat.android:id/wt_multi_data_item_qs_name", text=to_account)
                                if account_dialog.exists():
                                    self.safe_click(account_dialog)
                                    logger.info(f"重新点击账户切换弹窗")
                                    return True
                    except Exception as inner_e:
                        logger.error(f"重新导航异常：{inner_e}")
                        time.sleep(2)
                        
                send_notification(f"切换账户失败，请检查：{str(e)}")
                return False
        except Exception as e:
            logger.error(f"change_account函数异常: {str(e)}")
            return False
        
        # 确保函数总是有返回值
        return False