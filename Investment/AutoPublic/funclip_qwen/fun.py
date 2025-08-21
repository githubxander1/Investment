import subprocess
import os

'git clone https://gitee.com/aiwep/FunClip.git'
def auto_clip_video(input_video_path, output_video_path, keywords):
    """
    使用funclip自动剪辑视频
    """
    try:
        # 使用funclip命令行工具进行剪辑
        cmd = [
            'python', '-m', 'funclip',
            'autosub',  # 自动剪辑模式
            '--input', input_video_path,
            '--output', output_video_path,
            '--keywords', keywords  # 根据关键词剪辑
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"视频剪辑成功: {output_video_path}")
            return True
        else:
            print(f"视频剪辑失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"视频剪辑出错: {e}")
        return False
from openai import OpenAI

def generate_video_content(topic):
    """
    使用Qwen大模型生成视频标题和描述
    """
    qwen_client = OpenAI(
        base_url='https://api-inference.modelscope.cn/v1',
        api_key='ms-04756442-433d-4c9c-88c3-095de9dc36d3',
    )

    try:
        prompt = f"""
        请为"{topic}"这个主题创作一个吸引人的视频标题和描述，要求如下：
        
        1. 标题要求：
           - 吸引眼球但不过分夸张
           - 包含数字或利益点
           - 字数控制在20字以内
           
        2. 描述要求：
           - 简要介绍视频内容
           - 引导用户观看和互动
           - 字数控制在100字以内
           
        请直接输出标题和描述，格式如下：
        <title>视频标题</title>
        <description>视频描述</description>
        """

        response = qwen_client.chat.completions.create(
            model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的短视频内容创作者，擅长创作吸引人的视频标题和描述。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        # 解析AI返回的内容
        content = response.choices[0].message.content.strip()
        import re
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        desc_match = re.search(r'<description>(.*?)</description>', content, re.DOTALL)

        title = title_match.group(1).strip() if title_match else f" {topic}的精彩内容"
        description = desc_match.group(1).strip() if desc_match else f"欢迎观看关于{topic}的视频，记得点赞关注哦！"

        return title, description

    except Exception as e:
        print(f"使用AI生成视频内容失败: {e}")
        return f" {topic}的精彩内容", f"欢迎观看关于{topic}的视频，记得点赞关注哦！"
def send_video_with_qwen(page, video_path, topic):
    """使用Qwen大模型生成内容并发布视频"""
    # 进入创作页面
    start_creat = page.get_by_role("link", name="开始创作")
    if start_creat.is_visible():
        start_creat.click()
    page.get_by_role("link", name="视频").click()

    # 上传视频文件
    file_input = page.locator("input[type='file']")
    file_input.set_input_files(video_path)

    # 等待上传完成
    page.wait_for_selector(".upload-success", timeout=60000)

    # 获取AI生成的标题和描述
    ai_title, ai_description = generate_video_content(topic)

    # 填入标题
    page.get_by_role("textbox", name="请输入作品标题").fill(ai_title)

    # 填入描述
    description_editor = page.locator("div").filter(has_text=re.compile(r"^添加作品描述"))
    if description_editor.is_visible():
        description_editor.fill(ai_description)

    # 点击发布
    page.get_by_role("button", name="发布").click()

    print(f"视频发布成功: {ai_title}")
def auto_video_publish_workflow():
    """
    自动视频发布完整工作流程
    """
    # 1. 选择或生成视频素材
    # 这里可以根据需要从素材库选择或生成视频

    # 2. 使用AI确定视频主题
    topics = get_hot_topics_from_ai()
    selected_topic = topics[0] if topics else "生活技巧"

    # 3. 自动剪辑视频
    input_video = "path/to/raw_video.mp4"
    output_video = "path/to/clipped_video.mp4"

    if auto_clip_video(input_video, output_video, selected_topic):
        # 4. 发布到今日头条
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False, args=['--start-maximized'])
            context = browser.new_context()
            page = context.new_page()

            # 登录逻辑（复用您现有的代码）
            login_and_save_state(page, context)

            # 发布视频
            send_video_with_qwen(page, output_video, selected_topic)

            context.close()
            browser.close()
    else:
        print("视频剪辑失败，终止发布流程")
