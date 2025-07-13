from pprint import pprint
import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_note_detail():
    # 请求URL
    url = "https://api.djc8888.com/api/v2/note/detail"

    # URL参数
    params = {
        "deviceToken": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "noteid": "105369",#103484
        "sign": "68C40E285D209B6F4A125CAE231ABE5E",
        "timestamp": "1752406433935",
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
        "Cookie": '$Version="1"; acw_tc="0a47318c17524062790473918e0064f2c7a11858ca2f80f4ea3ecc4b2cae36";$Path="/";$Domain="api.djc8888.com"'
    }

    try:
        # 发送GET请求
        response = requests.get(url, params=params, headers=headers, verify=True)
        # 检查响应状态码
        response.raise_for_status()
        # 返回响应的JSON数据
        response_json = response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None

def parse_note_content(html_content):
    """解析noteContent字段中的HTML内容"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取纯文本内容
    text_content = soup.get_text()

    # 提取所有链接
    links = [a['href'] for a in soup.find_all('a', href=True)]

    # 提取所有图片
    images = [img['src'] for img in soup.find_all('img', src=True)]

    return {
        'text_content': text_content,
        'links': links,
        'images': images
    }

def extract_stock_info(soup):
    """从解析的HTML中提取股票相关信息"""
    stock_data = {
        '参考买入价格': None,
        '参考仓位': None,
        '参考目标价位': None,
        '参考止损价位': None
    }

    # 查找包含特定关键词的段落
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text.startswith('参考买入价格：'):
            stock_data['参考买入价格'] = text.split('：')[-1]
        elif text.startswith('参考仓位：'):
            stock_data['参考仓位'] = text.split('：')[-1]
        elif text.startswith('参考目标价位：'):
            stock_data['参考目标价位'] = text.split('：')[-1]
        elif text.startswith('参考止损价位：'):
            stock_data['参考止损价位'] = text.split('：')[-1]

    return stock_data

def extract_fundamentals(soup):
    """提取基本面分析内容"""
    fundamentals = {}
    current_key = None

    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text.startswith('一、基本面') or text.startswith('二、技术面'):
            break  # 停止当进入技术面部分

        if text.startswith('【') or text.startswith('strong>'):
            current_key = text
            fundamentals[current_key] = []
        elif current_key and text:
            fundamentals[current_key].append(text)

    return fundamentals

def extract_technical_analysis(soup):
    """提取技术面分析内容"""
    technical_analysis = {}
    current_key = None

    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text.startswith('二、技术面'):
            current_key = '技术面分析'
            technical_analysis[current_key] = []
        elif current_key and text:
            technical_analysis[current_key].append(text)

    return technical_analysis

def extract_risk_warnings(soup):
    """提取风险提示内容"""
    risk_warnings = []

    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text.startswith('风险提示：'):
            risk_warnings.extend(text.split('；'))

    return risk_warnings

def create_dataframe(data):
    """创建并返回多个DataFrame用于展示数据"""
    # 投顾人信息DataFrame
    advisor_df = pd.DataFrame({
        '姓名': [data['data']['bignameDto']['userName']],
        '执业编号': [data['data']['bignameDto']['certCode']],
        '认证标题': [data['data']['bignameDto']['attestationTitle']],
        '擅长领域': [data['data']['bignameDto']['userGoodAt']],
        '关注人数': [data['data']['bignameDto']['userNoticerNums']],
        '作品数量': [data['data']['bignameDto']['userNoteNums']]
    })

    # 策略概要信息DataFrame
    strategy_summary_df = pd.DataFrame({
        '策略标题': [data['data']['noteTitle']],
        '发布时间': [pd.to_datetime(data['data']['noteTime'], unit='ms')],
        '更新时间': [pd.to_datetime(data['data']['updateTime'], unit='ms')],
        '阅读人数': [data['data']['readerNums']],
        '评论数': [data['data']['commentNum']],
        '点赞数': [data['data']['satisfiedNums']]
    })

    # 解析noteContent
    html_content = data['data']['noteContent']
    soup = BeautifulSoup(html_content, 'html.parser')

    # 股票相关信息DataFrame
    stock_info = extract_stock_info(soup)
    stock_df = pd.DataFrame([stock_info])

    # 基本面分析DataFrame
    fundamentals = extract_fundamentals(soup)
    fundamentals_df = pd.DataFrame(fundamentals)

    # 技术面分析DataFrame
    technical_analysis = extract_technical_analysis(soup)
    technical_df = pd.DataFrame(technical_analysis)

    # 风险提示DataFrame
    risk_warnings = extract_risk_warnings(soup)
    risk_df = pd.DataFrame(risk_warnings, columns=['风险提示'])

    return {
        'advisor_df': advisor_df,
        'strategy_summary_df': strategy_summary_df,
        'stock_df': stock_df,
        'fundamentals_df': fundamentals_df,
        'technical_df': technical_df,
        'risk_df': risk_df
    }

# 主程序
if __name__ == "__main__":
    result = get_note_detail()
    if result:
        print("请求成功，返回数据:")
        pprint(result)

        # 创建DataFrames
        dfs = create_dataframe(result)

        # 打印各个DataFrame
        print("\n投顾人信息:")
        print(dfs['advisor_df'])

        print("\n策略概要:")
        print(dfs['strategy_summary_df'])

        print("\n股票相关信息:")
        print(dfs['stock_df'])

        print("\n基本面分析:")
        print(dfs['fundamentals_df'])

        print("\n技术面分析:")
        print(dfs['technical_df'])

        print("\n风险提示:")
        print(dfs['risk_df'])
