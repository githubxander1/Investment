from pprint import pprint

import pandas as pd
import requests


def get_api_data(offset_num=0, page_size=20, shape_type=2, chip_type=1,
                  sort_field="closing_profit", sort_order="desc",
                  filter_selfstock=0, date="2025-01-13"):
    url = "https://dq.10jqka.com.cn/fuyao/chip_shape_stock_selection/selection/v1/list"
    params = {
        "offset_num": offset_num,
        "page_size": page_size,
        "shape_type": shape_type,
        "chip_type": chip_type,
        "sort_field": sort_field,
        "sort_order": sort_order,
        "filter_selfstock": filter_selfstock,
        "date": date
    }
    cookies = {
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "user_status": "0",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "user": "MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM2NzMyMzMwOjo6MTY1ODE0Mjc4MDo2MDQ4MDA6MDoxMTcxNGNhNjA4OGM2NGZjNmY0MWVkNGQ5MmEwNTc1MzA6OjA=",
        "ticket": "1c551a19d21c9927ea95c883812c6140",
        "v": "A61oKwbStoh6cVJk9Y0oBFLKvkInCuHcaz5FsO-y6cSzZsK4t1rxrPuOVZJ8",
        "hxmPid": "ths_jeton_show"
    }
    headers = {
        "content-type": "application/json",
        "User-Agent": "okhttp/3.14.9"
    }
    try:
        response = requests.get(url, params=params, cookies=cookies, headers=headers)
        response.raise_for_status()  # 若请求不成功，抛出异常
        return response.json()  # 返回解析后的JSON数据
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


def extract_result(data):
    if data and data['status_code'] == 0:
        result_list = data.get("data", {}).get("list", [])
        extracted_data = []
        for item in result_list:
            stock_info = item.get('stock', {})
            extracted_data.append({
                '股票代码': stock_info.get('code'),
                '股票名称': stock_info.get('name'),
                '平均成本': item.get('average_cost'),
                '收盘收益': item.get('closing_profit'),
                '涨跌幅': item.get('increase')
            })
        return extracted_data
    return []

if __name__ == "__main__":
    api_data = get_api_data()
    pprint(api_data)
    extracted_result = extract_result(api_data)
    if extracted_result:
        df = pd.DataFrame(extracted_result)
        print(df)
        df.to_excel('筹码数据.xlsx', index=False)
    else:
        print("未提取到有效数据")
