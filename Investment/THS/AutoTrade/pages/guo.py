import time
import uiautomator2 as u2
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.pages.page_common import CommonPage

logger = setup_logger(__name__)
common_page = CommonPage()


class GuozhaiPage:
    def __init__(self, d):
        self.d = d
        self.common_page = CommonPage()

    def guozhai_change_account(self, account_name):
        """切换到指定账户"""
        try:
            # 切换到国债逆回购页面
            if not self.common_page.goto_guozhai_page():
                logger.error("无法进入国债逆回购页面")
                return False

            # 点击账户切换按钮
            account_button = self.d(resourceId="com.hexin.plat.android:id/account_switch_btn")
            if account_button.exists:
                account_button.click()
                time.sleep(1)

                # 查找并点击目标账户
                target_account = self.d(text=account_name)
                if target_account.exists:
                    target_account.click()
                    time.sleep(2)
                    logger.info(f"成功切换到账户: {account_name}")
                    return True
                else:
                    logger.error(f"未找到账户: {account_name}")
                    return False
            else:
                logger.error("未找到账户切换按钮")
                return False
        except Exception as e:
            logger.error(f"切换账户时发生异常: {e}")
            return False

    def guozhai_operation(self):
        """执行国债逆回购操作"""
        try:
            logger.info("开始执行国债逆回购操作...")

            # 确保在国债逆回购页面
            if not self.common_page.goto_guozhai_page():
                logger.error("无法进入国债逆回购页面")
                return False, "无法进入国债逆回购页面"

            # 点击"立即参与"或类似按钮
            participate_btn = self.d(resourceId="com.hexin.plat.android:id/participate_btn")
            if participate_btn.exists:
                participate_btn.click()
                time.sleep(1)
            else:
                # 尝试其他可能的按钮ID
                alternative_btn = self.d(text="立即参与")
                if alternative_btn.exists:
                    alternative_btn.click()
                    time.sleep(1)
                else:
                    logger.warning("未找到立即参与按钮，尝试直接操作")

            # 选择期限（通常默认是1天期，即GC001）
            # 如果需要选择其他期限，可以在这里添加逻辑

            # 输入金额（如果需要）
            # 通常系统会自动填入最大可用金额，但也可以手动设置

            # 点击确认按钮
            confirm_btn = self.d(resourceId="com.hexin.plat.android:id/confirm_btn")
            if confirm_btn.exists:
                confirm_btn.click()
                time.sleep(1)
            else:
                # 尝试其他可能的确认按钮
                alternative_confirm = self.d(text="确认")
                if alternative_confirm.exists:
                    alternative_confirm.click()
                    time.sleep(1)

            # 处理可能的确认对话框
            dialog_confirm = self.d(resourceId="android:id/button1")  # 通常是"确定"按钮
            if dialog_confirm.exists:
                dialog_confirm.click()
                time.sleep(2)

            # 检查操作是否成功
            success_indicator = self.d(textContains="成功")  # 查找包含"成功"的文本
            if success_indicator.exists:
                logger.info("国债逆回购操作成功")
                return True, "国债逆回购操作成功"
            else:
                # 检查是否有错误信息
                error_indicator = self.d(textContains="失败") or self.d(textContains="错误")
                if error_indicator.exists:
                    logger.error("国债逆回购操作失败")
                    return False, "国债逆回购操作失败"
                else:
                    # 如果没有明确的成功或失败信息，假设操作成功
                    logger.warning("无法明确判断操作结果，假设操作成功")
                    return True, "操作完成（结果待确认）"

        except Exception as e:
            logger.error(f"国债逆回购操作过程中发生异常: {e}")
            return False, f"操作异常: {str(e)}"

    def execute_guozhai_repurchase(self):
        """执行国债逆回购的完整流程"""
        try:
            logger.info("🚀 开始执行国债逆回购交易...")

            # 执行国债逆回购操作
            success, message = self.guozhai_operation()

            if success:
                logger.info("✅ 国债逆回购交易执行完成")
            else:
                logger.error(f"❌ 国债逆回购交易执行失败: {message}")

            return success, message
        except Exception as e:
            logger.error(f"❌ 国债逆回购交易执行异常: {e}")
            return False, str(e)
