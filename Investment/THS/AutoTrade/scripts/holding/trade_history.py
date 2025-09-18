import requests
import json
from pprint import pprint
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta
import os

from Investment.THS.AutoTrade.config.settings import Trade_history
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger(__name__)

# 确保在正确的目录下工作
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 定义账户信息
# ACCOUNTS = {
#     "中泰证券": "133508019",
#     "川财证券": "108048932",
#     "长城证券": "103353867",
#     "中山证券": "139269044"
# }

def fetch_trade_history(fund_key: str, account_name: str = "", start_date: str = "", end_date: str = ""):
    """调用交易历史接口，获取交易数据"""
    url = "https://tzzb.10jqka.com.cn/caishen_httpserver/tzzb/caishen_fund/pc/account/v2/get_money_history"
    
    # 如果没有指定日期，默认获取最近30天的数据
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")
    
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
        'Cookie': "shoudNotCookieRefresh=1; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=r95aF0YEFEII%2FfZ9g5ulaAhpaig1BwheK43AFXNPIyhQxPD1qLpBOWQTZGvIQ0SdHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=B7807F2C8A644E8FB60A96872F764F73; u_ttype=WEB; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzU4MTU2ODg3Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTQxNzk5YzJmNTU4OTY2YTEzYzk3NTM2NDUzOTQ3M2RmOmRlZmF1bHRfNTox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=dcbfad3de7a5f2da520075ac60682b7c; user_status=0; utk=a9d390aff644bd96885e1a125627463e; sess_tk=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6InNlc3NfdGtfMSIsImJ0eSI6InNlc3NfdGsifQ.eyJqdGkiOiJkZjczOTQ1MzY0NTM5NzNjYTE2Njg5NTUyZjljNzk0MTEiLCJpYXQiOjE3NTgxNTY4ODcsImV4cCI6MTc2MDgzNTI4Nywic3ViIjoiNjQxOTI2NDg4IiwiaXNzIjoidXBhc3MuMTBqcWthLmNvbS5jbiIsImF1ZCI6IjIwMjAxMTE4NTI4ODkwNzIiLCJhY3QiOiJvZmMiLCJjdWhzIjoiMWRjNjkxOGEzZWFjOGRiZTQ4Yjg4ZDQ2YjQzMTBmY2YzZjBkZTAzYjg0YzMwNGU3OTNlZWQzN2E4NmM5ZGNlMiJ9.nE6_VSuRDAr7jIOFPYiaR4K_xorA7mygZ_E3k37gL23ZvMIxtU3a69m68wbWdjBOsL4lu7dZCUPAZ_SsfojSIw; cuc=66a02uw6co1h; v=AyPt7hcXT8G3EQP1IQd3MmessmzIGLT_8ar7qFWBf9z42U0S3ehHqgF8i4Jm"
    }
    
    payload = {
        'terminal': "1",
        'version': "0.0.0",
        'userid': "641926488",
        'user_id': "641926488",
        'manual_id': "",
        'fund_key': fund_key,
        'rzrq_fund_key': "",
        'fundid': "",
        'start_date': start_date,
        'end_date': end_date,
        'query_list': "[]",
        'page': "1",
        'count': "100",  # 增加数量以获取更多数据
        'sort_type': "",
        'sort_order': "1",
        'h5id': "1758160055387"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        resp_json = response.json()
        print(f"成功获取 {account_name} 账户交易历史数据")
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


def extract_trade_details(resp_json: dict, account_name: str) -> dict:
    """提取交易历史关键信息"""
    # 提取交易历史列表
    trade_list = resp_json.get("ex_data", {}).get("list", [])
    
    # 交易详细信息
    extracted = []
    for item in trade_list:
        # 安全地转换数据类型
        def safe_int(value, default=0):
            try:
                if value is None or value == '':
                    return default
                return int(value)
            except (ValueError, TypeError):
                return default
                
        def safe_float(value, default=0.0):
            try:
                if value is None or value == '':
                    return default
                return float(value)
            except (ValueError, TypeError):
                return default
        
        # 字段映射
        detail = {
            "账户": account_name,
            "股票代码": item.get("code", ""),
            "股票名称": item.get("name", ""),
            "操作": item.get("op_name", ""),  # 买入/卖出
            "成交数量": safe_int(item.get("entry_count", 0)),
            "成交价格": safe_float(item.get("entry_price", 0.0)),
            "成交金额": safe_float(item.get("entry_money", 0.0)),
            "手续费": safe_float(item.get("fee_total", 0.0)),
            "成交日期": item.get("entry_date", ""),
            "成交时间": item.get("entry_time", ""),
            "市场代码": item.get("market_code", ""),
            "备注": item.get("remark", "")
        }
        extracted.append(detail)
        
    return {
        "trades": extracted
    }


def save_all_trade_history_to_excel(all_accounts_data: dict, filename: str = Trade_history):
    """将所有账户交易历史数据保存到同一个Excel文件的不同工作表中"""
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 为每个账户创建单独的工作表
        for account_name, data in all_accounts_data.items():
            if data["trades"]:
                trades_df = pd.DataFrame(data["trades"])
                # 按成交日期和时间排序
                trades_df = trades_df.sort_values(["成交日期", "成交时间"], ascending=[False, False])
                trades_df.to_excel(writer, sheet_name=f"{account_name}", index=False)
            else:
                # 如果没有交易数据，创建一个空表
                empty_df = pd.DataFrame([{
                    "账户": account_name,
                    "股票代码": "",
                    "股票名称": "无交易记录",
                    "操作": "",
                    "成交数量": 0,
                    "成交价格": 0.0,
                    "成交金额": 0.0,
                    "手续费": 0.0,
                    "成交日期": "",
                    "成交时间": "",
                    "市场代码": "",
                    "备注": ""
                }])
                empty_df.to_excel(writer, sheet_name=f"{account_name}", index=False)
    
    print(f"所有账户交易历史数据已保存到 {filename}")


def read_today_trade_history(history_file_path: str = Trade_history, account_name: str = None) -> pd.DataFrame:
    """
    读取Trade_history文件中指定账户当天的交易记录
    
    参数:
        history_file_path (str): Trade_history文件路径
        account_name (str): 账户名称，如果为None则读取所有账户
    
    返回:
        pd.DataFrame: 当天的交易记录
    """
    from Investment.THS.AutoTrade.utils.format_data import normalize_time
    today = normalize_time(datetime.now().strftime('%Y-%m-%d'))
    
    if not os.path.exists(history_file_path):
        logger.warning(f"交易历史文件不存在: {history_file_path}")
        return pd.DataFrame()
    
    try:
        with pd.ExcelFile(history_file_path, engine='openpyxl') as xls:
            # 如果指定了账户名称，只读取该账户的工作表
            if account_name:
                if account_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=account_name)
                    # 筛选当天的交易记录
                    if not df.empty and '成交日期' in df.columns:
                        # 将成交日期转换为标准格式进行比较
                        df['成交日期'] = pd.to_datetime(df['成交日期'], format='%Y%m%d', errors='coerce')
                        today_date = pd.to_datetime(today).date()
                        df = df[df['成交日期'].dt.date == today_date]
                        return df
                    else:
                        return pd.DataFrame()
                else:
                    logger.warning(f"账户 {account_name} 在交易历史文件中不存在")
                    return pd.DataFrame()
            else:
                # 读取所有账户的数据
                all_data = []
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    if not df.empty and '成交日期' in df.columns:
                        # 筛选当天的交易记录
                        df['成交日期'] = pd.to_datetime(df['成交日期'], format='%Y%m%d', errors='coerce')
                        today_date = pd.to_datetime(today).date()
                        df_filtered = df[df['成交日期'].dt.date == today_date]
                        if not df_filtered.empty:
                            df_filtered['账户'] = sheet_name
                            all_data.append(df_filtered)
                
                if all_data:
                    return pd.concat(all_data, ignore_index=True)
                else:
                    return pd.DataFrame()
                    
    except Exception as e:
        logger.error(f"读取交易历史文件失败: {e}")
        return pd.DataFrame()


