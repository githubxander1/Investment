from zhipuai import ZhipuAI
client = ZhipuAI(api_key="c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t")  # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4v-flash",  # 请填写您要调用的模型名称
    messages=[
        {"role": "user", "content": "作为一名情感恋爱大师，请为我，测试工程师，深圳工作，男等的社交形象一个吸引人的介绍，含多方面，至少200字"},
        {"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"},
        {"role": "assistant", "content": "恋爱大师"},
        {"role": "user", "content": "创作一个更精准且吸引人的介绍"}
    ],
)
print(response.choices[0].message)