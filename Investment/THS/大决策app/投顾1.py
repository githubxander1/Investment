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


from bs4 import BeautifulSoup
import re
import pandas as pd



def extract_stock_analysis(html_content):
    print(f"开始解析 noteContent...")

    if not html_content or not isinstance(html_content, str):
        print("❌ 输入内容为空或非字符串")
        return None

    soup = BeautifulSoup(html_content, 'lxml')
    print("✅ HTML 已解析为 soup 对象")

    # ✅ 使用更宽容的正则来匹配 style 属性中的 color: rgb(...)
    title_span = soup.find('span', style=re.compile(r'color\s*:\s*rgb$$[^)]+$$', re.IGNORECASE))

    if not title_span:
        print("❌ 未找到带有 color: rgb(...) 的 span 标签")
        return None
    else:
        print("✅ 找到标题 span:", title_span.text)

    combination_name_match = re.search(r'【(.+?)】', title_span.text)
    combination_name = combination_name_match.group(1) if combination_name_match else '未知组合'
    print("🔍 提取到策略标题:", combination_name)

    stock_links = title_span.find_all('a', href=re.compile(r'productdetails\?code='))
    stock_code = stock_links[0].get_text().strip() if len(stock_links) >= 1 else '无'
    stock_name = stock_links[1].get_text().strip() if len(stock_links) >= 2 else '无'
    print(f"✅ 提取到股票：{stock_code} {stock_name}")

    # 后续提取逻辑保持不变...
    # 提取参考信息
    # def get_value_by_label(label_text):
    #     label_tag = soup.find(lambda tag: tag.name == 'span' and label_text in tag.text)
    #     if label_tag:
    #         return label_tag.text.replace(label_text, '').strip().replace("：", "").strip()
    #     return '无'
    #
    # buy_price = get_value_by_label('参考买入价格')
    # position = get_value_by_label('参考仓位')
    # target_price = get_value_by_label('参考目标价位')
    # stop_loss = get_value_by_label('参考止损价位')
    #
    # # 提取公司业务介绍（第一个 p 段落）
    # business_intro = ''
    # for p in soup.find_all('p'):
    #     text = p.get_text().strip()
    #     if len(text) > 50:
    #         business_intro = text
    #         break
    #
    # # 提取技术面分析
    # technical_analysis = ''
    # tech_section = soup.find(lambda tag: tag.name == 'p' and '技术面' in tag.text)
    # if tech_section:
    #     next_p = tech_section.find_next('p')
    #     if next_p:
    #         technical_analysis = next_p.get_text().strip()
    #
    # # 提取风险提示
    # risk_warnings = []
    # risk_section = soup.find(lambda tag: tag.name == 'p' and '风险提示' in tag.text)
    # if risk_section:
    #     for li in risk_section.find_next_siblings('p'):
    #         txt = li.get_text().strip()
    #         if len(txt) > 5:
    #             risk_warnings.append(txt)
    #             if len(risk_warnings) >= 4:
    #                 break
    #
    # result = {
    #     '策略标题': combination_name,
    #     '股票代码': stock_code,
    #     '股票名称': stock_name,
    #     '买入价格区间': buy_price,
    #     '建议仓位': position,
    #     '目标价区间': target_price,
    #     '止损价区间': stop_loss,
    #     '公司业务介绍': business_intro,
    #     '技术面分析': technical_analysis,
    #     '风险提示': '; '.join(risk_warnings),
    # }
    #
    # return result



