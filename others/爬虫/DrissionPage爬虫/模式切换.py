from DrissionPage import WebPage
import time

def extract_info(page):
    # 使用 XPath 表达式选择元素
    items = page.eles('//div[contains(@class, "card") and contains(@class, "border-1") and contains(@class, "mb-3")]')
    if not items:
        print('No items found')
        return

    for item in items:
        title = item.ele('.//a[contains(@class, "title")]').text if item.ele('.//a[contains(@class, "title")]') else "标题未找到"
        description = item.ele('.//div[contains(@class, "card-text")]//div[contains(@class, "col-12") and contains(@class, "outline") and contains(@class, "text-secondary")]').text if item.ele('.//div[contains(@class, "card-text")]//div[contains(@class, "col-12") and contains(@class, "outline") and contains(@class, "text-secondary")]') else "描述未找到"
        yield title, description

# 创建页面对象
page = WebPage()
# 访问网址
page.get('https://gitee.com/explore')

# 控制浏览器，模拟点击搜索
page('#q').input('DrissionPage')
page('t:button@tx():搜索').click()
page.wait.load_start()

# 增加等待时间，确保页面加载完成
time.sleep(10)  # 等待10秒

# 提取信息
info_list = list(extract_info(page))

# 打印结果
if not info_list:
    print("未提取到任何信息")
else:
    for title, description in info_list:
        print(f"Title: {title}")
        print(f"Description: {description}\n")
