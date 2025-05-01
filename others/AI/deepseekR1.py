import json
from pprint import pprint

import requests


def deepseekR1(content):
    url = "https://aistudio.baidu.com/llm/lmapi/v3/chat/completions"

    headers = {
        'Authorization': "Bearer f1fe73e8d5aa997da6fc4a9164e8844ea29c8e86",
        'Content-Type': "application/json"
    }

    payload = json.dumps({
        "model": "deepseek-r1",
        "messages": [
            {
                "role": "system",  # AI的角色
                "content": "斯诺克高手台球专家"
            },
            {
                "role": "user",  # 用户角色
                "content": content
            }
        ],
        "stream": False,
        "temperature": 0.7  # 模型采样温度，默认为0.7,数值越高 AI 输出的结果越随机
    })

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            pprint(data)
            choices = data.get('choices', [])
            if choices:
                content_result = choices[0]['message']['content']
                reasoning_content = choices[0].get('reasoning_content', '')
                return {
                    'content': content_result,
                    'reasoning_content': reasoning_content
                }
            else:
                print("choices为空")
                return {'content': '', 'reasoning_content': ''}
        except (KeyError, ValueError) as e:
            print(f"解析响应失败: {e}")
            return {'content': '', 'reasoning_content': ''}
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print("响应内容：", response.json())
        return {'content': '', 'reasoning_content': ''}

if __name__ == '__main__':
    content = "请给出一个关于斯诺克的入门到放弃的全教程，含练习"
    result = deepseekR1(content)
    print("\nAI 推理过程：\n", result['reasoning_content'])
    print("AI 回答内容：\n", result['content'])
