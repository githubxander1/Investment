from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re
import os

# 目标网页的URL列表
daohang_list = [
    'https://jr1hlbk.com/category/jrhl/',
    'https://jr1hlbk.com/category/tthl/',
    'https://jr1hlbk.com/category/whhl/',
    'https://jr1hlbk.com/category/fcmg/',
    'https://jr1hlbk.com/category/sszz/',
    'https://jr1hlbk.com/category/syfl/',
    'https://jr1hlbk.com/category/xyhl/',
    'https://jr1hlbk.com/category/gxqw/',
    'https://jr1hlbk.com/category/hltt/',
    'https://jr1hlbk.com/category/zthl/',
    'https://jr1hlbk.com/category/hjlt/',
    'https://jr1hlbk.com/category/zklq/',
    'https://jr1hlbk.com/category/CRDJ/'
]

# 获取网页内容的接口调用函数
def fetch_web_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

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

    card_url = []
    image_list = []
    title_list = []

    # 找到 id="archive" 和 role="main" 的容器
    archive_container = soup.find('div', id='archive', role='main')
    if not archive_container:
        print("Archive container not found")
        return url_list, email_list, location_list, video_list, card_url, image_list, title_list

    # 提取每个 article 标签中的内容
    articles = archive_container.find_all('article')
    for article in articles:
        # 提取文章链接
        post_card_a = article.find('a', href=True)
        if post_card_a:
            post_card_href = post_card_a.get('href')
            post_card_url = urljoin(base_url, post_card_href)
            url_list.append(post_card_url)

            # 提取图片链接
            img = article.find('img', class_='blog-background')
            if img:
                src = img.get('src')
                if src:
                    image_url = urljoin(base_url, src)
                    image_list.append(image_url)

        # 提取标题
        # title_h2 = post_card.find(class_=lambda x:x and 'title' in x)
        title_h2 = article.find('div', "post-card-title")
        if title_h2:
            title = title_h2.text.strip()
            title_list.append(title)

    return url_list, email_list, location_list, video_list, card_url, image_list, title_list


# 主函数
def main():
    all_card_url = []
    all_image_list = []
    all_title_list = []

    for url in daohang_list:
        print(f"Fetching data from {url}")
        html_content = fetch_web_content(url)
        if html_content:
            url_list, email_list, location_list, video_list, card_url, image_list, title_list = process_data(html_content, url)
            all_card_url.extend(url_list)
            all_image_list.extend(image_list)
            all_title_list.extend(title_list)
            print(f'Found {len(url_list)} URLs from {url}')
            print(f"Found {len(image_list)} images from {url}")
            print(f"Found {len(title_list)} titles from {url}")

            # 对应展示图片和标题
            for img_url, title, url in zip(image_list, title_list, url_list):
                print(f'\nurl: {url}')
                print(f"Image URL: {img_url}")
                print(f"Title: {title}")

    # print("\nAll images found:")
    # for img_url in all_image_list:
    #     print(img_url)
    #
    # print("\nAll titles found:")
    # for title in all_title_list:
    #     print(title)

if __name__ == "__main__":
    main()
