
#访问百度网站
import requests

def get_html():
    url = 'https://www.baidu.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    response = requests.get(url=url,headers=headers)
    print(response.headers)
get_html()