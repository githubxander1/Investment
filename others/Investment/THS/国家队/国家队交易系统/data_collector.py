import pandas as pd
import requests
import json
from datetime import datetime

class NationalTeamDataCollector:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://data.hexin.cn/gjd/index/"
        }

    def fetch_team_data(self, data_type=1, page=1):
        """获取国家队相关数据"""
        url = f"https://data.hexin.cn/gjd/team/type/{data_type}/page/{page}/"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None

    def extract_stock_data(self, raw_data):
        """提取股票数据"""
        if not raw_data or 'data' not in raw_data:
            return []

        results = []
        for item in raw_data['data']:
            holders_info = ', '.join([f"{holder['name']}({holder['scale']}%)"
                                    for holder in item.get('holders', [])])

            results.append({
                'stock_code': item.get('code'),
                'stock_name': item.get('name'),
                'report_date': item.get('report'),
                'declare_date': item.get('declare'),
                'total_scale': float(item.get('scale', 0)),
                'holders_info': holders_info,
                'social_security': int(item.get('sb', 0)),
                'pension': int(item.get('ylj', 0)),
                'central_bank': int(item.get('zj', 0)),
                'huijin': int(item.get('hj', 0)),
                'fetch_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return results

    def save_to_excel(self, data, sheet_name='最新公布'):
        """保存到Excel文件"""
        if not data:
            print("没有数据可保存")
            return False

        df = pd.DataFrame(data)
        try:
            with pd.ExcelWriter('国家队持股数据.xlsx', mode='a', engine='openpyxl',
                               if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"成功保存 {sheet_name} 数据到Excel")
            return True
        except Exception as e:
            print(f"保存Excel时发生错误: {e}")
            return False

if __name__ == '__main__':
    collector = NationalTeamDataCollector()

    # 获取并保存各类数据
    data_types = {
        1: '最新公布',
        2: '持有最多',
        3: '增持最多',
        4: '持有最久'
    }

    all_data = {}
    for dtype, name in data_types.items():
        raw_data = collector.fetch_team_data(dtype)
        if raw_data:
            stock_data = collector.extract_stock_data(raw_data)
            all_data[name] = stock_data
            collector.save_to_excel(stock_data, name)
