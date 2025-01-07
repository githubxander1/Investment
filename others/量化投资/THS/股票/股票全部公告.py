import requests
import pandas as pd
from datetime import datetime

def get_stock_all_notices():
    """
    该函数用于向指定接口发送请求，获取股票（代码为600188）的全部公告信息。
    """
    # 接口的URL地址
    url = "https://basic.10jqka.com.cn/basicapi/notice/mobile/pub?type=stock&code=600188&market=17&classify=all&ctime=0&limit=20"

    # 请求头信息
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "hexin-v": "A-n_qD93zRi3WpbwDg-vcRvz8Z5Dtt3oR6oBfIveZVAPUgbE0wbtuNf6EUsY",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme=0 innerversion=G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Referer": "https://basic.10jqka.com.cn/astockph/briefinfo/notice.html?code=600188&marketid=17",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }

    # Cookie信息
    cookies = {
        "user_status": "0",
        "user": "MDptb18yNDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox",
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "ticket": "c9840d8b7eefc37ee4c5aa8dd6b90656",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "hxmPid": "free_stock_600188.dstx",
        "v": "A-n_qD93zRi3WpbwDg-vcRvz8Z5Dtt3oR6oBfIveZVAPUgbE0wbtuNf6EUsY"
    }

    try:
        # 发送GET请求
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求发生异常: {e}")
        return None

def process_notices(data):
    """
    该函数用于处理公告数据，提取关键字段并组织成DataFrame。
    """
    if not data or 'data' not in data or 'data' not in data['data']:
        print("数据格式不正确")
        return pd.DataFrame()

    notices = data['data']['data']
    extracted_data = []

    for notice in notices:
        extracted_data.append({
            '公告序号': notice.get('seq'),
            '公告GUID': notice.get('guid'),
            '公告标题': notice.get('title'),
            # '公告时间': datetime.fromtimestamp(notice.get('time', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            '移动版URL': notice.get('mobile_url'),
            'PC版URL': notice.get('pc_url'),
            'PDF URL': notice.get('pdf_url'),
            '原始URL': notice.get('raw_url'),
            '公告日期': notice.get('date'),
            '公告类型': notice.get('note_type'),
            '评论数': notice.get('comment_count'),
            '支持文件类型': ', '.join(notice.get('support_file_type', []))
        })

    df = pd.DataFrame(extracted_data)
    return df

if __name__ == "__main__":
    # 获取股票全部公告信息
    result = get_stock_all_notices()
    # print(result)
    if result:
        # 处理公告数据
        df = process_notices(result)
        print(df)
    #     # 保存为CSV文件
        df.to_csv('股票公告.xlsx', index=False, encoding='utf-8-sig')
