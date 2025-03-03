import logging

import jsonpath
import re
from .com_yaml import a_yaml
# 此方法主要是提取需要关联的响应信息写入关联文件中
def get_res_and_write_yaml(res, res_attr_name, expr, index, save_refer_name):
    """
    res是上游接口用例请求的响应对象
    res_attr_name是res的属性
    expr是正则表达式
    index是取值索引
    save_refer_name是存入关联yaml文件中的键名
    """
    # 对响应数据进行获取
    if res_attr_name == "json":
        # 通过反射获取json方法的对象值，再通过()调用方法返回值
        data = getattr(res, res_attr_name)()
    else:
        data = getattr(res, res_attr_name)
    # 使用正则或jsonpath提取
    if expr.startswith("$"):
        list_data = jsonpath.jsonpath(data, expr)
    else:
        list_data = re.findall(expr, str(data))
    # 将提取到的值写入关联文件
    if list_data:
        a_yaml("temp/refer.yaml", {save_refer_name: list_data[int(index)]})
    else:
        logging.warning(f"\n{data}\n获取到的响应数据没有关联值被写入到refer.yaml")
# 此方法主要是提取需要关联的请求信息写入关联文件中
def get_req_and_write_yaml(key, value):
    a_yaml("temp/refer.yaml", {key: value})