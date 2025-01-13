from pprint import pprint

import pandas as pd
import requests


def get_index_source():
    """
    该函数用于向指定接口发送请求获取指数源数据
    """
    # 接口地址
    url = "https://basic.10jqka.com.cn/fuyao/financial_reports_visual/finance/v1/index_source"
    # 请求参数，指定股票代码和市场
    params = {"code": "600188", "market": "17"}
    # 请求头信息
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "hexin-v": "A6q8bfCa3mVQDzVVlcr8HNwm8htMGy51IJ-iGTRjVv2IZ0WBHKt-hfAv8iMH",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Referer": "https://basic.10jqka.com.cn/astockph/briefinfo/index.html?code=600188&marketid=17",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    # Cookie信息（注意其中可能包含用户相关隐私数据，使用时需谨慎）
    cookies = {
        "user_status": "0",
        "user": "MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox",
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "ticket": "c9840d8b7eefc37ee4c5aa8dd6b90656",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "hxmPid": "sns_service_video_choice_detail_85853",
        "v": "A6q8bfCa3mVQDzVVlcr8HNwm8htMGy51IJ-iGTRjVv2IZ0WBHKt-hfAv8iMH"
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

def save_to_excel(data, filename='stock_data.xlsx'):
    """
    将数据保存到Excel文件中
    """
    # 创建一个Excel writer对象
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 保存banner_card到Excel
        banner_card_df = pd.DataFrame(data.get('banner_card', []))
        banner_card_df.to_excel(writer, sheet_name='banner_card', index=False)

        # 保存latest_index到Excel
        latest_index = data.get('latest_index', [])
        latest_index_df = pd.DataFrame([
            {
                '指标ID': item['index_id'],
                '名称': item['name'],
                '值': item['value'],
                '单位': item['unit'],
                '来源': item['source']
            }
            for item in latest_index
        ])
        latest_index_df.to_excel(writer, sheet_name='latest_index', index=False)

        # 保存jump_url到Excel
        jump_url_df = pd.DataFrame([{'jump_url': data.get('jump_url', '')}])
        jump_url_df.to_excel(writer, sheet_name='jump_url', index=False)

        # 保存main_operate_list到Excel（如果存在）
        main_operate_list = data.get('main_operate_list', [])
        if main_operate_list:
            main_operate_list_df = pd.DataFrame(main_operate_list)
            main_operate_list_df.to_excel(writer, sheet_name='main_operate_list', index=False)

        # 保存source到Excel
        source_df = pd.DataFrame([{'source': data.get('source', '')}])
        source_df.to_excel(writer, sheet_name='source', index=False)

        print(f"数据已保存到 {filename}")

if __name__ == "__main__":
    # 调用函数获取指数源数据
    data = get_index_source()
    if data:
        # 打印原始数据
        pprint(data)

        # 保存到Excel文件
        save_to_excel(data)
