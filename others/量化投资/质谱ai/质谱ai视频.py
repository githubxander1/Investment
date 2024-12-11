#视频理解示例、上传视频URL
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4v-flash",  # 填写需要调用的模型名称
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
                "url" : "https://www.ixigua.com/7445869578879500838"
            }
          },
          {
            "type": "text",
            "text": "请仔细描述这个视频"
          }
        ]
      }
    ]
)
print(response.choices[0].message)