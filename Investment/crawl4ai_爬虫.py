import os
import json
import asyncio
from dotenv import load_dotenv
from openai import OpenAI  # 改用OpenAI库方式调用

# 加载环境变量（通义千问API密钥）
load_dotenv()
# QWEN_API_KEY = os.getenv("QWEN_API_KEY")

# 使用与qwen3_bailian.py相同的配置
os.environ["OPENAI_API_KEY"] = "sk-5420708cfa8749f0aaf970fcf2da567d"
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def call_qwen3(prompt):
    """调用通义千问3 API，解析自然语言指令或提取数据"""
    try:
        completion = client.chat.completions.create(
            model="qwen3-coder-480b-a35b-instruct",  # 使用与qwen3_bailian.py相同的模型
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # 返回模型结果
        return completion.choices[0].message.content
    except Exception as e:
        return f"API调用失败: {str(e)}"


async def crawl_and_analyze(url, user_query):
    """
    1. 用crawl4ai爬取网页内容
    2. 用通义千问3解析内容，提取用户需要的信息
    """
    # 初始化crawl4ai爬虫（使用新的AsyncWebCrawler）
    from crawl4ai import AsyncWebCrawler
    
    try:
        # 创建异步爬虫实例
        async with AsyncWebCrawler() as crawler:
            # 爬取目标网页
            result = await crawler.arun(
                url=url,
                # 启用JavaScript渲染
                # 其他参数可以根据需要添加
            )

            # 若爬取成功，将页面内容和用户需求传给通义千问3
            if result.success:
                # 构造提示词：让AI根据用户需求解析爬取的内容
                prompt = f"""
我爬取了网页内容，需要你帮我提取信息。
用户需求：{user_query}
网页内容：{result.markdown[:5000]}  # 截取前5000字符避免过长
请以JSON格式返回结果，键名用中文（如"电影名称"、"评分"），只返回JSON，不添加其他内容。
"""
                # 调用通义千问3解析
                analysis_result = call_qwen3(prompt)
                # 打印原始结果用于调试
                print(f"API返回的原始结果: {analysis_result}")
                # 尝试解析为JSON（处理可能的格式错误）
                try:
                    # 检查返回结果是否以```json开头
                    if analysis_result.startswith("```json"):
                        analysis_result = analysis_result[7:-3]  # 去掉```json和```
                    return json.loads(analysis_result)
                except json.JSONDecodeError:
                    return {"error": "解析失败", "raw_result": analysis_result}
            else:
                return {"error": "爬取失败", "reason": result.error_message}
    except Exception as e:
        return {"error": "爬虫执行异常", "reason": str(e)}


async def main():
    # 目标URL：豆瓣电影Top250第一页
    target_url = "https://movie.douban.com/top250?start=0&filter="
    # 用户自然语言查询（可自定义）
    user_query = "提取前10部电影的名称、评分、导演和简介，忽略其他信息"

    # 执行爬取和分析
    result = await crawl_and_analyze(target_url, user_query)

    # 打印结果
    print("===== 爬取分析结果 =====")
    if "error" in result:
        print(f"错误: {result['error']}")
        # 如果有原始结果，也打印出来
        if "raw_result" in result:
            print(f"原始结果: {result['raw_result']}")
    else:
        for i, movie in enumerate(result, 1):
            print(f"\n第{i}部：")
            print(f"名称：{movie.get('电影名称', '未知')}")
            print(f"评分：{movie.get('评分', '未知')}")
            print(f"导演：{movie.get('导演', '未知')}")
            print(f"简介：{movie.get('简介', '未知')[:100]}...")  # 简介太长，截取前100字


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())