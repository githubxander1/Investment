# import datetime
import os

import akshare as ak
import pandas as pd
# from 龙虎榜1 import start_date


from datetime import datetime
start_date = '2023-06-13'
dt = datetime.strptime(start_date, "%Y-%m-%d")
start_date = dt.strftime("%Y%m%d")
print(start_date)
def download_stock_data(stock_infos, save_path='stock_data/双峰形态'):
    """下载股票 K 线数据并保存为 CSV 文件"""
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 获取当前日期并格式化为 YYYYMMDD
    end_date = datetime.now().strftime("%Y%m%d")

    for code, name in stock_infos.items():
        try:
            # 下载日 K 线数据
            stock_df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date,
                end_date=end_date
            )

            # 清理文件名中的路径分隔符
            safe_name = name.replace('/', '_').replace('\\', '_')
            file_path = os.path.join(save_path, f"{code}{safe_name}.csv")

            stock_df.to_csv(file_path, index=False)
            print(f"成功保存: {file_path}")
        except Exception as e:
            print(f"下载 {code}({name}) 失败: {str(e)}")

# 示例调用
if __name__ == "__main__":
    today = datetime.now().strftime('%Y%m%d')
    # nd_date = datetime.date.today().strftime("%Y%m%d")
    print(today)

    # stock_infos = {
    #     '002119': '康强电子',
    #     '688653': '康希通信',
    #     '002505': '彭都农牧',
    #     '301082': '久盛电气',
    #     '831526': '凯华材料'
    # }
    # stock_infos = {
    #     '900939': '汇丽B',
    #     '605258': '协和电子',
    #     '688107': '安路科技'
    #
    # }
    stock_infos = {
        '000011': '深物业A',
        '601869': '长飞光纤',
        '300433': '蓝思科技',
    }
    download_stock_data(stock_infos)