# 主程序
if __name__ == "__main__":
    # result = get_note_detail()
    # if result:
    #     print("请求成功，返回数据:")
    #     # pprint(result)
    #     note_content = result['data']['noteContent']
    #     # note_content = result['data']
    #     print(note_content)
        note_content = '<p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">【朱雀15号】 <a href="qcyzt://productdetails?code=sh603082">sh603082</a> <a href="qcyzt://productdetails?code=sh603082">北自科技</a></span></p><p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考买入价格：38.60-38.80</span></p><p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考仓位：10%</span></p><p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考目标价位：41.00-42.00</span></p><p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考止损价位：35.80-35.9</span></p><p style="text-indent: 2em;">公司主要从事智能物流系统和装备的研发、设计、制造与集成业务。公司提供的智能物流系统能够提高空间利用率和作业效率，降低占地面积、劳动强度和储运损耗，实现物流过程的数智化管理。从使用场景区分，智能物流系统可分为智能仓储物流系统和智能生产物流系统；从系统构成区分，智能物流系统可分为智能物流装备与智能物流软件。除智能物流系统外，公司存在少量销售智能物流装备以及提供运维及其他服务的情况。<br/>（1）智能仓储物流系统<br/>　　公司的智能仓储物流系统主要产品形态为企业的原材料库、成品库和物流配送中心等，应用于仓储环节物料储量大、流量高和品种多的行业，可实现货物出入库、仓储、配送、盘点等过程的自动化、数字化和智能化，具有通用性强、覆盖面广的特点。<br/>　　凭借50余年的技术发展与积淀，公司的智能仓储物流系统已广泛应用于化纤玻纤、食品饮料、家居家电、机械电子和医药等行业，系统采用标准化和模块化设计方法，融合<a href="qcyzt://productdetails?code=sz300024">机器人</a>、机器视觉、智能控制算法等先进技术，为客户提供自动化立体仓库、输送分拣、自动拆码垛等装备及其控制和软件系统，以满足不同客户的定制化需求。<br/>　　公司典型的智能仓储物流系统如所示：<br/>　　（2）智能生产物流系统<br/>　　公司的智能生产物流系统以包含线边库、周转库和复杂输送单元为主要特征，应用于生产过程中存在多品种小批量物料周转、仓储需求的行业，将物流系统与生产工艺相结合，可实现生产过程各环节物流活动的自动化、数字化和智能化，具有工艺复杂、专业性强的特点。<br/>　　基于对智能制造的深入理解，在多年智能仓储物流系统实践经验基础上，为满足客户持续增长的生产过程物料快速周转、准确配送和智能化管控需求，公司逐步拓展了智能生产物流系统业务。针对不同行业特点，公司将生产工艺、物流装备和软件信息系统紧密结合，自主开发了一系列掌握核心技术的细分行业智能生产物流系统解决方案，目前在以化纤、玻纤为代表的纤维制造领域得到广泛应用。<br/>　　公司典型的化纤长丝智能生产物流系统如所示：<br/>　　（3）智能物流装备<br/>　　公司提供的智能物流系统由多种智能物流装备构成，并可根据不同应用场景、客户需求及项目特点提供个性化定制方案。智能仓储物流系统通常包含立体货架、堆垛机、输送机、穿梭车、EMS系统、分拣系统、AGV等通用物流装备，智能生产物流系统除通用物流装备外还包括根据项目需要提供的定制堆垛机、定制输送机、<a href="qcyzt://productdetails?code=sz300024">机器人</a>工作站、全自动落丝机和龙门码垛机等专用物流装备。<br/>　　公司作为国内知名的智能物流系统解决方案供应商，在智能物流装备方面聚焦于控制系统的开发。公司以一体化设计理念自主开发的电气控制系统和物流软件经过长期迭代优化，有着匹配度高、管控准确的特点，能够实现物流装备精准、高效地运行与调度，且可根据客户需求变化及时对功能和流程进行优化，保证物流作业的连续性和装备作业效率的最大化。<br/>　　（4）智能物流软件<br/>　　公司团队深耕物流领域50余年，在我国第一座自动化立体仓库中负责了控制系统和管理软件的研发，多年来完成了众多智能仓储物流系统集成项目，形成了面向多个行业的知识库、工艺库、专家库和标准库，自主开发了WMS、WCS、InteiTwin数字孪生工业软件等多种软件系统，可根据不同行业用户的个性化需求开发软件系统，形成定制化解决方案。公司软件开发团队人员稳定，相关软件系统经过多年技术积累和迭代，具有较高的成熟度，拥有自主知识产权，确保智能物流系统安全、可靠、准确和高效运行。</p><p style="text-indent: 2em;">风险提示：产品及服务销售不及预期，市场波动超预期</p><p style="text-indent: 2em;">来源：2024年年报</p><p style="text-indent: 2em;">技术面：走势上上，股价近期回调，在前期低点附近开始止跌企稳，短期股价有望在此构建双底结构，同时KDJ指标出现低位金叉。</p><p style="text-indent: 2em;"><img src="https://file.djc8888.com/image/2025-06-11/a9c1a9991c33f612a9c1a9991c33f612.png" title="image.png" alt="" style="height:791px,width:1174px" width="1174" height="791"/></p><p style="white-space: normal; text-indent: 2em;">风险提示：<br/></p><p style="white-space: normal; text-indent: 2em;">1、大盘出现超预期波动。<br/></p><p style="white-space: normal; text-indent: 2em;">2、国际局势出现巨大变化。<br/></p><p style="white-space: normal; text-indent: 2em;">3、市场风格出现大幅变化。<br/></p><p style="white-space: normal; text-indent: 2em;">4、公司出现不可抗力的变故。<br/></p><pre style="margin-top: 0px; margin-bottom: 0px; padding: 0px; background-color: rgb(255, 255, 255); font-variant-numeric: normal; font-variant-east-asian: normal; line-height: 20px; white-space: pre-wrap; overflow-wrap: break-word; color: rgb(80, 80, 80); font-size: 15px; widows: 1;"><p><br/></p></pre><p style="text-indent: 2em;"><br/></p><p style="text-indent: 2em;"><br/></p>'

        analysis = extract_stock_analysis(note_content)
        print(analysis)

        if analysis:
            df = pd.DataFrame([analysis])
            print(df.to_string(index=False))

        # 创建DataFrames
        # dfs = create_dataframe(r)
        # # print(dfs)
        #
        # # 打印各个DataFrame
        # # print("\n投顾人信息:")
        # # print(dfs['advisor_df'])
        #
        # print("\n策略概要:")
        # print(dfs['strategy_summary_df'])
        #
        # print("\n股票相关信息:")
        # print(dfs['stock_df'])
        #
        # print("\n基本面分析:")
        # print(dfs['fundamentals_df'])
        #
        # print("\n技术面分析:")
        # print(dfs['technical_df'])
        #
        # print("\n风险提示:")
        # print(dfs['risk_df'])
