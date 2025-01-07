import logging
from pprint import pprint
import openpyxl
import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_and_save_holder_data(output_file, pages_to_fetch=2):
    """
    从指定 URL 获取股东增减持数据，并保存到 Excel 文件中。

    :param output_file: 输出的 Excel 文件路径
    :param pages_to_fetch: 需要获取的页数
    """
    base_url = "https://kuaicha.10jqka.com.cn/open/ths/v1/holder_yield/change_info"
    headers = {
        "Host": "kuaicha.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "hexin-v": "A7Sij1psb4bX6vtK3CKKXhZYjHkmjdl_Grlsu04VQEfDylujdp2oB2rBPFad",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting=normal getHXAPPAdaptOld534=true; jsessionid-yqapp=EE9BC3D8975F0E4F2DA35F723ACAEBF5; v=A7Sij1psb4bX6vtK3CKKXhZYjHkmjdl_Grlsu04VQEfDylujdp2oB2rBPFad",
        "source": "SDK",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mj34NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_488\",\"userid\":\"641926488\"}; hxmPid=masterholding_news; addGongGeTip533=true; addGongGeTip534=true; jsessionid-yqapp=EE9BC3D8975F0E4F2DA35F723ACAEBF5; v=A7Sij1psb4bX6vtK3CKKXhZYjHkmjdl_Grlsu04VQEfDylujdp2oB2rBPFad",
        "X-Requested-With": "com.hexin.plat.android"
    }

    all_holder_list = []

    for page in range(1, pages_to_fetch + 1):
        url = f"{base_url}?page={page}&page_size=20&raise_fail_type=ALL&cur_tracer_id=5af6696f"
        try:
            response = requests.get(url, headers=headers)
            # 确保请求成功，状态码为200
            if response.status_code == 200:
                data = response.json()
                holder_list = data["data"]["list"]
                all_holder_list.extend(holder_list)
            else:
                logging.error(f"请求失败，状态码: {response.status_code}")
                break
        except Exception as e:
            logging.error(f"解析 JSON 数据时出错: {e}")
            break

    # 转换 change_type 为 更直观的文本
    for holder in all_holder_list:
        holder["change_type"] = "增持" if holder["change_type"] == 1 else "减持"

    # 创建一个映射表，用于将 market 数值转换为中文描述
    market_mapping = {
        -111: "个人",
        17: "主板",
        # 添加其他可能的映射关系
    }

    # 使用映射表将 market 列转换为中文描述
    for holder in all_holder_list:
        holder["market"] = market_mapping.get(holder["market"], "未知")

    pprint(all_holder_list)
    df = pd.DataFrame(all_holder_list)

    # 设置 Excel 文件中各列的宽度
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

        # 获取 workbook 和 worksheet 对象
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # 设置列宽
        for idx, col_name in enumerate(df.columns):
            column_len = max(df[col_name].astype(str).map(len).max(), len(col_name))
            col_idx = idx + 1  # Excel 中的列索引从 1 开始
            worksheet.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = column_len

    print(df)
    logging.info("数据已成功保存到 Excel 文件")

# 示例调用
output_file = "机构-最新股东增减持变动-全部.xlsx"
fetch_and_save_holder_data(output_file, pages_to_fetch=2)
