import os
from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

# 定义提取数据的结构模型
class Heading(BaseModel):
    model_name: str = Field('glm-4v-flash', description="Name of the OpenAI model.")
    input_fee: str = Field("爬取这个接口'https://weibo.com/newlogin?tabtype=search&gid=&openLoginLayer=0&url='，总结返回", description="Fee for input token for the OpenAI model.")
    output_fee: str = Field('总结结果', description="Fee for output token for the OpenAI model.")

# 设置要爬取的URL
url = 'https://weibo.com/newlogin?tabtype=search&gid=&openLoginLayer=0&url='  # 替换为实际要爬取的网址

# 创建WebCrawler实例并预热
crawler = WebCrawler()
crawler.warmup()

# 运行爬虫并提取数据
result = crawler.run(
    url=url,
    word_count_threshold=1,
    extraction_strategy=LLMExtractionStrategy(
        provider="glm-4v-flash",  # 假设的模型名称
        api_token=os.getenv('c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t'),  # 假设的API Key环境变量
        schema=Heading.schema(),
        extraction_type="schema",
        instruction="""From the crawled content, extract all the headings.
                       One extracted heading JSON format should look like this:
                       {"heading_text": "Example Heading"}."""
    ),
    bypass_cache=True
)

# 打印提取的内容
print(result.extracted_content)