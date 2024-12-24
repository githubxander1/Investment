import datetime
from pprint import pprint

import schedule
import time
import requests
import pandas as pd
from plyer import notification

from others.量化投资.THS.自动化交易_同花顺.ths_logger import setup_logger

# 设置日志记录
# logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 根据股票代码判断市场
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import OPRATION_RECORD_DONE_FILE


def determine_market(stock_code):
    """根据股票代码判断市场"""
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('30'):
        return '创业板'
    elif stock_code.startswith(('4', '8')):
        return '北交所'
    else:
        return '其他'

# 获取组合名称和描述
def get_strategy_details(product_id):
    """获取组合名称和描述"""
    url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_portfolio_infos"
    headers = {
        "Host": "dq.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://t.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=19483",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=AxLXmrX7ofaqkd2K73acRpPBYdP0Ixa9SCcK4dxrPkWw771JxLNmzRi3WvOv"
    }
    params = {"product_id": product_id, "product_type": "portfolio"}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['status_code'] == 0:
            return {
                "组合id": product_id,
                "组合名称": result['data']['baseInfo']['productName'],
                "组合描述": result['data']['baseInfo']['productDesc']
            }
        else:
            logger.error(f"Failed to retrieve data for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        logger.error(f"请求出现错误: {e}")
        return None

# 获取历史调仓数据
def get_historical_data(portfolio_id):
    """获取历史调仓数据"""
    url = "https://t.10jqka.com.cn/portfolio/post/v2/get_relocate_post_list"
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=A-gtFDtpG9AGTjdUiWYWoHVzu936EUwbLnUgn6IZNGNW_YfHSiEcq36F8Czx"
    }
    params = {"id": portfolio_id, "dynamic_id": 0}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        pprint(response.json())
        return response.json()
    except requests.RequestException as e:
        logger.error(f"请求出现错误: {e}")
        return None

# 处理今天调仓数据
def process_today_trades(ids):
    """处理今天调仓数据"""
    all_records = []
    today = datetime.date.today().strftime('%Y-%m-%d')
    # print(f'今天{today}')
    # processed_ids = set(read_processed_ids())

    for portfolio_id in ids:
        data = get_historical_data(portfolio_id)
        # pprint(data)
        if data:
            for item in data['data']:
                create_at = item['createAt']
                # print(f'时间{create_at}')
                date_part = create_at.split()[0]
                if date_part == today:
                    content = item['content']
                    # need_relocate_reason = item['needRelocateReason']
                    for relocate in item['relocateList']:
                        code = relocate['code']
                        current_ratio = relocate['currentRatio']
                        final_price = relocate['finalPrice']
                        name = relocate['name']
                        # print(name)

                        # 检查股票名称是否为“匿名”
                        if '***' in name:
                            logger.warning(f"未订阅或股票名称显示异常 - 股票代码: {code}, 时间: {create_at}")
                            continue

                        new_ratio = relocate['newRatio']
                        market = determine_market(code)
                        operation = 'SALE' if new_ratio < current_ratio else 'BUY'
                        # 排除创业板的股票
                        # if market != '创业板':
                        all_records.append({
                            '组合id': portfolio_id,
                            '组合名称': get_strategy_details(portfolio_id).get("组合名称"),
                            '描述': get_strategy_details(portfolio_id).get("组合描述"),
                            '说明': content,
                            '时间': create_at,
                            '操作': operation,
                            '市场': market,
                            '股票名称': name,
                            '参考价': final_price,
                            '当前比例': f"{current_ratio * 100:.2f}%",
                            '新比例': f"{new_ratio * 100:.2f}%"
                        })
                            # processed_ids.add(unique_id)
    # pprint(all_records)
    if not all_records:
        logger.info("所选组合今天无调仓")
        return None

    return all_records

def send_notification(title, message):
    """发送桌面通知"""
    notification.notify(
        title=title,
        message=message,
        app_name="量化投资监控",
        timeout=10
    )


# 示例用法
def main():
    """主函数"""
    '''
    13081 好赛道出牛股
    16281 每天进步一点点
    18565 龙头一年三倍
    
    19347 超短稳定复利
    18710 用收益率征服您
    7152 中线龙头
    6994 梦想一号  死群，调仓好久好久甚至半年
    11094 低位题材
    14980 波段突击'''
    # ids = [6994, 18710, 16281, 19347, 13081]
    ids = [14980]

    today_trade_df = pd.DataFrame(process_today_trades(ids))
    # print(today_trade_df)

    if not today_trade_df.empty:
        today_trade_df.to_excel(file_path, sheet_name='组合今天调仓', index=False)

        today_trade_df_print = today_trade_df.drop(columns=['组合id', '描述', '说明'])
        today_trade_without_cyb_print = today_trade_df_print[today_trade_df['市场'] != '创业板']
        # print(today_trade_df_print)
        pprint(today_trade_without_cyb_print)

        if not today_trade_without_cyb_print.empty:
            send_notification("今日调仓提醒", "发现今日有新的调仓操作！组合")
            logger.info("发送通知成功: 今日有新的调仓操作（非创业板）")
            # 创建标志文件
            with open(f"{OPRATION_RECORD_DONE_FILE}", "w") as f:
                f.write("组合调仓已完成")
        else:
            logger.info("未发送通知: 组合今天有调仓，但是是创业板股票")
    else:
        logger.info("今天没有调仓")


if __name__ == "__main__":
    logger = setup_logger('组合_今天调仓.log')
    file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\整合\data\组合今天调仓.xlsx'
    main()
    # schedule.every(30).minutes.do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
