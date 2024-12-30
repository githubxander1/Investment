from pprint import pprint
import textwrap
from zhipuai import ZhipuAI
from pathlib import Path
import json

# 填写您自己的APIKey
client = ZhipuAI(api_key="c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t")

# 格式限制：.PDF .DOCX .DOC .XLS .XLSX .PPT .PPTX .PNG .JPG .JPEG .CSV .PY .TXT .MD .BMP .GIF
# 大小：单个文件50M、总数限制为100个文件
file_object = client.files.create(file=Path("面试通关大课-核心材料准备-课件.pdf"), purpose="file-extract")

# 获取文本内容
file_content = json.loads(client.files.content(file_id=file_object.id).content)["content"]

# 生成请求消息
message_content = f"请对\n{file_content}\n的内容进行分析，并撰写一份摘要。"

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[{"role": "user", "content": message_content}],
)

# 获取摘要内容
summary = response.choices[0].message.content

# 格式化输出
formatted_summary = textwrap.fill(summary, width=80)

# 打印格式化后的摘要
print(formatted_summary)

# 保存摘要到文件
output_file_path = "面试通关大课-核心材料准备-摘要.txt"
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(formatted_summary)

logger.info(f"摘要已保存到文件: {output_file_path}")
