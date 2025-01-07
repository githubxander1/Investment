from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re

# 目标网页的URL列表
daohang_list = [
    'https://jr1hlbk.com/archives/83782.html',
    # 'https://jr1hlbk.com/category/tthl/',
    # 'https://jr1hlbk.com/category/whhl/',
    # 'https://jr1hlbk.com/category/fcmg/',
    # 'https://jr1hlbk.com/category/sszz/',
    # 'https://jr1hlbk.com/category/syfl/',
    # 'https://jr1hlbk.com/category/xyhl/',
    # 'https://jr1hlbk.com/category/gxqw/',
    # 'https://jr1hlbk.com/category/hltt/',
    # 'https://jr1hlbk.com/category/zthl/',
    # 'https://jr1hlbk.com/category/hjlt/',
    # 'https://jr1hlbk.com/category/zklq/',
    # 'https://jr1hlbk.com/category/CRDJ/'
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

    # # 找到 id="archive" 和 role="main" 的容器
    archive_container = soup.find('vedio', preload='auto')
    # if not archive_container:
    #     print("Archive container not found")
    #     return url_list, email_list, location_list, video_list, image_list, title_list
    #
    # # 提取 URL
    # post_cards = archive_container.find_all('a')
    # for post_card in post_cards:
    #     # 提取文章链接
    #     post_card_href = post_card.get('href')
    #     if post_card_href:
    #         post_card_url = urljoin(base_url, post_card_href)
    #         url_list.append(post_card_url)
    #
    #         # 提取图片链接
    #         img = post_card.find('img')
    #         if img:
    #             src = img.get('src')
    #             if src:
    #                 image_url = urljoin(base_url, src)
    #                 image_list.append(image_url)
    #
    #         # 提取标题
    #         title_h2 = post_card.find('h2', class_='post-card-title')
    #         if title_h2:
    #             title_list.append(title_h2.text.strip())
    #         else:
    #             title_div = post_card.find('div', class_='post-card-title')
    #             if title_div:
    #                 title_list.append(title_div.text.strip())

    # 提取视频链接
    video_containers = archive_container.find_all('div', class_='plyr__video-wrapper')
    for video_container in video_containers:
        video = video_container.find('video')
        if video:
            source = video.find('source')
            if source:
                src = source.get('src')
                if src:
                    video_url = urljoin(base_url, src)
                    video_list.append(video_url)
    # url_list, email_list, location_list,, image_list, title_list
    return video_list

# 主函数
def main():
    all_image_list = []
    all_title_list = []
    all_url_list = []
    all_video_list = []

    for url in daohang_list:
        print(f"Fetching data from {url}")
        html_content = fetch_web_content(url)
        if html_content:
            # url_list, email_list, location_list, video_list, image_list, title_list = process_data(html_content, url)
            video_list = process_data(html_content, url)
            # all_url_list.extend(url_list)
            # all_image_list.extend(image_list)
            # all_title_list.extend(title_list)
            all_video_list.extend(video_list)
            # print(f"Found {len(image_list)} images from {url}")
            # print(f"Found {len(title_list)} titles from {url}")
            print(f"Found {len(video_list)} videos from {url}")

            # # 对应展示图片和标题
            # for img_url, title, post_url in zip(image_list, title_list, url_list):
            #     print(f"\nArticle URL: {post_url}")
            #     print(f"Image URL: {img_url}")
            #     print(f"Title: {title}")

            # 对应展示视频
            for video_url in video_list:
                print(f"\nVideo URL: {video_url}")

    # print("\nAll images found:")
    # for img_url in all_image_list:
    #     print(img_url)
    #
    # print("\nAll titles found:")
    # for title in all_title_list:
    #     print(title)
    #
    # print("\nAll URLs found:")
    # for post_url in all_url_list:
    #     print(post_url)

    print("\nAll videos found:")
    for video_url in all_video_list:
        print(video_url)

if __name__ == "__main__":
    main()
