import time
import uiautomator2 as u2

import requests
import json
from pprint import pprint
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import os

from Investment.THS.AutoTrade.config.settings import Account_holding_file


def fetch_stock_position(fund_key: str, account_name: str = ""):
    """调用股票持仓接口，获取原始position数据"""
    url = "https://tzzb.10jqka.com.cn/caishen_httpserver/tzzb/caishen_fund/pc/asset/v1/stock_position"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0 Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-ch-ua': "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://tzzb.10jqka.com.cn",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://tzzb.10jqka.com.cn/pc/index.html",
        'accept-language': "zh-CN,zh;q=0.9",
        'priority': "u=1, i",
        'Cookie': "shoudNotCookieRefresh=1; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0; u_dpass=fou%2F0LouwneNgg4aLANzv2enaqgkV1cyTWuTdDYhEScfYqYIyaTF3YeykygdN%2FRBHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=CC37D8EBB29D40329773B6DEFBD27A2F; u_ttype=WEB; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzU4MTExNTk1Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE1OTg3M2ZhNzYyZjc0NmVmNzZhMjgyNzNjMTY5YTAzOmRlZmF1bHRfNTox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c70e5cfdec172dd60b4e33da5350c9df; user_status=0; utk=2c7de60a214d547dd20f9089d3ef8b0d; sess_tk=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6InNlc3NfdGtfMSIsImJ0eSI6InNlc3NfdGsifQ.eyJqdGkiOiIwMzlhMTYzYzI3Mjg2YWY3NmU3NDJmNzZmYTczOTgxNTEiLCJpYXQiOjE3NTgxMTE1OTUsImV4cCI6MTc2MDc4OTk5NSwic3ViIjoiNjQxOTI2NDg4IiwiaXNzIjoidXBhc3MuMTBqcWthLmNvbS5jbiIsImF1ZCI6IjIwMjAxMTE4NTI4ODkwNzIiLCJhY3QiOiJvZmMiLCJjdWhzIjoiMzJiZGRiOWJlMTM1ZTY5NWUzNjlkYzBhZDcxOWIxZjIwNDlmYWNiYmEzMGVlYjcwMDkzNzQzNWFkMzkwM2Q5NSJ9.VBxfCBikgTJjC4ioQtoDOu1a0NooRz25PHy-muzrZS6LSKZCgmUoTHYogqWKAs7H2EcAT-ufy_CzN8u8N55rQQ; cuc=sufmt4wli5k8; v=AzhS_mYPpFE3sMjViWIsY1gVCe3PoZwr_gVwr3KphHMmjdbTGrFsu04VQDHB"
    }
    payload = {
        'terminal': "1",
        'version': "0.0",
        'userid': "641926488",
        'user_id': "641926488",
        'manual_id': "",
        'fund_key': fund_key,
        'rzrq_fund_key': ""
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        resp_json = response.json()
        print(f"成功获取 {account_name} 账户数据")
        return resp_json

    except requests.RequestException as e:
        print(f"HTTP请求异常: {str(e)}")
        return None
    except json.JSONDecodeError:
        print("响应格式错误（非JSON）")
        return None
    except Exception as e:
        print(f"未知异常: {str(e)}")
        return None


def extract_position_details(resp_json: dict, account_name: str) -> dict:
    """提取持仓关键信息（适配界面列：代码、名称、持有金额、当日盈亏等）"""
    # 提取position原始数据
    money_remain = resp_json.get("ex_data", {}).get("money_remain", 0)  # 账户余额
    position_rate = resp_json.get("ex_data", {}).get("position_rate", 0)  # 仓位
    total_asset = resp_json.get("ex_data", {}).get("total_asset", 0)  # 总资产
    total_liability = resp_json.get("ex_data", {}).get("total_liability", 0)  # 总负债
    total_value = resp_json.get("ex_data", {}).get("total_value", 0)  # 总市值
    position_list = resp_json.get("ex_data", {}).get("position", [])
    
    # 账户汇总信息
    account_summary = {
        "账户名称": account_name,
        "账户余额": money_remain,
        "仓位%": position_rate,
        "总资产": total_asset,
        "总市值": total_value,
        "总负债": total_liability,
        "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 持仓详细信息
    extracted = []
    for item in position_list:
        code = item.get("code", "")
        # 0开头的补足6位
        code = code if len(code) > 5 else "0" + code
        # 持仓占比 = item.get("position_rate", 0)
        #转为%形式，保留2位小数

        # 安全地将字符串转换为浮点数
        # try:
        #     position_rate_value = float(item.get("position_rate", 0))#接口计算有误
        # except (ValueError, TypeError):
        #     position_rate_value = 0
        value = item.get("value", 0)
        # 持仓占比=持仓金额/总资产
        position_rate_value = float(value) / float(total_asset)
        # 转换为百分比形式，保留2位小数
        position_rate_value = round(position_rate_value * 100, 2)

        # 字段映射（与界面展示一一对应）
        detail = {
            "账户": account_name,
            "股票代码": code,
            "股票名称": item.get("name", ""),
            "持有金额": value,
            "当日盈亏": item.get("pre_profit", 0),
            "当日涨幅/当日盈亏率": item.get("pre_rate", 0),
            "持有盈亏": item.get("hold_profit", 0),
            "持有盈亏率": item.get("hold_rate", 0),
            "成本价": item.get("cost", 0),
            "当前价": item.get("price", 0),
            "持仓天数": item.get("hold_days", 0),
            "持仓占比": position_rate_value,
            "回本涨幅": item.get("back", 0),
            "持有数量": item.get("count", 0),
            "累积盈亏": item.get("position_rate", 0),
            "本周盈亏": item.get("w_profit", 0),
            "今年盈亏": item.get("y_profit", 0),
        }
        extracted.append(detail)
    return {
        "account_summary": account_summary,
        "positions": extracted
    }


def save_all_accounts_to_excel(all_accounts_data: dict, filename: str = Account_holding_file):
    """将所有账户数据保存到同一个Excel文件的不同工作表中"""
    # filename = ""
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 创建汇总表
        summary_data = []
        for account_name, data in all_accounts_data.items():
            summary_data.append(data["account_summary"])
        
        summary_df = pd.DataFrame(summary_data)
        # 按总资产排序
        summary_df = summary_df.sort_values("总资产", ascending=False)
        summary_df.to_excel(writer, sheet_name="账户汇总", index=False)
        
        # 为每个账户创建单独的工作表
        for account_name, data in all_accounts_data.items():
            if data["positions"]:
                positions_df = pd.DataFrame(data["positions"])
                positions_df.to_excel(writer, sheet_name=f"{account_name}", index=False)
            else:
                # 如果没有持仓数据，创建一个空表
                empty_df = pd.DataFrame([{
                    "账户": account_name,
                    "股票代码": "",
                    "股票名称": "无持仓",
                    "持有金额": 0,
                    "当日盈亏": 0,
                    "成本价": 0,
                    "当前价": 0,
                    "持仓天数": 0,
                    "持仓占比": 0,
                    "回本涨幅": 0,
                    "持有数量": 0,
                    "持有盈亏": 0,
                    "持有盈亏率": 0,
                    "累积盈亏": 0,
                    "本周盈亏": 0,
                    "今年盈亏": 0
                }])
                empty_df.to_excel(writer, sheet_name=f"{account_name}", index=False)
    
    print(f"所有账户数据已保存到 {filename}")


def update_account_holding_main():
    """主函数：获取所有账户数据并保存到Excel"""
    # update_account_to_computer()
    # app_restart()
    time.sleep(5)
    all_accounts_data = {}
    
    # 获取所有账户的数据
    from Investment.THS.AutoTrade.config.settings import ACCOUNTS
    for account_name, fund_key in ACCOUNTS.items():
        print(f"正在获取 {account_name} 账户数据...")
        raw_positions = fetch_stock_position(fund_key, account_name)
        if raw_positions:
            extracted_data = extract_position_details(raw_positions, account_name)
            all_accounts_data[account_name] = extracted_data
        else:
            print(f"未能获取 {account_name} 账户数据")
            # 即使没有数据也保存空结构
            all_accounts_data[account_name] = {
                "account_summary": {
                    "账户名称": account_name,
                    "账户余额": 0,
                    "仓位": 0,
                    "总资产": 0,
                    "总市值": 0,
                    "总盈亏": 0,
                    "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "positions": []
            }
    
    # 保存到Excel文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = Account_holding_file
    save_all_accounts_to_excel(all_accounts_data, filename)
    
    # 同时保存一个不带时间戳的版本，方便查找
    # save_all_accounts_to_excel(all_accounts_data, "account_positions.xlsx")
    
    # 打印汇总信息
    print("\n账户汇总信息：")
    summary_list = [data['account_summary'] for data in all_accounts_data.values()]
    summary_df = pd.DataFrame(summary_list)
    # 按总资产排序并显示
    summary_df = summary_df.sort_values("总资产", ascending=False)
    print(summary_df.to_string(index=False))

def app_restart():
    d = u2.connect()
    print("设备连接成功:", d.info)

    # 打开应用
    d.app_start("com.hexin.zhanghu")
    print("打开账本")
    time.sleep(3)
    # 获取应用状态
    app_status = d.app_current()
    print("当前应用状态:", app_status)
    # 如果已经打开了账户app，重启应用
    if app_status["package"] == "com.hexin.zhanghu":
        print("账户app已打开，重启应用")
        d.app_stop("com.hexin.zhanghu")
        d.app_start("com.hexin.zhanghu")
    time.sleep(5)

def update_account_to_computer():
    """
    刷新账户持仓数据
    """
    try:
        print("开始同步数据到电脑上")
        d = u2.connect()
        print("设备连接成功:", d.info)

        # 打开应用
        d.app_start("com.hexin.zhanghu")
        print("打开账本")
        time.sleep(3)
        # 获取应用状态
        # app_status = d.app_current()
        # print("当前应用状态:", app_status)
        # # 如果已经打开了账户app，重启应用
        # if app_status["package"] == "com.hexin.zhanghu":
        #     print("账户app已打开，重启应用")
        #     d.app_stop("com.hexin.zhanghu")
        #     d.app_start("com.hexin.zhanghu")
        # if d.app_start("com.hexin.zhanghu"):
        #     print("账户app已打开，重启应用")
        #     d.app_stop("com.hexin.zhanghu")
        #     d.app_start("com.hexin.zhanghu")

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

        # time.sleep(3)
        # 点击首页
        d(text="首页").click()
        print("点击首页")

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
            d.swipe(0.5, 0.8, 0.5, 0.2)  # , duration=1
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
            d.swipe(0.5, 0.8, 0.5, 0.2)  # , duration=0.5
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
            print("结束上传数据到电脑上")
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
    # ========== 使用说明 ==========
    # 1. 确保Cookie有效（需要登录同花顺账户）
    # 2. 根据需要修改ACCOUNTS中的账户信息
    # 3. 运行脚本将自动获取所有账户数据并保存到Excel文件
    
    update_account_holding_main()
    # update_account_to_computer()
    # app_restart()