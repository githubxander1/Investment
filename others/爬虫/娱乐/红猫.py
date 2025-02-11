import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup


def extract_menu_items(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    menu_items = []

    # 找到所有的<ul>标签
    ul_tags = soup.find_all('ul')

    for ul in ul_tags:
        # 找到所有的<li>标签
        li_tags = ul.find_all('li')
        for li in li_tags:
            # 找到所有的<a>标签
            a_tag = li.find('a')
            if a_tag:
                title = a_tag.get_text(strip=True)
                link = a_tag.get('href')
                menu_items.append((title, link))

    return menu_items

def fetch_page(url, headers):
    """
    发送HTTP请求获取页面内容
    :param url: 目标URL
    :param headers: 请求头
    :return: 页面内容
    """
    # response = requests.get(url, headers=headers)
    # response.encoding = 'utf-8'
    # return response.text
    # 发送HTTP请求获取网页内容
    url = "https://fylhfyullx.top:2568/piclist/45.html"  # 请将此处替换为实际的网页地址
    response = requests.get(url)
    if response.status_code == 200:
        # 设置正确的编码（如果需要）
        response.encoding = response.apparent_encoding
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        # 定位id为menu的元素
        menu_elements = soup.find_all(id="menu")
        # 假设选中的是第一个（如果有多个，可以根据实际情况选择索引或其他判断条件）
        selected_menu = menu_elements[6] if menu_elements else None
        if selected_menu:
            print(selected_menu)
            return selected_menu
        else:
            print("未找到id为menu的元素")
    else:
        print(f"请求失败，状态码: {response.status_code}")
def main():
    base_url = 'https://fylhfyullx.top:2568/piclist/45.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    html_content = fetch_page(base_url, headers)
    menu_items = extract_menu_items(html_content)

    # fortitle, link in menu_items:

main()