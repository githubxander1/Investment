from pprint import pprint

import requests


def stock_risk_request():
    url = "http://dq.10jqka.com.cn/fuyao/stock_diagnosis/finance/v1/highlight_risk?code=002836&market=33&type=stock&industry_type=&report="
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

#提取数据
def extract_data(response_data):
    """
    提取 highlight、overview、risk 数据并返回结构化结果
    """
    data = response_data.get("data", {})

    extracted = {
        "股票名称": data.get("name"),
        "代码": data.get("code"),
        "亮点分析": [],
        "风险提示": [],
        "财务概览": ""
    }

    # 提取 highlight
    highlights = data.get("highlight", [])
    for item in highlights:
        extracted["亮点分析"].append({
            "指标": item.get("name", ""),
            "描述": item.get("comment", "")
        })

    # 提取 overview（可选：清洗 HTML 标签）
    overview = data.get("overview", "")
    extracted["财务概览"] = clean_html_tags(overview) if "<" in overview else overview

    # 提取 risk（当前为空列表，保留结构用于未来扩展）
    risks = data.get("risk", [])
    for item in risks:
        extracted["风险提示"].append({
            "类型": item.get("type", ""),
            "描述": item.get("comment", "")
        })

    return extracted


def clean_html_tags(text):
    """
    简单清理 HTML 标签（如 <span class='red'>出色</span> → 出色）
    """
    import re
    return re.sub(r"<[^>]+>", "", text)


# pprint(stock_risk_request())
pprint(extract_data(stock_risk_request()))