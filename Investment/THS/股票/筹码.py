from pprint import pprint
import pandas as pd
import requests

# 筹码形态映射字典
SHAPE_MAPPING = {
    1: "低位锁定(主力拉伸)",
    2: "低位密集(主力建仓)",
    3: "双峰形态(高抛低吸)",
    4: "高位密集(谨慎入场)"
}

def get_api_data(shape_type=2, sort_field="closing_profit", sort_order="desc",
                 page_size=5, date="2025-03-13"):
    """获取筹码数据API"""
    url = "https://dq.10jqka.com.cn/fuyao/chip_shape_stock_selection/selection/v1/list"
    params = {
        "offset_num": 0,
        "page_size": page_size,
        "shape_type": shape_type,
        "chip_type": 1,  # 固定为机构筹码
        "sort_field": sort_field,
        "sort_order": sort_order,
        "filter_selfstock": 0,
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
        response.raise_for_status()
        return response.json(), SHAPE_MAPPING.get(shape_type, f"未知形态{shape_type}")
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None, None

def extract_result(data):
    """从API响应中提取关键数据"""
    if not data or data.get('status_code') != 0:
        return []

    result_list = data.get("data", {}).get("list", [])
    extracted_data = []

    for item in result_list:
        stock_info = item.get('stock', {})

        # 处理可能为None的字段
        price = item.get('price') or 0
        increase = item.get('increase') or 0

        extracted_data.append({
            '股票代码': stock_info.get('code', ''),
            '股票名称': stock_info.get('name', ''),
            '平均成本': item.get('average_cost', 0),
            '收盘收益': item.get('closing_profit', 0),
            '涨跌幅': increase,
            '90%集中度': item.get('ninty_quantile_concentration', 0),
            '收盘价': price,
            '筹码形态': item.get('shape_type', 0)
        })

    return extracted_data

def get_all_shape_data(sort_field="closing_profit"):
    """获取所有筹码形态的数据"""
    all_data = {}

    for shape_type in SHAPE_MAPPING.keys():
        print(f"正在获取 {SHAPE_MAPPING[shape_type]} 数据...")
        api_data, shape_name = get_api_data(shape_type=shape_type, sort_field=sort_field)
        pprint(api_data)

        if api_data and shape_name:
            extracted = extract_result(api_data)
            if extracted:
                all_data[shape_name] = pd.DataFrame(extracted)
                print(f"  ✓ 获取到 {len(extracted)} 条记录")
            else:
                print(f"  ⚠️ 未提取到有效数据")
        else:
            print(f"  ❌ 请求失败")

    return all_data

def save_to_excel(data_dict, filename="筹码数据.xlsx"):
    """将不同形态的数据保存到Excel的不同工作表中"""
    if not data_dict:
        print("没有数据可保存")
        return

    # 映射API字段到中文列名
    column_mapping = {
        "increase": "涨跌幅",
        "closing_profit": "收盘收益",
        "average_cost": "平均成本",
        "ninty_quantile_concentration": "90%集中度",
        "price": "收盘价"
    }

    # 获取实际要排序的中文列名
    sort_column = column_mapping.get(sort_field_api, "收盘收益")

    with pd.ExcelWriter(filename) as writer:
        for shape_name, df in data_dict.items():
            # 简化工作表名称（Excel工作表名称限制为31字符）
            sheet_name = shape_name[:20] + "..." if len(shape_name) > 20 else shape_name

            # 按用户选择的排序字段排序
            if sort_column in df.columns:
                ascending = False if sort_field_api != "average_cost" else True
                df = df.sort_values(by=sort_column, ascending=ascending)

            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"\n所有数据已保存至: {filename}")

if __name__ == "__main__":
    # 用户可在此处自定义排序字段
    sort_field = input("请选择排序字段 (1.涨跌幅 2.收盘收益 3.平均成本 4.90%集中度 5.收盘价): ").strip()

    # 映射用户输入到API字段
    sort_mapping = {
        "1": "increase",
        "2": "closing_profit",
        "3": "average_cost",
        "4": "ninty_quantile_concentration",
        "5": "price"
    }

    # 默认按收盘收益排序
    sort_field_api = sort_mapping.get(sort_field, "closing_profit")
    print(f"使用排序字段: {sort_field_api}")

    # 获取所有筹码形态数据
    all_data = get_all_shape_data(sort_field=sort_field_api)
    print(all_data)

    # 保存到Excel
    if all_data:
        save_to_excel(all_data)
    else:
        print("未获取到任何有效数据")