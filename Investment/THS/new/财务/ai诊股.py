import requests
import pandas as pd
from Investment.THS.AutoTrade.config.settings import Ai_file

# 自定义股票代码列表
STOCK_CODES = ['601728', '000001', '301088']  # 可自由扩展
OUTPUT_DIR = "stock_diagnosis"
CSV_FILE_PATH = Ai_file  # 从 settings.py 中获取路径


def get_stock_basic_data(code):
    url = f"https://vaserviece.10jqka.com.cn/index/urp/getdata/basic?tag=%E6%89%8B%E7%82%92%E8%AF%8A%E8%82%A1%E5%AE%9E%E9%AA%8C_%E6%8E%A5%E5%85%A5lowcode&userid=641926488&codes={code}&logid=Jadz7weKFRbcQtRZE3cnhGK8tKPQmJXT&isKyc=true&version=v3"
    headers = {
        "Host": "vaserviece.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-Arsenal-Auth": "mb_advance",
        "hexin-v": "Ax7b9gEn-ldaQS4y-wrltxQnbb9g3-JZdKOWPcinimFc67FlMG8yaUQz5k-b",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.27.04 (Royal Flush) hxtheme/1 innerversion/G037.09.025.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://vaserviece.10jqka.com.cn/advancediagnosestock/html/{code}/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ0MjQ5NTA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTIyMTI5ZjM1YTMyODA1ZWJlOWE1ZDg0NDJkNzEyNjZiOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=8aa63297699e0283609802d6428a22ae; user_status=0; _clck=l14ts7%7C2%7Cfv9%7C0%7C0; hxmPid=free_zhengu_002652; v=Ax7b9gEn-ldaQS4y-wrltxQnbb9g3-JZdKOWPcinimFc67FlMG8yaUQz5k-b"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败（{code}）: {e}")
        return None


def extract_and_display_data(data, stock_code):
    if not data:
        print(f"股票 {stock_code} 数据获取失败")
        return {}

    # 提取核心数据（根据实际返回结构解析）
    components = data.get('answer', {}).get('components', [])

    # 综合评价（第一个组件）
    basic_component = next((c for c in components if c.get('cid') == 6729526), None)

    if not basic_component:
        print(f"未找到股票 {stock_code} 的基础数据组件")
        return {'股票代码': stock_code, '错误': '未找到基础数据'}

    basic_data = basic_component.get('data', {}).get('datas', [{}])[0]

    # 基础信息
    stock_name = basic_data.get('股票简称', '')
    current_price = basic_data.get('股价', '')
    price_update_time = basic_data.get('牛叉诊股_时间', '')

    # 综合评分
    overall_score = basic_data.get('牛叉诊股综合评分', '')
    industry_rank = basic_data.get('牛叉诊股综合评分行业排名', '')
    beat_percentage = basic_data.get('ko', '')  # 击败百分比

    # 趋势与建议
    short_suggestion = basic_data.get('short', '')
    mid_suggestion = basic_data.get('mid', '')
    long_suggestion = basic_data.get('long', '')
    hold_suggestion = basic_data.get('hold', '')
    operation_suggestion = basic_data.get('bull', '')  # 操作建议

    # 详细诊断内容
    diagnosis_content = basic_data.get('牛叉诊股_内容', '')
    net_flow = basic_data.get('牛叉诊股_标题', '')

    # 各维度评分
    cate_data = basic_data.get('cateData', {})
    dimension_scores = {
        '基本面': cate_data.get('basic', {}).get('score', ''),
        '资金面': cate_data.get('funds', {}).get('score', ''),
        '消息面': cate_data.get('message', {}).get('score', ''),
        '技术面': cate_data.get('technical', {}).get('score', ''),
        '行业表现': cate_data.get('trade', {}).get('score', ''),
    }

    # 各维度描述
    dimension_descriptions = {
        '基本面': cate_data.get('basic', {}).get('msg', ''),
        '资金面': cate_data.get('funds', {}).get('msg', ''),
        '消息面': cate_data.get('message', {}).get('msg', ''),
        '技术面': cate_data.get('technical', {}).get('msg', ''),
        '行业表现': cate_data.get('trade', {}).get('msg', ''),
    }

    # 技术面数据（支撑压力位）
    tech_component = next((c for c in components if c.get('cid') == 6729529), None)
    tech_data = tech_component.get('data', {}).get('datas', [{}])[0] if tech_component else {}
    support_short = tech_data.get('止盈止损(支撑位)', '')
    resistance_short = tech_data.get('止盈止损(压力位)', '')
    support_ultra_short = tech_data.get('分时止盈止损(支撑位)', '')
    resistance_ultra_short = tech_data.get('分时止盈止损(压力位)', '')

    # 资金面：主力控盘坚决度
    fund_component = next((c for c in components if c.get('cid') == 6729541), None)
    fund_status = fund_component.get('data', {}).get('content', '') if fund_component else ''

    # 基本面财务评分（第14个组件，cid=6729539）
    finance_component = next((c for c in components if c.get('cid') == 6729539), None)
    finance_data = finance_component.get('data', {}).get('datas', [{}])[0] if finance_component else {}
    financial_score = finance_data.get('财务诊断评分', '')
    finance_report_date = finance_data.get('报告期', '')  # 从实际数据提取
    industry_rank_finance = finance_data.get('行业排名', '')  # 从实际数据提取

    # 数据解读（基于各维度评分生成）
    data_interpretation = [
        f"1. 综合评分{overall_score}分，行业排名{industry_rank}，击败{beat_percentage}%同行。",
        f"2. 资金面显示{dimension_descriptions.get('资金面', '')}。",
        f"3. 基本面{dimension_descriptions.get('基本面', '')}。",
        f"4. 技术面{dimension_descriptions.get('技术面', '')}，当前支撑位{support_short}元，压力位{resistance_short}元。"
    ]

    # 控制台展示
    print("="*50)
    print(f"【{stock_name} ({stock_code}) 综合诊断报告】")
    print(f"诊断日期：{price_update_time} | 当前股价：{current_price}元")
    print("="*50)

    print(f"\n【综合评分】")
    print(f"总得分：{overall_score}分 | 行业排名：{industry_rank} | 击败市场：{beat_percentage}%")
    print(f"操作建议：{operation_suggestion}")
    print(f"短期趋势：{short_suggestion}")
    print(f"中期趋势：{mid_suggestion}")
    print(f"长期情况：{long_suggestion}")
    print(f"持仓建议：{hold_suggestion}")

    print(f"\n【各维度评分】")
    for dimension, score in dimension_scores.items():
        print(f"{dimension}：{score}分")

    print(f"\n【关键指标】")
    print(f"支撑位：短线 {support_short}元 | 超短线 {support_ultra_short}元")
    print(f"压力位：短线 {resistance_short}元 | 超短线 {resistance_ultra_short}元")
    print(f"资金流向：{net_flow}")

    print(f"\n【详细解读】")
    for dimension, desc in dimension_descriptions.items():
        print(f"{dimension}：{desc}")

    print(f"\n【财务表现】")
    print(f"财务总评分：{financial_score}分 | {finance_report_date} | 行业排名 {industry_rank_finance}")

    print(f"\n【数据总结】")
    for point in data_interpretation:
        print(f"- {point}")

    print(f"\n【操作建议】")
    print(diagnosis_content)

    # 返回用于表格的数据
    return {
        '股票代码': stock_code,
        '股票简称': stock_name,
        '当前股价': current_price,
        '综合评分': overall_score,
        '击败市场(%)': beat_percentage,
        '行业排名': industry_rank,
        '短期趋势': short_suggestion,
        '中期趋势': mid_suggestion,
        '长期趋势': long_suggestion,
        '操作建议': operation_suggestion,
        '持仓建议': hold_suggestion,
        '支撑位': support_short,
        '压力位': resistance_short,
        '超短线支撑位': support_ultra_short,
        '超短线压力位': resistance_ultra_short,
        '资金流向': net_flow,
        '基本面评分': dimension_scores.get('基本面'),
        '资金面评分': dimension_scores.get('资金面'),
        '消息面评分': dimension_scores.get('消息面'),
        '技术面评分': dimension_scores.get('技术面'),
        '行业表现评分': dimension_scores.get('行业表现'),
        '财务评分': financial_score,
        '财务报告期': finance_report_date,
        '财务行业排名': industry_rank_finance,
        '数据总结': '\n'.join(data_interpretation),
        '操作建议详情': diagnosis_content
    }


def save_to_csv(all_data):
    df = pd.DataFrame(all_data)
    # print(df)
    df.to_csv(CSV_FILE_PATH, index=False, encoding='utf-8-sig')
    print(f"\n✅ 所有股票诊断已保存至: {CSV_FILE_PATH}")


if __name__ == "__main__":
    all_extracted_data = []

    for code in STOCK_CODES:
        print(f"\n🔄 正在获取股票 {code} 的数据...")
        raw_data = get_stock_basic_data(code)
        parsed_data = extract_and_display_data(raw_data, code)
        all_extracted_data.append(parsed_data)

    # 保存为 CSV
    save_to_csv(all_extracted_data)
    # with pd.ExcelWriter("ai_诊股结果.xlsx", engine="openpyxl") as writer:
    #     for item in all_extracted_data:
    #         code = item["股票代码"]
    #         df = pd.DataFrame([item])
    #         df.to_excel(writer, sheet_name=code[:31], index=False)
    # print("✅ 已保存为 Excel，每只股票一个 sheet")
