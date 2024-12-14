from pprint import pprint
import requests
import pandas as pd

def get_etf_base_info(trade_code):
    """
    发送GET请求获取ETF基础信息的函数
    """
    url = "https://basic.10jqka.com.cn/fundf10/etf/v1/base"
    params = {
        "trade_code": trade_code,
        "group": "baseInfo"
    }
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://eq.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Referer": f"https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.3.html?tabid=cpbd&code={trade_code}&marketid=20",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0,ExLDQwOzYsMSw0MDs1,ExsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1,ExsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=sns_service_video_choice_detail_85853; v=A9jOG5agC-ekJCdjLsiu8hJsoA1qwTxLniUQzxLJJJPGrXc3utEM2-414Fxh",
        "X-Requested-With": "com.hexin.plat.android"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()  # 假设返回的数据是JSON格式，返回解析后的内容
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def extract_important_info(data):
    if data and data['status_code'] == 0:
        info = data['data']
        return {
            '基金名称': info.get('fullname'),
            '简称': info.get('simpleName'),
            '基金代码': info.get('trade_code'),
            '成立日期': info.get('estabDate'),
            '上市日期': info.get('listedDate'),
            '基金管理人': info.get('mgmtName'),
            '基金托管人': info.get('fundCustodianName'),
            '基金规模': info.get('fundScale'),
            '基金份额': info.get('fundShare'),
            '基金类型': info.get('l2name'),
            '跟踪指数': info.get('perfmCompareBenchmark'),
            '管理费率': info.get('manageFee'),
            '托管费率': info.get('custodyFee'),
            '运作费用': info.get('operateFee'),
            '基金经理': ', '.join([manager['fundManagerName'] for manager in info.get('fundManagerList', [])]),
            '投资目标': info.get('investGoal'),
            '投资范围': info.get('investScope'),
            '投资策略': info.get('investStrategy')
        }
    return {}

def print_fund_info(fund_ids):
    all_info = []
    for fund_id in fund_ids:
        data = get_etf_base_info(fund_id)
        pprint(data)
        info = extract_important_info(data)
        if info:
            all_info.append(info)
            print(f"基金{fund_id}的信息:")
            print(pd.DataFrame([info]))
            print("\n")

    if all_info:
        df = pd.DataFrame(all_info)
        df.to_excel('基金信息.xlsx', index=False)

if __name__ == "__main__":
    # 定义要查询的基金代码列表
    fund_ids = ["562500", "159819", "159655", "159696"]

    # 打印多个基金的信息并保存到Excel
    print_fund_info(fund_ids)
