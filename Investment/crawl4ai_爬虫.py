import os
import json
from dotenv import load_dotenv
from crawl4ai import WebCrawler
import requests

# 加载环境变量（通义千问API密钥）
load_dotenv()
# QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_ENDPOINT = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
QWEN_API_KEY = "ms-04756442-433d-4c9c-88c3-095de9dc36d3"
# QWEN_ENDPOINT = "https://api-inference.modelscope.cn/v1'"


def call_qwen3(prompt):
    """调用通义千问3 API，解析自然语言指令或提取数据"""
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        # "model": "Qwen/Qwen3-Coder-480B-A35B-Instruct",  # 使用通义千问3的免费模型
        "model": "qwen-turbo",  # 使用通义千问3的免费模型
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(QWEN_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API调用失败: {str(e)}"


def crawl_and_analyze(url, user_query):
    """
    1. 用crawl4ai爬取网页内容
    2. 用通义千问3解析内容，提取用户需要的信息
    """
    # 初始化crawl4ai爬虫（启用AI增强模式）
    crawler = WebCrawler()

    try:
        # 爬取目标网页（豆瓣电影Top250）
        result = crawler.crawl(
            url=url,
            mode="ai_enhanced",  # 启用AI增强，自动处理JavaScript渲染和反爬
            extract_structured_data=True  # 让crawl4ai初步提取结构化数据
        )

        # 若爬取成功，将页面内容和用户需求传给通义千问3
        if result.success:
            # 构造提示词：让AI根据用户需求解析爬取的内容
            prompt = f"""
            我爬取了网页内容，需要你帮我提取信息。
            用户需求：{user_query}
            网页内容：{result.content[:5000]}  # 截取前5000字符避免过长
            请以JSON格式返回结果，键名用中文（如"电影名称"、"评分"），只返回JSON，不添加其他内容。
            """
            # 调用通义千问3解析
            analysis_result = call_qwen3(prompt)
            # 尝试解析为JSON（处理可能的格式错误）
            try:
                return json.loads(analysis_result)
            except json.JSONDecodeError:
                return {"error": "解析失败", "raw_result": analysis_result}
        else:
            return {"error": "爬取失败", "reason": result.error_message}

    finally:
        crawler.close()  # 关闭爬虫资源


if __name__ == "__main__":
    # 目标URL：豆瓣电影Top250第一页
    target_url = "https://movie.douban.com/top250?start=0&filter="
    # 用户自然语言查询（可自定义）
    user_query = "提取前10部电影的名称、评分、导演和简介，忽略其他信息"

    # 执行爬取和分析
    result = crawl_and_analyze(target_url, user_query)

    # 打印结果
    print("===== 爬取分析结果 =====")
    if "error" in result:
        print(f"错误: {result['error']}")
    else:
        for i, movie in enumerate(result, 1):
            print(f"\n第{i}部：")
            print(f"名称：{movie.get('电影名称', '未知')}")
            print(f"评分：{movie.get('评分', '未知')}")
            print(f"导演：{movie.get('导演', '未知')}")
            print(f"简介：{movie.get('简介', '未知')[:100]}...")  # 简介太长，截取前100字
