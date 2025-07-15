import re
from bs4 import BeautifulSoup
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

console = Console()
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

import re
from bs4 import BeautifulSoup
import pandas as pd


def extract_and_merge_data(data, html_content):
    """
    提取策略概要信息 + HTML内容中的结构化股票信息，并合并为一个 DataFrame
    :param data: 接口返回的原始数据字典（用于提取策略概要）
    :param html_content: noteContent 字段的 HTML 内容
    :return: 合并后的 DataFrame
    """
    # 1. 提取策略概要信息
    strategy_summary = {
        # "策略名称": [data['data']['noteTitle'][1:-1]],
        # "策略ID": [data['data']['id']],
        # "作者编号": [data['data']['noteAuthorid']],
        "持仓股票": [', '.join(data['data']['noteStocks'])],
        "策略简介": [data['data']['noteSummary']],
        "发布时间": [pd.to_datetime(data['data']['noteTime'], unit='ms')],
        "更新时间": [pd.to_datetime(data['data']['updateTime'], unit='ms')],
        "创建时间": [pd.to_datetime(data['data']['createTime'], unit='ms')],
        "删除理由": [data['data'].get('deleteReason', '无')],
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

# def parse_note_content(html_content):
#     """解析noteContent字段中的HTML内容"""
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     # 提取纯文本内容
#     text_content = soup.get_text()
#
#     # 提取所有链接
#     links = [a['href'] for a in soup.find_all('a', href=True)]
#
#     # 提取所有图片
#     images = [img['src'] for img in soup.find_all('img', src=True)]
#
#     return {
#         'text_content': text_content,
#         'links': links,
#         'images': images
#     }

# def extract_data(data):
#     """创建并返回多个DataFrame用于展示数据"""
#     # 投顾人信息DataFrame
#     # advisor_df = pd.DataFrame({
#     #     '姓名': [data['data']['bignameDto']['userName']],
#     #     '执业编号': [data['data']['bignameDto']['certCode']],
#     #     '认证标题': [data['data']['bignameDto']['attestationTitle']],
#     #     '擅长领域': [data['data']['bignameDto']['userGoodAt']],
#     #     '关注人数': [data['data']['bignameDto']['userNoticerNums']],
#     #     '作品数量': [data['data']['bignameDto']['userNoteNums']]
#     # })
#
#     # 策略概要信息DataFrame
#     strategy_summary_df = pd.DataFrame({
#         # 标题去掉两边的【】
#         '策略名称': [data['data']['noteTitle'][1:-1]],
#         '策略id': [data['data']['id']],
#         '作者编号': [data['data']['noteAuthorid']],
#         '策略持仓': [data['data']['noteStocks']],
#         '策略简介': [data['data']['noteSummary']],
#         '发布时间': [pd.to_datetime(data['data']['noteTime'], unit='ms')],
#         '更新时间': [pd.to_datetime(data['data']['updateTime'], unit='ms')],
#         '创建时间': [pd.to_datetime(data['data']['createTime'], unit='ms')],
#         '删除理由': [(data['data']['deleteReason'])],
#     })
#     return strategy_summary_df
#
#
#
# # =======================
# # 1. 美化展示 HTML 内容
# # =======================
# def display_note_content(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     # 提取纯文本，并保留段落结构
#     paragraphs = []
#     for p in soup.find_all('p'):
#         text = p.get_text().strip()
#         if text:
#             paragraphs.append(text)
#
#     # 转换为 Markdown 格式显示（支持 rich 格式）
#     md_text = '\n\n'.join(paragraphs)
#     console.print(Markdown(md_text))
#
# # =======================
# # 2. 提取结构化信息
# # =======================
# def extract_note_info(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     full_text = soup.get_text()
#
#     # 提取策略名
#     strategy_name = re.search(r'【(.*?)】', full_text)
#     strategy_name = strategy_name.group(1) if strategy_name else '无'
#
#     # 提取股票名称
#     stock_name = re.search(r'【.*?】.*?(\w+科技)', full_text)
#     stock_name = stock_name.group(1) if stock_name else '无'
#     #         break  # 假设每个文档只有一个目标股票
#
#     # 提取股票代码
#     stock_code = re.search(r'(sh\d{6}|sz\d{6})', full_text)
#     stock_code = stock_code.group(1) if stock_code else '无'
#
#     # 提取买入价格
#     buy_price = re.search(r'参考买入价格：([\d\.\-]+)', full_text)
#     buy_price = buy_price.group(1) if buy_price else '无'
#
#     # 提取仓位
#     position = re.search(r'参考仓位：([\d\%\.]+)', full_text)
#     position = position.group(1) if position else '无'
#
#     # 提取目标价位
#     target_price = re.search(r'参考目标价位：([\d\.\-]+)', full_text)
#     target_price = target_price.group(1) if target_price else '无'
#
#     # 提取止损价位
#     stop_loss = re.search(r'参考止损价位：([\d\.\-]+)', full_text)
#     stop_loss = stop_loss.group(1) if stop_loss else '无'
#
#     # 提取时间
#     report_year = re.search(r'来源：(\d{4}年年报)', full_text)
#     report_year = report_year.group(1) if report_year else '无'
#
#     # 提取操作建议
#     operation = re.search(r'技术面：(.*?)(?=\n|$)', full_text)
#     operation = operation.group(1) if operation else '无'
#
#     strategy_info = [{
#         "策略名": strategy_name,
#         "股票名称": stock_name,
#         "股票代码": stock_code,
#         "参考买入价": buy_price,
#         "参考仓位": position,
#         "目标价位": target_price,
#         "止损价位": stop_loss,
#         "时间": report_year,
#         "操作建议": operation
#     }]
#     strategy_df = pd.DataFrame(strategy_info)
#     return strategy_df


if __name__ == '__main__':
    # 示例调用
    result = get_note_detail()  # 获取接口数据
    note_content = result['data']['noteContent']  # 提取 noteContent 字段
    pprint(result)

    # 调用新函数
    merged_df = extract_and_merge_data(result, note_content)
    merged_df.to_csv('大决策投顾策略详情.csv', index=False)

    # 打印结果
    print("=== 合并后的 DataFrame ===")
    print(merged_df.to_string(index=False))

#     result = get_note_detail()
#     pprint(result)
#     stock_df = extract_data(result)
#     print(stock_df)
#     note_content = result['data']['noteContent']
#     # note_content = '<p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">【朱雀15号】 <a href="qcyzt://productdetails?code=sh603082">sh603082</a> <a href="qcyzt://productdetails?code=sh603082">北自科技</a></span></p><p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考买入价格：38.60-38.80</span></p><p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考仓位：10%</span></p><p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考目标价位：41.00-42.00</span></p><p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考止损价位：35.80-35.9</span></p><p style="text-indent: 2em;">公司主要从事智能物流系统和装备的研发、设计、制造与集成业务。公司提供的智能物流系统能够提高空间利用率和作业效率，降低占地面积、劳动强度和储运损耗，实现物流过程的数智化管理。从使用场景区分，智能物流系统可分为智能仓储物流系统和智能生产物流系统；从系统构成区分，智能物流系统可分为智能物流装备与智能物流软件。除智能物流系统外，公司存在少量销售智能物流装备以及提供运维及其他服务的情况。<br/>（1）智能仓储物流系统<br/>　　公司的智能仓储物流系统主要产品形态为企业的原材料库、成品库和物流配送中心等，应用于仓储环节物料储量大、流量高和品种多的行业，可实现货物出入库、仓储、配送、盘点等过程的自动化、数字化和智能化，具有通用性强、覆盖面广的特点。<br/>　　凭借50余年的技术发展与积淀，公司的智能仓储物流系统已广泛应用于化纤玻纤、食品饮料、家居家电、机械电子和医药等行业，系统采用标准化和模块化设计方法，融合<a href="qcyzt://productdetails?code=sz300024">机器人</a>、机器视觉、智能控制算法等先进技术，为客户提供自动化立体仓库、输送分拣、自动拆码垛等装备及其控制和软件系统，以满足不同客户的定制化需求。<br/>　　公司典型的智能仓储物流系统如所示：<br/>　　（2）智能生产物流系统<br/>　　公司的智能生产物流系统以包含线边库、周转库和复杂输送单元为主要特征，应用于生产过程中存在多品种小批量物料周转、仓储需求的行业，将物流系统与生产工艺相结合，可实现生产过程各环节物流活动的自动化、数字化和智能化，具有工艺复杂、专业性强的特点。<br/>　　基于对智能制造的深入理解，在多年智能仓储物流系统实践经验基础上，为满足客户持续增长的生产过程物料快速周转、准确配送和智能化管控需求，公司逐步拓展了智能生产物流系统业务。针对不同行业特点，公司将生产工艺、物流装备和软件信息系统紧密结合，自主开发了一系列掌握核心技术的细分行业智能生产物流系统解决方案，目前在以化纤、玻纤为代表的纤维制造领域得到广泛应用。<br/>　　公司典型的化纤长丝智能生产物流系统如所示：<br/>　　（3）智能物流装备<br/>　　公司提供的智能物流系统由多种智能物流装备构成，并可根据不同应用场景、客户需求及项目特点提供个性化定制方案。智能仓储物流系统通常包含立体货架、堆垛机、输送机、穿梭车、EMS系统、分拣系统、AGV等通用物流装备，智能生产物流系统除通用物流装备外还包括根据项目需要提供的定制堆垛机、定制输送机、<a href="qcyzt://productdetails?code=sz300024">机器人</a>工作站、全自动落丝机和龙门码垛机等专用物流装备。<br/>　　公司作为国内知名的智能物流系统解决方案供应商，在智能物流装备方面聚焦于控制系统的开发。公司以一体化设计理念自主开发的电气控制系统和物流软件经过长期迭代优化，有着匹配度高、管控准确的特点，能够实现物流装备精准、高效地运行与调度，且可根据客户需求变化及时对功能和流程进行优化，保证物流作业的连续性和装备作业效率的最大化。<br/>　　（4）智能物流软件<br/>　　公司团队深耕物流领域50余年，在我国第一座自动化立体仓库中负责了控制系统和管理软件的研发，多年来完成了众多智能仓储物流系统集成项目，形成了面向多个行业的知识库、工艺库、专家库和标准库，自主开发了WMS、WCS、InteiTwin数字孪生工业软件等多种软件系统，可根据不同行业用户的个性化需求开发软件系统，形成定制化解决方案。公司软件开发团队人员稳定，相关软件系统经过多年技术积累和迭代，具有较高的成熟度，拥有自主知识产权，确保智能物流系统安全、可靠、准确和高效运行。</p><p style="text-indent: 2em;">风险提示：产品及服务销售不及预期，市场波动超预期</p><p style="text-indent: 2em;">来源：2024年年报</p><p style="text-indent: 2em;">技术面：走势上上，股价近期回调，在前期低点附近开始止跌企稳，短期股价有望在此构建双底结构，同时KDJ指标出现低位金叉。</p><p style="text-indent: 2em;"><img src="https://file.djc8888.com/image/2025-06-11/a9c1a9991c33f612a9c1a9991c33f612.png" title="image.png" alt="" style="height:791px,width:1174px" width="1174" height="791"/></p><p style="white-space: normal; text-indent: 2em;">风险提示：<br/></p><p style="white-space: normal; text-indent: 2em;">1、大盘出现超预期波动。<br/></p><p style="white-space: normal; text-indent: 2em;">2、国际局势出现巨大变化。<br/></p><p style="white-space: normal; text-indent: 2em;">3、市场风格出现大幅变化。<br/></p><p style="white-space: normal; text-indent: 2em;">4、公司出现不可抗力的变故。<br/></p><pre style="margin-top: 0px; margin-bottom: 0px; padding: 0px; background-color: rgb(255, 255, 255); font-variant-numeric: normal; font-variant-east-asian: normal; line-height: 20px; white-space: pre-wrap; overflow-wrap: break-word; color: rgb(80, 80, 80); font-size: 15px; widows: 1;"><p><br/></p></pre><p style="text-indent: 2em;"><br/></p><p style="text-indent: 2em;"><br/></p>'
#     # 展示美化后的内容
#     print("=== 美化后的内容展示 ===")
#     display_note_content(note_content)
#
#     # 提取结构化信息
#     print("\n=== 提取的结构化信息 ===")
#     structured_data = extract_note_info(note_content)
#     df = pd.DataFrame(structured_data)
#
#     # 设置显示选项以避免省略内容
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.width', 1000)
#     pd.set_option('display.colheader_justify', 'center')
#
#     # 打印 DataFrame
#     print("=== 提取的结构化信息 ===")
#     print(df.to_string(index=False))

    # 合并两个 DataFrame（按行）
    # combined_df = pd.concat([stock_df.reset_index(drop=True), df.reset_index(drop=True)], axis=1)
    # print("=== 合并后的 DataFrame ===")
    # print(combined_df.to_string(index=False))

