import time
import uiautomator2 as u2


def refresh_account_holding():
    """
    刷新账户持仓数据
    """
    try:
        d = u2.connect()
        print("设备连接成功:", d.info)

        # 打开应用
        d.app_start("com.hexin.zhanghu")
        print("打开账本")
        time.sleep(3)

        # 尝试多种方式点击股票
        print("尝试点击股票标签...")
        stock_clicked = False
        
        # 方式1: 通过resourceId和索引
        if d(resourceId="com.hexin.zhanghu:id/tv_table_label").count > 1:
            d(resourceId="com.hexin.zhanghu:id/tv_table_label")[1].click()
            print("通过索引点击股票标签")
            stock_clicked = True
        else:
            print("方式1失败: 未找到足够的标签")
            
        # 如果方式1失败，尝试其他方式
        if not stock_clicked:
            # 方式2: 通过文本查找
            if d(text="股票").exists():
                d(text="股票").click()
                print("通过文本点击股票标签")
                stock_clicked = True
            else:
                print("方式2失败: 未找到文本为'股票'的元素")
                
        # 如果方式2也失败，尝试通过className查找
        if not stock_clicked:
            stock_labels = d(className="android.widget.TextView", textContains="股票")
            if stock_labels.count > 0:
                stock_labels[0].click()
                print("通过className点击股票标签")
                stock_clicked = True
            else:
                print("方式3失败: 未找到包含'股票'的TextView元素")
                
        if not stock_clicked:
            print("所有方式都失败，无法点击股票标签")
            return False
            
        time.sleep(3)

        # 点击我的持仓
        print("尝试点击我的持仓...")
        holding_clicked = False
        
        # 方式1: 通过resourceId
        if d(resourceId="com.hexin.zhanghu:id/title").exists():
            d(resourceId="com.hexin.zhanghu:id/title").click()
            print("通过resourceId点击我的持仓")
            holding_clicked = True
        else:
            print("方式1失败: 未找到我的持仓按钮")
            
        # 方式2: 通过文本
        if not holding_clicked:
            if d(text="我的持仓").exists():
                d(text="我的持仓").click()
                print("通过文本点击我的持仓")
                holding_clicked = True
            else:
                print("方式2失败: 未找到文本为'我的持仓'的元素")
                
        if not holding_clicked:
            print("无法点击我的持仓")
            return False
            
        time.sleep(3)

        # 检查是否进入'我的持仓'页面
        print("检查是否进入'我的持仓'页面...")
        in_holding_page = False
        
        if d(resourceId="com.hexin.zhanghu:id/mainTitleTv").exists():
            print("通过mainTitleTv确认进入'我的持仓'页面")
            in_holding_page = True
        elif d(text="我的持仓").exists():
            print("通过文本确认进入'我的持仓'页面")
            in_holding_page = True
        else:
            print("警告: 可能未正确进入'我的持仓'页面")
            # 尝试继续执行，可能页面已正确加载但检测方式不匹配

        # 滑动到底部，直到出现'电脑上查看'的按钮
        print("开始滑动查找'电脑上查看'按钮...")
        scroll_attempts = 0
        max_scroll_attempts = 15
        while not d(text="电脑上查看").exists() and scroll_attempts < max_scroll_attempts:
            d.swipe(0.5, 0.8, 0.5, 0.2)#, duration=1
            print(f"下滑 {scroll_attempts + 1}")
            time.sleep(1.5)
            scroll_attempts += 1

        if d(text="电脑上查看").exists():
            print("找到'电脑上查看'按钮")
        else:
            print(f"警告: 达到最大滑动次数({max_scroll_attempts})，未找到'电脑上查看'按钮")

        # 同步账户
        print("尝试点击同步按钮...")
        sync_clicked = False
        
        # 方式1: 通过resourceId
        if d(resourceId="com.hexin.zhanghu:id/refreshIconTv").exists():
            d(resourceId="com.hexin.zhanghu:id/refreshIconTv").click()
            print("通过resourceId点击同步")
            sync_clicked = True
        else:
            print("方式1失败: 未找到同步按钮")
            
        # 方式2: 通过文本
        if not sync_clicked:
            if d(text="同步").exists():
                d(text="同步").click()
                print("通过文本点击同步")
                sync_clicked = True
            else:
                print("方式2失败: 未找到文本为'同步'的元素")
                
        if not sync_clicked:
            print("警告: 无法点击同步按钮，尝试继续执行")

        time.sleep(3)

        # 检查是否进入'账户同步'页面
        print("检查是否进入'账户同步'页面...")
        if d(text="账户同步").exists():
            print("进入'账户同步'页面")
        else:
            print("未检测到'账户同步'页面")

        # 处理同步过程
        print("尝试点击一键同步...")
        if d(text="一键同步").exists():
            d(text="一键同步").click()
            print("点击一键同步")
        else:
            print("未找到'一键同步'按钮，可能已自动同步")

        # 等待同步完成
        print("等待同步完成...")
        sync_timeout = 45  # 最多等待45秒
        start_time = time.time()
        while time.time() - start_time < sync_timeout:
            if d(text="同步完成").exists():
                print('同步完成')
                break
            time.sleep(1)
        else:
            print("同步超时，假设已完成")

        # 返回操作
        print("尝试返回操作...")
        back_success = False
        
        # 方式1: 通过className
        back_buttons = d(className="android.widget.Image")
        if back_buttons.exists:
            back_buttons.click()
            print("通过Image类点击返回")
            back_success = True
        else:
            print("方式1失败: 未找到Image类返回按钮")
            
        # 方式2: 通过resourceId
        if not back_success:
            if d(resourceId="com.hexin.zhanghu:id/title_bar_left_container").exists():
                d(resourceId="com.hexin.zhanghu:id/title_bar_left_container").click()
                print("通过标题栏返回")
                back_success = True
            else:
                print("方式2失败: 未找到标题栏返回按钮")
                
        # 方式3: 通过系统返回键
        if not back_success:
            d.press("back")
            print("通过系统返回键返回")
            back_success = True

        time.sleep(2)
        
        # 再次滑动到底部，查找'电脑上查看'按钮
        print("再次滑动查找'电脑上查看'按钮...")
        scroll_attempts = 0
        while not d(text="电脑上查看").exists() and scroll_attempts < 10:
            d.swipe(0.5, 0.8, 0.5, 0.2)#, duration=0.5
            print(f"下滑 {scroll_attempts + 1}")
            time.sleep(1)
            scroll_attempts += 1

        # 点击电脑上查看
        print("尝试点击'电脑上查看'...")
        if d(text="电脑上查看").exists():
            d(text="电脑上查看").click()
            print("点击电脑上查看")
        else:
            print("未找到'电脑上查看'按钮")

        # 点击上传
        print("尝试点击上传...")
        upload_button = d(resourceId="com.hexin.zhanghu:id/uploadTv")
        if upload_button.exists:
            upload_button.click()
            print("点击上传")
        else:
            print("未找到上传按钮")

        print("账户持仓刷新完成")
        # 返回
        d(resourceId="com.hexin.zhanghu:id/backImg").click()
        print("点击返回")
        time.sleep(1)
        d(resourceId="com.hexin.zhanghu:id/leftBackIv").click()
        print("点击返回2")

        # 检查是否进入'我的持仓'页面
        print("检查是否进入'我的持仓'页面...")
        in_holding_page = False

        if d(resourceId="com.hexin.zhanghu:id/title")[3].exists():
            print("通过mainTitleTv确认进入'我的持仓'页面")
            in_holding_page = True
        elif d(text="盈亏日历").exists():
            print("通过文本确认进入'我的持仓'页面")
            in_holding_page = True
        else:
            print("警告: 可能未正确进入'我的持仓'页面")
            d.press("back")
            print("点击返回")
        return True

    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def debug_ui_elements():
    """
    调试当前页面的UI元素
    """
    try:
        d = u2.connect()
        print("当前页面所有元素:")
        print(d.dump_hierarchy())
    except Exception as e:
        print(f"调试过程中出现错误: {e}")


if __name__ == "__main__":
    refresh_account_holding()
    # 如果需要调试UI元素，可以取消下面这行的注释
    # debug_ui_elements()