from pprint import pprint

import pandas as pd
import requests
import json


def get_dk_following_note_list():
    """获取关注的笔记列表数据（POST请求）"""
    # 请求URL
    url = "https://api.djc8888.com/api/v2/note/dkFollowingNoteList"

    # URL参数
    params = {
        "deviceToken": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "sign": "A461AE3D8CEDDF2CE4FF4DBF6CED19EB",
        "timestamp": "1752409312747",
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
        "pageNo": "1",
        "pageSize": "5",
        "noteAuthorid": "22"
    }

    try:
        # 发送POST请求
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=payload,  # 自动处理JSON序列化
            verify=True
        )
        response.raise_for_status()  # 检查响应状态码
        pprint(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求关注的笔记列表失败: {e}")
        return None

def parse_strategy_data(data):
    """解析策略数据，提取关键信息"""
    parsed_data = []

    for item in data:
        note_info = item

        # 提取基础策略信息
        strategy_base_info = {
            '笔记ID': note_info['id'],
            '作者ID': note_info['noteAuthorid'],
            '发布时间': pd.to_datetime(note_info['noteTime'], unit='ms'),
            '更新时间': pd.to_datetime(note_info['updateTime'], unit='ms'),
            '阅读人数': int(note_info['readerNums']),
            '评论数量': int(note_info['commentNum']),
            '点赞数量': int(note_info['satisfiedNums'])
        }

        # 提取关联的原始策略信息
        quote_info = note_info.get('quoteContent', '')
        if not quote_info and 'srcQuote' in note_info:
            src_quote = note_info['srcQuote']
            quote_info = src_quote.get('noteApiDto', {}).get('noteSummary', '')

        # 提取策略内容摘要
        summary = note_info.get('noteSummary', '')
        if not summary and 'srcQuote' in note_info:
            src_quote = note_info['srcQuote']
            summary = src_quote.get('noteApiDto', {}).get('noteSummary', '')

        # 提取股票相关信息
        stock_info = {
            '股票代码': note_info.get('stockCode', ''),
            '策略摘要': summary,
            '关联策略ID': note_info.get('quoteId', None),
            '关联策略类型': note_info.get('quoteType', None)
        }

        # 提取投顾人信息
        bigname_dto = note_info.get('bignameDto', {})
        advisor_info = {
            '投顾姓名': bigname_dto.get('userName', ''),
            '执业编号': bigname_dto.get('certCode', ''),
            '认证标题': bigname_dto.get('attestationTitle', ''),
            '擅长领域': bigname_dto.get('userGoodAt', ''),
            '关注人数': int(bigname_dto.get('userNoticerNums', 0)),
            '作品数量': int(bigname_dto.get('userNoteNums', 0))
        }

        # 组合最终数据
        combined_info = {
            **strategy_base_info,
            **stock_info,
            **advisor_info,
            '策略内容': quote_info
        }

        parsed_data.append(combined_info)

    return parsed_data
def create_strategy_dataframe(data):
    """创建并返回策略DataFrame"""
    parsed_data = parse_strategy_data(data)
    # pprint(parsed_data)
    df = pd.DataFrame(parsed_data)

    # 设置显示格式
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    return df

if __name__ == "__main__":
    strategy_data = get_dk_following_note_list()

    if strategy_data and 'data' in strategy_data:
        print("请求成功，处理策略列表数据:")
        df_strategy = create_strategy_dataframe(strategy_data['data'])
        df_strategy.to_csv('策略列表.csv', index=False)

        # 打印完整策略表格
        print("\n策略列表:")
        print(df_strategy)

        # 按发布时间排序并打印最新策略
        latest_strategies = df_strategy.sort_values('发布时间', ascending=False).head(5)
        print("\n最新的前5个策略:")
        print(latest_strategies[['投顾姓名', '发布时间', '策略摘要', '关联策略ID']])

        # 按阅读量排序并打印最热门策略
        popular_strategies = df_strategy.sort_values('阅读人数', ascending=False).head(5)
        print("\n阅读量最高的前5个策略:")
        print(popular_strategies[['投顾姓名', '股票代码', '阅读人数', '策略摘要']])
    else:
        print("未能获取到有效的策略数据")
