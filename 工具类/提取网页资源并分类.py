from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import re

# 目标网页的URL
# url = "https://45thlbk.com/"
url = "https://45thlbk.com/archives/2427.html"

# 获取网页内容
response = requests.get(url)
html_content = response.content

# 解析网页内容
soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有链接地址
links = soup.find_all('a')

# 初始化分类存储
url_list = []
email_list = []
location_list = []
video_list = []
image_list = []

# 分类提取
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
        video_list.append(urljoin(url, src))
    elif video.name == 'iframe' and 'youtube' in video.get('src', ''):
        video_list.append(urljoin(url, video.get('src')))

# 提取图片链接
images = soup.find_all('img')
for img in images:
    src = img.get('src')
    if src:
        image_list.append(urljoin(url, src))

# 打印结果
print("URLs:", url_list)
print("Emails:", email_list)
print("Locations:", location_list)
print("Videos:", video_list)
print("Images:", image_list)
