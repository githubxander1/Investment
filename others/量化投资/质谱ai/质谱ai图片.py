import base64
from zhipuai import ZhipuAI

'''图片url或者base64编码。图像大小上传限制为每张图像 5M以下，且像素不超过 6000*6000。
支持jpg、png、jpeg格式。
说明： GLM-4V-Flash 不支持base64编码'''
def analyze_image(image_source, question, image_path=None, image_url=None, ):
    """
    分析图像内容，可以选择本地图片路径或图片URL
    :param image_source: 'local' 或 'url'
    :param image_path: 本地图片路径（如果 image_source 是 'local'）
    :param image_url: 图片URL（如果 image_source 是 'url'）
    :return: 分析结果
    """
    client = ZhipuAI(api_key="c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t")  # 请填写您自己的APIKey

    if image_source == 'local':
        if not image_path:
            raise ValueError("image_path is required when image_source is 'local'")
        with open(image_path, 'rb') as img_file:
            img_base = base64.b64encode(img_file.read()).decode('utf-8')
        content = [
            {
                "type": "image_base64",
                "image_base64": img_base
            },
            {
                "type": "text",
                "text": "图里有什么"
            }
        ]
    elif image_source == 'url':
        if not image_url:
            raise ValueError("图片URL 是必填项")
        content = [
            {
                "type": "text",
                "text": question
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            }
        ]
    else:
        raise ValueError("图片源必须是 'local' 或 'url")

    response = client.chat.completions.create(
        model="glm-4v-flash",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    return response.choices[0].message

# 示例调用：使用本地图片
question = "请分析图片内容，并给出分析结果"
local_image_path = r"D:\1document\1test\PycharmProject_gitee\others\量化投资\Quicker_20231015_132533.jpg"
result_local = analyze_image(image_source='local', question=question, image_path=local_image_path, )
print("分析结果如下:")
print(result_local)

# 示例调用：使用URL图片
# url_image_url = "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1703696400&t=f3028c7a1dca43a080aeb8239f09cc2f"
# url_image_url = r"D:\1document\1test\PycharmProject_gitee\zothers\量化投资\质谱ai\wx.png"
# result_url = analyze_image(image_source='url', image_url=url_image_url)
# print("\nURL Image Analysis Result:")
# print(result_url)
