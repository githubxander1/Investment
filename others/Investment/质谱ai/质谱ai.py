import textwrap

from zhipuai import ZhipuAI


def AIchat(content):
    client = ZhipuAI(api_key="c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t")  # 请填写您自己的APIKey

    response = client.chat.completions.create(
        model="glm-4v-flash",  # 请填写您要调用的模型名称
        temperature=0.9,
        response_format={
            "type": "text"
        },#返回格式json_object
        messages=[     #作为一名情感恋爱大师，
            # {"role": "system", "content": "恋爱大师"},
            # {"role": "user", "content": "请为我，测试工程师，深圳工作，男等的社交形象一个吸引人的交友介绍，含多方面，至少200字"},
            {"role": "user", "content": content},
            # {"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
            # {"role": "user", "content": "智谱AI开放平台"},
            # {"role": "user", "content": "创作一个更精准且吸引人的介绍"}
        ],
        # 调用工具
        tools=[
                    {
                        "type": "retrieval",
                        "retrieval": {
                            "knowledge_id": "your knowledge id",
                            "prompt_template": "从文档\n\"\"\"\n{{knowledge}}\n\"\"\"\n中找问题\n\"\"\"\n{{question}}\n\"\"\"\n的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。\n不要复述问题，直接开始回答。"
                        }
                    }
                    ],
        # stream=True,#使用同步调用时，此参数应当设置为 Fasle 或者省略。表示模型生成完所有内容后一次性返回所有内容。如果设置为 True，模型将通过标准 Event Stream ，逐块返回模型生成内容。Event Stream 结束时会返回一条data: [DONE]消息。
    )

    # 获取生成的回复内容
    generated_content = response.choices[0].message.content
    # 使用 textwrap 模块美化输出
    wrapped_content = textwrap.fill(generated_content, width=80)
    return wrapped_content


# content = "怎么成为系统学习网络安全"
# # 打印生成的内容
# response_content = AIchat(content)
# pprint(response_content)

# # 使用 textwrap 模块美化输出
# wrapped_content = textwrap.fill(response_content, width=80)
# print(wrapped_content)
