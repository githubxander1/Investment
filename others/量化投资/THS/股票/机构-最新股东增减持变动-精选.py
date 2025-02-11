from pprint import pprint

import pandas as pd
import requests
from openpyxl.utils import get_column_letter


def fetch_and_save_holder_data_jingxuan(output_file, pages_to_fetch=2):
    '''
    获取指定数量的精选持股

    :param output_file: 输出excel的路径
    :param pages_to_fetch: 输出页数
    '''
    url = "https://kuaicha.10jqka.com.cn/open/ths/v1/holder_yield/top_holder_change_info"

    headers = {
        "Host": "kuaicha.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "hexin-v": "Ay07lJsrNu1GJdIB_yKjhcdnNcKnimEq67_FMG8yaWsya0I4N9pxLHsO1RD8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme=0 innerversion=G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "source": "SDK",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb18yNDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=masterholding_news; addGongGeTip533=true; addGongGeTip534=true; jsessionid-yqapp=EE9BC3D8975F0E4F2DA35F723ACAEBF5; v=Ay07lJsrNu1GJdIB_yKjhcdnNcKnimEq67_FMG8yaWsya0I4N9pxLHsO1RD8",
        "X-Requested-With": "com.hexin.plat.android"
    }

    all_holder_list = []

    for page in range(1, pages_to_fetch + 1):
        params = {
            "pom": page,
            "page_size": 20,
            "is_org": 1,
            "cur_tracer_id": "a88198583"
        }

        # 发送GET请求
        response = requests.get(url, headers=headers, params=params)

        # 确保请求成功，状态码为200
        if response.status_code == 200:
            data = response.json()
            holder_list = data["testdata"]["list"]

            for holder in holder_list:
                holder["change_type"] = "增持" if holder["change_type"] == 1 else "减持"
            all_holder_list.extend(holder_list)
        else:
            print(f"请求第 {page} 页失败，状态码: {response.status_code}")
            break

    if all_holder_list:
        df = pd.DataFrame(all_holder_list)
        pprint(df)
        save_to_excel(df, output_file, 'Sheet1')
        print(f"数据已成功保存到 {output_file}")
    else:
        print("没有获取到任何数据")

def save_to_excel(df, file_name, sheet_name):
    if df.empty:
        print("没有获取到任何数据")
        return None

    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        # 获取worksheet对象
        worksheet = writer.sheets[sheet_name]

        # 设置列宽
        for idx, col_name in enumerate(df.columns):
            # 计算列宽
            series = df[col_name]
            max_len = max((
                series.astype(str).map(len).max(),  # 获取字符串的最大长度
                len(str(series.name))  # 获取列名的长度
            )) + 1  # 额外的空白

            # 设置最大最小限制
            adjusted_width = min(max_len, 30)  # 最大宽度为30
            adjusted_width = max(adjusted_width, 8)  # 最小宽度为8

            col_idx = idx + 1  # Excel中的列索引从1开始
            worksheet.column_dimensions[get_column_letter(col_idx)].width = adjusted_width

# 示例调用
fetch_and_save_holder_data_jingxuan("机构-最新股东增减持变动-精选.xlsx", pages_to_fetch=2)
