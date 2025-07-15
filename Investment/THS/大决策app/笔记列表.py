import re
from pprint import pprint

import pandas as pd
import requests
import json

from bs4 import BeautifulSoup


def get_dk_note_list():
    """获取笔记列表数据（POST请求）"""
    # 请求URL
    url = "https://api.djc8888.com/api/v2/note/dkNoteList"

    # URL参数（拼接在URL后）
    params = {
        "deviceToken": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "sign": "7AEDEA4301F744578BC7670E1435A340",
        "timestamp": "1752409144225",
        "version": "3.7.12",
        "versionCode": "3071200",
        "deviceId": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "platform": "android"
    }

    # 请求头
    headers = {
        "mobileInfo": "Android 29 xiaomi Redmi Note 7 Pro",
        "vendingPackageName": "com.mi.djc",
        "Accept": "application/json; charset=UTF-8",
        "Connection": "Keep-Alive",
        "User-Agent": "android/10 com.djc.qcyzt/3.7.12",
        "Charset": "UTF-8",
        "Accept-Encoding": "gzip",
        "packageName": "com.djc.qcyzt",
        "deviceId": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "version": "3.7.12",
        "versionCode": "3071200",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "api.djc8888.com",
        "Cookie": '$Version="1"; acw_tc="0aef815717524091047248391e00660ff0d8b48847fdc9e4cc5af9c93fc559";$Path="/";$Domain="api.djc8888.com"'
    }

    # 请求体（JSON数据）
    payload = {
        "list_type": "4",
        "pageNo": "1",
        "sign": "教学",
        "pageSize": "1",
        "noteAuthorid": "22",
        "note_type": "1,3,5,6"
    }

    try:
        # 发送POST请求，JSON参数通过json参数传递（自动处理Content-Type）
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=payload,  # 自动序列化并设置Content-Type为application/json
            verify=True
        )
        response.raise_for_status()  # 检查HTTP状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求笔记列表失败: {e}")
        return None
def extract_and_merge_data(data,html_content):
    """
    提取策略概要信息 + HTML内容中的结构化股票信息，并合并为一个 DataFrame
    :param data: 接口返回的原始数据字典（用于提取策略概要）
    :param html_content: noteContent 字段的 HTML 内容
    :return: 合并后的 DataFrame
    """
    # 1. 提取策略概要信息
    strategy_summary = {
        # "策略名称": [data.get('data']['noteTitle'][1:-1]],
        # "策略ID": [data.get('data']['id']],
        # "作者编号": [data.get('data']['noteAuthorid']],
        # "持仓股票": [', '.join(data.get('noteStocks'])],
        "策略简介": data.get('noteSummary', '无'),
        "发布时间": pd.to_datetime(data.get('noteTime', 0), unit='ms') if data.get('noteTime') else pd.NaT,
        "更新时间": pd.to_datetime(data.get('updateTime', 0), unit='ms') if data.get('updateTime') else pd.NaT,
        "创建时间": pd.to_datetime(data.get('createTime', 0), unit='ms') if data.get('createTime') else pd.NaT,
        # "删除理由": [data.get('deleteReason', '无')],
    }
    strategy_df = pd.DataFrame(strategy_summary)

    # 2. 提取结构化信息 from HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    full_text = soup.get_text()

    # 正则提取关键字段
    strategy_name = re.search(r'【(.*?)】', full_text)
    # stock_name = re.search(r'【.*?】.*?(\w+科技)', full_text)
    stock_name = [m.group(1) for m in re.finditer(r'【.*?】.*?(\w+科技)', full_text)]

    stock_code = re.search(r'(sh\d{6}|sz\d{6})', full_text)
    buy_price = re.search(r'参考买入价格：([\d\.\-]+)', full_text)
    position = re.search(r'参考仓位：([\d\%\.]+)', full_text)
    target_price = re.search(r'参考目标价位：([\d\.\-]+)', full_text)
    stop_loss = re.search(r'参考止损价位：([\d\.\-]+)', full_text)
    report_year = re.search(r'来源：(\d{4}年年报)', full_text)
    operation = re.search(r'技术面：(.*?)(?=\n|$)', full_text)

    structured_info = [{
        "策略名称": strategy_name.group(1) if strategy_name else '无',
        # "股票名称": stock_name.group(1) if stock_name else '无',
        "股票名称": stock_name if stock_name else '无',
        "股票代码": stock_code.group(1) if stock_code else '无',
        "参考买入价": buy_price.group(1) if buy_price else '无',
        "参考仓位": position.group(1) if position else '无',
        "目标价位": target_price.group(1) if target_price else '无',
        "止损价位": stop_loss.group(1) if stop_loss else '无',
        "报告年份": report_year.group(1) if report_year else '无',
        "操作建议": operation.group(1) if operation else '无'
    }]
    info_df = pd.DataFrame(structured_info)

    # 3. 合并两个 DataFrame
    merged_df = pd.concat([strategy_df.reset_index(drop=True), info_df.reset_index(drop=True)], axis=1)
    merged_df['参考买入价'] = pd.to_numeric(merged_df['参考买入价'].str.split('-').str[0], errors='coerce')
    merged_df['目标价位'] = pd.to_numeric(merged_df['目标价位'].str.split('-').str[0], errors='coerce')

    return merged_df

if __name__ == "__main__":
    note_data = get_dk_note_list()['data']  # 获取笔记数据，是一个 list
    # print("笔记列表数据类型:", type(note_data))  # 应该是 <class 'list'>
    # print("笔记列表长度:", len(note_data))

    if note_data:
        print("笔记列表数据:")
        pprint(note_data)
        for idx, item in enumerate(note_data):
            print(f"--- 第 {idx + 1} 条笔记 ---")
            pprint(item)  # 打印每条笔记内容

            # 提取 noteContent 字段
            note_content = item.get('noteContent', '')
            pprint(note_content)
            merged_df = extract_and_merge_data(note_data, note_content)
            #显示完整的，不省略
            pd.set_option('display.max_columns', None)

            merged_df.to_csv(f'策略列表_{idx + 1}.csv', index=False)
            print(merged_df)


