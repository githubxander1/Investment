import os
import re
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

base_url = 'https://fylhfyullx.top:2568/'

# 下载图片的函数
def download_image(img_url, save_folder):
    if img_url.startswith('data:image'):
        print(f"Skipping Base64 encoded image: {img_url}")
        return

    try:
        img_response = requests.get(img_url)
        img_response.raise_for_status()
        img_name = os.path.basename(img_url)
        img_path = os.path.join(save_folder, img_name)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f"Downloaded {img_url} to {img_path}")
    except requests.RequestException as e:
        print(f"Error downloading {img_url}: {e}")

# 处理数据的函数
def process_list_data(html_content, base_url, save_folder):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取总项目数量
    # total_items_span = soup.find('span', string=re.compile('共'))
    # if total_items_span:
    #     total_items = int(total_items_span.parent.text.split()[1])
    #     print(f"共 {total_items} 个项目")
    # else:
    #     total_items = 0
    detail_urls = []

    infors = []

    id = 0

    container = soup.find_all('div', class_="listpic")
    for item in container:
        a_tag = item.find('a')
        if a_tag:
            href = a_tag.get('href')
            global full_href
            full_href = urljoin(base_url, href) if not href.startswith('http') else href

            img_div = a_tag.find('div', class_="vodpic lazyload")
            if img_div:
                img_tag = img_div.find('img')
                img_url = img_tag.get('src') if img_tag else None
                full_img_url = urljoin(base_url, img_url) if img_url and not img_url.startswith('http') else img_url

                title_tag = a_tag.find('div', class_="vodname")
                title = title_tag.text.strip() if title_tag else None


                # if full_img_url and not full_img_url.startswith('data:image'):
                    # print(f'\n项目编号: {item_counter["count"]}')
                print(f"详情链接: {full_href}")
                print(f"图片链接: {img_url}")
                print(f"标题: {title}")

                info = {
                    '项目编号': id,
                    '详情链接': full_href,
                    '图片链接': full_img_url,
                    '标题': title
                }
                id += 1

                # 汇总详情链接
                detail_urls.append(full_href)

                infors.append([full_href, img_url, title])

    return detail_urls, title

# 滚动页面以触发懒加载
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 滚动到底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 等待页面加载
        time.sleep(2)
        # 计算新的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 获取详情页面的 HTML 内容并解析图片链接
def get_detail_page(detail_url, save_folder):
    driver.get(detail_url)
    time.sleep(10)  # 等待页面加载完成
    scroll_to_bottom(driver)
    detail_html = driver.page_source
    detail_soup = BeautifulSoup(detail_html, 'html.parser')
    nbodys = detail_soup.find('div', class_='nbodys')
    img_urls = []
    title = None
    if nbodys:
        img_tags = nbodys.find_all('img')
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url and not img_url.startswith('data:image'):
                print(f"详情页图片链接: {img_url}")
                # download_image(img_url, save_folder)
                img_urls.append(img_url)
            else:
                print(f"跳过 Base64 编码的图片: {img_url}")

    else:
        print("未找到详情页面内容")

    return img_urls

# 主函数
def main():
    save_folder = '下载_图片'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 设置 Edge 选项
    edge_options = Options()
    edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    edge_options.add_argument("--disable-gpu")  # 禁用 GPU
    edge_options.add_argument("--no-sandbox")  # 禁用沙盒
    edge_options.add_argument("--log-level=3")  # 设置日志级别为 3，减少日志输出
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # 设置用户代理

    # 启动 Edge 浏览器
    global driver
    driver = webdriver.Edge(options=edge_options)

    current_page = 1
    total_pages = 1  # 假设总共有5页
    total_items = 0  # 初始化总项目数量
    detail_urls = []  # 存储详情链接
    data_to_save = []  # 存储要保存到 Excel 的数据

    # 只处理前两页的数据
    for id in range(45, 46):  # 45 对应第一页
        for page in range(1, total_pages + 1):
            page_url = f'https://fylhfyullx.top:2568/piclist/{id}.html?page={page}'
            print(f"\n正在处理URL: {page_url}")
            driver.get(page_url)
            scroll_to_bottom(driver)

            # 使用显式等待等待页面加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='app_hm']/div[30]/div[4]/ul/li[1]/span"))
            )

            # 获取页面内容
            html_content = driver.page_source

            # 处理数据
            # its, title = process_list_data(html_content, base_url, save_folder)
            # print(its)
            # total_items += len(its)

            # 更新进度
            # print(f"第 {pom} 页处理完毕，共 {total_items} 个项目。")
            print(f"第 {page} 页处理完毕")


    detail_urls = ['https://fylhfyullx.top:2568/picdetail/9545620.html', 'https://fylhfyullx.top:2568/picdetail/9545624.html', 'https://fylhfyullx.top:2568/picdetail/9545630.html']
    # 处理详情链接
    for idx, detail_url in enumerate(detail_urls, start=1):
        print(f"正在处理详情链接: {detail_url}")
        img_urls = get_detail_page(detail_url, save_folder)
        print(f"图片链接: {img_urls}")
        # data_to_save.append({
        #     '项目编号': idx,
        #     '详情链接': detail_url,
        #     # '图片链接': ', '.join(img_urls) if img_urls else None,  # 将图片链接列表转换为字符串
        #     '图片链接': img_urls,  # 将图片链接列表转换为字符串
        #     '标题': title
        # })
        # print(data_to_save)

    # 保存数据到 Excel
    # save_to_excel(data_to_save, '项目数据.xlsx')

    print(f"总共有 {total_items} 个项目。")
    driver.quit()

if __name__ == "__main__":
    main()
