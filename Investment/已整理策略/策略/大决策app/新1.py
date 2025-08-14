import datetime
from pprint import pprint

import requests

from Investment.THS.AutoTrade.utils.format_data import determine_market
# from Investment.THS.AutoTrade.utils import logger
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger  = setup_logger(__name__)

def get_portfolio_industry_theme():
    """获取组合行业主题数据（GET请求）"""
    # 请求URL
    url = "https://nkmapiv3.aniu.tv/nkm-api/Rest2/api/INKBPortfolio/getPortfolioIndustryThemeV2"

    # URL参数
    params = {
        "aniu_uid": "3a51f1c06372435cbb79e41609285c1a",
        "get_type": "0",
        "pfId": "132008",
        "pfid": "132008",
        "user_level": "1",
        "channelid": "700015",
        "clienttype": "3",
        "clientid": "first_install_android_id",
        "devid": "800009",
        "time": "20250714130243",
        "version": "6.9.63",
        "platform": "app_anzt_anzt",
        "platForm": "app_anzt_anzt",
        "sign": "d27c8505dccf72ab39afe62effadefd3"
    }

    # 请求头
    headers = {
        "Host": "nkmapiv3.aniu.tv",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.2.0"
    }

    try:
        # 发送GET请求
        response = requests.get(
            url,
            params=params,
            headers=headers,
            verify=True
        )
        response.raise_for_status()
        response_json = response.json()
        print(response_json)
        return response_json

    except requests.RequestException as e:
        # logger.error(f"请求出错 (ID: {portfolio_id}): {e}")
        return []

    # today_trades = []
    # noteContent = response_json.get('noteContent', [])

    # for item in noteContent:
    #     createAt = item.get('createAt', '') or ''
    #     raw_content = item.get('content', '') or ''
    #     relocateList = item.get('relocateList', [])
    #
    #     # 提取调仓理由和标的名称
    #     extracted_name, clean_reason = extract_stock_analysis(raw_content)
    #
    #     for infos in relocateList:
    #         code = str(infos.get('code', '')).zfill(6)
    #         name = (infos.get('name') or '').replace('\n', '').strip() or '无'
    #
    #         if '***' in name:
    #             name = extracted_name
    #
    #         current_ratio = infos.get('currentRatio', 0)
    #         new_ratio = infos.get('newRatio', 0)
    #         operation = '买入' if new_ratio > current_ratio else '卖出'
    #         market = determine_market(code)
    #
    #         history_post = {
    #             '组合名称': id_to_name.get(str(portfolio_id), '未知组合'),
    #             '操作': operation,
    #             '标的名称': name,
    #             '代码': str(code).zfill(6),
    #             '最新价': infos.get('finalPrice'),
    #             '新比例%': round(new_ratio * 100, 2),
    #             '市场': market,
    #             '时间': createAt,
    #             '调仓理由': clean_reason
    #         }
    #
    #         # 判断是否是今日数据
    #         today = datetime.datetime.now().strftime('%Y-%m-%d')
    #         if today == createAt.split()[0]:
    #             today_trades.append(history_post)
    #
    # return today_trades

from bs4 import BeautifulSoup
import re
import pandas as pd


