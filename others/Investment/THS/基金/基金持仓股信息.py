import requests
import pandas as pd
from pprint import pprint

# 定义函数用于获取基金持仓股票信息
def get_fund_hold_stock(trade_code):
    # 接口的URL地址
    url = "https://basic.10jqka.com.cn/fuyao/fund_trans/fund/v1/hold_stock"
    # 请求参数，这里指定了基金代码
    params = {"tradeCode": trade_code}

    # 请求头信息，模拟浏览器请求
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://eq.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Referer": "https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.3.html?tabid=cpbd&code=562500&marketid=20",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    # Cookie信息，可能用于用户身份识别或会话管理等（注意隐私问题）
    cookies = {
        "user_status": "0",
        "user": "MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox",
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "ticket": "c9840d8b7eefc37ee4c5aa8dd6b90656",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "hxmPid": "sns_service_video_choice_detail_85853",
        "v": "A4aQAbRGHc0mqsmpTGjYaNAS3ncI58qhnCv-BXCvcqmEcykt2HcasWy7ThpD"
    }

    try:
        # 发送GET请求
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        # 如果请求成功（状态码为200）
        if response.status_code == 200:
            # 尝试解析返回的JSON数据并返回
            return response.json()
        else:
            # 打印请求失败的状态码信息
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        # 打印请求发生异常的信息
        print(f"请求发生异常: {e}")
        return None

# 定义函数用于处理数据并保存到Excel的不同工作表
def save_to_excel(data, trade_code, writer):
    # 提取所需字段
    stock_data = []
    for stock in data['testdata']:
        stock_info = {
            '板块': stock['block'],
            '基金代码': stock['code'],
            '证券名称': stock['secName'],
            '证券代码': stock['secCode'],
            '持仓市值比例': f"{float(stock['secMktValueRate']) * 100:.2f}%",
            '持仓数量': f"{int(stock['positionCnt']) / 1000000:.2f}百万",
            '持仓市值': f"{float(stock['positionCap']) / 100000000:.2f}亿元",
            '报告类型': stock['reportType'],
            '报告开始日期': stock['startDate'],
            '报告结束日期': stock['endDate'],
            '发布日期': stock['pubDate'],
            '市场ID': stock['marketid'],
            '二级行业': stock['second_industry'],
            '三级行业': stock['third_industry']
        }
        stock_data.append(stock_info)

    # 创建DataFrame
    df = pd.DataFrame(stock_data)

    # 保存到Excel文件的不同工作表
    df.to_excel(writer, sheet_name=f'基金_{trade_code}', index=False)

    # 打印DataFrame到控制台
    pprint(df)

if __name__ == "__main__":
    # 定义要查询的基金代码列表
    # trade_codes = ["562500", "159819", "159655", "159696"]
    trade_codes = ["159300", "159925", "515310", "159673"]

    # 创建一个Excel writer对象
    with pd.ExcelWriter('基金持股信息.xlsx', engine='openpyxl') as writer:
        for code in trade_codes:
            # 调用函数获取基金持仓股票信息
            result = get_fund_hold_stock(code)
            if result:
                # 如果获取到数据，则保存到Excel的不同工作表并打印数据
                save_to_excel(result, code, writer)
