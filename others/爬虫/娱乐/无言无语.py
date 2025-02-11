import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 初始化UserAgent
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

def fetch_page(url, headers):
    """
    发送HTTP请求获取页面内容
    :param url: 目标URL
    :param headers: 请求头
    :return: 页面内容
    """
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return response.text

def parse_content(html):
    """
    解析HTML内容，提取所需信息
    :param html: HTML内容
    :return: 提取的内容列表
    """
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='post', itemscope=True, itemtype='http://schema.org/BlogPosting')
    contents = []

    for article in articles:
        content_div = article.find('div', class_='post-content', itemprop='articleBody')
        if content_div:
            content = content_div.get_text(strip=True)
            contents.append(content)

    return contents

def save_to_file(contents, filename='output.txt'):
    """
    将内容保存到文件
    :param contents: 内容列表
    :param filename: 文件名
    """
    with open(filename, 'a', encoding='utf-8') as f:
        for content in contents:
            f.write(content + '\n')

def main(times, base_url='https://www.nihaowua.com/page/'):
    """
    主函数，控制爬虫流程
    :param times: 需要抓取的内容数量
    :param base_url: 基础URL
    """
    count = 0
    page = 1
    seen_contents = set()  # 用于存储已抓取的内容，避免重复

    while count < times:
        url = f'{base_url}{page}/'
        html = fetch_page(url, headers)
        contents = parse_content(html)

        for content in contents:
            if content not in seen_contents:
                seen_contents.add(content)
                save_to_file([content], '污言污语.txt')
                count += 1
                print(f'正在抓取，第{count}次，内容为：{content}')
                if count == times:
                    return

        page += 1  # 进入下一页

if __name__ == '__main__':
    main(30)
