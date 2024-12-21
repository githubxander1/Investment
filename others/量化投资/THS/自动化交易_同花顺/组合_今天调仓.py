import datetime
import logging
from pprint import pprint

import requests
import pandas as pd
from plyer import notification

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 根据股票代码判断市场
def determine_market(stock_code):
    """根据股票代码判断市场"""
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('300'):
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
            logging.error(f"Failed to retrieve data for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        logging.error(f"请求出现错误: {e}")
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
        return response.json()
    except requests.RequestException as e:
        logging.error(f"请求出现错误: {e}")
        return None

# 处理今天调仓数据
def process_today_trades(ids):
    """处理今天调仓数据"""
    all_records = []
    today = datetime.date.today().strftime('%Y-%m-%d')

    for portfolio_id in ids:
        data = get_historical_data(portfolio_id)
        if data:
            for item in data['data']:
                create_at = item['createAt']
                date_part = create_at.split()[0]
                if date_part == today:
                    content = item['content']
                    need_relocate_reason = item['needRelocateReason']
                    for stock in item['relocateList']:
                        code = stock['code']
                        current_ratio = stock['currentRatio']
                        final_price = stock['finalPrice']
                        name = stock['name']

                        # 检查股票名称是否为“匿名”
                        if '***' in name:
                            logging.warning(f"未订阅或股票名称显示异常 - 股票代码: {code}, 时间: {create_at}")
                            continue

                        new_ratio = stock['newRatio']
                        market = determine_market(code)
                        operation = 'SALE' if new_ratio < current_ratio else 'BUY'
                        # 排除创业板的股票
                        if market != '创业板':
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

    if not all_records:
        logging.info("所选组合今天无调仓")
        return None

    today_trade_df = pd.DataFrame(all_records)
    return today_trade_df

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
    ids = [6994, 18710, 16281, 19347, 13081]

    today_trade_df = process_today_trades(ids)

    if today_trade_df is not None:
        today_trade_df_print = today_trade_df.drop(columns=['组合id', '描述', '说明'])
        file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\保存的数据\组合今天调仓.xlsx'
        today_trade_df_print.to_excel(file_path, sheet_name='组合今天调仓', index=False)
        pprint(today_trade_df_print)
        send_notification("今日调仓提醒", "发现今日有新的调仓操作！组合")
    else:
        logging.info("没有今天的调仓数据可供打印")

if __name__ == "__main__":
    main()
