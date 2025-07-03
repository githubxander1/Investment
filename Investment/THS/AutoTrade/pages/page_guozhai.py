# page_guozhai.py

import uiautomator2 as u2
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger('nihuigou.log')



def guozhai_operation(d):
    logger.info("---------------------国债逆回购任务开始执行---------------------")
    prompt_content = d(resourceId="com.hexin.plat.android:id/prompt_content")
    confirm_button = d(resourceId="com.hexin.plat.android:id/ok_btn")
    back_button = d(resourceId="com.hexin.plat.android:id/title_bar_img")

    try:
        # 点击右上角第二个图标（通常是国债逆回购入口）
        d(resourceId="com.hexin.plat.android:id/title_right_image")[1].click()
        logger.info("点击国债逆回购入口")

        # 下滑到出现“沪市”位置，然后点击 stock_list 下的第一个 LinearLayout
        d.swipe(0.5, 0.8, 0.5, 0.2)
        logger.info("下滑到‘沪市’")

        # 点击第一个线性布局（通常为第一个国债逆回购选项）
        yitianqi = d(className="android.widget.LinearLayout")[20]
        yitianqi.click()
        logger.info("点击‘一天期’")

        # 点击“借出”按钮
        d(resourceId="com.hexin.plat.android:id/btn_jiechu").click()
        logger.info("点击‘借出’按钮")

        # 检查弹窗内容，判断是否为资金不足的情况
        if prompt_content.exists:
            prompt_text = prompt_content.get_text()
            if not '委托已提交' in prompt_text:
                logger.warning(f"委托失败: {prompt_text}")
                confirm_button.click()
                back_button.click()
                back_button.click()
                send_notification(f"国债逆回购任务失败: {prompt_text}")
                return False, prompt_text

        # 获取 content_layout 里的所有 TextView 内容
        content_layout = d(resourceId="com.hexin.plat.android:id/content_layout")
        if content_layout.exists:
            text_views = content_layout.child(className="android.widget.TextView")
            content_texts = []
            for tv in text_views:
                content_texts.append(tv.get_text())
            # print(f"弹窗内容: {content_texts}")
            if '委托已提交' in content_texts:
                confirm_button.click()
                logger.info(f"国债逆回购委托成功：{content_texts}")
            else:
                logger.warning("委托失败")
                return False, f"委托失败: {content_texts}"
        else:
            error_info = "弹窗不存在"
            logger.warning(error_info)
            return False, error_info

        # # 点击“确认借出”按钮
        # if confirm_button.exists:
        #     confirm_button.click()
        #     logger.info("点击‘确认借出’按钮")
        # else:
        #     error_info = "确定按钮不存在"
        #     logger.warning(error_info)
        #     return False, error_info

        # # 获取提示内容并打印（如果需要）
        # if prompt_content.exists:
        #     print(f"弹窗内容: {prompt_content.get_text()}")

        # 返回上级页面
        if back_button.exists:
            back_button.click()
            logger.info("返回上级页面")
        else:
            logger.warning("返回按钮不存在")

        logger.info("---------------------国债逆回购任务执行完毕---------------------")
        return True, "操作成功"

    except Exception as e:
        logger.error(f"错误: {e}")
        return False, str(e)

if __name__ == '__main__':
    d = u2.connect()
    success, message = guozhai_operation(d)
    if success:
        print("Operation succeeded.")
    else:
        print(f"Operation failed: {message}")
