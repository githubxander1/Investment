import datetime
from pprint import pprint
import requests
import pandas as pd
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def determine_market(stock_code):
    # 根据股票代码判断市场
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

def get_name_desc(product_id):
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
    params = {
        "product_id": product_id,
        "product_type": "portfolio"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['status_code'] == 0:
            product_name = result['testdata']['baseInfo']['productName']
            product_desc = result['testdata']['baseInfo']['productDesc']
            return {
                "策略id": product_id,
                "策略名称": product_name,
                "策略描述": product_desc
            }
        else:
            print(f"Failed to retrieve testdata for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def get_history_data(portfolioId):
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
    params = {
        "id": portfolioId,
        "dynamic_id": 0
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        # pprint(response.json())
        return response.json()
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def extract_and_filter_today_data(data, portfolioId):
    today = datetime.date.today().strftime('%Y-%m-%d')
    records = []
    for item in data['testdata']:
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
                new_ratio = stock['newRatio']
                market = determine_market(code)
                operation = '卖出' if new_ratio < current_ratio else '买入'
                records.append({
                    '策略id': portfolioId,
                    '策略名称': get_name_desc(portfolioId).get("策略名称"),
                    '描述': get_name_desc(portfolioId).get("策略描述"),
                    '说明': content,
                    '时间': create_at,
                    '股票名称': name,
                    '所属市场': market,
                    '参考价': final_price,
                    '操作': operation,
                    '当前比例': f"{current_ratio * 100:.2f}%",
                    '新比例': f"{new_ratio * 100:.2f}%"
                })
    return records

def main():
    ids = [
        19483, 14533, 16281, 23768, 8426, 9564, 6994, 7152,
        20335, 19347, 8187, 18565, 14980, 16428
    ]
    # ids =['20335']#财经皮克桃
    all_records = []
    for portfolio_id in ids:
        data = get_history_data(portfolio_id)
        # pprint(testdata)
        if data:
            records = extract_and_filter_today_data(data, portfolio_id)
            all_records.extend(records)

    df = pd.DataFrame(all_records)
    df.sort_values(by='时间', ascending=False, inplace=True)
    print(df)
    df.to_excel(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\调仓历史_今天.xlsx', index=False)

if __name__ == "__main__":
    main()
