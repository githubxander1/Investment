import json
import logging
import uuid
from textwrap import fill

import requests

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_key = "c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t"

def run_v4_sync(content):
    msg = [
        {
            "role": "user",
            "content": content
        }
    ]
    tool = "web-search-pro"
    url = "https://open.bigmodel.cn/api/paas/v4/tools"
    request_id = str(uuid.uuid4())
    data = {
        "request_id": request_id,
        "tool": tool,
        "stream": False,
        "messages": msg
    }

    try:
        resp = requests.post(
            url,
            json=data,
            headers={'Authorization': api_key},
            timeout=300
        )
        resp.raise_for_status()  # 检查响应状态码
    except requests.exceptions.RequestException as e:
        logging.error(f"请求失败: {e}")
        return None

    # 解析响应内容
    response_content = resp.json()
    choices = response_content.get("choices", [])

    results = []
    for choice in choices:
        message = choice.get("message", {})
        tool_calls = message.get("tool_calls", [])

        for tool_call in tool_calls:
            search_results = tool_call.get("search_result", [])

            for result in search_results:
                title = result.get("title", "")
                content = result.get("content", "")
                link = result.get("link", "")

                formatted_result = {
                    '标题': title,
                    '链接': link,
                    '内容': fill(content, width=80)
                }
                results.append(formatted_result)

                print(f"### 标题: {title}\n")
                print(formatted_result['内容'])
                print(f"\n链接: {link}\n")
                print("-" * 80 + "\n")

    return results

def save_to_file(data, file_path):
    '''
    将数据保存到文件中

    参数：
    testdata: 要保存的数据
    file_path: 文件名，包括路径
    '''
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            logging.info(f"数据已保存到文件：{file_path}")
    except IOError as e:
        logging.error(f"保存文件时发生错误：{e}")

if __name__ == '__main__':
    content = "请用中文回答：怎么系统学习ai"
    response = run_v4_sync(content)
    if response:
        save_to_file(response, "联搜索结果1.txt")
