from pprint import pprint

import pandas as pd
import requests


def get_advisor_ranking():
    """获取顾问操作排行榜数据"""
    # 请求URL
    url = "https://api.djc8888.com/api/v2/divineStock/list"

    # URL参数
    params = {
        "deviceToken": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "sign": "5DEB8E5350228963DA5F900269F46B30",
        "timestamp": "1752406993039",
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
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "api.djc8888.com",
        "Cookie": '$Version="1"; acw_tc="0a47329d17524068135554445e0057a28f6f65d5e3cc0364bbc2cf834a58ca";$Path="/";$Domain="api.djc8888.com"'
    }

    try:
        # 发送GET请求
        response = requests.get(
            url,
            params=params,
            headers=headers,
            verify=True  # 生产环境建议保持True，验证SSL证书
        )
        # 检查响应状态码
        response.raise_for_status()
        # 返回JSON格式数据
        response_json = response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        print(f"请求顾问操作排行榜失败: {e}")
        return None
def parse_ranking_data(data):
    """解析排行榜数据，提取关键信息"""
    parsed_data = []

    for item in data:
        advisor_info = item['bignameDto']
        note_comments = item['noteComments']

        # 提取投顾人基本信息
        advisor_base_info = {
            '姓名': advisor_info['userName'],
            '编号id': advisor_info['userid'],
            '编号': advisor_info['userNoteNums'],
            '编号1': advisor_info['userNoticerNums'],
            '写编号': advisor_info['userWriteNums'],
            '执业编号': advisor_info['certCode'],
            '认证标题': advisor_info['attestationTitle'],
            '擅长领域': advisor_info['userGoodAt'],
            '关注人数': int(advisor_info['userNoticerNums']),
            '作品数量': int(advisor_info['userNoteNums']),
            '用户简介': advisor_info['userProfiles']
        }

        # 提取股票操作信息
        stock_info = {
            '股票代码': item['stockCode'],
            '股票名称': item['stockName'],
            '买入价格': float(item['buyPrice']),
            '卖出价格': float(item['sellPrice']),
            '涨幅百分比': float(item['increase']),
            '推荐内容': item['recommendedContent'],
            '笔记ID': item['noteId']
        }

        # 计算平均评分
        if note_comments:
            avg_score = sum(int(comment['bestNum']) for comment in note_comments) / len(note_comments)
        else:
            avg_score = 0

        # 组合最终数据
        combined_info = {
            **advisor_base_info,
            **stock_info,
            '平均评分': round(avg_score, 2),
            '评论数量': len(note_comments)
        }

        parsed_data.append(combined_info)

    return parsed_data

def create_ranking_dataframe(data):
    """创建并返回排名DataFrame"""
    parsed_data = parse_ranking_data(data)
    df = pd.DataFrame(parsed_data)
    df.to_csv('顾问排名.csv', index=False)

    # 设置显示格式
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.float_format', '{:.2f}'.format)

    return df

if __name__ == "__main__":
    ranking_data = get_advisor_ranking()
    pprint(ranking_data)

    if ranking_data and 'data' in ranking_data:
        print("请求成功，处理顾问操作排行榜数据:")
        df_ranking = create_ranking_dataframe(ranking_data['data'])
        df_ranking.to_csv('advisor_ranking.csv', index=False)

        # 打印完整排名表格
        print("\n顾问操作排行榜:")
        print(df_ranking)

        # 按涨幅排序并打印前5名
        top_performers = df_ranking.sort_values('涨幅百分比', ascending=False).head(5)
        print("\n表现最佳的前5位顾问:")
        print(top_performers[['姓名', '股票名称', '涨幅百分比', '平均评分', '评论数量']])

        # 按关注人数排序并打印前5名
        most_popular = df_ranking.sort_values('关注人数', ascending=False).head(5)
        print("\n最受关注的前5位顾问:")
        print(most_popular[['姓名', '关注人数', '作品数量', '涨幅百分比']])
    else:
        print("未能获取到有效的排行榜数据")
