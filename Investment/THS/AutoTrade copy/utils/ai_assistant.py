import uiautomator2
from openai import OpenAI
import json
import time
import base64

# 初始化千问API客户端
class AIAssistant:
    def __init__(self):
        self.client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key='ms-04756442-433d-4c9c-88c3-095de9dc36d3', # ModelScope Token
        )
    
    def get_element_info(self, screenshot_path, task_description):
        """
        使用AI识别屏幕截图中的元素位置
        :param screenshot_path: 屏幕截图路径
        :param task_description: 任务描述，例如"点击买入按钮"
        :return: 元素位置信息
        """
        # 读取图片并编码为base64
        with open(screenshot_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = f"""
        请分析这张图片并找到执行以下任务所需的元素：
        任务：{task_description}
        
        请提供元素的边界框坐标（x1, y1, x2, y2）和元素类型。
        以JSON格式返回结果，例如：
        {{
            "element_type": "button",
            "coordinates": [100, 200, 150, 250]
        }}
        """
        
        # 调用千问API
        response = self.client.chat.completions.create(
            model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/png;base64,{encoded_image}'
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        # 解析响应
        response_text = response.choices[0].message.content
        try:
            # 提取JSON部分
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]
            element_info = json.loads(json_str)
            return element_info
        except Exception as e:
            raise Exception(f"解析AI响应失败: {e}\n响应内容: {response_text}")
    
    def click_element(self, d, element_info):
        """
        根据AI提供的元素信息执行点击操作
        :param d: uiautomator2设备对象
        :param element_info: AI提供的元素信息
        """
        coordinates = element_info["coordinates"]
        x = (coordinates[0] + coordinates[2]) // 2
        y = (coordinates[1] + coordinates[3]) // 2
        
        # 执行点击操作
        d.click(x, y)
        
    def handle_element_not_found(self, d, task_description, max_retries=3):
        """
        处理元素未找到的情况
        :param d: uiautomator2设备对象
        :param task_description: 任务描述
        :param max_retries: 最大重试次数
        """
        for i in range(max_retries):
            try:
                # 截图
                screenshot_path = f"screenshot_{int(time.time())}.png"
                d.screenshot(screenshot_path)
                
                # 使用AI识别元素
                element_info = self.get_element_info(screenshot_path, task_description)
                
                # 点击元素
                self.click_element(d, element_info)
                
                # 如果成功执行，跳出循环
                break
            except Exception as e:
                print(f"第{i+1}次尝试失败: {e}")
                if i == max_retries - 1:
                    raise e
                time.sleep(2)