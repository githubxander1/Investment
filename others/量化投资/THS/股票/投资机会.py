from pprint import pprint
import pandas as pd
import requests
import openpyxl
from openpyxl.utils import get_column_letter

# 接口的URL，这里日期部分是固定写死的示例中的2024-12-17，你可以根据实际需求动态调整
url = "https://data.hexin.cn/tradetip/trade/day/2024-12-17/"

# 请求头，按照原始请求信息进行设置
headers = {
    "Host": "testdata.hexin.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting/0",
    "Referer": "https://data.hexin.cn/tradetip/index/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "v=A9YRHyHjrcCLZplkbMOIWOCCLofYdxoXbLZOFUA_wtNUHXk9qAdqwTxLni4T"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 判断请求是否成功（状态码为200）
if response.status_code == 200:
    data = response.json()
    # 这里先简单打印出整个返回的JSON数据，你需要根据接口实际返回的数据结构进一步提取投资机会相关的具体信息
    pprint(data)

    # 定义一个函数来处理并保存每个类型的表格
    def save_to_sheet(data_list, sheet_name, writer, columns_mapping):
        if not data_list:
            print(f"{sheet_name} 没有获取到数据")
            return

        df = pd.DataFrame(data_list)
        df.rename(columns=columns_mapping, inplace=True)
        df.fillna(value='', inplace=True)

        print(df)

        df.to_excel(writer, sheet_name=sheet_name, index=False)

        # 获取worksheet对象
        worksheet = writer.sheets[sheet_name]

        # 设置列宽
        for idx, col_name in enumerate(df.columns):
            # 计算列宽
            series = df[col_name]
            max_len = max((
                series.astype(str).map(len).max(),  # 内容的最大长度
                len(str(series.name))  # 列名的长度
            )) + 1  # 额外的空白

            # 设置最大和最小宽度限制
            adjusted_width = min(max_len, 20)  # 最大宽度为20
            adjusted_width = max(adjusted_width, 8)  # 最小宽度为8

            col_idx = idx + 1  # Excel中的列索引从1开始
            worksheet.column_dimensions[get_column_letter(col_idx)].width = adjusted_width

        print(f"数据已成功保存到 {sheet_name} 工作表")
    # 创建ExcelWriter对象
    with pd.ExcelWriter('投资机会.xlsx', engine='openpyxl') as writer:
        # 处理每个类型的表格
        save_to_sheet(data['dzjj']['plan'], '定增计划', writer, {
            'code': '股票代码',
            'name': '股票名称',
            'scale': '规模'
        })

        save_to_sheet(data['fhsz']['testdata'], '分红送股', writer, {
            'bonus': '分红方案',
            'code': '股票代码',
            'name': '股票名称'
        })

        save_to_sheet(data['tfp']['tp'], '停复牌', writer, {
            'code': '股票代码',
            'name': '股票名称',
            'reason': '原因'
        })

        save_to_sheet(data['xgfx']['testdata'], '新股发行', writer, {
            'code': '股票代码',
            'name': '股票名称',
            'limit': '发行数量'
        })

        save_to_sheet(data['yjyg']['testdata'], '业绩预告', writer, {
            'code': '股票代码',
            'name': '股票名称',
            'type': '类型'
        })

else:
    print(f"请求失败，状态码: {response.status_code}")
