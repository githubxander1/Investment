import requests
import json
from pprint import pprint
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import os

# 定义账户信息
ACCOUNTS = {
    "中泰证券": "133508019",
    "川财证券": "108048932", 
    "长城证券": "103353867",
    "中山证券": "139269044"
}

def fetch_stock_position(fund_key: str, account_name: str = ""):
    """调用股票持仓接口，获取原始position数据"""
    url = "https://tzzb.10jqka.com.cn/caishen_httpserver/tzzb/caishen_fund/pc/asset/v1/stock_position"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-ch-ua': "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://tzzb.10jqka.com.cn",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://tzzb.10jqka.com.cn/pc/index.html",
        'accept-language': "zh-CN,zh;q=0.9",
        'priority': "u=1, i",
        'Cookie': "shoudNotCookieRefresh=1; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=fou%2F0LouwneNgg4aLANzv2enaqgkV1cyTWuTdDYhEScfYqYIyaTF3YeykygdN%2FRBHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=CC37D8EBB29D40329773B6DEFBD27A2F; u_ttype=WEB; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzU4MTExNTk1Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE1OTg3M2ZhNzYyZjc0NmVmNzZhMjgyNzNjMTY5YTAzOmRlZmF1bHRfNTox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c70e5cfdec172dd60b4e33da5350c9df; user_status=0; utk=2c7de60a214d547dd20f9089d3ef8b0d; sess_tk=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6InNlc3NfdGtfMSIsImJ0eSI6InNlc3NfdGsifQ.eyJqdGkiOiIwMzlhMTYzYzI3Mjg2YWY3NmU3NDJmNzZmYTczOTgxNTEiLCJpYXQiOjE3NTgxMTE1OTUsImV4cCI6MTc2MDc4OTk5NSwic3ViIjoiNjQxOTI2NDg4IiwiaXNzIjoidXBhc3MuMTBqcWthLmNvbS5jbiIsImF1ZCI6IjIwMjAxMTE4NTI4ODkwNzIiLCJhY3QiOiJvZmMiLCJjdWhzIjoiMzJiZGRiOWJlMTM1ZTY5NWUzNjlkYzBhZDcxOWIxZjIwNDlmYWNiYmEzMGVlYjcwMDkzNzQzNWFkMzkwM2Q5NSJ9.VBxfCBikgTJjC4ioQtoDOu1a0NooRz25PHy-muzrZS6LSKZCgmUoTHYogqWKAs7H2EcAT-ufy_CzN8u8N55rQQ; cuc=sufmt4wli5k8; v=AzhS_mYPpFE3sMjViWIsY1gVCe3PoZwr_gVwr3KphHMmjdbTGrFsu04VQDHB"
    }
    payload = {
        'terminal': "1",
        'version': "0.0.0",
        'userid': "641926488",
        'user_id': "641926488",
        'manual_id': "",
        'fund_key': fund_key,
        'rzrq_fund_key': ""
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        resp_json = response.json()
        print(f"成功获取 {account_name} 账户数据")
        return resp_json

    except requests.RequestException as e:
        print(f"HTTP请求异常: {str(e)}")
        return None
    except json.JSONDecodeError:
        print("响应格式错误（非JSON）")
        return None
    except Exception as e:
        print(f"未知异常: {str(e)}")
        return None


def extract_position_details(resp_json: dict, account_name: str) -> dict:
    """提取持仓关键信息（适配界面列：代码、名称、持有金额、当日盈亏等）"""
    # 提取position原始数据
    money_remain = resp_json.get("ex_data", {}).get("money_remain", 0.0)  # 账户余额
    position_rate = resp_json.get("ex_data", {}).get("position_rate", 0.0)  # 仓位
    total_asset = resp_json.get("ex_data", {}).get("total_asset", 0.0)  # 总资产
    total_liability = resp_json.get("ex_data", {}).get("total_liability", 0.0)  # 总市值
    total_value = resp_json.get("ex_data", {}).get("total_value", 0.0)  # 总盈亏
    position_list = resp_json.get("ex_data", {}).get("position", [])
    
    # 账户汇总信息
    account_summary = {
        "账户名称": account_name,
        "账户余额": money_remain,
        "仓位": position_rate,
        "总资产": total_asset,
        "总市值": total_liability,
        "总盈亏": total_value,
        "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 持仓详细信息
    extracted = []
    for item in position_list:
        # 字段映射（与界面展示一一对应）
        detail = {
            "账户": account_name,
            "股票代码": item.get("code", ""),
            "股票名称": item.get("name", ""),
            "持有金额": item.get("value", 0.0),  # 对应界面"持有金额"
            "当日盈亏": item.get("d_profit", 0.0),  # 对应界面"当日盈亏"
            "成本价": item.get("cost", 0.0),
            "当前价": item.get("price", 0.0),
            "持仓天数": item.get("hold_days", 0),
            "持仓占比": item.get("position_rate", 0.0),
            "回本涨幅": item.get("back", 0.0),
            "持有数量": item.get("count", 0),
            "持有盈亏": item.get("hold_profit", 0.0),
            "持有盈亏率": item.get("hold_rate", 0.0),
            "累积盈亏": item.get("position_rate", 0.0),
            "本周盈亏": item.get("w_profit", 0.0),
            "今年盈亏": item.get("y_profit", 0.0),
        }
        extracted.append(detail)
    return {
        "account_summary": account_summary,
        "positions": extracted
    }


def save_all_accounts_to_excel(all_accounts_data: dict, filename: str = "account_positions.xlsx"):
    """将所有账户数据保存到同一个Excel文件的不同工作表中"""
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 创建汇总表
        summary_data = []
        for account_name, data in all_accounts_data.items():
            summary_data.append(data["account_summary"])
        
        summary_df = pd.DataFrame(summary_data)
        # 按总资产排序
        summary_df = summary_df.sort_values("总资产", ascending=False)
        summary_df.to_excel(writer, sheet_name="账户汇总", index=False)
        
        # 为每个账户创建单独的工作表
        for account_name, data in all_accounts_data.items():
            if data["positions"]:
                positions_df = pd.DataFrame(data["positions"])
                positions_df.to_excel(writer, sheet_name=f"{account_name}持仓", index=False)
            else:
                # 如果没有持仓数据，创建一个空表
                empty_df = pd.DataFrame([{
                    "账户": account_name,
                    "股票代码": "",
                    "股票名称": "无持仓",
                    "持有金额": 0,
                    "当日盈亏": 0,
                    "成本价": 0,
                    "当前价": 0,
                    "持仓天数": 0,
                    "持仓占比": 0,
                    "回本涨幅": 0,
                    "持有数量": 0,
                    "持有盈亏": 0,
                    "持有盈亏率": 0,
                    "累积盈亏": 0,
                    "本周盈亏": 0,
                    "今年盈亏": 0
                }])
                empty_df.to_excel(writer, sheet_name=f"{account_name}持仓", index=False)
    
    print(f"所有账户数据已保存到 {filename}")


def main():
    """主函数：获取所有账户数据并保存到Excel"""
    all_accounts_data = {}
    
    # 获取所有账户的数据
    for account_name, fund_key in ACCOUNTS.items():
        print(f"正在获取 {account_name} 账户数据...")
        raw_positions = fetch_stock_position(fund_key, account_name)
        if raw_positions:
            extracted_data = extract_position_details(raw_positions, account_name)
            all_accounts_data[account_name] = extracted_data
        else:
            print(f"未能获取 {account_name} 账户数据")
            # 即使没有数据也保存空结构
            all_accounts_data[account_name] = {
                "account_summary": {
                    "账户名称": account_name,
                    "账户余额": 0.0,
                    "仓位": 0.0,
                    "总资产": 0.0,
                    "总市值": 0.0,
                    "总盈亏": 0.0,
                    "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "positions": []
            }
    
    # 保存到Excel文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"account_positions_{timestamp}.xlsx"
    save_all_accounts_to_excel(all_accounts_data, filename)
    
    # 同时保存一个不带时间戳的版本，方便查找
    save_all_accounts_to_excel(all_accounts_data, "account_positions.xlsx")
    
    # 打印汇总信息
    print("\n账户汇总信息：")
    summary_list = [data['account_summary'] for data in all_accounts_data.values()]
    summary_df = pd.DataFrame(summary_list)
    # 按总资产排序并显示
    summary_df = summary_df.sort_values("总资产", ascending=False)
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    # ========== 使用说明 ==========
    # 1. 确保Cookie有效（需要登录同花顺账户）
    # 2. 根据需要修改ACCOUNTS中的账户信息
    # 3. 运行脚本将自动获取所有账户数据并保存到Excel文件
    
    main()