import os
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# '成人小说': 'https://fylhfyullx.top:2568/txtlist/57.html'#51-58
# '都市情感': 'https://fylhfyullx.top:2568/txtlist/51.html'
# '日韩无码': 'https://fylhfyullx.top:2568/vediolist/77.html'#77-84
# '性爱自拍': 'https://fylhfyullx.top:2568/piclist/45.html'#42-49

# 目标网页的URL列表
daohang_list = [
    # 'https://fylhfyullx.top:2568/picdetail/9481011.html',
    'https://fylhfyullx.top:2568/vodlist/83.html',
    'https://fylhfyullx.top:2568/piclist/45.html',
    # 'https://fylhfyullx.top:2568/voddetail/1768855.html',
    # 其他 URL
]

# 下载图片的函数
def download_image(img_url, save_folder):
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
def process_data(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 初始化分类存储
    url_list = []
    email_list = []
    location_list = []
    video_list = []
    image_list = []
    title_list = []

    # 分类提取
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            if re.match(r'^https?://', href):
                url_list.append(href)
            elif re.match(r'^mailto:', href):
                email_list.append(href[7:])  # 去掉"mailto:"部分
            elif re.match(r'^geo:', href):
                location_list.append(href[4:])  # 去掉"geo:"部分

    # 提取视频链接
    videos = soup.find_all(['video', 'iframe', 'source'])
    for video in videos:
        src = video.get('src')
        if src:
            video_list.append(urljoin(base_url, src))
        elif video.name == 'iframe' and video.get('src'):
            video_list.append(urljoin(base_url, video.get('src')))

    # 提取图片链接
    images = soup.find_all('img')
    for img in images:
        src = img.get('src')
        data_src = img.get('data-src')
        if src and (src.lower().endswith('.jpg') or src.lower().endswith('.png')):
            image_list.append(urljoin(base_url, src))
        elif data_src and (data_src.lower().endswith('.jpg') or data_src.lower().endswith('.png')):
            image_list.append(urljoin(base_url, data_src))

    # 提取标题
    titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for title in titles:
        title_list.append(title.text.strip())

    # 提取 class 属性中包含 'title' 的元素内容
    class_titles = soup.find_all(class_=lambda x: x and 'title' in x)
    for class_title in class_titles:
        title_list.append(class_title.text.strip())

    return url_list, email_list, location_list, video_list, image_list, title_list

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

# 主函数
def main():
    save_folder = 'downloaded_图片'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 设置 Edge 选项
    edge_options = Options()
    edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    edge_options.add_argument("--disable-gpu")  # 禁用 GPU
    edge_options.add_argument("--no-sandbox")  # 禁用沙盒
    edge_options.add_argument("--log-level=3")  # 设置日志级别为 3，减少日志输出
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # 设置用户代理

    # 设置 EdgeDriver 服务
    # edge_driver_path = 'path/to/msedgedriver.exe'  # 替换为你的 EdgeDriver 路径
    # service = Service(edge_driver_path)

    # 启动 Edge 浏览器
    driver = webdriver.Edge(options=edge_options)

    all_url_list = []
    all_image_list = []
    all_title_list = []
    all_video_list = []

    for url in daohang_list:
        print(f"Fetching data from {url}")
        try:
            driver.get(url)
            # 滚动页面以触发懒加载
            scroll_to_bottom(driver)

            # 使用显式等待等待页面加载完成
            time.sleep(15)
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "app_hm"))
            # )

            # 获取页面内容
            html_content = driver.page_source
            # print(html_content)

            # 处理数据
            url_list, email_list, location_list, video_list, image_list, title_list = process_data(html_content, url)
            all_url_list.extend(url_list)
            all_image_list.extend(image_list)
            all_title_list.extend(title_list)
            all_video_list.extend(video_list)
            print(f'发现 {len(url_list)} URLs 从 {url}')
            print(f"发现 {len(image_list)} 图片 从 {url}")
            print(f"发现 {len(title_list)} 标题s 从 {url}")
            print(f"发现 {len(video_list)} videos 从 {url}")

            # 对应展示图片和标题
            for img_url, title, post_url in zip(image_list, title_list, url_list):
                print(f'\nArticle URL: {post_url}')
                print(f"Image URL: {img_url}")
                print(f"标题: {title}")

            # 对应展示视频
            for video_url in video_list:
                print(f"\nVideo URL: {video_url}")
                download_video(video_url, save_folder)

        except Exception as e:
            print(f"Error processing {url}: {e}")

    print("\n所有 图片 发现:")
    for img_url in all_image_list:
        print(img_url)

    print("\n所有 标题s 发现:")
    for title in all_title_list:
        print(title)

    print("\n所有 链接 发现:")
    for post_url in all_url_list:
        print(post_url)

    print("\n所有 视频 发现:")
    for video_url in all_video_list:
        print(video_url)

    driver.quit()

if __name__ == "__main__":
    main()
