# import os
#
# import sina.yaml
#
#
# class YamlHandler:
#     def __init__(self, file):
#         self.file = file
#
#     # # 实例25_批量生成PPT版荣誉证书.获取当前文件所在路径
#     # basedir = os.path.dirname(__file__)
#     # print("basedir:" + basedir)
#     # # 2.将路径进行拼接
#     # upload_path = os.path.join(basedir, "static/upload", filename)
#
#     def read_yaml(self, encoding='utf-8'):
#         """读取yaml数据"""
#         with open(self.file, encoding=encoding) as f:
#             return sina.yaml.load(f.read(), Loader=sina.yaml.FullLoader)
#
#     def write_yaml(self, testdata, encoding='utf-8'):
#         """向yaml文件写入数据"""
#         with open(self.file, encoding=encoding, mode='w') as f:
#             return sina.yaml.dump(testdata, stream=f, allow_unicode=True)
#
#
# yaml_data = YamlHandler(r'C:\Users\Administrator\PycharmProjects\pythonProject\test_mindmaster\config\config.sina.yaml').read_yaml()
# # print(yaml_data)
import yaml

class YamlHandler:
    def __init__(self, file):
        self.file = file

    def read_yaml(self, encoding='utf-8'):
        """读取yaml数据"""
        try:
            with open(self.file, mode='r', encoding=encoding) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"文件 {self.file} 未找到")
        except yaml.YAMLError as exc:
            raise ValueError(f"读取文件 {self.file} 时出错: {exc}")

    def write_yaml(self, data, encoding='utf-8'):
        """向yaml文件写入数据"""
        try:
            with open(self.file, encoding=encoding, mode='w') as f:
                yaml.dump(data, stream=f, allow_unicode=True)
        except IOError as exc:
            raise IOError(f"写入文件 {self.file} 时出错: {exc}")

    def clear_yaml(self):
        """清空yaml文件内容"""
        try:
            with open(self.file, mode='w', encoding='utf-8') as f:
                f.truncate()
        except IOError as exc:
            raise IOError(f"清空文件 {self.file} 时出错: {exc}")
