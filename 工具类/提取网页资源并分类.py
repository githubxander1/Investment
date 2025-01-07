from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re

# 目标网页的URL列表

# 获取网页内容的接口调用函数
def fetch_web_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url,headers=headers)
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
        elif video.name == 'iframe' and 'youtube' in video.get('src', ''):
            video_list.append(urljoin(base_url, video.get('src')))

    # 提取图片链接
    images = soup.find_all('img')
    for img in images:
        src = img.get('src')
        if src and src.lower().endswith('.jpg'):
            image_list.append(urljoin(base_url, src))

    # 提取标题
    titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for title in titles:
        title_list.append(title.text.strip())

    # 提取 class 属性中包含 'title' 的元素内容
    class_titles = soup.find_all(class_=lambda x: x and 'title' in x)
    for class_title in class_titles:
        title_list.append(class_title.text.strip())

    return url_list, email_list, location_list, video_list, image_list, title_list

# 主函数
def main(url_lists):
    all_image_list = []
    all_title_list = []

    for url in url_lists:
        print(f"Fetching data from {url}")
        html_content = fetch_web_content(url)
        print(html_content)
        if html_content:
            url_list, email_list, location_list, video_list, image_list, title_list = process_data(html_content, url)
            all_image_list.extend(image_list)
            all_title_list.extend(title_list)
            print(f" {len(image_list)} PNG images from {url}")
            print(f" {len(title_list)} 标题提取 from {url}")

    print("\nAll PNG images found:")
    for img_url in all_image_list:
        print(img_url)

    print("\nAll 标题提取 found:")
    for title in all_title_list:
        print(title)

if __name__ == "__main__":
    url_lists = ['https://fylhfyullx.top:2568/picdetail/9481011.html']
    main(url_lists)
    # content = fetch_web_content(url_list)
    # process_data(content,url_list)