def main():
    """主函数：获取所有账户交易历史数据并保存到Excel"""
    all_accounts_data = {}
    
    # 获取所有账户的数据
    from Investment.THS.AutoTrade.config.settings import ACCOUNTS
    for account_name, fund_key in ACCOUNTS.items():
        print(f"正在获取 {account_name} 账户交易历史数据...")
        raw_trades = fetch_trade_history(fund_key, account_name)
        if raw_trades:
            extracted_data = extract_trade_details(raw_trades, account_name)
            all_accounts_data[account_name] = extracted_data
        else:
            print(f"未能获取 {account_name} 账户交易历史数据")
            # 即使没有数据也保存空结构
            all_accounts_data[account_name] = {
                "trades": []
            }
    
    # 保存到Excel文件
    save_all_trade_history_to_excel(all_accounts_data, Trade_history)
    
    # 打印汇总信息
    logger.info("账户交易记录统计：")
    for account_name, data in all_accounts_data.items():
        logger.info(f"{account_name}: {len(data['trades'])} 条记录")
    logger.info("交易历史数据获取和保存完成")


if __name__ == "__main__":
    # ========== 使用说明 ==========
    # 1. 确保Cookie有效（需要登录同花顺账户）
    # 2. 根据需要修改ACCOUNTS中的账户信息
    # 3. 运行脚本将自动获取所有账户交易历史数据并保存到Excel文件
    
    main()