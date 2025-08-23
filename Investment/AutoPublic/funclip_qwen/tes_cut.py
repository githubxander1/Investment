import os
import sys
import time
from openai import OpenAI

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from Investment.AutoPublic.funclip_qwen.fun import auto_clip_video, generate_video_content

def get_video_keywords_from_ai(video_topic):
    """
    使用AI分析视频主题并生成剪辑关键词
    """
    client = OpenAI(
        base_url='https://api-inference.modelscope.cn/v1',
        api_key='ms-04756442-433d-4c9c-88c3-095de9dc36d3',
    )

    try:
        prompt = f"""
        请为"{video_topic}"这个视频主题生成适合自动剪辑的关键词，要求如下：
        
        1. 分析视频可能包含的重要内容片段
        2. 提取3-5个最能代表视频精华内容的关键词或短语
        3. 关键词应该具体且具有辨识度，便于精准剪辑
        4. 每个关键词用逗号分隔
        
        直接输出关键词，无需额外说明，例如：
        关键词1,关键词2,关键词3
        """

        response = client.chat.completions.create(
            model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的视频编辑师，擅长分析视频内容并提取关键片段。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200
        )

        keywords = response.choices[0].message.content.strip()
        return keywords

    except Exception as e:
        print(f"使用AI生成关键词失败: {e}")
        # 返回默认关键词
        return "重要,精华,关键,重点,亮点"

def analyze_video_content(video_path):
    """
    分析视频内容并确定主题（模拟实现）
    在实际应用中，这里可以集成视频内容分析模型
    """
    # 从文件名推断视频主题
    filename = os.path.basename(video_path)
    topic = os.path.splitext(filename)[0]  # 移除扩展名
    # 简单处理文件名，将下划线和连字符替换为空格
    topic = topic.replace('_', ' ').replace('-', ' ')
    return topic

def ai_powered_video_clip(input_video_path, output_video_path):
    """
    使用AI智能剪辑视频
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_video_path):
        print(f"错误: 找不到输入视频文件 '{input_video_path}'")
        print("请确保在指定路径下放置需要剪辑的视频文件")
        return False

    # 分析视频内容确定主题
    video_topic = analyze_video_content(input_video_path)
    print(f"检测到视频主题: {video_topic}")

    # 使用AI生成剪辑关键词
    keywords = get_video_keywords_from_ai(video_topic)
    print(f"AI生成的剪辑关键词: {keywords}")

    # 使用FunClip自动剪辑视频
    print(f"开始使用AI生成的关键词剪辑视频: {input_video_path}")
    success = auto_clip_video(input_video_path, output_video_path, keywords)

    if success:
        print(f"视频剪辑完成: {output_video_path}")
        # 生成视频标题和描述
        title, description = generate_video_content(video_topic)
        print(f"AI生成的标题: {title}")
        print(f"AI生成的描述: {description}")
    else:
        print("视频剪辑失败")

    return success

def clip_test_video():
    """
    剪辑test_video文件
    """
    # 定义输入和输出路径 - 使用原始字符串避免转义问题
    input_video_path = r"D:\1document\Investment\Investment\AutoPublic\funclip_qwen\test_vedio.mp4"  # 输入视频文件
    output_video_path = "clipped_test_video.mp4"  # 输出剪辑后的视频文件

    # 使用AI智能剪辑视频
    return ai_powered_video_clip(input_video_path, output_video_path)

if __name__ == "__main__":
    clip_test_video()
