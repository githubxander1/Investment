
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t")  # 请填写您自己的APIKey

# 创建知识库
result = client.knowledge.create(
    embedding_id=3,
    name="knowledge name",
    description="knowledge description"
)
print(result.id)

# 上传文件
resp = client.knowledge.document.create(
    file=open("xxx.xlsx", "rb"),
    purpose="retrieval",
    knowledge_id="1798330146986561536",
    sentence_size=202,
    custom_separator=["\n"]
)
print(resp)