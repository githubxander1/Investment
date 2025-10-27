from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


def fetch_dynamic_stock_data(
        url: str = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board",
        save_path= "dynamic_stock_data.csv",
        wait_time= 10  # 页面加载等待时间（秒）
):
    """
    动态爬取东方财富网A股数据（Selenium模拟浏览器）

    Args:
        url: 爬取目标URL
        save_path: 数据保存路径（None表示不保存）
        wait_time: 页面加载等待时间（动态页面需足够时间渲染）

    Returns:
        包含股票数据的DataFrame（失败返回None）
    """
    driver = None
    try:
        # 1. 初始化Chrome浏览器（自动安装匹配的ChromeDriver）
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        time.sleep(wait_time)  # 等待动态数据加载（显式等待更优，此处简化用sleep）

        # 2. 定位表格并提取数据
        stock_elements = driver.find_elements(By.XPATH, '//table[@class="table"]//tr[position()>1]')
        stock_data = []

        for element in stock_elements:
            cols = element.find_elements(By.TAG_NAME, "td")
            if len(cols) < 5:
                continue

            stock_info = {
                "代码": cols[0].text.strip(),
                "名称": cols[1].text.strip(),
                "最新价": cols[2].text.strip(),
                "涨跌幅(%)": cols[3].text.strip().replace("%", ""),
                "成交量(手)": cols[4].text.strip()
            }
            stock_data.append(stock_info)

        # 3. 转换为DataFrame并保存
        df = pd.DataFrame(stock_data)
        if save_path:
            df.to_csv(save_path, index=False, encoding="utf-8-sig")
            print(f"动态数据已保存至：{save_path}")

        return df

    except Exception as e:
        print(f"动态爬取失败：{str(e)}")
        return None

    finally:
        # 4. 关闭浏览器（无论成功/失败）
        if driver:
            driver.quit()

df = fetch_dynamic_stock_data()
print(df)