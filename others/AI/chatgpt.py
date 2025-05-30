from pprint import pprint
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

# 初始化客户端
client = OpenAI(api_key="sk-proj-nBWz_E8dP76OlnFzyhw5-3YG4-jmaPZPBTTvFAFSvkanqVLYEYH0W04f7d-Dmy0IlLAAwLnNDrT3BlbFJ4r9Susoi2AMHZLXvNoKyVXrkKFy2DYi7-1FyrZQihySk8FoCZeBJ14-KMlsZmbHePx-zvKKSgA")

# 使用指定类型构造用户消息
user_message = ChatCompletionUserMessageParam(role="user", content="生成一个关于机器学习的系统教程")

# 发起请求
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[user_message]
)

# 输出响应
pprint(response)

# response = client.response.create(
#     model="gpt-4.1",
#     input=[
#         {"role": "user", "content": "what teams are playing in this image?"},
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "input_image",
#                     "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg"
#                 }
#             ]
#         }
#     ]
# )
#
# print(response.output_text)