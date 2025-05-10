from pprint import pprint

import pandas as pd
import requests

def stock_finance_request():
    url = "http://dq.10jqka.com.cn/fuyao/stock_diagnosis/finance/v1/ablility?code=002836&market=33&type=stock&industry_type="
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
def extract_data(response_data):
    """
    提取重要财务能力指标数据并返回结构化列表
    """
    data = response_data.get("data", {})
    abilities = data.get("diagnosis_abilities", [])

    extracted = []
    for item in abilities:
        extracted.append({
            "能力名称": item.get("diagnosis_ability_name"),
            "关键词": item.get("keyword"),
            "当前得分": round(float(item.get("current_score")),2),
            "行业平均": round(float(item.get("industry_average")),2),
            "排名": item.get("rank")
        })

    extracted.append({
        "能力名称": "",
        "关键词": "综合评分",
        "当前得分": round(float(data.get("share_comprehensive_score", 0)), 2),
        "行业平均": "",
        "排名": f"{data.get('rank', 'N/A')}/{data.get('total', 'N/A')}"
    })
    return extracted

def save_to_csv(data, filename="stock_finance_data.csv"):
    """
    使用 pandas 保存提取的数据到 CSV 文件
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"数据已保存至 {filename}")
    print("\n表格展示：")
    print(df)



if __name__ == "__main__":
    response = stock_finance_request()
    pprint(response)
    if response and response.get("status_code") == 0:
        extracted_data = extract_data(response)
        save_to_csv(extracted_data)
    else:
        print("请求失败或返回数据格式异常")
