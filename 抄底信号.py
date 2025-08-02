import requests
import pandas as pd
import pprint

def fetch_bottom_signal_data():
    """获取抄底机会数据"""
    url = "https://opbiz.tianhongjijin.com.cn/cdxh/v2/indexs"
    params = {
        "activityId": "cdxh20231016",
        "channelId": "iFinD",
        "platformId": "iFinDAPP",
        "templateId": "cdxh",
        "pageId": "cdxh20231016",
        "userId": "Tcyt2oYXn7bq9SBjBZ3zFbeseCZjei4J",
        "requestSignal": "全部"
    }
    headers = {
        "Host": "opbiz.tianhongjijin.com.cn",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Falcon/0.2.15",
        "Origin": "https://yd.tianhongjijin.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://yd.tianhongjijin.com.cn/shh/otherh5/cdxhThs/v0.0.1/index.html?aid=cdxh20231016&cid=iFinD&platformId=iFinDAPP",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求异常：{e}")
        return None

def extract_and_save_data(json_data, save_path="抄底机会数据.csv"):
    """提取数据并用Pandas展示和保存"""
    if not json_data or "businessObject" not in json_data:
        print("数据格式异常，无法提取")
        return
    
    # 提取核心数据列表
    data_list = json_data["businessObject"].get("list", [])
    if not data_list:
        print("没有可提取的数据")
        return
    
    # 定义需要提取的字段（与数据对应）
    columns = [
        "指数名称", "基金名称", "基金代码", "信号强度", "历史1年收益率(%)",
        "波动情况", "波动详情", "估值水平", "估值详情", "盈利概率", "风险等级"
    ]
    
    # 提取数据并整理
    rows = []
    for item in data_list:
        row = [
            item.get("indexName", ""),  # 指数名称
            item.get("fundName", ""),   # 基金名称
            item.get("fundCode", ""),   # 基金代码
            item.get("signalInfo", ""), # 信号强度
            item.get("showValue", ""),  # 历史1年收益率
            item.get("showChgStr", ""), # 波动情况（如跌幅大）
            item.get("showChgTxt", ""), # 波动详情（如高点下跌21%）
            item.get("showPeRankStr", ""), # 估值水平（如估值较低）
            item.get("showPeRankTxt", ""), # 估值详情（如比58%时间低）
            item.get("showYieldTxt", ""),  # 盈利概率
            item.get("labels", "")         # 风险等级
        ]
        rows.append(row)
    
    # 创建DataFrame并展示
    df = pd.DataFrame(rows, columns=columns)
    print("\n抄底机会数据整理结果：")
    print(df.to_string(index=False))  # 不显示索引
    
    # 保存为CSV
    try:
        df.to_csv(save_path, index=False, encoding="utf-8-sig")
        print(f"\n数据已成功保存至：{save_path}")
    except Exception as e:
        print(f"保存文件失败：{e}")

if __name__ == "__main__":
    # 获取数据
    bottom_data = fetch_bottom_signal_data()
    if bottom_data:
        # 提取并保存
        extract_and_save_data(bottom_data)