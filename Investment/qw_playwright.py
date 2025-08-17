from openai import OpenAI
import subprocess
import tempfile
import os
from playwright.sync import sync_playwright

# 初始化通义千问3客户端（ModelScope接口）
client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key='ms-04756442-433d-4c9c-88c3-095de9dc36d3',  # 替换为你的ModelScope Token
)


def generate_browser_code(user指令):
    """调用Qwen3生成Playwright浏览器操作代码"""
    prompt = f"""
    请生成使用Playwright（Python）实现以下操作的代码：
    {user指令}

    要求：
    1. 代码必须可直接运行，包含完整的导入语句和执行逻辑
    2. 使用sync_playwright()同步模式
    3. 操作完成后自动关闭浏览器
    4. 若需要保存结果，使用截图功能（page.screenshot()），保存路径为当前目录
    5. 避免使用复杂语法，确保兼容性
    """

    # 调用Qwen3-Coder模型生成代码
    response = client.chat.completions.create(
        model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
        messages=[
            {'role': 'system', 'content': '你是专业的Python代码生成助手，擅长编写浏览器自动化脚本。'},
            {'role': 'user', 'content': prompt}
        ],
        stream=False  # 非流式获取完整代码
    )

    # 提取生成的代码（去除多余解释，只保留代码块）
    code = response.choices[0].message.content
    # 清理代码（去除可能的markdown标记）
    if '```python' in code:
        code = code.split('```python')[1].split('```')[0].strip()
    return code


def execute_browser_code(code):
    """执行生成的浏览器自动化代码"""
    try:
        # 创建临时文件保存代码
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file_path = f.name

        # 执行临时脚本
        result = subprocess.run(
            ['python', temp_file_path],
            capture_output=True,
            text=True
        )

        # 输出执行结果
        if result.returncode == 0:
            print("浏览器自动化操作成功！")
            print("输出日志：\n", result.stdout)
        else:
            print("操作失败，错误信息：\n", result.stderr)

    finally:
        # 清理临时文件
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


if __name__ == "__main__":
    # 1. 安装Playwright浏览器（首次运行需要）
    subprocess.run(['playwright', 'install', 'chromium'], check=True)

    # 2. 用户自然语言指令（可替换为其他需求）
    user指令 = """
    1. 打开Chrome浏览器，访问同花顺行情中心（https://hq.10jqka.com.cn/）
    2. 在搜索框输入"贵州茅台"并回车
    3. 等待页面加载完成后，截取当前页面并保存为"maotai_price.png"
    4. 关闭浏览器
    """

    # 3. 调用Qwen3生成浏览器操作代码
    print("正在生成浏览器自动化代码...")
    browser_code = generate_browser_code(user指令)
    print("生成的代码：\n", browser_code)

    # 4. 执行生成的代码
    print("\n开始执行浏览器操作...")
    execute_browser_code(browser_code)
