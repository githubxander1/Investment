# data_loader.py
import pandas as pd
import akshare as ak

class DataLoader:
    def __init__(self, config):
        self.config = config

    def load_local_data(self, file_path):
        """加载本地Excel数据"""
        try:
            with pd.ExcelFile(file_path) as xls:
                data = {
                    sheet: pd.read_excel(xls, sheet_name=sheet)
                    for sheet in xls.sheet_names
                }
            return data
        except Exception as e:
            print(f"数据加载失败: {str(e)}")
            return None

    def download_market_data(self, stock_list, period='daily'):
        """下载市场行情数据"""
        market_data = {}
        for code in stock_list:
            try:
                df = ak.stock_zh_a_hist(
                    symbol=code.split(':')[1],
                    period=period,
                    start_date=self.config['data']['start_date'],
                    end_date=self.config['data']['end_date']
                )
                df['code'] = code
                market_data[code] = df
            except Exception as e:
                print(f"下载{code}失败: {str(e)}")
        return market_data
