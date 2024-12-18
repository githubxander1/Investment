import requests
import pandas as pd
from pprint import pprint

def get_showRelocateData(portfolioId):
    url = "https://t.10jqka.com.cn/portfolio/base/showRelocateData"
    params = {
        "portfolioId": portfolioId
    }
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id={portfolioId}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0,ExLDQwOzYsMSw0MDs1,ExsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1,ExsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=sns_service_video_choice_detail_85853; v=A1BGY94YA48K6d-L6Aq26kqEKJWiGTRmVv2IZ0ohHKt-hf-P8ikE86YNWOaZ",
        "X-Requested-With": "com.hexin.plat.android"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()  # 假设返回的是JSON格式数据
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def process_ids(ids):
    all_holding_info = []
    for portfolio_id in ids:
        result = get_showRelocateData(portfolio_id)
        if result and result['errorCode'] == 0:
            holding_info = result['result']['holdingInfo']
            # 检查并处理可能的None值
            profit_loss_rate = holding_info.get('profitLossRate')
            position_real_ratio = holding_info.get('positionRealRatio')

            if profit_loss_rate is not None:
                profit_loss_rate *= 100
            if position_real_ratio is not None:
                position_real_ratio *= 100

            holding_info['profitLossRate'] = profit_loss_rate
            holding_info['positionRealRatio'] = position_real_ratio
            holding_info['portfolioId'] = portfolio_id
            all_holding_info.append(holding_info)
        else:
            print(f"Failed to retrieve data for portfolioId: {portfolio_id}")

    # 定义列名映射以中文显示
    column_mapping = {
        'code': '股票代码',
        'costPrice': '成本价',
        'name': '股票名称',
        'positionRealRatio': '持仓比例 (%)',
        'presentPrice': '现价',
        'profitLossRate': '盈亏率 (%)',
        'portfolioId': '组合ID'
    }

    df = pd.DataFrame(all_holding_info).rename(columns=column_mapping)
    print(df)
    df.to_excel(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\持仓详情.xlsx', index=False)

ids = [
    19483,
    14533,
    16281,
    23768,
    8426,
    9564,
    6994,
    7152,
    20335,
    21302,
    19347,
    8187,
    18565,
    14980,
    16428
]

process_ids(ids)
