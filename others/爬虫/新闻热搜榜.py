from pprint import pprint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def get_news_baidu(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_list = []
    for item in soup.find_all('div', class_="content_1YWBm"):
        news_title = item.find('div', class_="c-single-text-ellipsis")
        news_url = item.find('a', href=True)
        if news_title and news_url:
            news_list.append({'title': news_title.text.strip(), 'url': news_url['href']})
    return news_list

def get_news_sogou(url):
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    wd = webdriver.Edge(options)
    wd.get(url)
    soup = BeautifulSoup(wd.page_source, 'html.parser')
    # print(soup)

    news_list = []
    for item in soup.find_all('td'):
        url = item.find('a', href=True)
        if url:
            news_list.append({'title': url.text.strip(), 'url': url['href']})
    wd.quit()  # 关闭浏览器
    return news_list

def get_news(urls):
    all_news = []
    for url in urls:
        if 'baidu' in url:
            all_news.extend(get_news_baidu(url))
        elif 'so.com' in url:
            all_news.extend(get_news_sogou(url))
    return all_news

def print_news(news_data):
    for news in news_data:
        print(f"{news['title']} ({news['url']})")

if __name__ == '__main__':
    urls = [
        'https://top.baidu.com/board?tab=realtime',
        'https://trends.so.com/hot'
    ]
    news_data = get_news(urls)
    print_news(news_data)

    # 使用 pandas 数据框展示
    df = pd.DataFrame(news_data)
    df['News'] = df['title'] + ' (' + df['url'] + ')'
    print(df[['News']])
