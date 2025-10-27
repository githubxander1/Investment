import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
# from typing import Optional, DataFrame


def fetch_static_stock_data(
        url: str = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board",
        save_path = "stock_data.csv"
):
    """
    静态爬取东方财富网A股行情数据

    Args:
        url: 爬取目标URL（默认A股行情页）
        save_path: 数据保存路径（None表示不保存）

    Returns:
        包含股票数据的DataFrame（失败返回None）

    Raises:
        打印异常信息（网络错误、解析错误等）
    """
    try:
        # 1. 生成随机User-Agent（反爬基础）
        ua = UserAgent()
        headers = {"User-Agent": ua.random}

        # 2. 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 若状态码非200，抛出HTTPError
        html_content = response.text

        # 3. 解析HTML表格数据
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", {"class": "table"})
        if not table:
            print("未找到股票数据表格，请检查页面结构是否变化")
            return None

        rows = table.find_all("tr")[1:]  # 跳过表头（第0行）
        stock_data = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:  # 确保列数足够（至少包含代码、名称、最新价、涨跌幅、成交量）
                continue

            stock_info = {
                "代码": cols[0].text.strip(),
                "名称": cols[1].text.strip(),
                "最新价": cols[2].text.strip(),
                "涨跌幅(%)": cols[3].text.strip().replace("%", ""),  # 清理百分号，便于后续计算
                "成交量(手)": cols[4].text.strip()
            }
            stock_data.append(stock_info)

        # 4. 转换为DataFrame并保存（可选）
        df = pd.DataFrame(stock_data)
        if save_path:
            df.to_csv(save_path, index=False, encoding="utf-8-sig")  # utf-8-sig解决中文乱码
            print(f"静态数据已保存至：{save_path}")

        return df

    except Exception as e:
        print(f"静态爬取失败：{str(e)}")
        return None

df = fetch_static_stock_data()
print(df)