def extract_stock_analysis(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取组合名 & 股票名 & 代码
    title_span = soup.find('span', style=re.compile(r'color:\s*rgb$'))
    if not title_span:
        return None

    combination_name_match = re.search(r'【(.+?)】', title_span.text)
    combination_name = combination_name_match.group(1) if combination_name_match else '未知组合'

    stock_link = title_span.find('a', href=re.compile(r'productdetails\?code='))
    if not stock_link:
        return None

    stock_code = stock_link.get_text().strip()
    stock_name = stock_link.find_next('a').get_text().strip() if stock_link.find_next('a') else '未知'

    # 提取参考信息
    def get_value_by_label(label_text):
        label_tag = soup.find(lambda tag: tag.name == 'span' and label_text in tag.text)
        if label_tag:
            return label_tag.text.replace(label_text, '').strip().replace("：", "").strip()
        return '无'

    buy_price = get_value_by_label('参考买入价格')
    position = get_value_by_label('参考仓位')
    target_price = get_value_by_label('参考目标价位')
    stop_loss = get_value_by_label('参考止损价位')

    # 提取公司业务介绍（第一个 p 段落）
    business_intro = ''
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if len(text) > 50:
            business_intro = text
            break

    # 提取技术面分析
    technical_analysis = ''
    tech_section = soup.find(lambda tag: tag.name == 'p' and '技术面' in tag.text)
    if tech_section:
        next_p = tech_section.find_next('p')
        if next_p:
            technical_analysis = next_p.get_text().strip()

    # 提取风险提示
    risk_warnings = []
    risk_section = soup.find(lambda tag: tag.name == 'p' and '风险提示' in tag.text)
    if risk_section:
        for li in risk_section.find_next_siblings('p'):
            txt = li.get_text().strip()
            if len(txt) > 5:
                risk_warnings.append(txt)
                if len(risk_warnings) >= 4:
                    break

    result = {
        '组合名称': combination_name,
        '股票代码': stock_code,
        '股票名称': stock_name,
        '买入价格区间': buy_price,
        '建议仓位': position,
        '目标价区间': target_price,
        '止损价区间': stop_loss,
        '公司业务介绍': business_intro,
        '技术面分析': technical_analysis,
        '风险提示': '; '.join(risk_warnings),
    }

    return result


# 示例使用
if __name__ == '__main__':
#     html_content = '''<p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">【朱雀15号】 <a href='qcyzt://productdetails?code=sh603082'>sh603082</a> <a href='qcyzt://productdetails?code=sh603082'>北自科技</a></span></p>
# <p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考买入价格：38.60-38.80</span></p>
# <p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考仓位：10%</span></p>
# <p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考目标价位：41.00-42.00</span></p>
# <p></p><p style="text-indent: 2em;"><span style="color: rgb(255, 0, 0);">参考止损价位：35.80-35.9</span></p>
# <p style="text-indent: 2em;">公司主要从事智能物流系统和装备的研发...</p>
# <p style="text-indent: 2em;">风险提示：产品及服务销售不及预期，市场波动超预期</p>
# <p style="text-indent: 2em;">来源：2024年年报</p>
# <p style="text-indent: 2em;">技术面：走势上上，股价近期回调...</p>'''
    html_content = get_portfolio_industry_theme()
    pprint(html_content)
    analysis = extract_stock_analysis(html_content)
    if analysis:
        df = pd.DataFrame([analysis])
        print(df.to_string(index=False))
        # 可选保存到 Excel 或 CSV
        # df.to_excel('stock_analysis.xlsx', index=False)


# async def process_stock_operations():
#     all_today_trades = []
#     for portfolio_id in all_ids:
#         trades = fetch_and_extract_data(portfolio_id)
#         all_today_trades.extend(trades)
#
#     # 按时间倒序排序
#     all_today_trades.sort(key=lambda x: x['时间'], reverse=True)
#
#     # 转换为 DataFrame
#     df_today = pd.DataFrame(all_today_trades)
#
#     if not df_today.empty:
#         df_today['时间'] = df_today['时间'].apply(normalize_time)
#         df_today = df_today.reset_index(drop=True).set_index(df_today.index + 1)
#     else:
#         logger.info("⚠️ 今日无交易数据")
#         return False
#
#     # 过滤掉非沪深A股的数据
#     df_today = df_today[df_today['市场'] == '沪深A股']
#
#     # 读取历史记录
#     history_df_file = Combination_portfolio_today_file
#     expected_columns = ['组合名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间', '调仓理由']
#     try:
#         df_history = read_portfolio_record_history(history_df_file)
#     except (FileNotFoundError, pd.errors.EmptyDataError):
#         df_history = pd.DataFrame(columns=expected_columns)
#         save_to_excel(df_history, history_df_file, index=False)
#
#     # 格式标准化
#     df_today = standardize_dataframe(df_today)
#     df_history = standardize_dataframe(df_history)
#
#     # 获取新增数据
#     new_data = get_new_records(df_today, df_history)
#
#     if not new_data.empty:
#         # 保存到文件
#         today_str = normalize_time(datetime.date.today().strftime('%Y-%m-%d'))
#         save_to_excel(new_data, history_df_file, sheet_name=today_str, index=False)
#
#         # 发送通知（去掉“调仓理由”列）
#         new_data_without_reason = new_data.drop(columns=['调仓理由'], errors='ignore')
#         send_notification(f"📈 新增交易 {len(new_data)} 条：\n{new_data_without_reason.to_string(index=False)}")
#
#         return True
#     else:
#         logger.info("--------------- 无新增交易数据 ----------------")
#         return False

if __name__ == '__main__':
    asyncio.run(process_stock_operations())
