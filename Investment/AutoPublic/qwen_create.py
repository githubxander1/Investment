import random
import time

from openai import OpenAI


def get_hot_topics_from_ai(max_retries=3, timeout=30):
    """
    使用Qwen大模型获取当前热门话题
    """
    # Qwen API配置
    qwen_client = OpenAI(
        base_url='https://api-inference.modelscope.cn/v1',
        api_key='ms-04756442-433d-4c9c-88c3-095de9dc36d3',  # ModelScope Token
    )

    for attempt in range(max_retries):
        try:
            prompt = """
            请提供10个当前在中文互联网上热门、高关注度且贴近生活的话题，要求：
            1. 话题要具体、细化，避免过于宽泛，如"旅行"应具体为"周末短途旅行推荐"等
            2. 贴近普通人日常生活，如职场、家庭、情感、消费、教育等具体场景
            3. 具有实用价值或情感共鸣，能引起读者兴趣
            4. 每个话题简洁明了，不超过15个字
            5. 直接列出话题，每行一个，不要序号和其他说明

            示例格式：
            周末短途旅行推荐
            家庭收纳小妙招
            职场新人沟通技巧
            ...
            """

            response = qwen_client.chat.completions.create(
                model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的热点话题分析师，擅长发现和总结当前热门且贴近普通人生活的话题。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500,
                timeout=timeout
            )

            # 解析AI返回的话题列表
            topics_text = response.choices[0].message.content.strip()
            print(f"AI返回的话题列表：{topics_text}")
            topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()]

            # 过滤掉太长或无效的话题
            topics = [topic for topic in topics if len(topic) <= 20 and len(topic) > 2]

            if topics:
                print(f"AI推荐的热门话题: {topics}")
                return topics
            else:
                print("AI未返回有效话题，使用默认话题")
                # return get_default_topics()

        except Exception as e:
            print(f"获取AI推荐话题失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            # return get_default_topics()

    print("达到最大重试次数，无法获取AI推荐话题")
    return []


# qwen生成文章
def generate_article_with_qwen(topic, max_retries=3, timeout=60):
    """
    使用Qwen大模型获取当前热门话题
    """
    # Qwen API配置
    qwen_client = OpenAI(
        base_url='https://api-inference.modelscope.cn/v1',
        api_key='ms-04756442-433d-4c9c-88c3-095de9dc36d3',  # ModelScope Token
    )

    for attempt in range(max_retries):
        try:
            prompt = f"""
            请围绕"{topic}"这个主题，创作一篇适合在今日头条发布的文章，要求如下：

            1. 标题要求：
               - 吸引眼球但不过分夸张
               - 包含数字或利益点
               - 字数控制在20字以内

            2. 正文要求：
               - 开头用黄金7秒原则抓住注意力
               - 内容要有信息增量，每500字左右插入反常识观点
               - 语言风格轻松自然，像和朋友聊天
               - 结尾要有互动引导
               - 总字数控制在1500-2000字左右

            3. 内容结构：
               - 开头：引人入胜的开场
               - 主体：分段论述，逻辑清晰
               - 结尾：总结并引导互动

            请直接输出标题和正文，格式如下：
            <title>文章标题</title>
            <content>文章正文内容</content>
            不要含
            """

            response = qwen_client.chat.completions.create(
                model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的自媒体内容创作者，擅长创作适合今日头条平台的高质量文章。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                timeout=timeout
            )

            # 解析AI返回的内容
            article_content = response.choices[0].message.content.strip()
            print(f"AI生成文章内容：{article_content}")

            # time.sleep(60)
            # 提取标题和正文
            import re
            title_match = re.search(r'<title>(.*?)</title>', article_content, re.DOTALL)
            content_match = re.search(r'<content>(.*?)</content>', article_content, re.DOTALL)
            print("标题：", title_match, "正文：", content_match)

            title = title_match.group(1).strip() if title_match else ""
            content = content_match.group(1).strip() if content_match else ""

            if title and content:
                print(f"AI生成文章标题：{title}")
                return title, content
            else:
                print("AI未返回有效文章内容")
                return None, None

        except Exception as e:
            print(f"使用AI生成文章失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            return None, None


if __name__ == '__main__':
    topics = get_hot_topics_from_ai()
    print(topics)
    if topics:
        random_one_topic = random.choice(topics)
        print(generate_article_with_qwen(random_one_topic))
