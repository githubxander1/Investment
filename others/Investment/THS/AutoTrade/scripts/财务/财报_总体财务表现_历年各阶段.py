from pprint import pprint

import requests


def stock_diagnosis_request_for_final_score():
    url = "http://dq.10jqka.com.cn/fuyao/stock_diagnosis/finance/v2/ablility_history?type=stock&industry_type=&ability_id=final_score&code=002836&market=33"
    headers = {
        "cookie": "user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ0MjQ5NTA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTIyMTI5ZjM1YTMyODA1ZWJlOWE1ZDg0NDJkNzEyNjZiOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=8aa63297699e0283609802d6428a22ae; user_status=0; _clck=l14ts7%7C2%7Cfv9%7C0%7C0; hxmPid=seq_667782078; v=A0SBYHclmDfacURuvCLfGRoFF8k2XWg1Kob8C17l0bLTnOvzhm04V3qRzMet",
        "content-type": "application/json",
        "Host": "dq.10jqka.com.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None
import pandas as pd
import re


def extract_data(response_data):
    """
    提取历史评分数据并返回结构化列表
    """
    data = response_data.get("data", {})
    details = data.get("current_ability_details", [])

    extracted = []
    for item in details:
        report = item.get("report", {})
        extracted.append({
            "报告期": report.get("report_name"),
            "日期": report.get("date"),
            "综合评分": float(item.get("final_score", 0)),
            "行业排名": f"{item.get('rank')}/{item.get('total')}",
            "百分比排名": float(item.get("percent", 0)) * 100,
            "评价摘要": clean_html_tags(item.get("comment", ""))
        })

    return extracted


def clean_html_tags(text):
    """
    简单清理 HTML 标签
    """
    return re.sub(r"<[^>]+>", "", text)


def display_and_save(data, filename="stock_final_score_history.csv"):
    """
    使用 pandas 展示表格并保存为 CSV
    """
    df = pd.DataFrame(data)
    print("\n📊 表格展示：")
    print(df.to_string(index=False))
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"\n✅ 数据已保存至 {filename}")

if __name__ == "__main__":
    response = stock_diagnosis_request_for_final_score()
    if response and response.get("status_code") == 0:
        extracted_data = extract_data(response)
        display_and_save(extracted_data)
    else:
        print("请求失败或返回数据格式异常")
