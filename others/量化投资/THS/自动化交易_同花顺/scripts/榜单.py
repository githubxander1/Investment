from pprint import pprint

import pandas as pd
import requests

from others.量化投资.THS.自动化交易_同花顺.config.settings import Combination_list_file

# url = "https://t.10jqka.com.cn/portfoliolist/tgserv/v2/block_list?offset=0&page_size=20&block_id=0&list_type=4&match_id=14"
url = "https://t.10jqka.com.cn/portfoliolist/tgserv/v2/block_list"
params = {
    "offset": "0",
    "page_size": "20",
    "block_id": "0",
    "list_type": "4",
    "match_id": "0" #14为etf
}
headers = {
    "Host": "t.10jqka.com.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "com.hexin.plat.android",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://t.10jqka.com.cn/rankfront/portfolioSquare/index.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": "userid=641926488; u_name=mo_641926488; escapename=mo_641926488; user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM5MTUxNjM1Ojo6MTY1ODE0Mjc4MDo2MDQ4MDA6MDoxMmIyZjQ0YTY4ODFiODQ3NzVjNjYzMzYwYzY0ZTFmMzA6OjA%3D; ticket=3420cf092830838b512cc96c07f9bd09; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=sns_lungu_t_stock_2185680805; v=Axjd5MuZy1OaUOfTBDtls8cB602qAX2N3nJQD1IJZCEENbd3-hFMGy51ILKh"
}

response = requests.get(url, headers=headers,params=params)
if response.status_code == 200:
    data = response.json()
    # 提取所需字段
    extracted_data = []
    for item in data['data']['list']:
        portfolio_labels = ', '.join([label['label'] for label in item['portfolio_labels']])
        user_name = item['user_info']['user_name']
        extracted_data.append({
            '组合id': item['portfolio_id'],
            '组合名称': item['portfolio_name'],
            '收益率%': round(item['income_rate'] * 100 ,2),
            '标签': portfolio_labels,
            '作者': user_name
        })

    # 创建DataFrame
    df = pd.DataFrame(extracted_data)

    # 打印DataFrame
    pprint(df)

    # 保存到Excel文件
    # df.to_excel('榜单数据.xlsx', index=False)
    df.to_excel(Combination_list_file, index=False)
    print("数据已保存到 '榜单数据.xlsx'")
else:
    print(f"请求失败，状态码: {response.status_code}")
