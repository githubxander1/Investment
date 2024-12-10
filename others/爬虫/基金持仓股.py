import requests
from lxml import etree
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_html(url):
         headers = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
         }
         try:
             response = requests.get(url, headers=headers)
             response.raise_for_status()
             return response.text
         except requests.RequestException as e:
             logging.error(f"请求失败: {e}")
             return None


def parse_holding_table(html_content):
    """解析持仓成分表格"""
    holding_list = []
    parser = etree.HTMLParser()
    tree = etree.fromstring(html_content, parser)

    # 使用XPath定位表格
    # holding_table = tree.xpath('/html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[2]/div[1]/div/table')
    holding_table = tree.cssselect('#cctable > div:nth-child(1) > div > table')
    if not holding_table:
        logging.warning("未找到表格元素。")
        return holding_list

    holding_table = holding_table[0]  # 获取第一个匹配的表格
    rows = holding_table.xpath('.//tr')[1:]  # 跳过表头
    for row in rows:
        cells = row.xpath('.//td')
        if len(cells) < 9:
            logging.warning("表格行数据不完整")
            continue

        stock_code = cells[1].xpath('.//a/text()')[0].strip()
        stock_name = cells[2].xpath('.//a/text()')[0].strip()
        latest_price = cells[3].xpath('.//span/text()')[0].strip()
        change_rate = cells[4].xpath('.//span/text()')[0].strip()
        net_value_ratio = cells[6].text.strip()
        holding_volume = cells[7].text.strip()
        market_value = cells[8].text.strip()

        holding_list.append({
            '股票代码': stock_code,
            '股票名称': stock_name,
            '最新价': latest_price,
            '涨跌幅': change_rate,
            '占净值比例': net_value_ratio,
            '持股数（万股）': holding_volume,
            '持仓市值（万元人民币）': market_value
        })

    return holding_list

def get_etf_holding(stock_code):
    """
    根据ETF代码获取持仓成分

    Args:
        stock_code: ETF代码

    Returns:
        持仓成分列表
    """
    url = f"https://fundf10.eastmoney.com/ccmx_{stock_code}.html"
    html_content = fetch_html(url)
    if html_content is None:
        return []

    return parse_holding_table(html_content)

# 示例用法
if __name__ == "__main__":
    stock_code = "159920"  # 华夏恒生ETF(QDII)代码
    holdings = get_etf_holding(stock_code)
    for holding in holdings:
        logging.info(holding)
