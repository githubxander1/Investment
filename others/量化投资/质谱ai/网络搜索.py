from zhipuai import ZhipuAI

search_prompt = """

# 以下是来自互联网的信息：
{search_result}

# 当前日期: 2024-XX-XX

# 要求：
根据最新发布的信息回答用户问题，当回答引用了参考信息时，必须在句末使用对应的[ref_序号]来标明参考信息来源。

"""

client = ZhipuAI(api_key=zhipu_api_key) # 填写您自己的APIKey

tools = [{
      "type": "web_search",
      "web_search": {
          "enable": True,#启用网络搜索 每次网络搜索大约会增加1000个 tokens 的消耗。
          "search_query": "最近国内有哪些新闻",#可以自定义搜索内容，提升搜索结果的相关性和精确度。 如果不传 search_query 参数，系统将根据用户的消息自动进行网页检索。
          "search_result": True,
          "search_prompt": search_prompt
      }
  }]


response = client.chat.completions.create(
# response = client.chat.asyncCompletions.create(  # 异步调用
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "总结文中的内容：https://www.chinanews.com.cn/cj/2024/07-05/10246755.shtml"
                                    "问：最近国内有哪些新闻，答："}
    ],
    top_p=0.7,
    temperature=0.1,
    tools=tools
)

print(response)