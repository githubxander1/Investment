# scripts/组合_今天调仓.py
import logging
import datetime
import requests
import pandas as pd

from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import COMBINATION_TODAY_ADJUSTMENT_LOG_FILE, \
    COMBINATION_TODAY_ADJUSTMENT_FILE, COMBINATION_ID_TO_NAME
from others.量化投资.THS.自动化交易_同花顺.整合.utils.notification import send_notification
from others.量化投资.THS.自动化交易_同花顺.整合.utils.ths_logger import setup_logger

logger = setup_logger(COMBINATION_TODAY_ADJUSTMENT_LOG_FILE)




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

def fetch_latest_trades(portfolio_id):
    """获取指定组合的最新交易信息"""
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
        # response.raise_for_status()
        data = response.json()
        latest_trade = data.get('result', {}).get('latestTrade', {})
        trade_date = latest_trade.get('tradeDate', 'N/A')
        trade_stocks = latest_trade.get('tradeStocks', [])
        return trade_date, trade_stocks
    except requests.RequestException as e:
        logger.error(f"请求失败，状态码: {response.status_code}，组合ID: {portfolio_id}")
        return None, []

def process_trade_info(trade_info, combination_name, current_date):
    """处理单个交易信息"""
    code = trade_info.get('stkCode', 'N/A').split('.')[0]
    trade_entry = {
        '组合名称': combination_name,
        '时间': trade_info.get('tradeDate', 'N/A'),
        '操作': trade_info.get('operationType', 'N/A'),
        '股票名称': trade_info.get('stkName', 'N/A'),
        '市场': determine_market(code),
        '参考价': trade_info.get('tradePrice', 'N/A'),
        '数量': trade_info.get('tradeAmount', 'N/A'),
    }
    if trade_entry['时间'] == current_date and trade_entry['市场'] != '创业板':
        return trade_entry
    return None

def save_to_excel(df, filename, sheet_name, index=False):
    """保存DataFrame到Excel文件"""
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
        logger.info(f"成功保存数据到Excel文件: {filename}, 表名称: {sheet_name}")
    except Exception as e:
        logger.error(f"保存数据到Excel文件失败: {e}")

def main():
    combination_ids = ['1001', '1002', '1003']
    all_today_trades_info_without_cyb = []
    current_date = datetime.date.today().strftime('%Y%m%d')

    logger.info("开始处理组合调仓信息")
    for combination_id in combination_ids:
        combination_name = COMBINATION_ID_TO_NAME.get(combination_id, '未知组合')
        trade_date, trade_stocks = fetch_latest_trades(combination_id)
        if trade_stocks:
            for trade_info in trade_stocks:
                processed_trade = process_trade_info(trade_info, combination_name, current_date)
                if processed_trade:
                    all_today_trades_info_without_cyb.append(processed_trade)

    today_trades_without_cyb_df = pd.DataFrame(all_today_trades_info_without_cyb)
    if not today_trades_without_cyb_df.empty:
        save_to_excel(today_trades_without_cyb_df, COMBINATION_TODAY_ADJUSTMENT_FILE, '组合今天调仓')
        send_notification("今天有新的调仓操作！组合")
        logger.info(f'去除创业板的今天交易信息\n{today_trades_without_cyb_df}')
    else:
        logger.info("今天没有调仓操作")

    logger.info("组合调仓信息处理完成")

if __name__ == '__main__':
    main()
